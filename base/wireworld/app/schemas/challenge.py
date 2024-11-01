from typing import List, Optional, Union, Literal
from pydantic import BaseModel

from app.models.challenge import EditableArea, Grid, Meta
from app.simulator.wireworld import GridState
from app.simulator.cells import CellUnion


# Input message models
class SimulateMessage(BaseModel):
    type: Literal["simulate"]
    design: List[List[CellUnion]]


class GetInfoMessage(BaseModel):
    type: Literal["get_info"]


class ResetMessage(BaseModel):
    type: Literal["reset"]


# Output message models
class SimulationResultMessage(BaseModel):
    type: Literal["simulation_result"] = "simulation_result"
    success: bool
    final_state: GridState
    flag: Optional[str]


class WorldUpdateMessage(BaseModel):
    type: Literal["world_update"] = "world_update"
    grid_state: GridState


class ChallengeInfoMessage(BaseModel):
    type: Literal["challenge_info"] = "challenge_info"
    meta: Meta
    grid: Grid
    editable_area: EditableArea
    initial_state: GridState


class ErrorMessage(BaseModel):
    type: Literal["error"]
    message: str


# Union type for input messages
WebSocketMessageUnion = Union[SimulateMessage, GetInfoMessage, ResetMessage]
