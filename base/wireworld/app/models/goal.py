from typing import List, Literal, Union
from pydantic import BaseModel, Field

from app.simulator.wireworld import Wireworld
from app.simulator.components import Detector, ElectronFlow


class Goal(BaseModel):
    x: int
    y: int
    required_matches: int = Field(default=1)
    current_matches: int = Field(default=0)

    def check(self, world: Wireworld) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    def update(self, world: Wireworld) -> bool:
        if self.check(world):
            self.current_matches += 1
            return self.current_matches >= self.required_matches
        return False

    def is_achieved(self) -> bool:
        return self.current_matches >= self.required_matches


class SpecificPeriodGoal(Goal):
    type: Literal["SpecificPeriodGoal"]
    target_period: int

    def check(self, world: Wireworld) -> bool:
        component = world.get_component(self.x, self.y)
        if isinstance(component, Detector):
            return component.period == self.target_period
        return False


class ElectronFlowGoal(Goal):
    type: Literal["ElectronFlowGoal"]
    allowed_flows: List[ElectronFlow] = Field(default_factory=list)
    forbidden_flows: List[ElectronFlow] = Field(default_factory=list)
    failed: bool = Field(default=False)

    def check(self, world: Wireworld) -> bool:
        if self.failed:
            return False

        component = world.get_component(self.x, self.y)
        if isinstance(component, Detector):
            if component.last_flow in self.forbidden_flows:
                self.failed = True
                return False
            return component.last_flow in self.allowed_flows
        return False

    def update(self, world: Wireworld) -> bool:
        if self.failed:
            return False

        if self.check(world):
            self.current_matches += 1
            return self.current_matches >= self.required_matches
        return False

    def is_achieved(self) -> bool:
        return not self.failed and self.current_matches >= self.required_matches


GoalUnion = Union[SpecificPeriodGoal, ElectronFlowGoal]
