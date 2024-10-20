from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.goal import GoalUnion
from app.models.component import ComponentConfigUnion
from app.simulator.cells import CellUnion
from app.simulator.wireworld import GridState


class Meta(BaseModel):
    name: str
    description: str
    cell_descriptions: dict[str, str] = Field(default={})
    component_descriptions: dict[str, str] = Field(default={})


class EditableArea(BaseModel):
    x: int
    y: int
    width: int
    height: int


class Grid(BaseModel):
    width: int
    height: int
    max_steps: int


class InitialState(BaseModel):
    cell_grid: List[str]
    component_grid: List[str]


class ChallengeConfig(BaseModel):
    meta: Meta
    grid: Grid
    editable_area: EditableArea
    initial_state: InitialState
    components: List[ComponentConfigUnion] = Field(default=[])
    goals: List[GoalUnion]


class UserDesign(BaseModel):
    design: List[List[CellUnion]]


class SimulationResult(BaseModel):
    success: bool
    final_state: GridState
    flag: Optional[str]


class ChallengeInfo(BaseModel):
    meta: Meta
    grid: Grid
    editable_area: EditableArea
    initial_state: GridState
