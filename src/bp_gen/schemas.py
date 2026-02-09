from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class PlanMeta(BaseModel):
    """Top-level plan metadata for the business plan graph."""

    name: str
    horizon: str
    scope: str
    themes: List[str] = Field(default_factory=list)


class Objective(BaseModel):
    """Business objective that the plan intends to achieve."""

    id: str
    title: str
    rationale: str
    owner_role: Optional[str] = None
    priority: str


class KPI(BaseModel):
    """Key performance indicator that measures objective progress."""

    id: str
    objective_id: str = Field(
        description="Must reference an Objective.id (validator will enforce)."
    )
    name: str
    definition: str
    formula: Optional[str] = None
    baseline: Optional[str] = None
    target: str
    frequency: str
    data_source: Optional[str] = None
    leading_or_lagging: str


class Initiative(BaseModel):
    """Optional initiative that supports objectives (when enabled)."""

    id: str
    name: str
    description: Optional[str] = None


class Capability(BaseModel):
    """Optional capability required to execute initiatives (when enabled)."""

    id: str
    name: str
    description: Optional[str] = None


class Output(BaseModel):
    """Optional output delivered by initiatives (when enabled)."""

    id: str
    name: str
    description: Optional[str] = None


class Link(BaseModel):
    """Directed relationship between nodes in the plan graph."""

    from_type: str
    from_id: str
    to_type: str
    to_id: str
    type: str


class Gap(BaseModel):
    """Assumption or data gap captured for later validation."""

    item: str
    needed: str
    impact: str


class BusinessPlan(BaseModel):
    """Full business plan graph representation."""

    plan: PlanMeta
    objectives: List[Objective] = Field(min_length=1)
    kpis: List[KPI] = Field(min_length=1)
    initiatives: Optional[List[Initiative]] = Field(
        default=None, description="Optional array; omit or empty unless enabled."
    )
    capabilities: Optional[List[Capability]] = Field(
        default=None, description="Optional array; omit or empty unless enabled."
    )
    outputs: Optional[List[Output]] = Field(
        default=None, description="Optional array; omit or empty unless enabled."
    )
    links: List[Link] = Field(default_factory=list)
    assumptions_and_gaps: List[Gap] = Field(default_factory=list)


class BusinessContext(BaseModel):
    """Input context required to generate a plan."""

    scope: Optional[str] = None
    time_horizon: Optional[str] = None
    problem_statement: Optional[str] = None
    success_definition: Optional[str] = None
    plan_name: Optional[str] = None


class GenerationFlags(BaseModel):
    """Feature flags controlling optional entities."""

    include_initiatives: bool = False
    include_capabilities: bool = False
    include_outputs: bool = False


class GeneratePlanRequest(BaseModel):
    """Request payload for plan generation."""

    business_context: BusinessContext
    constraints: Optional[List[str]] = None
    flags: GenerationFlags = Field(default_factory=GenerationFlags)
    allowed_relationships: List[str] = Field(
        description="Authoritative list of allowed relationship types."
    )
    generation_controls: Optional[Dict[str, str]] = None


class GeneratePlanResponse(BaseModel):
    """Response payload that returns a plan or clarifying questions."""

    plan: Optional[BusinessPlan] = None
    clarifying_questions: Optional[List[str]] = None


class ClarifyingQuestions(BaseModel):
    """Clarifying questions returned when essential context is missing."""

    clarifying_questions: List[str]


class GenerationErrorResponse(BaseModel):
    """Validation errors returned when a generated plan is invalid."""

    errors: List[Dict[str, str]] = Field(default_factory=list)
    required_user_inputs: List[str] = Field(default_factory=list)
