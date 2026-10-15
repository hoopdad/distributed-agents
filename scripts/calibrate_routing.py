from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from azure.identity.aio import AzureCliCredential

from demo.artifacts import ArtifactError, canonical_bytes, decode_document, digest
from demo.config import required
from demo.contracts import ORIGIN
from demo.foundry import data_client
from demo.routing import (
    Calibration, CalibrationObservation, DecisionClient, calibration_state, decision_request, load_calibration,
    select_policy,
)
from demo.terminal import private_state_path, verify_lab


async def calibrate(args):
    _, subscription, _ = verify_lab()
    output = private_state_path(args.output)
    evidence = private_state_path(str(output) + ".observations.jsonl")
    if output.exists() or evidence.exists():
        raise ArtifactError("CALIBRATION_OUTPUT_ALREADY_EXISTS")
    corpus = decode_document((ROOT / "config" / "routing-corpus.json").read_bytes())
    if corpus["maximum_calls"] != 12 or len(corpus["cases"]) != 12:
        raise ArtifactError("DECISION_CALIBRATION_CORPUS")
    observations = []
    with evidence.open("x", encoding="utf-8", newline="\n") as journal:
        def record(value):
            journal.write(canonical_bytes(value).decode() + "\n")
            journal.flush()
            os.fsync(journal.fileno())

        async with AzureCliCredential(subscription=subscription, process_timeout=30) as credential, \
                data_client(socks=args.socks) as http:
            client = DecisionClient(
                http=http, credential=credential, origin=ORIGIN,
                deployment=required("DECISION_MODEL_DEPLOYMENT"), headers={},
            )
            for case in corpus["cases"]:
                state = calibration_state(case["state"])
                request_hash = digest(decision_request(state, case["allowed"], client.deployment))
                record({
                    "event": "prepared", "case_id": case["id"], "state_sha256": digest(state),
                    "request_sha256": request_hash,
                })
                outcome, _ = await client.score(state, case["allowed"])
                observations.append(CalibrationObservation(
                    case_id=case["id"], expected=case["expected"], allowed=case["allowed"], outcome=outcome,
                    state_sha256=digest(state),
                    request_sha256=request_hash,
                ))
                record({"event": "observed", "observation": observations[-1].model_dump(mode="json")})
    threshold, margin = select_policy(observations)
    calibration = Calibration(
        corpus_sha256=digest(corpus), deployment=client.deployment, observations=observations,
        threshold=threshold, margin=margin,
    )
    calibration.validate_evaluation(corpus)
    with output.open("xb") as file:
        file.write(canonical_bytes(calibration))
    print(json.dumps({
        "status": "CALIBRATION_PASSED", "calls": len(observations),
        "corpus_sha256": calibration.corpus_sha256, "calibration_sha256": digest(calibration),
        "threshold": threshold, "margin": margin,
    }))


def export_successful(source_path, output_path):
    source = private_state_path(source_path)
    destination = Path(output_path).resolve()
    if destination != (ROOT / "config" / "routing-calibration.json").resolve():
        raise ArtifactError("CALIBRATION_PUBLIC_PATH")
    calibration = load_calibration(
        source, ROOT / "config" / "routing-corpus.json", required("DECISION_MODEL_DEPLOYMENT"),
    )
    raw = canonical_bytes(calibration)
    if destination.exists():
        if destination.read_bytes() != raw:
            raise ArtifactError("CALIBRATION_OUTPUT_ALREADY_EXISTS")
    else:
        with destination.open("xb") as file:
            file.write(raw)
    return {
        "status": "PUBLIC_CALIBRATION_EXPORTED", "calibration_sha256": digest(calibration),
        "policy_version": calibration.policy_version, "corpus_sha256": calibration.corpus_sha256,
    }


def validate_runtime():
    calibration = load_calibration(
        ROOT / "config" / "routing-calibration.json", ROOT / "config" / "routing-corpus.json",
        required("DECISION_MODEL_DEPLOYMENT"),
    )
    return {"status": "RUNTIME_CALIBRATION_VALIDATED", "calibration_sha256": digest(calibration),
            "policy_version": calibration.policy_version, "corpus_sha256": calibration.corpus_sha256}


def main():
    parser = argparse.ArgumentParser(description="Twelve bounded synthetic Decision-1 calibration calls; no retries.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--socks")
    mode.add_argument("--export-successful")
    mode.add_argument("--validate-runtime", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    if not args.validate_runtime and args.output is None:
        parser.error("Calibration/export requires an explicit output.")
    if args.validate_runtime and args.output is not None:
        parser.error("Read-only runtime validation does not write an output.")
    try:
        if args.validate_runtime:
            print(json.dumps(validate_runtime()))
        elif args.export_successful:
            print(json.dumps(export_successful(args.export_successful, args.output)))
        else:
            asyncio.run(calibrate(args))
    except ArtifactError as exc:
        print(f"BLOCKED: {exc.code}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
