from main.components.animator import Animator
from main.objects.object import Object
from main.render.animation import Animation
from main.render.renderer import Renderer


class Enemy(Object):
    def __init__(self, transform):
        super().__init__(transform)
        self.components.append(Animator(self, [Animation.load_points("./resources/enemy/walk.anim")]))

    def update(self) -> None:
        pass

    def render(self, renderer: Renderer) -> None:
        self.components[0].update()
        self.components[0].render(renderer)
