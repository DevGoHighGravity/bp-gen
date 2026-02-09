# Business Case Generator Agent

Production-quality starter project for a schema-first Business Case Generator Agent. The service generates a plan graph JSON response that enforces objective/KPI alignment, optional entities via flags, and explicit assumptions/gaps when data is missing.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run the API

```bash
uvicorn bp_gen.api:app --reload
```

POST `http://localhost:8000/generate-plan` with a JSON payload.

## Run the CLI

```bash
bp-gen generate-plan --input samples/example_input.json --output out/plan.json
```

## Run tests

```bash
pytest
```

## Example Input

```json
{
  "business_context": {
    "scope": "North America customer support operations",
    "time_horizon": "12 months",
    "problem_statement": "Rising support costs and declining CSAT in priority accounts.",
    "success_definition": "Reduce cost per ticket and restore CSAT to target levels.",
    "plan_name": "Support Efficiency and Experience Plan"
  },
  "constraints": [
    "Budget capped at $500k",
    "No net-new headcount"
  ],
  "flags": {
    "include_initiatives": true,
    "include_capabilities": true,
    "include_outputs": true
  },
  "allowed_relationships": [
    "objective_to_kpi",
    "objective_to_initiative",
    "initiative_to_capability",
    "initiative_to_output"
  ]
}
```

## Example Output

```json
{
  "plan": {
    "name": "Support Efficiency and Experience Plan",
    "horizon": "12 months",
    "scope": "North America customer support operations",
    "themes": [
      "Problem resolution",
      "Success definition alignment"
    ]
  },
  "objectives": [
    {
      "id": "obj-1",
      "title": "Resolve Rising support costs and declining CSAT in priority accounts.",
      "rationale": "Directly addresses the stated problem: Rising support costs and declining CSAT in priority accounts..",
      "owner_role": null,
      "priority": "high"
    }
  ],
  "kpis": [
    {
      "id": "kpi-1-1",
      "objective_id": "obj-1",
      "name": "Progress on Resolve Rising support costs and declining CSAT in priority accounts.",
      "definition": "Measures advancement toward objective 'Resolve Rising support costs and declining CSAT in priority accounts.'.",
      "formula": null,
      "baseline": null,
      "target": "Aligned to success definition: Reduce cost per ticket and restore CSAT to target levels.",
      "frequency": "monthly",
      "data_source": null,
      "leading_or_lagging": "lagging"
    }
  ],
  "links": [
    {
      "from_type": "objective",
      "from_id": "obj-1",
      "to_type": "kpi",
      "to_id": "kpi-1-1",
      "type": "objective_to_kpi"
    }
  ],
  "assumptions_and_gaps": [
    {
      "item": "KPI baselines",
      "needed": "Baseline values for each KPI.",
      "impact": "Cannot quantify improvement without starting measurements."
    }
  ]
}
```
