import os
import pickle

from main.util.math.point import Point


class Animation:
    def __init__(self, frames: list[list[Point]], size: tuple, fps: int):
        self.frames: list[list[Point]] = frames
        self.size: tuple = size
        self.fps: int = fps
