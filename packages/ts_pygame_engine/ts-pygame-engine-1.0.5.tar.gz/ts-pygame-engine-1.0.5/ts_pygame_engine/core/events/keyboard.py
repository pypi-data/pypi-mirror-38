from typing import Optional, Callable, Iterable, List

from pygame.constants import KEYUP, KEYDOWN, KMOD_CTRL, KMOD_SHIFT, KMOD_ALT
from pygame.event import Event

from .input import InputBinding, InputDevice

__all__ = [
    'KeyBinding',
    'Keyboard'
]

Events = Iterable[Event]


class KeyBinding(InputBinding):
    def __init__(self, func: Callable[[Optional[bool]], None], key: int, hold: bool = False, ctrl: bool = False,
                 shift: bool = False, alt: bool = False):
        super().__init__(func)
        self.key = key
        self.hold = hold
        self.holding = False
        self.ctrl = ctrl
        self.shift = shift
        self.alt = alt

    def _check_mod(self, keyboard: 'Keyboard'):
        return self.ctrl == keyboard.ctrl \
               and self.shift == keyboard.shift \
               and self.alt == keyboard.alt

    def process(self, keyboard: 'Keyboard'):
        if self.hold:
            if self.holding and self._check_mod(keyboard) and self.key in keyboard.keys:
                if self.func:
                    self.func()
                self.triggered = True

        if (self.key in keyboard.keys) != self.holding:
            self.holding = not self.holding
            if not self.hold and self._check_mod(keyboard):
                if self.func:
                    self.func(self.holding)
                self.triggered = True
        self.triggered = False


class Keyboard(InputDevice):
    def __init__(self):
        super().__init__()
        self.ctrl = False
        self.shift = False
        self.alt = False
        self.watched_event_types = [KEYUP, KEYDOWN]
        self.focus: Callable[[Events], None] = None

    def events(self, events: Events):
        if self.focus is not None:
            self.focus([x for x in events if x.type in self.watched_event_types])
        else:
            super().events(events)

    def _process(self, event: Event):
        self.ctrl = bool(event.mod & KMOD_CTRL)
        self.shift = bool(event.mod & KMOD_SHIFT)
        self.alt = bool(event.mod & KMOD_ALT)

        if event.type == KEYDOWN:
            self.keys.add(event.key)
        elif event.type == KEYUP:
            self.keys.discard(event.key)
