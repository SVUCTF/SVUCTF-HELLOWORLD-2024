from typing import Literal, Union
from pydantic import BaseModel


class EmptyCell(BaseModel):
    type: Literal["EmptyCell"] = "EmptyCell"

    def update(self, world: "Wireworld", x: int, y: int) -> "EmptyCell":
        return self

    def __str__(self) -> str:
        return "."


class ElectronHead(BaseModel):
    type: Literal["ElectronHead"] = "ElectronHead"

    def update(self, world: "Wireworld", x: int, y: int) -> "ElectronTail":
        return ElectronTail()

    def __str__(self) -> str:
        return "H"


class ElectronTail(BaseModel):
    type: Literal["ElectronTail"] = "ElectronTail"

    def update(self, world: "Wireworld", x: int, y: int) -> "Conductor":
        return Conductor()

    def __str__(self) -> str:
        return "t"


class Conductor(BaseModel):
    type: Literal["Conductor"] = "Conductor"

    def update(
        self, world: "Wireworld", x: int, y: int
    ) -> Union["Conductor", "ElectronHead"]:
        count = world.count_electron_head_neighbors(x, y)
        if count in (1, 2):
            return ElectronHead()
        return self

    def __str__(self) -> str:
        return "#"


CellUnion = Union[EmptyCell, ElectronHead, ElectronTail, Conductor]
