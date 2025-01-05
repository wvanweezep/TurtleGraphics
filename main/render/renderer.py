import turtle

from main.render.camera import Camera


class Renderer:

    def __init__(self, screen: turtle.Screen):
        self.screen: turtle.Screen = screen
        self.pen: turtle.Turtle = turtle.Turtle()
        self.camera = Camera()

        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()

    def render(self) -> None:
        """Render the new frame"""
        self.screen.update()