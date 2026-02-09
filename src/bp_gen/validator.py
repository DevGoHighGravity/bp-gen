from __future__ import annotations

from typing import List

from bp_gen.models import Flags, PlanGraph


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
