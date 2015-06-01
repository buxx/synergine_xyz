from synergine.core.exceptions import NotFound


class MapException(Exception):
    pass


class MapConfigurationException(MapException):
    pass


class NoMatch(MapConfigurationException):
    pass


class NotFound(MapConfigurationException, NotFound):
    pass