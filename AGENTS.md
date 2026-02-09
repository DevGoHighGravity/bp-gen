# Business Case Generator Agent Instructions

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
