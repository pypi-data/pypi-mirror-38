import pygame
from pygame.font import Font

from ts_pygame_engine.primitives import Vector
from ts_pygame_engine.ui import ColorType
from ts_pygame_engine.ui.core import Widget


class Text(Widget):
    def __init__(self, text: str, font: Font, color: ColorType):
        super().__init__(0, 0)
        self._text = text
        self._font = font
        self._color = color
        self.needs_redraw = True

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.needs_redraw = True

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        self.needs_redraw = True

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.needs_redraw = True

    def _render(self, text) -> pygame.Surface:
        return self.font.render(text, True, self._color)

    def redraw(self):
        self.needs_redraw = False
        lines = []
        for line in self._text.split('\n'):
            lines.append(self._render(line))
        width = max(line.get_width() for line in lines)
        height = sum(line.get_height() for line in lines)
        self.create_surface(width, height)
        offset = 0
        for line in lines:
            self.surface.blit(line, (0, offset))
            offset += line.get_height()
