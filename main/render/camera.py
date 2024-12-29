from main.util.math.vector2 import Vector2


class Camera:

    def __init__(self):
        self.position: Vector2 = Vector2(0, 0)
        self.targets: list[(Vector2, float)] = []
        self.zoom: float = 1

    def add_target(self, target: Vector2) -> None:
        self.targets.append(target)

    def remove_target(self, target: Vector2) -> None:
        self.targets.remove(target)

    def update(self) -> None:
        """Update the camera position"""
        sum_target: Vector2 = Vector2.zero()
        weight: float = 0
        for target in self.targets:
            sum_target += target[0] * target[1]
            weight += target[1]
        self.position.lerp(sum_target / weight, .1)
