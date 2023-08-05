from typing import List, Dict, Tuple, Union

from localizator.localization_describer import LocalizationDescriber
from localizator.localization_description import LocalizationDescription
from localizator.localizations_provider import LocalizationsProvider
from localizator.yamlloc.yaml_localizations_provider import YamlLocalizationsProvider


class Localizator:
    """
    Suppa-duppa amazing class for localizations!
    """
    def __init__(self, localizations_provider: LocalizationsProvider = None, default_language='en'):
        """
        Creates new localizator.

        :param localizations_provider: provider of localizations.
        :param default_language: default language to use.
        """
        if localizations_provider is None:
            localizations_provider = YamlLocalizationsProvider()

        self.default_language = default_language
        self.localizations_provider = localizations_provider

    def get_localization(self,
                         localization_description: Union[LocalizationDescription, LocalizationDescriber],
                         language=None) -> str:
        """
        Gets localization string by it description in specified language.

        :param localization_description: description of localization path and args to pass to str.format
        :param language: language in which localization look for.
        :return: localized string.
        """
        if isinstance(localization_description, LocalizationDescriber):
            localization_description = localization_description.get_description()

        if language is None:
            language = self.default_language

        localization = self.localizations_provider.get_localization(language)
        localization_str = localization.get_string(localization_description.path)

        args, kwargs = self.__convert_args(localization_description.args, localization_description.kwargs, language)

        return localization_str.format(*args, **kwargs)

    def __convert_args(self, args: List, kwargs: Dict, language: str) -> Tuple[List[str], Dict[str, str]]:
        args = [
            self.get_localization(arg, language)
            if isinstance(arg, (LocalizationDescriber, LocalizationDescription))
            else str(arg)

            for arg in args
        ]

        kwargs = {
            key: (
                self.get_localization(kwargs[key], language)
                if isinstance(kwargs[key], (LocalizationDescriber, LocalizationDescription))
                else str(kwargs[key])
            )

            for key in kwargs
        }

        return args, kwargs
