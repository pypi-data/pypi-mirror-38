import pygame
from typing import List, Type, Union, Iterable

from .settings import Config
from .drawer import Drawer
from .events import KeyBinding, Keyboard
from .events import Mouse, MouseKeyBinding
from ts_pygame_engine.ui.core import UIScreen

__all__ = [
    'GameObject',
    'Game'
]


class GameObject:
    def __init__(self, config: Config):
        self.bindings: List[KeyBinding] = []

    def process(self, game: 'Game', time: float):
        pass

    def draw(self, screen: pygame.Surface):
        pass

    def check_collision(self, other):
        return False


class Game:
    def __init__(self, config: Config):
        resolution = (config['width'], config['height'])
        screen = pygame.display.set_mode(resolution, config['display_flags'])
        self.config: Config = config
        self.drawer = Drawer(screen, self.config['background_color'])
        self.ui = UIScreen(screen, self.config['width'], self.config['height'])
        self.objects: List[GameObject] = []
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.exit = False
        self.time = 0

    def register_list(self, obj_list: List[GameObject], zindex: int=1):
        for obj in obj_list:
            self.register(obj, zindex)

    def register(self, obj: Union[GameObject, Type[GameObject]], zindex=1):
        if isinstance(obj, type):  # if obj is not initialized. Example: Ball instead of Ball()
            obj = obj(self.config)

        self.objects.append(obj)
        self.drawer.register(obj, zindex)
        for binding in obj.bindings:
            if type(binding) is KeyBinding:
                self.keyboard.bind(binding)
            elif type(binding) is MouseKeyBinding:
                self.mouse.bind(binding)

    def process(self, time: float):
        self.time += time
        for obj in self.objects:
            obj.process(self, time)
        self.check_collisions()
        self.ui.process(self, time)
        self.drawer.draw()
        self.ui.draw()

    def save(self):
        pass  # for further use

    def events(self, events: Iterable[pygame.event.Event]):
        if any(event.type == pygame.QUIT for event in events):
            self.save()
            self.exit = True

        self.keyboard.events(events)
        self.mouse.events(events)
        self.ui.events(events)

    def get_config(self) -> Config:
        return self.config

    def check_collisions(self):
        for z, obj1 in enumerate(self.objects):
            for obj2 in self.objects[z + 1:]:
                obj1.check_collision(obj2)

