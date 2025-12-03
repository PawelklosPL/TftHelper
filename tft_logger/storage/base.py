# storage/base.py
from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def append_state(self, timestamp: float, gold: int, level: int) -> None:
        """Zapisuje pojedynczy stan gry (timestamp + gold + level)."""
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Porządki na koniec (zamykanie pliku itp.)."""
        raise NotImplementedError
