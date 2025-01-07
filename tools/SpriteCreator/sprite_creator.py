import time, pickle, os

from main.render.animation import Animation
from main.util.math.point import Point
from main.util.math.vector2 import Vector2
from main.window import Window
from main.render.renderer import Renderer

"""
This program allows for the creation of sprites and animations 
within the limitations of turtle.

M1      - Action
M2      - Select all
M3      - Select closest

Q       - Add points/Duplicate selection
W       - Remove points/Remove selection
E       - Connect points  
R       - Move points/Move selection
T       - Disconnect points
S       - Save animation to file

SPACE   - Play the animation
LEFT    - Previous frame
RIGHT   - Next frame
UP      - Insert new frame (duplicate of current)
DOWN    - Remove current frame

A       - Lower frames per second
D       - Higher frames per second
"""


class SpriteCreator:

    def __init__(self, file_name: str, size: tuple = None, fps: int = None):
        self.points: list[list[Point]] = [[]]
        self.file_name: str = file_name
        self.size: tuple = size
        self.fps: int = fps
        self.load_points()

        self.window: Window = Window("Sprite Wizard", self.size)
        self.window.resize((1000, 1000), False)
        self.window.screen._root.config(cursor="none")
        self.renderer: Renderer = Renderer(self.window.screen)
        self._initialize_keybinding()

        self.frame: int = 0
        self.saved_points: list[Point] = []
        self.m_pos: Vector2 = Vector2.zero()
        self.mode: str = "add"

        self.playing: bool = False


    def _initialize_keybinding(self) -> None:
        """Sets all keybinding during program runtime"""
        #Action on mouse clicks
        self.window.screen.onscreenclick(self._on_left_click, btn=1)
        self.window.screen.onscreenclick(self._on_middle_click, btn=2)
        self.window.screen.onscreenclick(self._on_right_click, btn=3)
        #Actions on key clicks
        self.window.screen.onkey(lambda: self._set_mode("add"), "q")
        self.window.screen.onkey(lambda: self._set_mode("remove"), "w")
        self.window.screen.onkey(lambda: self._set_mode("connect"), "e")
        self.window.screen.onkey(lambda: self._set_mode("move"), "r")
        self.window.screen.onkey(lambda: self._set_mode("cut"), "t")
        self.window.screen.onkey(lambda: self._set_frame(1), "Right")
        self.window.screen.onkey(lambda: self._set_frame(-1), "Left")
        self.window.screen.onkey(self._remove_frame, "Down")
        self.window.screen.onkey(self._add_frame, "Up")
        self.window.screen.onkey(lambda: self._set_fps(-1), "a")
        self.window.screen.onkey(lambda: self._set_fps(1), "d")
        self.window.screen.onkey(self._set_play, " ")
        self.window.screen.onkey(self.save_points, "s")
        #Action on mouse movement
        self.window.screen._root.bind("<Motion>", self._mouse_motion)

    def _set_mode(self, mode: str) -> None:
        """Sets the mode to an arbitrary string"""
        if self.mode == "select":
            self._select_action(mode)
            if mode == "move" or mode == "add":
                self.mode = "move"
                return
        self.saved_points.clear()
        self.mode = mode

    def _set_frame(self, delta: int) -> None:
        """Moves to a different frame of the animation"""
        self.saved_points.clear()
        self.frame += delta
        if self.frame < 0: self.frame = len(self.points) - 1
        elif self.frame > len(self.points) - 1: self.frame = 0

    def _set_play(self) -> None:
        self.playing = not self.playing

    def _set_fps(self, delta: int) -> None:
        """Change the fps by a certain delta"""
        self.fps += delta
        if self.fps < 1: self.fps = 1

    def _mouse_motion(self, event) -> None:
        """Updates the mouse position"""
        delta: Vector2 = Vector2(event.x - (1000 - self.size[0])/2, self.size[1] - event.y + (1000 - self.size[1])/2) - self.m_pos
        if self.mode == "move" and len(self.saved_points) > 0:
            for point in self.saved_points:
                point.position += delta
        self.m_pos.set(event.x - (1000 - self.size[0])/2, self.size[1] - event.y + (1000 - self.size[1])/2)

    def _find_closest_point(self, pos: Vector2) -> Point:
        """Finds the closest point to the cursor"""
        result: Point = self.points[self.frame][0]
        for point in self.points[self.frame]:
            if point.position.dist(pos) < result.position.dist(pos):
                result = point
        return result


    def _on_left_click(self, x, y) -> None:
        """Handles action redirect at left-click"""
        match self.mode:
            case "add": self._add_action()
            case "remove": self._remove_action()
            case "connect": self._connect_action()
            case "move": self._move_action()
            case "cut": self._cut_action()

    def _on_middle_click(self, x, y) -> None:
        """Selects all points on middle-click"""
        if self.mode != "select": self._set_mode("select")
        self.saved_points.clear()
        self.saved_points.extend(self.points[self.frame])

    def _on_right_click(self, x, y) -> None:
        """Selects points on right-click"""
        if self.mode != "select": self._set_mode("select")
        if self._find_closest_point(self.m_pos) not in self.saved_points:
            self.saved_points.append(self._find_closest_point(self.m_pos))

    def _select_action(self, mode: str) -> None:
        """Handles selection follow-up actions"""
        match mode:
            case "remove": self._selection_remove_action()
            case "add": self._selection_add_action()

    def _add_action(self) -> None:
        """Adds a point to the list of points"""
        self.points[self.frame].append(Point(self.m_pos.copy()))

    def _selection_add_action(self) -> None:
        """Duplicates the selected points and there connections"""
        point_map = {point: point.copy() for point in self.saved_points}
        self.points[self.frame].extend(point_map.values())
        self.saved_points.clear()
        for original_point, copied_point in point_map.items():
            copied_point.connections = []
            for connection in original_point.connections:
                if connection in point_map:
                    copied_point.connections.append(point_map[connection])
            self.saved_points.append(copied_point)

    def _remove_action(self) -> None:
        """Removes a point from the list of points"""
        target: Point = self._find_closest_point(self.m_pos)
        for point in target.connections:
            point.connections.remove(target)
        self.points[self.frame].remove(target)

    def _selection_remove_action(self) -> None:
        """Removes all selected points"""
        for point in self.saved_points:
            for connection in point.connections:
                connection.connections.remove(point)
            self.points[self.frame].remove(point)

    def _connect_action(self) -> None:
        """Connects to points to each other"""
        if not len(self.saved_points) == 1:
            self.saved_points.append(self._find_closest_point(self.m_pos))
        elif not len(self.saved_points) == 2:
            self.saved_points.append(self._find_closest_point(self.m_pos))
            if self.saved_points[0] == self.saved_points[1]:
                self.saved_points.clear()
        if len(self.saved_points) == 2:
            self.saved_points[0].add_point(self.saved_points[1])
            self.saved_points[1].add_point(self.saved_points[0])
            self.saved_points.clear()

    def _move_action(self) -> None:
        """Moves a point"""
        if not len(self.saved_points) > 0:
            self.saved_points.append(self._find_closest_point(self.m_pos))
        else: self.saved_points.clear()

    def _cut_action(self) -> None:
        """Cuts a connection between points"""
        if not len(self.saved_points) == 1:
            self.saved_points.append(self._find_closest_point(self.m_pos))
        elif not len(self.saved_points) == 2:
            self.saved_points.append(self._find_closest_point(self.m_pos))
            if self.saved_points[0] == self.saved_points[1]:
                self.saved_points.clear()
        if len(self.saved_points) == 2:
            self.saved_points[0].remove_point(self.saved_points[1])
            self.saved_points[1].remove_point(self.saved_points[0])
            self.saved_points.clear()

    def _remove_frame(self) -> None:
        """Removes/clears a frame from the animation"""
        self.points.remove(self.points[self.frame])
        if len(self.points) == 0: self._add_frame()
        self._set_frame(-1)

    def _add_frame(self) -> None:
        """Adds a frame to the animation (duplicating the previous)"""
        self.points.insert(self.frame + 1, [])
        point_map = {point: point.copy() for point in self.points[self.frame]}
        for original_point, copied_point in point_map.items():
            copied_point.connections = []
            for connection in original_point.connections:
                if connection in point_map:
                    copied_point.connections.append(point_map[connection])
            self.points[self.frame + 1].append(copied_point)
        self._set_frame(1)


    def _render_grid(self, size: int) -> None:
        for i in range(self.size[0]//size + 1):
            self.renderer.render_connection(Vector2(0, size * i), Vector2(self.size[0], size * i), color=(.1, .1, .1))
        for i in range(self.size[1]//size + 1):
            self.renderer.render_connection(Vector2(size * i, 0), Vector2(size * i, self.size[1]), color=(.1, .1, .1))

    def _render_union_skin_past(self, depth: int) -> None:
        """Renders frames before the current frame at a certain depth"""
        if len(self.points) <= 1: return
        total_frames = len(self.points)
        for i in range(depth):
            frame = self.frame - 1 - i
            if total_frames > 1: frame = frame % total_frames
            self.renderer.render_points(self.points[frame], color=(0, 0, 1/(i+1)))

    def _render_union_skin_future(self, depth: int) -> None:
        """Renders frames after the current frame at a certain depth"""
        if len(self.points) <= 1: return
        total_frames = len(self.points)
        for i in range(depth):
            frame = self.frame + 1 + i
            if total_frames > 1: frame = frame % total_frames
            self.renderer.render_points(self.points[frame], color=(1/(i+1), 0, 0))

    def _render_ui(self) -> None:
        """Renders the basic UI for the application"""
        self.renderer.write(f'File: {self.file_name}', (2, self.size[1] - 25))
        self.renderer.write(f'(size: {self.size} ,fps: {self.fps})', (2, self.size[1] - 37))
        self.renderer.write(f'Frame: {self.frame}', (2, self.size[1] - 49))


    def save_points(self) -> None:
        """Save an Animation to a file."""
        with open(self.file_name, 'wb') as file:
            pickle.dump(Animation(self.points, self.size, self.fps), file)
        print(f"Animation has been saved to {self.file_name}.")

    def load_points(self) -> None:
        """Load self.points from a file. Create the file if it doesn't exist."""
        if not os.path.exists(self.file_name):
            print(f"{self.file_name} does not exist. Creating a new file with default data.")
            self.save_points()
        else:
            with open(self.file_name, 'rb') as file:  # Use read mode for binary ('rb')
                temp = pickle.load(file)
                self.points = temp.frames
                if not self.size: self.size = temp.size
                if not self.fps: self.fps = temp.fps
            print(f"Animation has been loaded from {self.file_name}.")


    def _update(self) -> None:
        """Update the window"""
        if self.playing:
            self.renderer.pen.clear()
            self._render_grid(50)
            self._set_frame(1)
            self.renderer.render_points(self.points[self.frame], render_points=False)
            self._render_ui()
            self.renderer.write('Playing animation...', (2, self.size[1] - 61))
            self.renderer.render()
            time.sleep(1/self.fps)
        else:
            self.renderer.pen.clear()
            self._render_grid(50)
            self._render_union_skin_past(1)
            self._render_union_skin_future(1)
            self.renderer.render_points(self.points[self.frame], debug_points=self.saved_points)
            self.renderer.render_point(self.m_pos, color='magenta')  # Cursor
            self._render_ui()
            self.renderer.write(f'Mode: {self.mode}', (2, self.size[1] - 61))
            self.renderer.render()

    def run(self) -> None:
        """Keeps the engine running"""
        while self.window.active:
            self._update()


SpriteCreator("assets/enemy/attack.anim").run()