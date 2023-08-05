from abc import ABC, abstractmethod
from typing import Iterable


class Localization(ABC):
    """This abstract class should return some localization string by it path (list of keys)"""

    @abstractmethod
    def get_string(self, path: Iterable[str]) -> str:
        """Returns string by it path inside locale"""
        ...
