import os
import json
from typing import Optional, Any

__all__ = [
    'Config'
]

CONFIG_FILE = './config'

DEFAULTS = {
    'debug': False,
    'width': 800,
    'height': 600,
    'fps': 30,
    'frame_ms': 1000 / 30,  # 1000ms / FPS
    'background_color': (100, 100, 100),
    'display_flags': 0
}


class Config:
    def __init__(self, config_file: Optional[str]=None):
        self._config = DEFAULTS.copy()

        if config_file is None:
            config_file = CONFIG_FILE

        if not os.path.exists(config_file):
            return

        with open(config_file, 'r') as f:
            try:
                config = json.load(f)
            except json.decoder.JSONDecodeError:
                return

        for k, v in config.items():
            self._config[k] = v

    def save(self, config_file: Optional[str]=None):
        if config_file is None:
            config_file = CONFIG_FILE
        with open(config_file, 'w') as f:
            json.dump(self._config, f)

    def __getitem__(self, item: str):
        if item not in self._config:
            raise AttributeError('no such option')
        return self._config[item]

    def __setitem__(self, key: str, value: Any):
        self._config[key] = value

    def __delitem__(self, item: str):
        del self._config[item]

    def __contains__(self, item: str):
        return item in self._config
