import json
from pathlib import Path

from bp_gen.schemas import BusinessPlan, GenerationFlags
from bp_gen.validator import validate_business_plan

SAMPLES = Path(__file__).parent.parent / "samples"


def load_golden_plan() -> BusinessPlan:
    data = json.loads((SAMPLES / "golden_plan.json").read_text())
    return BusinessPlan.model_validate(data)


def test_golden_plan_is_valid():
    plan = load_golden_plan()
    flags = GenerationFlags(
        include_initiatives=True,
        include_capabilities=True,
        include_outputs=True,
    )
    result = validate_business_plan(plan, flags)
    assert result["ok"] is True
    assert result["errors"] == []


def test_kpi_missing_objective_id():
    plan = load_golden_plan()
    plan.kpis[0].objective_id = "missing-objective"
    flags = GenerationFlags(
        include_initiatives=True,
        include_capabilities=True,
        include_outputs=True,
    )
    result = validate_business_plan(plan, flags)
    assert result["ok"] is False
    assert any(error["code"] == "kpi_unknown_objective" for error in result["errors"])


def test_objectives_empty():
    plan = load_golden_plan()
    plan.objectives = []
    flags = GenerationFlags(
        include_initiatives=True,
        include_capabilities=True,
        include_outputs=True,
    )
    result = validate_business_plan(plan, flags)
    assert result["ok"] is False
    assert any(error["code"] == "objectives_required" for error in result["errors"])


def test_outputs_disabled_with_outputs_present():
    plan = load_golden_plan()
    flags = GenerationFlags(
        include_initiatives=True,
        include_capabilities=True,
        include_outputs=False,
    )
    result = validate_business_plan(plan, flags)
    assert result["ok"] is False
    assert any(error["code"] == "outputs_disabled" for error in result["errors"])
