from typing import List, Dict, Tuple, Optional, Any, overload

from localizator.localization_description import LocalizationDescription


class LocalizationDescriber:
    """
    This amazing and cool class provides easy way to generate :obj:`localizator.LocalizationDescription`.

    Amazing example:
    ```Python
    localizator = Localizator()
    d = LocalizationDescriber()

    cool_localization = localizator.get_localization(d.some_cool.foo.bar)
    cool_formatted_localization = localizator.get_localization(d.format_me("Hello, world!")
    ```
    """

    def __init__(self, path_parts: List[str] = None, args: Tuple = None, kwargs: Dict = None):
        """
        Creates new describer (usually arguments used by internal methods and you do not need them).

        :param path_parts: list of keys similar to path in :obj:localizator.Localization
        :param args: args that will be passed to str.format()
        :param kwargs: kwargs that will be passed to str.format()
        """
        self.path = path_parts or list()
        self.args = args or list()
        self.kwargs = kwargs or dict()

    def __getattr__(self, item) -> 'LocalizationDescriber':
        return LocalizationDescriber(self.path + [item], self.args, self.kwargs)

    def __call__(self, path: Optional[str] = ..., *args, **kwargs) -> 'LocalizationDescriber':
        """
        Ho-ho-ho. Magic! This method can work in two ways. First one is only for *empty* describer. Usually you just
        pass args and kwargs that will be passed to str.format, but also you could pass as the first argument
        full path to localization string separated with dots, those arguments that left will be treated as usually,
        except that first argument will be saved as path. Next two examples of call should explain situation describers:

        d = LocalizationDescriber()
        a = d.foo.bar(hello=world, foo=bar)
        b = d('foo.bar', hello=world, foo=bar)
        a == b # True

        :param path: Optional full path to localization string (ignored if instance of this object already has path)
        :param args: args that will be passed to str.format()
        :param kwargs: kwargs that will be passed to str.format()
        :return: new describer with saved path, args and kwargs
        """
        new_path = self.path
        if len(self.path) == 0 and path is not ...:
            new_path = path.split('.')
        elif path is not ...:
            args = [path] + list(args)

        return LocalizationDescriber(new_path, args, kwargs)

    def get_description(self) -> LocalizationDescription:
        """
        Converts describer to descriptions.

        :return: final description
        """
        return LocalizationDescription(self.path, *self.args, **self.kwargs)
