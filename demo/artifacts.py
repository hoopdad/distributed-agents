from __future__ import annotations

import hashlib
import json
import re
from typing import Annotated, Any, Literal
from urllib.parse import urlsplit
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

MAX_DOCUMENT_BYTES = 131072
MAX_DOCUMENT_DEPTH = 16
MAX_REQUIREMENTS_BYTES = 24000
MAX_ACCEPTED_ARTIFACTS = 256
Role = Literal["coordinator", "architect", "reviewer"]
Container = Literal["control", "candidates", "reviews"]
ArtifactType = Literal["requirements", "candidate", "review", "decision"]
Action = Literal["ask_architect", "ask_reviewer", "finish", "request_input"]
Identifier = Annotated[str, Field(pattern=r"^[a-f0-9]{32}$")]
Digest = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
BoundedId = Annotated[str, Field(min_length=1, max_length=256)]


class ArtifactError(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def _check_depth(value: Any, depth: int = 0) -> None:
    if depth > MAX_DOCUMENT_DEPTH:
        raise ArtifactError("ARTIFACT_DEPTH_LIMIT")
    if isinstance(value, dict):
        for item in value.values():
            _check_depth(item, depth + 1)
    elif isinstance(value, list):
        for item in value:
            _check_depth(item, depth + 1)


def canonical_bytes(value: Any) -> bytes:
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    _check_depth(value)
    try:
        raw = json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    except (ValueError, TypeError, UnicodeError) as exc:
        raise ArtifactError("ARTIFACT_JSON") from exc
    if len(raw) > MAX_DOCUMENT_BYTES:
        raise ArtifactError("ARTIFACT_BYTE_LIMIT")
    return raw


def decode_document(raw: bytes) -> Any:
    if len(raw) > MAX_DOCUMENT_BYTES:
        raise ArtifactError("ARTIFACT_BYTE_LIMIT")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ArtifactError("ARTIFACT_DUPLICATE_KEY")
            result[key] = value
        return result

    def nonfinite(_value):
        raise ArtifactError("ARTIFACT_JSON")

    try:
        value = json.loads(raw, object_pairs_hook=pairs, parse_constant=nonfinite)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ArtifactError("ARTIFACT_JSON") from exc
    canonical_bytes(value)
    return value


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class ImmutableModel(StrictModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


class ScopeBinding(ImmutableModel):
    project: str = Field(min_length=1, max_length=512)
    tenant: str
    principal: BoundedId
    parent_session: BoundedId

    @model_validator(mode="after")
    def canonical_scope(self):
        uri = urlsplit(self.project)
        if (
            uri.scheme != "https" or uri.port not in (None, 443) or uri.username or uri.password
            or uri.query or uri.fragment or not uri.hostname
            or not re.fullmatch(r"[a-z0-9-]+\.(services\.ai|ai)\.azure\.com", uri.hostname)
            or not re.fullmatch(r"/api/projects/[A-Za-z0-9_-]+", uri.path)
            or self.project != f"https://{uri.hostname}{uri.path}"
        ):
            raise ValueError("A canonical configured project is required.")
        if str(UUID(self.tenant)) != self.tenant or UUID(self.tenant).int == 0:
            raise ValueError("A canonical tenant UUID is required.")
        return self

    @classmethod
    def from_platform(cls, config, context, *, project: str, tenant: str):
        if (
            not config.is_hosted or not config.session_id or not context.user_id or not context.call_id
            or (context.session_id and context.session_id != config.session_id)
        ):
            raise ArtifactError("TRUSTED_PARENT_REQUIRED")
        return cls(
            project=project, tenant=tenant, principal=context.user_id, parent_session=config.session_id
        )

    @property
    def prefix(self) -> str:
        return (
            f"v1/{digest(self.project)}/{digest([self.tenant, self.principal])}/"
            f"{digest(self.parent_session)}/"
        )


class ArtifactRef(ImmutableModel):
    container: Container
    name: str = Field(min_length=1, max_length=512)
    sha256: Digest
    artifact_type: ArtifactType
    schema_version: Literal[1] = 1
    requirements_revision: int = Field(ge=1, le=50)
    candidate_revision: int | None = Field(default=None, ge=1)

    def assert_scope(self, scope: ScopeBinding) -> None:
        directories = {"requirements": "requirements", "decision": "decisions", "candidate": "candidates", "review": "reviews"}
        if not self.name.startswith(scope.prefix) or not re.fullmatch(
            re.escape(scope.prefix) + directories[self.artifact_type] + r"/[1-9][0-9]*/[a-f0-9]{32}\.json",
            self.name,
        ):
            raise ArtifactError("ARTIFACT_SCOPE")
        expected = {"requirements": "control", "decision": "control", "candidate": "candidates", "review": "reviews"}
        if self.container != expected[self.artifact_type]:
            raise ArtifactError("ARTIFACT_CONTAINER")


class Producer(ImmutableModel):
    role: Role
    name: BoundedId
    version: BoundedId
    session_id: BoundedId
    response_id: BoundedId | None = None


class Requirements(ImmutableModel):
    kind: Literal["requirements"] = "requirements"
    chunks: list[Annotated[str, Field(min_length=1, max_length=4000)]] = Field(min_length=1, max_length=50)

    @model_validator(mode="after")
    def bounded_source(self):
        if len(canonical_bytes(self.chunks)) > MAX_REQUIREMENTS_BYTES:
            raise ValueError("Requirements exceed their bounded source budget.")
        return self


class Candidate(ImmutableModel):
    kind: Literal["candidate"] = "candidate"
    requirements_revision: int = Field(ge=1, le=50)
    candidate_revision: int = Field(ge=1)
    design: str = Field(min_length=1, max_length=12000)


class Review(ImmutableModel):
    kind: Literal["review"] = "review"
    requirements_revision: int = Field(ge=1, le=50)
    candidate_revision: int = Field(ge=1)
    approved: bool
    blocking_findings: list[Annotated[str, Field(min_length=1, max_length=1000)]] = Field(max_length=20)
    unresolved_requirements: list[Annotated[str, Field(min_length=1, max_length=1000)]] = Field(max_length=20)
    recommendation: str = Field(min_length=1, max_length=2000)

    @model_validator(mode="after")
    def coherent(self):
        if self.approved and (self.blocking_findings or self.unresolved_requirements):
            raise ValueError("Approval cannot contain blockers.")
        return self


class Decision(ImmutableModel):
    kind: Literal["decision"] = "decision"
    policy_version: Literal["routing-v2", "routing-v3"] = "routing-v2"
    input_schema_version: Literal[2] = 2
    state_sha256: Digest
    model: Literal["Microsoft-Decision-1"] = "Microsoft-Decision-1"
    deployment: BoundedId
    alternatives: list[Action] = Field(min_length=2, max_length=4)
    action: Action
    probabilities: dict[Action, float]
    confidence: float = Field(ge=0, le=1, allow_inf_nan=False)
    input_tokens: int | None = Field(default=None, ge=0, le=1000000)
    output_tokens: int | None = Field(default=None, ge=0, le=1000000)
    provider_request_id: BoundedId | None = None
    gated_action: Action | Literal["hold"]
    reason: str = Field(min_length=1, max_length=256)
    calibration_sha256: Digest


Content = Annotated[Requirements | Candidate | Review | Decision, Field(discriminator="kind")]


class Artifact(ImmutableModel):
    schema_version: Literal[1] = 1
    artifact_type: ArtifactType
    scope_binding: ScopeBinding
    operation_id: Identifier
    producer: Producer
    input_refs: list[ArtifactRef] = Field(max_length=4)
    requirements_revision: int = Field(ge=1, le=50)
    candidate_revision: int | None = Field(default=None, ge=1)
    content: Content
    content_sha256: Digest
    publication_state: Literal["proposal"] = "proposal"

    @model_validator(mode="after")
    def coherent(self):
        if self.content.kind != self.artifact_type or digest(self.content) != self.content_sha256:
            raise ValueError("Artifact kind/hash mismatch.")
        if self.producer.response_id is None:
            raise ValueError("An output requires its actual producing response.")
        owners = {"requirements": "coordinator", "candidate": "architect", "review": "reviewer", "decision": "coordinator"}
        if self.producer.role != owners[self.artifact_type]:
            raise ValueError("Artifact producer role mismatch.")
        if isinstance(self.content, Requirements):
            if len(self.content.chunks) != self.requirements_revision or self.candidate_revision is not None:
                raise ValueError("Requirements revision mismatch.")
        if isinstance(self.content, (Candidate, Review)) and (
            self.content.requirements_revision != self.requirements_revision
            or self.content.candidate_revision != self.candidate_revision
        ):
            raise ValueError("Artifact revision mismatch.")
        for ref in self.input_refs:
            ref.assert_scope(self.scope_binding)
        return self

    def ref(self) -> ArtifactRef:
        directories = {"requirements": "requirements", "candidate": "candidates", "review": "reviews", "decision": "decisions"}
        containers = {"requirements": "control", "candidate": "candidates", "review": "reviews", "decision": "control"}
        return ArtifactRef(
            container=containers[self.artifact_type],
            name=f"{self.scope_binding.prefix}{directories[self.artifact_type]}/{self.requirements_revision}/{self.operation_id}.json",
            sha256=digest(self), artifact_type=self.artifact_type,
            requirements_revision=self.requirements_revision, candidate_revision=self.candidate_revision,
        )


class Assignment(ImmutableModel):
    schema_version: Literal[1] = 1
    scope_binding: ScopeBinding
    operation_id: Identifier
    producer: Producer
    input_refs: list[ArtifactRef] = Field(min_length=1, max_length=3)
    requirements_revision: int = Field(ge=1, le=50)
    candidate_revision: int = Field(ge=1)
    output_type: Literal["candidate", "review"]
    deadline_epoch: int = Field(ge=1)

    @model_validator(mode="after")
    def coherent(self):
        role = "architect" if self.output_type == "candidate" else "reviewer"
        if self.producer.role != role:
            raise ValueError("Assignment role mismatch.")
        for ref in self.input_refs:
            ref.assert_scope(self.scope_binding)
        return self

    def validate_receiver(
        self, *, config, context, manifest: Manifest, now: int, completed_output: bool = False
    ) -> None:
        trusted_child = ScopeBinding.from_platform(
            config, context, project=self.scope_binding.project, tenant=self.scope_binding.tenant
        )
        producer = self.producer
        child = manifest.children.get(producer.role)
        if (
            trusted_child.principal != self.scope_binding.principal
            or config.project_endpoint != self.scope_binding.project
            or config.agent_name != producer.name or config.agent_version != producer.version
            or trusted_child.parent_session != producer.session_id
            or child is None or not child.bound or child.hosted_id != producer.session_id
            or child.role != producer.role or child.name != producer.name or child.version != producer.version
            or manifest.scope_binding != self.scope_binding
            or (now > self.deadline_epoch and not completed_output)
        ):
            raise ArtifactError("ASSIGNMENT_RECEIVER")
        effect = manifest.effect
        if (
            effect is None or effect.kind != "call" or effect.operation_id != self.operation_id
            or effect.role != producer.role or effect.input_refs != self.input_refs
            or effect.assignment_sha256 != digest(self)
            or effect.status not in ("dispatched", "response_observed")
            or self.requirements_revision != manifest.turn
            or manifest.requirements is None or self.input_refs[0] != manifest.requirements
            or any(ref not in manifest.accepted for ref in self.input_refs)
        ):
            raise ArtifactError("ASSIGNMENT_PREREQUISITES")
        expected_revision = manifest.candidate_revision + (self.output_type == "candidate")
        if self.candidate_revision != expected_revision:
            raise ArtifactError("ASSIGNMENT_REVISION")
        if self.output_type == "review" and (
            manifest.candidate is None or len(self.input_refs) != 2 or self.input_refs[1] != manifest.candidate
        ):
            raise ArtifactError("ASSIGNMENT_PREREQUISITES")
        expected = [manifest.requirements]
        if manifest.candidate is not None:
            expected.append(manifest.candidate)
        if self.output_type == "candidate" and manifest.review is not None:
            expected.append(manifest.review)
        if self.input_refs != expected:
            raise ArtifactError("ASSIGNMENT_PREREQUISITES")


class AssignmentLocator(StrictModel):
    schema_version: int = Field(ge=1, le=1)
    scope_binding: ScopeBinding
    operation_id: str


class OutputLocator(StrictModel):
    schema_version: int = Field(ge=1, le=1)
    artifact_ref: ArtifactRef


class ChildBinding(StrictModel):
    role: Literal["architect", "reviewer"]
    name: BoundedId
    version: BoundedId
    hosted_id: BoundedId
    framework: dict[str, Any]
    bound: bool = False


class Effect(StrictModel):
    operation_id: Identifier
    kind: Literal["create", "call", "decision"]
    status: Literal["prepared", "dispatched", "response_observed", "output_observed", "accepted", "unknown", "failed"]
    role: Role
    input_refs: list[ArtifactRef] = Field(max_length=3)
    output_ref: ArtifactRef | None = None
    response_id: BoundedId | None = None
    failure: str | None = Field(default=None, max_length=256)
    routing_operation_id: Identifier | None = None
    reserved_name: str | None = Field(default=None, max_length=512)
    assignment_sha256: Digest | None = None


class Manifest(StrictModel):
    schema_version: Literal[1] = 1
    scope_binding: ScopeBinding
    generation: int = Field(default=0, ge=0)
    turn: int = Field(default=0, ge=0, le=50)
    candidate_revision: int = Field(default=0, ge=0)
    requirements: ArtifactRef | None = None
    candidate: ArtifactRef | None = None
    review: ArtifactRef | None = None
    accepted: list[ArtifactRef] = Field(default_factory=list, max_length=MAX_ACCEPTED_ARTIFACTS)
    children: dict[Literal["architect", "reviewer"], ChildBinding] = Field(default_factory=dict)
    effect: Effect | None = None
    active_response_id: BoundedId | None = None
    coordinator_version: BoundedId | None = None
    next_action: Action | None = None
    routing_operation_id: Identifier | None = None
    deadline_epoch: int | None = Field(default=None, ge=1)
    calls: int = Field(default=0, ge=0, le=6)
    rounds: int = Field(default=0, ge=0, le=3)
    decisions: int = Field(default=0, ge=0, le=10)
    status: str = Field(default="NEW", min_length=1, max_length=64)

    @model_validator(mode="after")
    def coherent(self):
        for ref in self.accepted:
            ref.assert_scope(self.scope_binding)
        if len({(ref.container, ref.name) for ref in self.accepted}) != len(self.accepted):
            raise ValueError("Duplicate manifest refs.")
        for ref in (self.requirements, self.candidate, self.review):
            if ref is not None and ref not in self.accepted:
                raise ValueError("Current prerequisites must be accepted.")
        for ref, expected in ((self.requirements, "requirements"), (self.candidate, "candidate"), (self.review, "review")):
            if ref is not None and ref.artifact_type != expected:
                raise ValueError("Current prerequisite kind mismatch.")
        if self.requirements and self.requirements.requirements_revision != self.turn:
            raise ValueError("Stale requirements.")
        if self.candidate and (
            self.candidate.requirements_revision != self.turn
            or self.candidate.candidate_revision != self.candidate_revision
        ):
            raise ValueError("Stale candidate.")
        if self.review and (
            not self.candidate or self.review.requirements_revision != self.turn
            or self.review.candidate_revision != self.candidate_revision
        ):
            raise ValueError("Stale review.")
        return self
