import time

from main.util.debug.logger import Logger


class Ticker:
    def __init__(self, fps: int):
        self.clock = {'prev': time.time(), 'current': time.time()}
        self.spf: float = 1/fps
        self._accum: float = 0.0

    def tick(self, update, render, args) -> None:
        """Ticks the program, calling the update the appropriate amount of times."""
        #Tick the clock and update the accumulator
        self.clock['current'] = time.time()
        self._accum += self.clock['current'] - self.clock['prev']
        self.clock['prev'] = self.clock['current']

        #Execute the update the appropriate amount of times
        ticks: int = int(self._accum/self.spf)
        for _ in range(ticks):
            update(args)
            self._accum -= self.spf
        render(args)

        frame_time: float = time.time() - self.clock['current']
        if frame_time < self.spf:
            time.sleep(self.spf - frame_time)
        if frame_time > self.spf:
            Logger.log("Ticker", f"Program running at a lower fps: {1//frame_time}",
                       warning=True)

        #Log when an anomaly in ticks occurs
        if ticks > 2: Logger.log("Ticker",
                       f"Multiple ticks detected: {ticks}",
                       warning=True)