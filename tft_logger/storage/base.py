# storage/base.py
from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def append_state(self, timestamp: float, gold: int, map: str, expo: str = None, player_level: int = None) -> None:
        """Saves a single game state (timestamp + gold + map + expo + player_level)."""
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Cleanup at the end (closing file etc.)."""
        raise NotImplementedError
