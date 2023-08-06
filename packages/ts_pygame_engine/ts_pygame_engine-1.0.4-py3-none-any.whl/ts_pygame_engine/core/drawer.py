from math import ceil
from typing import Tuple

from pygame import Surface

__all__ = [
    'Layer',
    'Drawer'
]


class Layer:
    def __init__(self, screen: Surface, index: int):
        self.screen = screen
        self.zindex = index
        self.objects = []

    def __str__(self):
        return '<Layer with %s objects>' % len(self.objects)

    def append(self, obj: 'GameObject'):
        self.objects.append(obj)

    def remove(self, obj: 'GameObject'):
        self.objects.remove(obj)

    def pop(self, index: int=-1):
        self.objects.pop(index)

    def draw(self):
        for obj in self.objects:
            obj.draw(self.screen)


class Drawer:
    def __init__(self, screen: Surface, bg_color: Tuple[int, int, int]):
        self.screen = screen
        self.layers = []
        self.bg_color = bg_color

    def __str__(self):
        return '<Drawer with %s layers>' % len(self.layers)

    def _layer_index(self, zindex: int) -> float:
        for index, layer in enumerate(self.layers):
            if layer.zindex == zindex:
                return float(index)
            elif layer.zindex < zindex:
                return float(index) - 0.5
        return len(self.layers) - 0.5

    def _get_or_create_layer(self, zindex: int) -> Layer:
        layer_index = self._layer_index(zindex)
        if not layer_index.is_integer():
            self.layers.insert(int(ceil(layer_index)), Layer(self.screen, zindex))
        return self.layers[int(layer_index)]

    def __getitem__(self, zindex: int) -> Layer:
        layer_index = self._layer_index(zindex)
        if not layer_index.is_integer():
            raise IndexError('No layer with such zindex')
        return self.layers[int(layer_index)]

    def register(self, obj: 'GameObject', zindex: int):
        if type(zindex) is not int:
            raise TypeError("'layer' parameter must be int")
        layer = self._get_or_create_layer(zindex)
        layer.append(obj)

    def draw(self):
        self.screen.fill(self.bg_color)
        for layer in self.layers:
            layer.draw()
