import logging
from typing import Iterable, Dict, Optional

from localizator.localization import Localization

logger = logging.getLogger(__name__)


class DictLocalization(Localization):
    """
    Purpose of this implementation is to get localizations from dictionaries.
    """
    def __init__(self, localizations: Dict, language: str = None):
        """
        Creates DictLocalization from some dictionary.

        :param localizations: all localizations in one dictionary.
        :param language: language of this localization (used in warnings)
        """
        self.language = language
        self.localizations = localizations

    def get_string(self, path: Iterable[str]) -> str:
        localization = self.__get_recursive(path, self.localizations)

        if localization is None:
            s = 'Missing string for key `{}`, language: `{}`'.format(path, self.language)
            logger.warning(s)

            return s

        return localization

    def __get_recursive(self, keys: Iterable[str], localizations: Dict) -> Optional[str]:
        head, *tail = keys

        if head in localizations:
            new_localizations = localizations[head]
            if not tail:
                if isinstance(new_localizations, str):
                    return new_localizations
            elif hasattr(new_localizations, '__contains__'):
                return self.__get_recursive(tail, new_localizations)

        return None
