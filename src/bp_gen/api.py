from __future__ import annotations

from fastapi import FastAPI

from bp_gen.schemas import (
    BusinessPlan,
    ClarifyingQuestions,
    GeneratePlanRequest,
    GenerationErrorResponse,
)
from bp_gen.services.plan_generator import generate_plan

app = FastAPI(title="Business Case Generator Agent")


@app.post(
    "/generate-plan",
    response_model=BusinessPlan | ClarifyingQuestions | GenerationErrorResponse,
    response_model_exclude_none=True,
)
def generate_plan_endpoint(request: GeneratePlanRequest):
    result = generate_plan(request)
    return result
