import asyncio
from typing import List
from fastapi import HTTPException
from pydantic import Field
import rtoml
from app.core.config import settings
from app.models.challenge import (
    ChallengeConfig,
    ChallengeInfo,
    EditableArea,
    Grid,
    Meta,
    SimulationResult,
)
from app.models.component import ClockConfig, DiodeConfig
from app.simulator.components import ClockGenerator, Diode, Detector, DiodeDirection
from app.simulator.cells import (
    CellUnion,
    ElectronHead,
    ElectronTail,
    Conductor,
    EmptyCell,
)
from app.simulator.wireworld import Wireworld


class ChallengeService:
    config: ChallengeConfig
    world: Wireworld
    completed: bool = Field(default=False)

    @classmethod
    def load_challenge(cls):
        try:
            with open(settings.CHALLENGE_FILE, encoding="utf-8") as f:
                config_dict = rtoml.load(f)

            cls.config = ChallengeConfig(**config_dict)
            cls.world = Wireworld(
                width=cls.config.grid.width, height=cls.config.grid.height
            )
            cls._setup_initial_state()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to load challenge: {str(e)}"
            ) from e

    @classmethod
    def _setup_initial_state(cls):
        initial_state = cls.config.initial_state
        for y, (component_row, cell_row) in enumerate(
            zip(
                initial_state.component_grid,
                initial_state.cell_grid,
            )
        ):
            for x, (component, cell) in enumerate(zip(component_row, cell_row)):
                if component != ".":
                    cls._set_component(x, y, component)
                if cell != ".":
                    cls._set_cell(x, y, cell)

        cls._apply_component_configs()

    @classmethod
    def _set_component(cls, x: int, y: int, component_type: str):
        component_map = {
            "C": ClockGenerator,
            "<": lambda: Diode(direction=DiodeDirection.LEFT),
            ">": lambda: Diode(direction=DiodeDirection.RIGHT),
            "X": Detector,
        }
        if component_type in component_map:
            cls.world.set_component(component_map[component_type](), x, y)
        else:
            raise ValueError(f"Unknown component type: {component_type}")

    @classmethod
    def _set_cell(cls, x: int, y: int, cell_type: str):
        cell_map = {
            "#": Conductor,
            "H": ElectronHead,
            "t": ElectronTail,
        }
        if cell_type in cell_map:
            cls.world.set_cell(cell_map[cell_type](), x, y)
        else:
            raise ValueError(f"Unknown cell type: {cell_type}")

    @classmethod
    def _apply_component_configs(cls):
        for config in cls.config.components:
            if isinstance(config, ClockConfig):
                cls.world.set_component(
                    ClockGenerator(
                        period=config.period,
                        start_step=config.start_step,
                        stop_step=config.stop_step,
                    ),
                    config.x,
                    config.y,
                )
            elif isinstance(config, DiodeConfig):
                cls.world.set_component(
                    Diode(direction=config.direction), config.x, config.y
                )

    @classmethod
    def _is_within_editable_area(cls, x: int, y: int) -> bool:
        area = cls.config.editable_area
        return 0 <= x < area.width and 0 <= y < area.height

    @classmethod
    def _apply_user_design(cls, design: List[List[CellUnion]]):
        area = cls.config.editable_area
        for y, row in enumerate(design):
            for x, cell in enumerate(row):
                if cls._is_within_editable_area(x, y):
                    world_x = area.x + x
                    world_y = area.y + y
                    if isinstance(cell, Conductor):
                        cls.world.set_cell(Conductor(), world_x, world_y)
                    elif isinstance(cell, ElectronHead):
                        cls.world.set_cell(ElectronHead(), world_x, world_y)
                    elif isinstance(cell, ElectronTail):
                        cls.world.set_cell(ElectronTail(), world_x, world_y)
                    elif isinstance(cell, EmptyCell):
                        cls.world.set_cell(EmptyCell(), world_x, world_y)

    @classmethod
    def reset(cls):
        cls.world = Wireworld(
            width=cls.config.grid.width, height=cls.config.grid.height
        )
        cls._setup_initial_state()
        for goal in cls.config.goals:
            goal.reset()
        cls.completed = False

    @classmethod
    async def run_simulation(cls, user_design: List[List[CellUnion]]):
        cls.reset()
        cls._apply_user_design(user_design)

        yield cls.world.get_grid_state()

        for _ in range(cls.config.grid.max_steps):
            cls.world.step()

            for goal in cls.config.goals:
                goal.update(cls.world)

            if all(goal.is_achieved() for goal in cls.config.goals):
                cls.completed = True
                break

            yield cls.world.get_grid_state()
            await asyncio.sleep(0.1)

        cls.completed = True

    @classmethod
    def get_simulation_result(cls) -> SimulationResult:
        if not cls.completed:
            raise RuntimeError("Simulation has not completed yet")
        success = all(goal.is_achieved() for goal in cls.config.goals)
        return SimulationResult(
            success=success,
            final_state=cls.world.get_grid_state(),
            flag=settings.FLAG if success else None,
        )

    @classmethod
    def get_challenge_info(cls):
        return ChallengeInfo(
            meta=Meta(
                name=cls.config.meta.name,
                description=cls.config.meta.description,
                cell_descriptions=cls.config.meta.cell_descriptions,
                component_descriptions=cls.config.meta.component_descriptions,
            ),
            grid=Grid(
                width=cls.config.grid.width,
                height=cls.config.grid.height,
                max_steps=cls.config.grid.max_steps,
            ),
            editable_area=EditableArea(**cls.config.editable_area.model_dump()),
            initial_state=cls.world.get_grid_state(),
        )
