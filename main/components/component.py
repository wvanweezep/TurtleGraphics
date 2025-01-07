from abc import abstractmethod, ABC

from main.render.renderer import Renderer


class Component(ABC):
    """
    Base class for a `Component` with a `render` and `update`
    abstract method and a `active` field
    """

    def __init__(self, active: bool = True):
        self._active: bool = active

    def get_active(self) -> bool:
        """Getter for Component state"""
        return self._active

    def set_active(self, state: bool) -> None:
        """Setter for Component state"""
        self._active = state

    @abstractmethod
    def update(self) -> None:
        """Updates the component logic"""
        pass

    @abstractmethod
    def render(self, renderer: Renderer) -> None:
        """Renders the component (if applicable)"""
        pass