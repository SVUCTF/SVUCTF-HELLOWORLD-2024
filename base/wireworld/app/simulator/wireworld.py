from typing import List, Tuple, Optional
from pydantic import BaseModel, Field
from app.simulator.cells import CellUnion, EmptyCell, ElectronHead
from app.simulator.components import ComponentUnion, Detector


class GridState(BaseModel):
    cell_grid: List[List[CellUnion]]
    component_grid: List[List[Optional[ComponentUnion]]]
    step: int

    class Config:
        arbitrary_types_allowed = True


class Wireworld(BaseModel):
    width: int
    height: int
    current_step: int = Field(default=0)
    cell_grid: List[List[CellUnion]] = Field(default_factory=list)
    component_grid: List[List[Optional[ComponentUnion]]] = Field(default_factory=list)
    detectors: List[Tuple[int, int]] = Field(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)
        self.cell_grid = [
            [EmptyCell() for _ in range(self.width)] for _ in range(self.height)
        ]
        self.component_grid = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]
        self.detectors = []

    def get_cell(self, x: int, y: int) -> Optional[CellUnion]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cell_grid[y][x]
        return None

    def set_cell(self, cell: CellUnion, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cell_grid[y][x] = cell

    def get_component(self, x: int, y: int) -> Optional[ComponentUnion]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.component_grid[y][x]
        return None

    def set_component(self, cell: ComponentUnion, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.component_grid[y][x] = cell
            if isinstance(cell, Detector):
                self.detectors.append((x, y))

    def get_grid_state(self) -> GridState:
        return GridState(
            cell_grid=self.cell_grid,
            component_grid=self.component_grid,
            step=self.current_step,
        )

    def count_electron_head_neighbors(self, x: int, y: int) -> int:
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if isinstance(self.cell_grid[ny][nx], ElectronHead):
                        count += 1
        return count

    def step(self):
        new_cell_grid = [
            [cell.update(self, x, y) for x, cell in enumerate(row)]
            for y, row in enumerate(self.cell_grid)
        ]
        self.cell_grid = new_cell_grid

        new_component_grid = [
            [
                component.update(self, x, y) if component else None
                for x, component in enumerate(row)
            ]
            for y, row in enumerate(self.component_grid)
        ]
        self.component_grid = new_component_grid

        self.current_step += 1

    def run(self, steps: int):
        for _ in range(steps):
            self.step()

    def __str__(self):
        return "\n".join(
            "".join(
                str(self.component_grid[y][x] or self.cell_grid[y][x])
                for x in range(self.width)
            )
            for y in range(self.height)
        )
