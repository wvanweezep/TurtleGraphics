import turtle

from window import Window
from renderer import Renderer


class Engine:
  def __init__(self):
    self.window: Window = Window("Version:1.0", (800, 600))
    self.renderer: Renderer = Renderer(self.window.screen)

  def _update(self) -> None:
      """Update the window"""
      self.renderer.render()

  def run(self):
    while self.window.active:
      self._update()
