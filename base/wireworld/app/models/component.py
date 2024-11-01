from typing import Literal, Optional, Union
from pydantic import BaseModel

from app.simulator.components import DiodeDirection


class ClockConfig(BaseModel):
    type: Literal["ClockConfig"]
    x: int
    y: int
    period: int
    start_step: int
    stop_step: Optional[int] = None


class DiodeConfig(BaseModel):
    type: Literal["DiodeConfig"]
    x: int
    y: int
    direction: DiodeDirection


ComponentConfigUnion = Union[ClockConfig, DiodeConfig]
