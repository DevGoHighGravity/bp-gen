from __future__ import annotations

import argparse
import json
from pathlib import Path

from bp_gen.generator import generate_plan
from bp_gen.models import ClarifyingQuestions, GeneratePlanRequest
from bp_gen.validator import validate_plan


def _load_payload(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> None:
    parser = argparse.ArgumentParser(description="Business Case Generator Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate-plan", help="Generate a plan")
    generate_parser.add_argument("--input", required=True, help="Path to JSON input file")

    args = parser.parse_args()

    if args.command == "generate-plan":
        payload = _load_payload(Path(args.input))
        request = GeneratePlanRequest.model_validate(payload)
        result = generate_plan(request)

        if isinstance(result, ClarifyingQuestions):
            print(json.dumps(result.model_dump(exclude_none=True), indent=2))
            return

        errors = validate_plan(result, request.flags)
        if errors:
            raise SystemExit(f"Validation failed: {errors}")

        print(json.dumps(result.model_dump(exclude_none=True), indent=2))


if __name__ == "__main__":
    main()
