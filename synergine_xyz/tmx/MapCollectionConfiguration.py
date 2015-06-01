from synergine.synergy.collection.Configuration import Configuration


class MapCollectionConfiguration(Configuration):

    def __init__(self, objects_definitions, config):
        self._objects_definitions = objects_definitions
        self._config = config

    def get_start_objects(self, collection, context):
        objects = []

        for object_definition in self._objects_definitions:
            obj = self._get_class(object_definition['object'])(collection, context)
            obj.set_position(object_definition['position'])
            objects.append(obj)

        return objects

    def _get_class(self, name):
        return self._config['object'][name]

    def get_start_position(self):
        # TODO: Devra etre base sur element de la tilemap !
        return 0, 1, 1