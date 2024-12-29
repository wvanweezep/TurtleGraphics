import turtle


class Window:

    def __init__(self, title: str, screen_size: tuple):
        self.screen: turtle.Screen = turtle.Screen()
        self._config(screen_size)
        self.active: bool = True

        self.screen.setup(screen_size[0], screen_size[1])
        self.screen.setworldcoordinates(0, 0, screen_size[0], screen_size[1])
        self.screen.title(title)
        self.screen.bgcolor("black")
        self.screen.tracer(0)

    def _config(self, screen_size: tuple) -> None:
        """Configures the underlying tkinter window."""
        root = self.screen._root
        root.protocol("WM_DELETE_WINDOW", self._on_close)
        root.geometry(f"{screen_size[0]}x{screen_size[1]}")
        root.resizable(False, False)

    def _on_close(self) -> None:
        """Protocol for closing ``turtle.Screen``, setting the active flag to ``False``"""
        self.active = False

    def resize(self, screen_size: tuple) -> None:
        self._config(screen_size)
        self.screen.setup(screen_size[0], screen_size[1])
        self.screen.setworldcoordinates(0, 0, screen_size[0], screen_size[1])

    def rename(self, title: str) -> None:
        self.screen.title(title)
