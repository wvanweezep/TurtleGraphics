from main.util.math.vector2 import Vector2

class Transform:

    def __init__(self, position: Vector2, scale: Vector2, rotation: float):
        self.position: Vector2 = position
        self.scale: Vector2 = scale
        self.rotation: float = rotation
