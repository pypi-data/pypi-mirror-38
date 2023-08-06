from typing import List, Tuple
from pygame import Surface

from ts_pygame_engine.ui.colors import ColorType, TRANSPARENT
from .widget import Widget

__all__ = [
    'Container'
]


class Container(Widget):
    def __init__(self, width, height, bg_color: ColorType = TRANSPARENT):
        super().__init__(width, height, bg_color)
        self.widgets: List[Widget] = []

    def process(self, game: 'Game', time: float):
        for widget in self.widgets:
            if widget is not None:
                widget.process(game, time)
        if any(widget.needs_redraw for widget in self.widgets):
            self.redraw()

    def how_to_blit(self, index: int, widget: Widget) -> Tuple[Surface, Tuple[int, int]]:
        pass

    def redraw(self):
        self.clear()
        for index, widget in enumerate(self.widgets):
            if widget.needs_redraw:
                widget.redraw()
            self.surface.blit(widget.surface, self.how_to_blit(index, widget))
        self.needs_redraw = False
