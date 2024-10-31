from enum import Enum
from typing import Literal, Optional, Union
from pydantic import BaseModel, Field
from app.simulator.cells import ElectronHead, ElectronTail, Conductor


class ClockGenerator(BaseModel):
    type: Literal["ClockGenerator"] = "ClockGenerator"

    period: int = Field(default=4)
    start_step: int = Field(default=0)
    stop_step: Optional[int] = Field(default=None)
    counter: int = Field(default=0)

    def update(self, world: "Wireworld", x: int, y: int) -> "ClockGenerator":
        if self.start_step <= world.current_step:
            if self.stop_step and self.stop_step <= world.current_step:
                return self
            self.counter += 1
            if self.counter >= self.period:
                self.counter = 0
                world.set_cell(ElectronHead(), x, y)
        return self

    def __str__(self) -> str:
        return "C"


class DiodeDirection(str, Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Diode(BaseModel):
    type: Literal["Diode"] = "Diode"
    direction: DiodeDirection

    def update(self, world: "Wireworld", x: int, y: int) -> "Diode":
        if (
            self.direction == DiodeDirection.LEFT
            and isinstance(world.get_cell(x - 1, y), ElectronTail)
            and isinstance(world.get_cell(x, y), ElectronHead)
        ):
            world.set_cell(Conductor(), x, y)
        elif (
            self.direction == DiodeDirection.RIGHT
            and isinstance(world.get_cell(x + 1, y), ElectronTail)
            and isinstance(world.get_cell(x, y), ElectronHead)
        ):
            world.set_cell(Conductor(), x, y)
        return self

    def __str__(self) -> str:
        return "<" if self.direction == DiodeDirection.LEFT else ">"


class ElectronFlow(str, Enum):
    LEFT_TO_RIGHT = "LEFT_TO_RIGHT"
    RIGHT_TO_LEFT = "RIGHT_TO_LEFT"
    UP_TO_DOWN = "UP_TO_DOWN"
    DOWN_TO_UP = "DOWN_TO_UP"
    NONE = "NONE"


class Detector(BaseModel):
    type: Literal["Detector"] = "Detector"
    last_detection: int = Field(default=0)
    period: int = Field(default=0)
    last_flow: ElectronFlow = Field(default=ElectronFlow.NONE)

    def update(self, world: "Wireworld", x: int, y: int) -> "Detector":
        if isinstance(world.get_cell(x, y), ElectronHead):
            if self.last_detection > 0:
                self.period = self.last_detection + 1
            self.last_detection = 0
            self.last_flow = self.detect_flow(world, x, y)
        else:
            self.last_flow = ElectronFlow.NONE
            self.last_detection += 1
        return self

    def detect_flow(self, world: "Wireworld", x: int, y: int) -> ElectronFlow:
        if isinstance(world.get_cell(x, y), ElectronHead):
            if isinstance(world.get_cell(x - 1, y), ElectronTail):
                return ElectronFlow.LEFT_TO_RIGHT
            if isinstance(world.get_cell(x + 1, y), ElectronTail):
                return ElectronFlow.RIGHT_TO_LEFT
            if isinstance(world.get_cell(x, y - 1), ElectronTail):
                return ElectronFlow.UP_TO_DOWN
            if isinstance(world.get_cell(x, y + 1), ElectronTail):
                return ElectronFlow.DOWN_TO_UP
        return ElectronFlow.NONE

    def __str__(self) -> str:
        return "X"


ComponentUnion = Union[ClockGenerator, Diode, Detector]
