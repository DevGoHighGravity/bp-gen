from bp_gen.schemas import BusinessContext, GeneratePlanRequest
from bp_gen.services.plan_generator import generate_plan


def test_missing_context_returns_clarifying_questions():
    request = GeneratePlanRequest(
        business_context=BusinessContext(scope="North America"),
        allowed_relationships=["objective_to_kpi"],
    )

    result = generate_plan(request)

    assert hasattr(result, "clarifying_questions")
    assert 3 <= len(result.clarifying_questions) <= 7
