from __future__ import annotations

import asyncio
import copy
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from pydantic import ValidationError

from demo.artifacts import ArtifactError, canonical_bytes, decode_document, digest
from demo.routing import DecisionClient, ProviderResult, calibration_state, gated_choice, reserve_decision
from scripts import calibrate_routing
from test_workflow import MemoryBackend, TestRuntime, make_store, synthetic_calibration


ALLOWED = ["ask_architect", "request_input"]


def outcome():
    return {
        "model": "Microsoft-Decision-1", "answers": {"next_action": {
            "type": "choice", "choice": "ask_architect", "confidence": 0.9,
            "probabilities": {"ask_architect": 0.9, "request_input": 0.1},
        }},
    }


class RoutingTests(unittest.IsolatedAsyncioTestCase):
    async def test_runtime_validation_rejects_fact_drift_without_recalibration_or_writes(self):
        corpus = (Path(__file__).resolve().parents[1] / "config" / "routing-corpus.json").read_bytes()
        with patch("demo.contracts.FACTS", "Synthetic calibrated facts with spaces."):
            calibration = synthetic_calibration()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "config").mkdir()
            (root / "config" / "routing-corpus.json").write_bytes(corpus)
            path = root / "config" / "routing-calibration.json"
            original = canonical_bytes(calibration)
            path.write_bytes(original)
            with patch.object(calibrate_routing, "ROOT", root), \
                    patch.object(calibrate_routing, "required", return_value=calibration.deployment):
                with patch("demo.contracts.FACTS", "Synthetic calibrated facts with spaces."):
                    self.assertEqual(calibrate_routing.validate_runtime()["calibration_sha256"], digest(calibration))
                with patch("demo.contracts.FACTS", "Different synthetic facts."):
                    with self.assertRaisesRegex(ArtifactError, "DECISION_CALIBRATION_PROVENANCE"):
                        calibrate_routing.validate_runtime()
            self.assertEqual(path.read_bytes(), original)

    async def test_all_native_roles_forward_the_same_calibrated_fact_sheet(self):
        descriptor = (Path(__file__).resolve().parents[1] / "azure.yaml").read_text()
        self.assertEqual(descriptor.count("DEMO_FACT_SHEET: ${DEMO_FACT_SHEET}"), 3)

    async def test_calibration_export_is_validated_exact_and_idempotent(self):
        corpus = (Path(__file__).resolve().parents[1] / "config" / "routing-corpus.json").read_bytes()
        calibration = synthetic_calibration()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "app"
            (root / "config").mkdir(parents=True)
            (root / "config" / "routing-corpus.json").write_bytes(corpus)
            source = Path(temporary) / "private-success.json"
            source.write_bytes(canonical_bytes(calibration))
            output = root / "config" / "routing-calibration.json"
            with patch.object(calibrate_routing, "ROOT", root), \
                    patch.object(calibrate_routing, "private_state_path", side_effect=Path), \
                    patch.object(calibrate_routing, "required", return_value=calibration.deployment):
                result = calibrate_routing.export_successful(source, output)
                self.assertEqual(result["calibration_sha256"], digest(calibration))
                self.assertEqual(output.read_bytes(), canonical_bytes(calibration))
                self.assertEqual(calibrate_routing.export_successful(source, output), result)
                with self.assertRaises(ArtifactError) as caught:
                    calibrate_routing.export_successful(source, root / "another.json")
                self.assertEqual(caught.exception.code, "CALIBRATION_PUBLIC_PATH")
                output.write_bytes(b"historical bytes")
                with self.assertRaises(ArtifactError) as caught:
                    calibrate_routing.export_successful(source, output)
                self.assertEqual(caught.exception.code, "CALIBRATION_OUTPUT_ALREADY_EXISTS")
                self.assertEqual(output.read_bytes(), b"historical bytes")

    async def test_calibration_export_rejects_changed_policy_before_creating_output(self):
        corpus = (Path(__file__).resolve().parents[1] / "config" / "routing-corpus.json").read_bytes()
        calibration = synthetic_calibration()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "app"
            (root / "config").mkdir(parents=True)
            (root / "config" / "routing-corpus.json").write_bytes(corpus)
            source = Path(temporary) / "private-success.json"
            source.write_bytes(canonical_bytes(calibration))
            output = root / "config" / "routing-calibration.json"
            with patch.object(calibrate_routing, "ROOT", root), \
                    patch.object(calibrate_routing, "private_state_path", side_effect=Path), \
                    patch.object(calibrate_routing, "required", return_value=calibration.deployment), \
                    patch("demo.routing.INSTRUCTIONS", "Changed policy."):
                with self.assertRaises(ArtifactError):
                    calibrate_routing.export_successful(source, output)
                self.assertFalse(output.exists())

    async def test_provider_uses_serialized_state_and_preserves_missing_usage(self):
        http = SimpleNamespace(post=AsyncMock(return_value=SimpleNamespace(
            status_code=200, content=canonical_bytes(outcome()), headers={"x-ms-request-id": "synthetic-request"},
        )))
        credential = SimpleNamespace(get_token=AsyncMock(return_value=SimpleNamespace(token="synthetic-token")))
        client = DecisionClient(
            http=http, credential=credential, origin="https://example.services.ai.azure.com",
            deployment="synthetic-decision", headers={},
        )
        result, request_id = await client.score({"requirements": ["Synthetic."]}, ALLOWED)
        body = http.post.call_args.kwargs["json"]
        self.assertIsInstance(body["state"], str)
        self.assertEqual(decode_document(body["state"].encode()), {"requirements": ["Synthetic."]})
        self.assertEqual(set(body["questions"]["next_action"]["criteria"]), set(ALLOWED))
        self.assertIsNone(result.usage)
        self.assertEqual(request_id, "synthetic-request")
        credential.get_token.assert_awaited_once_with("https://cognitiveservices.azure.com/.default")

    async def test_provider_error_is_not_retried_or_replaced(self):
        http = SimpleNamespace(post=AsyncMock(return_value=SimpleNamespace(status_code=429)))
        client = DecisionClient(
            http=http, credential=SimpleNamespace(get_token=AsyncMock(return_value=SimpleNamespace(token="synthetic"))),
            origin="https://example.services.ai.azure.com", deployment="synthetic-decision", headers={},
        )
        with self.assertRaises(ArtifactError) as caught:
            await client.score({"requirements": ["Synthetic."]}, ALLOWED)
        self.assertEqual(caught.exception.code, "DECISION_HTTP_429")
        http.post.assert_awaited_once()

    async def test_invalid_provider_distributions_fail_closed(self):
        for invalid in (
            {"ask_architect": True, "request_input": 0.0},
            {"ask_architect": float("nan"), "request_input": 0.0},
            {"ask_architect": 0.8},
            {"ask_architect": 0.8, "request_input": 0.1},
            {"ask_architect": 0.4, "request_input": 0.6},
            {"ask_architect": 0.8, "request_input": 0.2, "finish": 0.0},
        ):
            with self.subTest(probabilities=invalid):
                raw = outcome()
                raw["answers"]["next_action"]["probabilities"] = invalid
                with self.assertRaises((ArtifactError, ValidationError)):
                    ProviderResult.model_validate(raw).answer(ALLOWED)
        raw = outcome()
        raw["model"] = "another-model"
        with self.assertRaises(ArtifactError):
            ProviderResult.model_validate(raw).answer(ALLOWED)

    async def test_confidence_and_margin_gates_hold_without_inventing_a_choice(self):
        answer = ProviderResult.model_validate(outcome()).answer(ALLOWED)
        self.assertEqual(gated_choice(answer, 0.95, 0.0), "hold")
        self.assertEqual(gated_choice(answer, 0.5, 0.9), "hold")
        self.assertEqual(gated_choice(answer, 0.9, 0.5), "ask_architect")

    async def test_calibration_uses_exact_runtime_state_and_rejects_changed_evidence(self):
        corpus = decode_document((Path(__file__).resolve().parents[1] / "config" / "routing-corpus.json").read_bytes())
        calibration = synthetic_calibration()
        calibration.validate_evaluation(corpus)
        state = calibration_state(corpus["cases"][2]["state"])
        self.assertEqual([item["artifact_type"] for item in state["prerequisite_refs"]], [
            "requirements", "candidate", "review",
        ])
        self.assertEqual(state["requirements"]["chunks"], ["All ingress must be private."])
        self.assertFalse(state["review"]["approved"])
        self.assertEqual(calibration.observations[2].state_sha256, digest(state))
        changed = copy.deepcopy(corpus)
        changed["cases"][0]["state"]["requirements"].append("Changed synthetic requirement.")
        with self.assertRaises(ArtifactError):
            calibration.validate_evaluation(changed)
        changed_observation = calibration.observations[0].model_copy(update={"state_sha256": "f" * 64})
        changed_calibration = calibration.model_copy(update={
            "observations": [changed_observation, *calibration.observations[1:]],
        })
        with self.assertRaises(ArtifactError):
            changed_calibration.validate_evaluation(corpus)
        with patch("demo.routing.INSTRUCTIONS", "Different question policy."):
            with self.assertRaises(ArtifactError):
                calibration.validate_evaluation(corpus)

    async def test_admission_is_shared_across_parents_and_rejects_replay(self):
        backend = MemoryBackend()
        first = TestRuntime(backend, None)
        second = TestRuntime(backend, None, parent="second-parent")
        store = make_store(backend, first.scope, "coordinator")
        other = make_store(backend, second.scope, "coordinator")
        with patch("demo.routing.time", SimpleNamespace(time=lambda: 1000.0)):
            await reserve_decision(store, operation_id="1" * 32, deployment="synthetic", limit=1, deadline=1100)
            with self.assertRaises(ArtifactError) as caught:
                await reserve_decision(other, operation_id="1" * 32, deployment="synthetic", limit=1, deadline=1100)
            self.assertEqual(caught.exception.code, "DECISION_ADMISSION_REPLAY")
            with patch("demo.routing.asyncio", SimpleNamespace(
                sleep=AsyncMock(side_effect=asyncio.CancelledError),
            )):
                with self.assertRaises(asyncio.CancelledError):
                    await reserve_decision(other, operation_id="2" * 32, deployment="synthetic", limit=1, deadline=1100)
        self.assertEqual(len(backend.blobs), 1)
        state = decode_document(next(iter(backend.blobs.values())))
        self.assertEqual([item["operation_id"] for item in state["reservations"]], ["1" * 32])
        self.assertFalse(backend.leases)
        with patch("demo.routing.time", SimpleNamespace(time=lambda: 1061.0)):
            await reserve_decision(other, operation_id="2" * 32, deployment="synthetic", limit=1, deadline=1100)

    async def test_admission_rejects_backward_clock_without_changing_reservations(self):
        backend = MemoryBackend()
        runtime = TestRuntime(backend, None)
        store = make_store(backend, runtime.scope, "coordinator")
        clock = SimpleNamespace(time=lambda: 1000.0)
        with patch("demo.routing.time", clock):
            await reserve_decision(store, operation_id="1" * 32, deployment="synthetic", limit=17, deadline=1100)
            before = copy.deepcopy(backend.blobs)
            # A real prior reservation is now ten seconds in the future (>5).
            clock.time = lambda: 990.0
            with self.assertRaises(ArtifactError) as caught:
                await reserve_decision(
                    store, operation_id="2" * 32, deployment="synthetic", limit=17, deadline=1100,
                )
            self.assertEqual(caught.exception.code, "DECISION_ADMISSION_CLOCK")
            self.assertEqual(backend.blobs, before)
            self.assertFalse(backend.leases)

    async def test_admission_configuration_conflicts_are_explicit(self):
        backend = MemoryBackend()
        runtime = TestRuntime(backend, None)
        store = make_store(backend, runtime.scope, "coordinator")
        with patch("demo.routing.time", SimpleNamespace(time=lambda: 1000.0)):
            await reserve_decision(store, operation_id="1" * 32, deployment="synthetic", limit=17, deadline=1100)
            with self.assertRaises(ArtifactError) as caught:
                await reserve_decision(store, operation_id="2" * 32, deployment="synthetic", limit=18, deadline=1100)
            self.assertEqual(caught.exception.code, "DECISION_ADMISSION_CONFIGURATION")
