import os, pickle

from main.util.math.point import Point


class Animation:
    def __init__(self, frames: list[list[Point]], size: tuple, fps: int):
        self.frames: list[list[Point]] = frames
        self.size: tuple = size
        self.fps: int = fps

    @staticmethod
    def load_points(path: str) -> 'Animation':
        """Load self.points from a file. Create the file if it doesn't exist."""
        if not os.path.exists(path):
            print(f"{path} does not exist.")
        else:
            with open(path, 'rb') as file:
                return pickle.load(file)