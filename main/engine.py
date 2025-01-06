from main.window import Window
from main.render.renderer import Renderer


class Engine:

    def __init__(self):
        self.window: Window = Window("Version:1.0", (1800, 1000))
        self.renderer: Renderer = Renderer(self.window.screen)

    def _update(self) -> None:
        """Update the window"""
        self.renderer.render()

    def run(self) -> None:
        """Keeps the engine running"""
        while self.window.active:
            self._update()
