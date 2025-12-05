# storage/json_storage.py
import json
from typing import TextIO

from .base import BaseStorage


class JsonStorage(BaseStorage):
    """
    A simple storage that saves each state as a single JSON line.
    For example:
    {"timestamp": 123.45, "gold": 20, "level": 6}
    """

    def __init__(self, path: str):
        self._path = path
        self._file: TextIO = open(self._path, "a", encoding="utf-8")

    def append_state(self, timestamp: float, gold: int, map: str, expo: str = None, player_level: int = None) -> None:
        entry = {
            "timestamp": timestamp,
            "gold": gold,
            "map": map,
            "expo": expo,
            "player_level": player_level,
        }
        self._file.write(json.dumps(entry) + "\n")
        self._file.flush()

    def close(self) -> None:
        self._file.close()
