import turtle

from main.components.transform import Transform
from main.render.camera import Camera
from main.util.math.point import Point
from main.util.math.vector2 import Vector2


class Renderer:

    def __init__(self, screen: turtle.Screen):
        self.screen: turtle.Screen = screen
        self.pen: turtle.Turtle = turtle.Turtle()
        self.camera = Camera()

        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()

    def render_points(self, points: list[Point], transform: Transform, size: tuple, color: str | tuple = 'white', render_points: bool = True, debug_points: list[Point] = ()) -> None:
        """Renders all points and connections in a list of points"""
        point_map = self.transform_points(points, transform, size)
        for point, connections in point_map.items():
            if render_points:
                if point in debug_points: self.render_point(point, color='lime')
                else: self.render_point(point, color=color)
            for connection in connections:
                self.render_connection(point, connection, color=color)

    def transform_points(self, points: list[Point], transform: Transform, size: tuple) -> dict[tuple[int, int], list[tuple[int, int]]]:
        t: Vector2 = transform.get_position() - self.camera.position
        return {((point.position + t)*self.camera.zoom).tuple(): [((c.position + t)*self.camera.zoom).tuple() for c in point.connections]
               for point in points}


    def render_point(self, position: tuple[int, int], color: str | tuple = 'white', size: int = 5) -> None:
        """Renders a singular point at a given position"""
        self.pen.penup()
        self.pen.pensize(size)
        self.pen.color(color)
        self.pen.goto(position[0], position[1])
        self.pen.pendown()
        self.pen.goto(position[0], position[1] + 1)

    def render_connection(self, origin: tuple[int, int], destination: tuple[int, int], color: str | tuple = 'white', size: int = 2) -> None:
        """Renders a connection between points"""
        self.pen.penup()
        self.pen.pensize(size)
        self.pen.color(color)
        self.pen.goto(origin[0], origin[1])
        self.pen.pendown()
        self.pen.goto(destination[0], destination[1])

    def write(self, arg: str, pos: tuple[int, int]):
        """Write text on the screen"""
        self.pen.penup()
        self.pen.color('white')
        self.pen.goto(pos)
        self.pen.pendown()
        self.pen.write(arg, move=False, align='left', font=('Arial', 8, 'normal'))

    def update_screen(self) -> None:
        """Render the new frame"""
        self.screen.update()