from synergine.synergy.collection.Configuration import Configuration


class MapCollectionConfiguration(Configuration):

    def __init__(self, objects_definitions, config, dynamic_classes):
        self._objects_definitions = objects_definitions
        self._config = config
        self._dynamic_classes = dynamic_classes

    def get_start_objects(self, collection, context):
        objects = []

        for object_definition in self._objects_definitions:
            obj = self._get_class(object_definition)(collection, context)
            obj.set_position(object_definition['position'])
            objects.append(obj)

        return objects

    def _get_class(self, object_definition):
        object_class_name = object_definition['object']
        object_class = self._config['object'][object_class_name]
        tile_set_id = object_definition['tile_set']
        return self._dynamic_classes.get_production_class(object_class, tile_set_id)

    def get_start_position(self):
        # TODO: Devra etre base sur element de la tilemap !
        return 0, 1, 1