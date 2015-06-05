from synergine_xyz.exceptions import NotFound


class DynamicClasses():

    def __init__(self):
        self._collection_classes = {}

    def get_production_class(self, object_class, collection_id):
        if collection_id not in self._collection_classes:
            self._collection_classes[collection_id] = {}
        if object_class not in self._collection_classes[collection_id]:
            class_name = object_class.__name__
            dynamic_class_name = 'Collection%s%s' % (collection_id, class_name)
            self._collection_classes[collection_id][object_class] = type(dynamic_class_name, (object_class, ), {})
        return self._collection_classes[collection_id][object_class]
    
    def get_production_class_collection_id(self, production_class):
        for collection_id in self._collection_classes:
            for dynamic_class in self._collection_classes[collection_id]:
                if production_class == self._collection_classes[collection_id][dynamic_class]:
                    return collection_id
        raise NotFound()

    def get_production_classes(self, object_class):
        production_classes = []
        for collection_id in self._collection_classes:
            for dynamic_class_key in self._collection_classes[collection_id]:
                dynamic_class = self._collection_classes[collection_id][dynamic_class_key]
                if issubclass(dynamic_class, object_class):
                    production_classes.append(dynamic_class)
        return production_classes
