from typing import Optional, Callable

from pygame import MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION
from pygame.event import Event

from .input import InputDevice, InputBinding

from ts_pygame_engine.primitives import Vector

__all__ = [
    'MouseKeyBinding',
    'Mouse'
]


class MouseKeyBinding(InputBinding):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    SCROLL_UP = 4
    SCROLL_DOWN = 5

    def __init__(self, func: Callable[[Optional[bool]], None], key: int, hold: bool = False):
        super().__init__(func)
        self.key = key
        self.hold = hold
        self.holding = False

    def process(self, mouse: 'Mouse'):
        if self.hold:
            if self.holding and self.key in mouse.keys:
                if self.func:
                    self.func(mouse.pos)
                self.triggered = True

        if (self.key in mouse.keys) != self.holding:
            self.holding = not self.holding
            if not self.hold:
                if self.func:
                    self.func(self.holding, mouse.pos)
                self.triggered = True
        self.triggered = False


class MouseMotionBinding(InputBinding):
    def __init__(self, func: Callable[[Vector, Vector], None]):
        super().__init__(func)

    def process(self, mouse: 'Mouse'):
        if mouse.pos != mouse.prev_pos:
            self.func(mouse.pos, mouse.pos - mouse.prev_pos)


class Mouse(InputDevice):
    def __init__(self):
        super().__init__()
        self.pos: Vector = Vector()
        self.prev_pos: Vector = Vector()
        self.watched_event_types = [MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION]

    def _process(self, event: Event):
        if event.type == MOUSEBUTTONDOWN:
            self.keys.add(event.button)
        elif event.type == MOUSEBUTTONUP:
            self.keys.discard(event.button)
        elif event.type == MOUSEMOTION:
            self.prev_pos = self.pos
            self.pos = Vector(event.pos)

