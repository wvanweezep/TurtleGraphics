from abc import abstractmethod, ABC

from main.render.renderer import Renderer


class Component(ABC):

    def __init__(self, active: bool = True):
        self.active: bool = active

    @abstractmethod
    def update(self) -> None:
        """Updates the component logic"""
        pass

    @abstractmethod
    def render(self, renderer: Renderer) -> None:
        """Renders the component (if applicable)"""
        pass