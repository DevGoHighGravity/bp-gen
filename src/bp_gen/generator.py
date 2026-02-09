from __future__ import annotations

from datetime import datetime
from typing import List, Union

from bp_gen.models import (
    AssumptionGap,
    ClarifyingQuestions,
    GeneratePlanRequest,
    KPI,
    Link,
    Objective,
    PlanGraph,
    PlanMetadata,
)


def _needs_clarification(request: GeneratePlanRequest) -> List[str]:
    questions: List[str] = []
    if not request.business_context.summary:
        questions.append("Provide a concise business context summary.")
    if not request.business_context.goals:
        questions.append("List the primary business goals to translate into objectives and KPIs.")
    return questions


def generate_plan(
    request: GeneratePlanRequest,
) -> Union[PlanGraph, ClarifyingQuestions]:
    questions = _needs_clarification(request)
    if questions:
        return ClarifyingQuestions(clarifying_questions=questions)

    goals = request.business_context.goals or []

    objectives = [
        Objective(id=f"obj-{idx+1}", name=goal, description=None)
        for idx, goal in enumerate(goals)
    ]
    kpis = [
        KPI(
            id=f"kpi-{idx+1}",
            objective_id=objective.id,
            name=f"Progress toward {objective.name}",
            description=None,
            unit=None,
            baseline=None,
            target=None,
            data_source=None,
            owner=None,
            target_date=None,
        )
        for idx, objective in enumerate(objectives)
    ]

    links = [
        Link(
            id=f"link-{idx+1}",
            source_id=kpi.objective_id,
            target_id=kpi.id,
            type="objective_to_kpi",
        )
        for idx, kpi in enumerate(kpis)
    ]

    assumptions = [
        AssumptionGap(
            id="gap-1",
            description="Baseline values, data sources, owners, and target dates are not provided; they remain null until confirmed.",
        )
    ]

    plan = PlanGraph(
        metadata=PlanMetadata(
            plan_id="plan-1",
            title="Business Case Plan",
            created_at=datetime.utcnow(),
        ),
        objectives=objectives,
        kpis=kpis,
        initiatives=[] if request.flags.enable_initiatives else None,
        capabilities=[] if request.flags.enable_capabilities else None,
        outputs=[] if request.flags.enable_outputs else None,
        links=links,
        assumptions_and_gaps=assumptions,
    )

    return plan
