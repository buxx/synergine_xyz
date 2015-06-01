

class SynergyObjectRepresentation:

    def __init__(self, synergy_object_class):
        self._synergy_object_class = synergy_object_class

    def get_synergy_object(self, collection, context):
        return self._synergy_object_class(collection, context)