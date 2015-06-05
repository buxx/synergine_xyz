class DynamicClasses():

    def __init__(self):
        self._classes = {}

    def get_production_class(self, object_class, collection_id):
        if collection_id not in self._classes:
            self._classes[collection_id] = {}
        if object_class not in self._classes[collection_id]:
            class_name = object_class.__name__
            dynamic_class_name = 'Collection%s%s' % (collection_id, class_name)
            self._classes[collection_id][object_class] = type(dynamic_class_name, (object_class, ), {})
        return self._classes[collection_id][object_class]
