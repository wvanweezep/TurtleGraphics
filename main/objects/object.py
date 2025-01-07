from abc import abstractmethod, ABC
from typing import Optional, Type

from main.components.component import Component
from main.components.transform import Transform
from main.render.renderer import Renderer


class Object(ABC):
    """
    Class for the creation of object with certain behaviours.
    It can hold multiple components, each with their own behaviour
    and updates/renders them accordingly. All objects have a `Transform`
    and can be set to inactive.
    """

    def __init__(self, transform, active: bool = True):
        self._active: bool = active
        self._transform: Transform = transform
        self._components: list[Component] = []

    def get_active(self) -> bool:
        """Getter for Object state"""
        return self._active

    def set_active(self, state: bool) -> None:
        """Setter for Object state"""
        self._active = state

    def get_transform(self) -> Transform:
        """Getter for Object transform"""
        return self._transform

    def add_component(self, comp: Component) -> None:
        self._components.append(comp)

    def get_component(self, t: Type[Component]) -> Optional[Component]:
        """Returns the requested component if present, otherwise returns None"""
        for comp in self._components:
            if isinstance(comp, t):
                return comp
        return None

    @abstractmethod
    def update(self) -> None:
        """Updates all components of the object"""
        for comp in self._components:
            if comp.get_active(): comp.update()

    @abstractmethod
    def render(self, renderer: Renderer) -> None:
        """Renders all components (if implemented) of the object"""
        for comp in self._components:
            if comp.get_active(): comp.render(renderer)