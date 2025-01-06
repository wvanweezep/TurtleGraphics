from main.util.math.vector2 import Vector2


class Point:
    def __init__(self, position: Vector2, connections: list['Point'] = None):
        self.position: Vector2 = position
        if not connections: self.connections: list['Point'] = []
        else: self.connections = connections

    def __repr__(self):
        return f'{self.position.__repr__()}\n'

    def add_point(self, new_point: 'Point') -> None:
        for point in self.connections:
            if point == new_point: return
        self.connections.append(new_point)

    def remove_point(self, point: 'Point') -> None:
        if point in self.connections: self.connections.remove(point)

    def copy(self) -> 'Point':
        return Point(self.position, self.connections)