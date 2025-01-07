from main.components.transform import Transform
from main.ticker import Ticker
from main.util.math.vector2 import Vector2
from main.objects.enemy import Enemy
from main.objects.object import Object
from main.window import Window
from main.render.renderer import Renderer


class Engine:

    def __init__(self):
        self.window: Window = Window("Version:1.0", (1800, 1000))
        self.renderer: Renderer = Renderer(self.window.screen)
        self.ticker: Ticker = Ticker(60)
        self.objects: list[Object] = [Enemy(Transform(Vector2(0, 0), Vector2(1, 1), 0))]

    def _update(self) -> None:
        """Update the window"""
        self.renderer.pen.clear()
        self.objects[0].render(self.renderer)
        self.renderer.render()

    def _render(self) -> None:
        """Renders all objects in the window"""
        pass

    def run(self) -> None:
        """Keeps the engine running"""
        while self.window.active:
            self.ticker.tick(Engine._update, Engine._render, self)
