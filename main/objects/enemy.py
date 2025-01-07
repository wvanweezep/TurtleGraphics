from main.components.animator import Animator
from main.objects.object import Object
from main.render.animation import Animation
from main.render.renderer import Renderer


class Enemy(Object):
    def __init__(self, transform):
        super().__init__(transform)
        self.add_component(Animator(self, {'walk':Animation.load_points("./resources/enemy/walk.anim")}))

    def update(self) -> None:
        super().update()

    def render(self, renderer: Renderer) -> None:
        self.get_component(Animator).render(renderer)
