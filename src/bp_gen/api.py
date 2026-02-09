from __future__ import annotations

from fastapi import FastAPI, HTTPException

from bp_gen.generator import generate_plan
from bp_gen.models import ClarifyingQuestions, GeneratePlanRequest, PlanGraph
from bp_gen.validator import validate_plan

app = FastAPI(title="Business Case Generator Agent")


@app.post("/generate-plan", response_model=PlanGraph | ClarifyingQuestions, response_model_exclude_none=True)
def generate_plan_endpoint(request: GeneratePlanRequest):
    result = generate_plan(request)
    if isinstance(result, ClarifyingQuestions):
        return result

    errors = validate_plan(result, request.flags)
    if errors:
        raise HTTPException(status_code=400, detail=errors)

    return result
