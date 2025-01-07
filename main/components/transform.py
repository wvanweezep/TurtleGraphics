from main.util.math.vector2 import Vector2


class Transform:
    """Class for holding transformation data for an `Object`."""

    def __init__(self, position: Vector2, scale: Vector2, rotation: float):
        self._position: Vector2 = position
        self._scale: Vector2 = scale
        self._rotation: float = rotation

    def get_position(self) -> Vector2:
        """Getter for position"""
        return self._position.copy()

    def set_position(self, position: Vector2) -> None:
        """Setter for position"""
        self._position.set(position.x, position.y)

    def get_scale(self) -> Vector2:
        """Getter for scale"""
        return self._scale.copy()

    def set_scale(self, scale: Vector2) -> None:
        """Setter for scale"""
        self._scale.set(scale.x, scale.y)

    def get_rotation(self) -> float:
        """Getter for rotation"""
        return self._rotation

    def set_rotation(self, rotation: float) -> None:
        """Setter for rotation"""
        self._rotation = rotation
