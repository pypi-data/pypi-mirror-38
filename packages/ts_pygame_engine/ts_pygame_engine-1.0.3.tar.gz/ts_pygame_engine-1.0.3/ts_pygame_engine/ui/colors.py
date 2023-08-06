from typing import Union, Tuple

from pygame import Color

ColorType = Union[
    Color,
    Tuple[int, int, int],
    Tuple[int, int, int, int]
]

TRANSPARENT = Color(0, 0, 0, 0)

