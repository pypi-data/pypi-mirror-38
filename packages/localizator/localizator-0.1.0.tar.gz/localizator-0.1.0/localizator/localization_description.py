from typing import Iterable


class LocalizationDescription:
    """
    This class contains simple description of localization string inside localization.
    """
    def __init__(self, path: Iterable[str], *args, **kwargs):
        self.path = path
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        args = list(map(str, self.args)) + list(map(lambda key: '{}={}'.format(key, self.kwargs[key]), self.kwargs))
        return '{}({})'.format('.'.join(self.path), ', '.join(args))
