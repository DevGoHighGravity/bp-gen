# Business Case Generator Agent Instructions

## Non-negotiables
- Business Plan output MUST include Objectives[] and KPIs[] (both required; >=1).
- Optional entities Outputs/Capabilities/Initiatives are controlled by config flags.
- Never invent baselines, data sources, owners, or dates. Use null + assumptions_and_gaps[].
- If essential context is missing, return { "clarifying_questions": [...] } only.
- JSON/schema-first. Validate locally.

## Setup commands
- Install dependencies: `pip install -e .`
- Run API locally: `uvicorn bp_gen.api:app --reload`
- Run tests: `pytest`

## Code conventions
- Follow existing scaffold structure.
- Prefer stdlib for CLI unless repo already uses a CLI lib.
- Add tests for validator and one golden sample.

## Objectives and KPIs
- Every generated plan **must** include at least one Objective and at least one KPI.
- Each KPI must reference a valid Objective by ID.

## Optional Entities (Config-Driven)
- Initiatives, Capabilities, and Outputs are optional and **must only appear** when enabled via configuration flags.

## Data Integrity Rules
- Do **not** fabricate baselines, data sources, owners, or dates.
- If any of those fields are unknown, set them to `null` and add a corresponding entry in `assumptions_and_gaps`.

## Missing Context
- If required context is missing to generate a compliant plan, return `clarifying_questions` instead of a plan.
