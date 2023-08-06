import sys
from typing import Callable

import pygame

from .game import Game
from .settings import Config

__all__ = [
    'main'
]


def main(start_func: Callable[[Game], None]=None):
    """
    Optimal (maybe) realization of very first function to be called
    :param start_func: A function that would be called after game initialising
    :return: None
    """
    config = Config()

    pygame.init()

    game = Game(config)

    if start_func:
        start_func(game)

    while not game.exit:
        time = pygame.time.wait(int(game.config['frame_ms'])) / 1000

        events = pygame.event.get()
        game.events(events)

        game.process(time)

        pygame.display.flip()

    sys.exit(0)


if __name__ == "__main__":
    main()
