from abc import ABC, abstractmethod

from localizator.localization import Localization


class LocalizationsProvider(ABC):
    """
    Simple abstraction for getting localizations of specified language.
    """
    @abstractmethod
    def get_localization(self, language: str) -> Localization:
        """
        Gets localization by language.

        :param language:
        :return: localization of specified language.
        """
        ...
