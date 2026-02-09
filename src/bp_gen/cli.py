from __future__ import annotations

import argparse
import json
from pathlib import Path

from bp_gen.schemas import (
    ClarifyingQuestions,
    GeneratePlanRequest,
    GenerationErrorResponse,
)
from bp_gen.services.plan_generator import generate_plan


def _load_payload(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> None:
    parser = argparse.ArgumentParser(description="Business Case Generator Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate-plan", help="Generate a plan")
    generate_parser.add_argument("--input", required=True, help="Path to JSON input file")
    generate_parser.add_argument(
        "--output",
        required=True,
        help="Path to write the generated plan JSON",
    )

    args = parser.parse_args()

    if args.command == "generate-plan":
        payload = _load_payload(Path(args.input))
        request = GeneratePlanRequest.model_validate(payload)
        result = generate_plan(request)

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        payload = result.model_dump(exclude_none=True)
        output_path.write_text(json.dumps(payload, indent=2))

        if isinstance(result, ClarifyingQuestions):
            return
        if isinstance(result, GenerationErrorResponse):
            raise SystemExit(f"Validation failed: {payload}")


if __name__ == "__main__":
    main()
