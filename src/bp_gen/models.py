from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Flags(BaseModel):
    enable_initiatives: bool = False
    enable_capabilities: bool = False
    enable_outputs: bool = False


class PlanMetadata(BaseModel):
    plan_id: str
    title: str
    created_at: datetime
    version: str = "v1"


class Objective(BaseModel):
    id: str
    name: str
    description: Optional[str] = None


class KPI(BaseModel):
    id: str
    objective_id: str
    name: str
    description: Optional[str] = None
    unit: Optional[str] = None
    baseline: Optional[float] = None
    target: Optional[float] = None
    data_source: Optional[str] = None
    owner: Optional[str] = None
    target_date: Optional[str] = None


class Initiative(BaseModel):
    id: str
    name: str
    description: Optional[str] = None


class Capability(BaseModel):
    id: str
    name: str
    description: Optional[str] = None


class Output(BaseModel):
    id: str
    name: str
    description: Optional[str] = None


class Link(BaseModel):
    id: str
    source_id: str
    target_id: str
    type: str


class AssumptionGap(BaseModel):
    id: str
    description: str


class PlanGraph(BaseModel):
    metadata: PlanMetadata
    objectives: List[Objective] = Field(min_length=1)
    kpis: List[KPI] = Field(min_length=1)
    initiatives: Optional[List[Initiative]] = None
    capabilities: Optional[List[Capability]] = None
    outputs: Optional[List[Output]] = None
    links: List[Link]
    assumptions_and_gaps: List[AssumptionGap]


class ClarifyingQuestions(BaseModel):
    clarifying_questions: List[str]


class BusinessContext(BaseModel):
    summary: Optional[str] = None
    goals: Optional[List[str]] = None
    current_state: Optional[str] = None


class GeneratePlanRequest(BaseModel):
    business_context: BusinessContext
    constraints: Optional[List[str]] = None
    flags: Flags = Field(default_factory=Flags)
