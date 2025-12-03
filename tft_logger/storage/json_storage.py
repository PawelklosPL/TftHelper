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

    def append_state(self, timestamp: float, gold: int, level: int) -> None:
        entry = {
            "timestamp": timestamp,
            "gold": gold,
            "level": level,
        }
        self._file.write(json.dumps(entry) + "\n")
        # od razu flush, żeby nic nie zginęło przy craszu
        self._file.flush()

    def close(self) -> None:
        self._file.close()
