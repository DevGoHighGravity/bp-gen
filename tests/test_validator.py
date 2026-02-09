import json
from pathlib import Path

import pytest

from bp_gen.models import Flags, PlanGraph
from bp_gen.validator import validate_plan

FIXTURES = Path(__file__).parent / "fixtures"


def load_golden_plan() -> PlanGraph:
    data = json.loads((FIXTURES / "golden_plan.json").read_text())
    return PlanGraph.model_validate(data)


def test_golden_plan_is_valid():
    plan = load_golden_plan()
    errors = validate_plan(plan, Flags())
    assert errors == []


def test_kpi_missing_objective():
    plan = load_golden_plan()
    plan.kpis[0].objective_id = "missing-obj"
    errors = validate_plan(plan, Flags())
    assert any("missing objective" in error for error in errors)


def test_optional_arrays_disabled():
    plan = load_golden_plan()
    plan.outputs = []
    errors = validate_plan(plan, Flags())
    assert "Outputs are present but disabled by flags." in errors
