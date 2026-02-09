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
bp-gen generate-plan --input examples/input.json
```

## Run tests

```bash
pytest
```

## Example Input

```json
{
  "business_context": {
    "summary": "We need to reduce churn in the mid-market segment.",
    "goals": ["Increase retention"]
  },
  "constraints": ["No new headcount in Q3"],
  "flags": {
    "enable_initiatives": false,
    "enable_capabilities": false,
    "enable_outputs": false
  }
}
```

## Example Output

```json
{
  "metadata": {
    "plan_id": "plan-1",
    "title": "Business Case Plan",
    "created_at": "2024-01-01T00:00:00Z",
    "version": "v1"
  },
  "objectives": [
    {
      "id": "obj-1",
      "name": "Increase retention",
      "description": null
    }
  ],
  "kpis": [
    {
      "id": "kpi-1",
      "objective_id": "obj-1",
      "name": "Progress toward Increase retention",
      "description": null,
      "unit": null,
      "baseline": null,
      "target": null,
      "data_source": null,
      "owner": null,
      "target_date": null
    }
  ],
  "links": [
    {
      "id": "link-1",
      "source_id": "obj-1",
      "target_id": "kpi-1",
      "type": "objective_to_kpi"
    }
  ],
  "assumptions_and_gaps": [
    {
      "id": "gap-1",
      "description": "Baseline values, data sources, owners, and target dates are not provided; they remain null until confirmed."
    }
  ]
}
```
