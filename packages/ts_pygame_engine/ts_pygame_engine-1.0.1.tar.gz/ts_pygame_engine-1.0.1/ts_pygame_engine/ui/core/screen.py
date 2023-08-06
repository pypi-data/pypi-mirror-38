from typing import Tuple, Union, Iterable

import pygame
from pygame import Surface, VIDEORESIZE
from pygame.event import Event
from .widget import Widget
from .container import Container


class UIScreen(Container):
    def __init__(self, screen: Surface, width: int, height: int):
        super().__init__(width, height)
        self.screen = screen
        self.widgets = []

    def events(self, events: Iterable[Event]):
        events = list(filter(lambda x: x.type == VIDEORESIZE, events))
        if len(events) == 0:
            return
        width = events[-1].w
        height = events[-1].h
        self.needs_redraw = True
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        if self.main_widget is not None:
            self.main_widget.parent_resize(width, height)

    @property
    def main_widget(self) -> Union[Widget, None]:
        if len(self.widgets) == 1:
            return self.widgets[0]
        return None

    @main_widget.setter
    def main_widget(self, value: Union[Widget, None]):
        self.needs_redraw = True
        if value is None:
            self.widgets = []
        else:
            self.widgets = [value]

    def how_to_blit(self, index: int, widget: Widget) -> Tuple[int, int]:
        return 0, 0

    def draw(self):
        self.screen.blit(self.surface, (0, 0))
