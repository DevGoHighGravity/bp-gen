from __future__ import annotations

from typing import Dict, List, Set

from bp_gen.models import Flags, PlanGraph
from bp_gen.schemas import BusinessPlan, GenerationFlags


def validate_plan(plan: PlanGraph, flags: Flags) -> List[str]:
    errors: List[str] = []

    if not plan.objectives:
        errors.append("At least one objective is required.")

    if not plan.kpis:
        errors.append("At least one KPI is required.")

    objective_ids = {objective.id for objective in plan.objectives}
    for kpi in plan.kpis:
        if kpi.objective_id not in objective_ids:
            errors.append(f"KPI '{kpi.id}' references missing objective '{kpi.objective_id}'.")

    link_pairs = {(link.source_id, link.target_id) for link in plan.links}
    for kpi in plan.kpis:
        if (kpi.objective_id, kpi.id) not in link_pairs:
            errors.append(
                f"Missing link from objective '{kpi.objective_id}' to KPI '{kpi.id}'."
            )

    if not flags.enable_initiatives and plan.initiatives is not None:
        errors.append("Initiatives are present but disabled by flags.")

    if not flags.enable_capabilities and plan.capabilities is not None:
        errors.append("Capabilities are present but disabled by flags.")

    if not flags.enable_outputs and plan.outputs is not None:
        errors.append("Outputs are present but disabled by flags.")

    return errors


def validate_business_plan(plan: BusinessPlan, flags: GenerationFlags) -> Dict[str, object]:
    errors: List[Dict[str, str]] = []

    def add_error(code: str, message: str, path: str) -> None:
        errors.append({"code": code, "message": message, "path": path})

    objectives = plan.objectives or []
    kpis = plan.kpis or []

    if len(objectives) < 1:
        add_error("objectives_required", "At least one objective is required.", "objectives")

    if len(kpis) < 1:
        add_error("kpis_required", "At least one KPI is required.", "kpis")

    objective_ids = {objective.id for objective in objectives}
    kpis_by_objective: Dict[str, List[str]] = {objective.id: [] for objective in objectives}
    for index, kpi in enumerate(kpis):
        if kpi.objective_id not in objective_ids:
            add_error(
                "kpi_unknown_objective",
                f"KPI '{kpi.id}' references unknown objective '{kpi.objective_id}'.",
                f"kpis[{index}].objective_id",
            )
        else:
            kpis_by_objective[kpi.objective_id].append(kpi.id)

    for index, objective in enumerate(objectives):
        if len(kpis_by_objective.get(objective.id, [])) < 1:
            add_error(
                "objective_missing_kpi",
                f"Objective '{objective.id}' must have at least one KPI.",
                f"objectives[{index}].id",
            )

    if not flags.include_initiatives and plan.initiatives:
        add_error(
            "initiatives_disabled",
            "Initiatives are present but disabled by flags.",
            "initiatives",
        )

    if not flags.include_capabilities and plan.capabilities:
        add_error(
            "capabilities_disabled",
            "Capabilities are present but disabled by flags.",
            "capabilities",
        )

    if not flags.include_outputs and plan.outputs:
        add_error(
            "outputs_disabled",
            "Outputs are present but disabled by flags.",
            "outputs",
        )

    def collect_ids(items: List[object]) -> Set[str]:
        return {item.id for item in items}

    id_registry: Dict[str, Set[str]] = {
        "objective": collect_ids(objectives),
        "kpi": collect_ids(kpis),
        "initiative": collect_ids(plan.initiatives or []),
        "capability": collect_ids(plan.capabilities or []),
        "output": collect_ids(plan.outputs or []),
    }

    for index, link in enumerate(plan.links):
        if link.from_type not in id_registry:
            add_error(
                "link_unknown_type",
                f"Link from_type '{link.from_type}' is not recognized.",
                f"links[{index}].from_type",
            )
        elif link.from_id not in id_registry[link.from_type]:
            add_error(
                "link_unknown_id",
                f"Link from_id '{link.from_id}' not found for type '{link.from_type}'.",
                f"links[{index}].from_id",
            )

        if link.to_type not in id_registry:
            add_error(
                "link_unknown_type",
                f"Link to_type '{link.to_type}' is not recognized.",
                f"links[{index}].to_type",
            )
        elif link.to_id not in id_registry[link.to_type]:
            add_error(
                "link_unknown_id",
                f"Link to_id '{link.to_id}' not found for type '{link.to_type}'.",
                f"links[{index}].to_id",
            )

    return {"ok": len(errors) == 0, "errors": errors}
