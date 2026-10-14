from __future__ import annotations

import hashlib
import math
import os
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .config import project_scope

Role = Literal["architect", "reviewer"]
Action = Literal["ask_architect", "ask_reviewer", "finish", "request_input"]

AGENTS = {
    "coordinator": "multi-agent-coordinator",
    "architect": "multi-agent-architect",
    "reviewer": "multi-agent-reviewer",
}
PROJECT, ORIGIN = project_scope()
LEDGER_KEY = "multi_agent_v1"
FACTS = os.environ.get(
    "DEMO_FACT_SHEET",
    "Synthetic architecture exercise: application ingress must be private. "
    "Use managed identity and private TLS endpoints. Do not invent resource "
    "availability, prices, live health or deployment approval. "
    "This demo cannot query or mutate Azure.",
)


class DemoError(RuntimeError):
    def __init__(self, code: str, details: Any | None = None):
        self.code = code
        self.details = details
        super().__init__(code)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Candidate(StrictModel):
    requirements_revision: int = Field(ge=1)
    candidate_revision: int = Field(ge=1)
    design: str = Field(min_length=1, max_length=16000)


class Review(StrictModel):
    requirements_revision: int = Field(ge=1)
    candidate_revision: int = Field(ge=1)
    approved: bool
    blocking_findings: list[str] = Field(max_length=20)
    unresolved_requirements: list[str] = Field(max_length=20)
    recommendation: str = Field(min_length=1, max_length=4000)

    @model_validator(mode="after")
    def coherent_approval(self) -> Review:
        if self.approved and (self.blocking_findings or self.unresolved_requirements):
            raise ValueError("An approval cannot contain unresolved blockers.")
        return self


class Child(StrictModel):
    role: Role
    name: str
    version: str
    hosted_id: str
    framework: dict[str, Any]
    bound: bool = False


class Operation(StrictModel):
    id: str
    role: Role
    kind: Literal["create", "call"]
    status: Literal["pending", "completed", "uncertain"] = "pending"
    response_id: str | None = None


class Ledger(StrictModel):
    schema_version: Literal[1] = 1
    parent_framework_id: str
    generation: int = 0
    turn: int = 0
    requirements: list[str] = Field(default_factory=list, max_length=50)
    candidate_revision: int = 0
    candidate: Candidate | None = None
    review: Review | None = None
    calls: int = 0
    rounds: int = 0
    decisions: int = 0
    children: dict[str, Child] = Field(default_factory=dict)
    operation: Operation | None = None
    status: str = "NEW"

    def allowed(self) -> tuple[Action, ...]:
        if self.candidate is None or self.candidate.requirements_revision != self.turn:
            return ("ask_architect", "request_input")
        if self.review is None or self.review.candidate_revision != self.candidate_revision:
            return ("ask_reviewer", "request_input")
        if self.review.approved and not (
            self.review.blocking_findings or self.review.unresolved_requirements
        ):
            return ("finish", "request_input")
        return ("ask_architect", "request_input")

    def brief(self, role: Role) -> dict[str, Any]:
        return {
            "role": role,
            "requirements_revision": self.turn,
            "candidate_revision": self.candidate_revision + (role == "architect"),
            "requirements": self.requirements,
            "candidate": self.candidate.model_dump() if self.candidate else None,
            "review": self.review.model_dump() if self.review else None,
        }


def alias(value: str | None) -> str | None:
    return hashlib.sha256(value.encode()).hexdigest()[:12] if value else None


def read_choice(payload: Any, allowed: tuple[Action, ...]) -> tuple[Action, float]:
    if not isinstance(payload, dict):
        raise DemoError("DECISION_SCHEMA")
    answers = payload.get("answers")
    answer = answers.get("next_action") if isinstance(answers, dict) else None
    if not isinstance(answer, dict) or answer.get("type") != "choice":
        raise DemoError("DECISION_SCHEMA")
    choice = answer.get("choice")
    probabilities = answer.get("probabilities")
    if choice not in allowed or not isinstance(probabilities, dict):
        raise DemoError("DECISION_SCHEMA")
    if set(probabilities) != set(allowed):
        raise DemoError("DECISION_SCHEMA")
    for probability in probabilities.values():
        if (
            isinstance(probability, bool)
            or not isinstance(probability, (int, float))
            or not math.isfinite(probability)
            or not 0 <= probability <= 1
        ):
            raise DemoError("DECISION_SCHEMA")
    if not math.isclose(sum(probabilities.values()), 1.0, abs_tol=0.01):
        raise DemoError("DECISION_SCHEMA")
    if probabilities[choice] < max(probabilities.values()):
        raise DemoError("DECISION_SCHEMA")
    return choice, float(probabilities[choice])
