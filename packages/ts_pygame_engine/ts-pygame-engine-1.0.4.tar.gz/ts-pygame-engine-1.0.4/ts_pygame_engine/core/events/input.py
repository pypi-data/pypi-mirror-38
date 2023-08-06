from typing import List, Callable, Iterable

from pygame.event import Event

__all__ = [
    'InputBinding',
    'InputDevice'
]

# TODO implement InputBinding bool queries
Watcher = Callable[[Event], None]


class InputBinding:
    def __init__(self, func: Callable[[], None]):
        self.func = func
        self.triggered = False

    def process(self, device: 'InputDevice'):
        pass


class InputDevice:
    def __init__(self):
        self.keys = set()
        self.bindings: List[InputBinding] = []
        self.watched_event_types = []

    def events(self, events: Iterable[Event]):
        for event in events:
            if event.type in self.watched_event_types:
                self._process(event)

        for binding in self.bindings:
            binding.process(self)

    def _process(self, event: Event):
        pass

    def bind(self, binding: InputBinding):
        self.bindings.append(binding)

    def unbind(self, binding: InputBinding) -> bool:
        try:
            self.bindings.remove(binding)
            return True
        except ValueError:
            return False
