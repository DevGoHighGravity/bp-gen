from __future__ import annotations

from typing import List, Sequence

from bp_gen.schemas import (
    BusinessPlan,
    BusinessContext,
    ClarifyingQuestions,
    Gap,
    GeneratePlanRequest,
    GenerationErrorResponse,
    KPI,
    Link,
    Objective,
    PlanMeta,
)
from bp_gen.validator import validate_business_plan


REQUIRED_CONTEXT_FIELDS = (
    "scope",
    "time_horizon",
    "problem_statement",
    "success_definition",
)


def _build_clarifying_questions(context: BusinessContext) -> List[str]:
    questions: List[str] = []
    if not context.scope:
        questions.append("What is the scope (business unit, region, or product line) for this plan?")
    if not context.time_horizon:
        questions.append("What is the time horizon for achieving the desired outcomes?")
    if not context.problem_statement:
        questions.append("What is the core problem statement to address?")
    if not context.success_definition:
        questions.append("How will success be defined or measured for this effort?")

    if len(questions) < 3:
        questions.extend(
            [
                "What constraints or guardrails should the plan respect?",
                "Which stakeholders or teams must be involved in delivering the outcomes?",
                "Are there existing metrics that matter most for this business context?",
            ]
        )

    return questions[:7]


def _missing_context(context: BusinessContext) -> bool:
    return any(getattr(context, field) in (None, "") for field in REQUIRED_CONTEXT_FIELDS)


def _objective_priority(index: int) -> str:
    if index == 0:
        return "high"
    if index == 1:
        return "medium"
    return "medium"


def _build_objectives(
    problem_statement: str,
    success_definition: str,
    scope: str,
) -> List[Objective]:
    titles = [
        f"Resolve {problem_statement}",
        f"Achieve {success_definition}",
        f"Sustain improvements across {scope}",
    ]
    rationales = [
        f"Directly addresses the stated problem: {problem_statement}.",
        f"Aligns outcomes to the stated success definition: {success_definition}.",
        f"Ensures gains are maintained within the defined scope: {scope}.",
    ]
    return [
        Objective(
            id=f"obj-{idx + 1}",
            title=title,
            rationale=rationales[idx],
            owner_role=None,
            priority=_objective_priority(idx),
        )
        for idx, title in enumerate(titles)
    ]


def _build_kpis(
    objectives: Sequence[Objective],
    success_definition: str,
) -> List[KPI]:
    kpis: List[KPI] = []
    for obj_index, objective in enumerate(objectives):
        for kpi_index in range(2):
            kpi_id = f"kpi-{obj_index + 1}-{kpi_index + 1}"
            leading_or_lagging = "lagging" if kpi_index == 0 else "leading"
            name = f"Progress on {objective.title}"
            definition = (
                f"Measures advancement toward objective '{objective.title}'."
                if kpi_index == 0
                else f"Tracks leading indicators for '{objective.title}'."
            )
            kpis.append(
                KPI(
                    id=kpi_id,
                    objective_id=objective.id,
                    name=name,
                    definition=definition,
                    formula=None,
                    baseline=None,
                    target=f"Aligned to success definition: {success_definition}",
                    frequency="monthly",
                    data_source=None,
                    leading_or_lagging=leading_or_lagging,
                )
            )
    return kpis


def _build_links(kpis: Sequence[KPI], allowed_relationships: Sequence[str]) -> List[Link]:
    if "objective_to_kpi" in allowed_relationships:
        link_type = "objective_to_kpi"
    elif allowed_relationships:
        link_type = allowed_relationships[0]
    else:
        link_type = "objective_to_kpi"

    return [
        Link(
            from_type="objective",
            from_id=kpi.objective_id,
            to_type="kpi",
            to_id=kpi.id,
            type=link_type,
        )
        for kpi in kpis
    ]


def _build_gaps() -> List[Gap]:
    return [
        Gap(
            item="KPI baselines",
            needed="Baseline values for each KPI.",
            impact="Cannot quantify improvement without starting measurements.",
        ),
        Gap(
            item="KPI data sources",
            needed="Authoritative data sources for KPI reporting.",
            impact="Risk of inconsistent measurement across teams.",
        ),
        Gap(
            item="Objective ownership",
            needed="Owner roles for each objective.",
            impact="Accountability is unclear without designated owners.",
        ),
        Gap(
            item="Target dates",
            needed="Target dates for KPI achievement.",
            impact="Unable to sequence delivery without timelines.",
        ),
    ]


def generate_plan(
    request: GeneratePlanRequest,
) -> BusinessPlan | ClarifyingQuestions | GenerationErrorResponse:
    context = request.business_context
    if _missing_context(context):
        return ClarifyingQuestions(clarifying_questions=_build_clarifying_questions(context))

    objectives = _build_objectives(
        problem_statement=context.problem_statement or "",
        success_definition=context.success_definition or "",
        scope=context.scope or "",
    )
    kpis = _build_kpis(objectives, context.success_definition or "")
    links = _build_links(kpis, request.allowed_relationships)
    plan = BusinessPlan(
        plan=PlanMeta(
            name=context.plan_name or f"{context.scope} Business Plan",
            horizon=context.time_horizon or "",
            scope=context.scope or "",
            themes=["Problem resolution", "Success definition alignment"],
        ),
        objectives=objectives,
        kpis=kpis,
        initiatives=[] if request.flags.include_initiatives else None,
        capabilities=[] if request.flags.include_capabilities else None,
        outputs=[] if request.flags.include_outputs else None,
        links=links,
        assumptions_and_gaps=_build_gaps(),
    )

    validation = validate_business_plan(plan, request.flags)
    if not validation["ok"]:
        return GenerationErrorResponse(
            errors=validation["errors"],
            required_user_inputs=[
                "Provide missing relationships or required fields highlighted in errors.",
            ],
        )

    return plan
