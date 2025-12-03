# storage/base.py
from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def append_state(self, timestamp: float, gold: int, level: int) -> None:
        """Saves a single game state (timestamp + gold + level)."""
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Cleanup at the end (closing file etc.)."""
        raise NotImplementedError
