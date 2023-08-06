import pygame

from ts_pygame_engine.ui.colors import ColorType, TRANSPARENT

__all__ = [
    'Widget'
]


class Widget:
    def __init__(self, width, height, bg_color: ColorType = TRANSPARENT):
        self.needs_redraw: bool = True
        self.bg_color = bg_color
        self.surface: pygame.Surface = None
        self.create_surface(width, height)

    @property
    def size(self):
        return self.surface.get_size()

    @property
    def rect(self):
        return self.surface.get_rect()

    def create_surface(self, width: int, height: int):
        self.surface = pygame.Surface((width, height), flags=pygame.SRCALPHA)

    def process(self, game: 'Game', time: float):
        pass

    def redraw(self):
        self.needs_redraw = False
        self.surface.fill(self.bg_color)

    def clear(self):
        self.needs_redraw = True
        self.surface.fill(self.bg_color)

    def parent_resize(self, width: int, height: int):
        pass
