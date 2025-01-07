from main.components.component import Component
from main.objects.object import Object
from main.render.animation import Animation
from main.render.renderer import Renderer
from main.util.debug.logger import Logger





class Animator(Component):
    """
    `Component` handling the animation of an Object. Animations can be queued
    by entering their name in the queue, or just directly played using
    `play_animation(name)`.
    """

    def __init__(self, obj: Object, animations: dict[str, Animation]):
        super().__init__()
        self._object: Object = obj
        self.animations: dict[str, Animation] = animations
        self._active_animation: tuple[str, Animation] = next(iter(self.animations.items()))
        self._queue: list[str] = []
        self.paused: bool = False
        self._accum: int = 0

    def play_animation(self, name: str) -> None:
        """Plays an animation if present"""
        if name in self.animations:
            self._active_animation = self.animations[name]
        else: Logger.log(f'{type(self._object)}:Animator',
                         f'Animator does not have animation: {name}',
                         error=True)

    def queue_animation(self, name: str) -> None:
        """Queues an animation if present"""
        if name in self.animations:
            self._queue.append(name)
        else: Logger.log(f'{type(self._object)}:Animator',
                         f'Animator does not have animation: {name}',
                         error=True)

    def clear_queue(self) -> None:
        """Clears the current animation queue"""
        self._queue.clear()

    def _check_queue(self) -> None:
        """Play switch animations if one is queued"""
        if len(self._queue):
            self.play_animation(self._queue.pop(0))

    def update(self) -> None:
        """Updates the accumulator for program ticks"""
        if not self.paused: self._accum += 1
        if self._accum >= len(self._active_animation[1].frames) * (60/self._active_animation[1].fps):
            self._accum = 0
            self._check_queue()

    def render(self, renderer: Renderer) -> None:
        """Renders the current frame to the Canvas"""
        renderer.render_points(self._active_animation[1].frames[self._accum//6], render_points=False)
