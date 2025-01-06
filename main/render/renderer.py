import turtle

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

    def render_points(self, points: list[Point], color: str | tuple = 'white', render_points: bool = True, debug_points: list[Point] = ()) -> None:
        """Renders all points and connections in a list of points"""
        for point in points:
            if render_points:
                if point in debug_points: self.render_point(point.position, color='lime')
                else: self.render_point(point.position, color=color)
            for connection in point.connections:
                self.render_connection(point.position, connection.position, color=color)

    def render_point(self, position: Vector2, color: str | tuple = 'white', size: int = 5) -> None:
        """Renders a singular point at a given position"""
        self.pen.penup()
        self.pen.pensize(size)
        self.pen.color(color)
        self.pen.goto(position.x, position.y)
        self.pen.pendown()
        self.pen.goto(position.x, position.y + 1)

    def render_connection(self, origin: Vector2, destination: Vector2, color: str | tuple = 'white', size: int = 2) -> None:
        """Renders a connection between points"""
        self.pen.penup()
        self.pen.pensize(size)
        self.pen.color(color)
        self.pen.goto(origin.x, origin.y)
        self.pen.pendown()
        self.pen.goto(destination.x, destination.y)

    def write(self, arg: str, pos: tuple[int, int]):
        self.pen.penup()
        self.pen.color('white')
        self.pen.goto(pos)
        self.pen.pendown()
        self.pen.write(arg, move=False, align='left', font=('Arial', 8, 'normal'))

    def render(self) -> None:
        """Render the new frame"""
        self.screen.update()