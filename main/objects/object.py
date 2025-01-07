from abc import abstractmethod, ABC
from typing import Optional, Type

from main.components.component import Component
from main.components.transform import Transform
from main.render.renderer import Renderer


class Object(ABC):

    def __init__(self, transform, active: bool = True):
        self.active: bool = active
        self.transform: Transform = transform
        self.components: list[Component] = []

    def get_component(self, t: Type[Component]) -> Optional[Component]:
        """Returns the requested component if present, otherwise returns None"""
        for comp in self.components:
            if isinstance(comp, t):
                return comp
        return None

    @abstractmethod
    def update(self) -> None:
        """Updates all components of the object"""
        for comp in self.components:
            if comp.active: comp.update()

    @abstractmethod
    def render(self, renderer: Renderer) -> None:
        """Renders all components (if implemented) of the object"""
        for comp in self.components:
            if comp.active: comp.update()