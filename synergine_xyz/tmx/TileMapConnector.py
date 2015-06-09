from synergine_xyz.tmx.DynamicClasses import DynamicClasses
from synergine_xyz.tmx.Map import Map
from synergine_xyz.tmx.MapCollectionConfiguration import MapCollectionConfiguration
from PIL import Image


class TileMapConnector:
    """
    Load simulation from prepared TMX file.
    """

    @classmethod
    def from_file(cls, file_name, config):
        """

        Return TileMapConnector instance with file_name tmx map as reference.

        :param file_name:
        :return:
        """
        return cls(Map.load(file_name), config)

    def __init__(self, tile_map: Map, config):
        """

        :param tile_map: Map
        :return:
        """
        self._tile_map = tile_map
        self._config = config
        self._dynamic_classes = DynamicClasses()

    def get_dynamic_classes(self):
        return self._dynamic_classes

    def create_simulations(self):
        """

        Create simulation (with collections, configurations) from the map.

        :return: Simulation objects
        """
        simulation_definition = self._get_simulation_definition()
        return self._get_simulation_from_definition(simulation_definition)

    def _get_simulation_definition(self):
        """

        Return definition of simulation from the map

        :return: simulation definition
        """
        simulation_definition = {}
        tiles = self._tile_map.get_tiles_data()

        for tile in tiles:
            simulation_class = self._get_simulation_class(tile['simulation'])
            collection_class = self._get_collection_class(tile['collection'])
            tile_set = tile['tile_set']

            if simulation_class not in simulation_definition:
                simulation_definition[simulation_class] = {}

            if tile_set not in simulation_definition[simulation_class]:
                simulation_definition[simulation_class][tile_set] = {}

            if collection_class not in simulation_definition[simulation_class][tile_set]:
                simulation_definition[simulation_class][tile_set][collection_class] = []

            simulation_definition[simulation_class][tile_set][collection_class].append(tile)

        return simulation_definition

    def _get_simulation_class(self, simulation_name):
        """

        Return the simulation class for given simulation name from config

        :param simulation_name:
        :return: Simulation class
        """
        if simulation_name not in self._config['simulation']:
            raise Exception('Unknown simulation %s' % simulation_name)
        return self._config['simulation'][simulation_name]

    def _get_collection_class(self, collection_name):
        """

        Return the collection class for given collection name from config

        :param collection_name:
        :return: Collection class
        """
        if collection_name not in self._config['collection']:
            raise Exception('Unknown collection %s' % collection_name)
        return self._config['collection'][collection_name]

    def _get_object_class(self, object_name):
        """

        Return the synergy object class for given synergy object name from config

        :param object_name:
        :return: SynergyObject class
        """
        if object_name not in self._config['object']:
            raise Exception('Unknown object %s' % object_name)
        return self._config['object'][object_name]

    def _get_simulation_from_definition(self, definition):
        """

        return simulation (with collections, configurations) from a simulation definition

        :param definition:
        :return:
        """
        simulations = []
        for simulation_class in definition:
            collections_list = definition[simulation_class]
            collections = []
            for collection_key in collections_list:
                collections_definitions = collections_list[collection_key]
                for collection_class in collections_definitions:
                    objects_definitions = collections_definitions[collection_class]
                    map_collection_configuration = MapCollectionConfiguration(objects_definitions,
                                                                              dict(self._config),
                                                                              self._dynamic_classes)
                    collection = collection_class(map_collection_configuration)
                    collections.append(collection)
            simulation = simulation_class(collections)
            simulations.append(simulation)

        return simulations

    def extract_objects_images(self):
        """

        Return a dict with extracted image for each synergy object

        :return: dict of {object_class: PIL.Image._ImageCrop, ...}
        :rtype: dict
        """
        objects_images = {}
        objects_definitions = self._tile_map.get_objects_definitions()

        for obj_gid in objects_definitions:
            object_definition = objects_definitions[obj_gid]
            object_tile_set = self._tile_map.get_tile_set(object_definition['tile_set'])
            image = self._extract_image_from_tile_set(object_tile_set, object_definition['position'])

            obj_class = self._get_object_class(object_definition['object'])
            obj_tile_set_id = object_definition['tile_set']
            production_class = self._dynamic_classes.get_production_class(obj_class, obj_tile_set_id)
            if production_class not in objects_images:
                objects_images[production_class] = image

        return objects_images

    def _extract_image_from_tile_set(self, tile_set, object_position):
        """

        Return PIL.Image._ImageCrop image of object position in tileset.

        :param tile_set: tmx.Tileset where extract image
        :param object_position: position of the image object wanted
        :return: PIL.Image._ImageCrop image of object position
        :rtype: PIL.Image._ImageCrop
        """
        tile_set_image = Image.open(tile_set.image.source)
        x1, y1, x2, y2 = self._get_object_tile_position(tile_set, object_position)
        return tile_set_image.crop((x1, y1, x2, y2))

    @staticmethod
    def _get_object_tile_position(tile_set, object_position):
        """

        Return tuple of x1, y1, x2, y2 corresponding to position of object in tileset image.

        :param tile_set: tmx.Tileset where extract positions
        :param object_position: position of wanted object positions
        :return: tuple of x1, y1, x2, y2 corresponding to position of object in tileset image
        :rtype: tuple
        """
        absolute_start_x = tile_set.tilewidth * object_position
        y_decal = absolute_start_x // int(tile_set.image.width)
        start_y = tile_set.tileheight * y_decal
        start_x = absolute_start_x % int(tile_set.image.width)
        return int(start_x), int(start_y), int(start_x + tile_set.tilewidth), int(start_y + tile_set.tileheight)

    def add_object_callback_to_visualisation(self, visualizer, objects_classes, callback_container):
        for object_class in objects_classes:
            objects_production_classes = self._dynamic_classes.get_production_classes(object_class)
            for object_production_class in objects_production_classes:
                callback = callback_container(self, object_production_class)
                visualizer.add_callback(object_production_class, callback)

    def extract_image_with_class(self, tile_set_id, tile_class):
        class_tile_position = self._tile_map.get_tile_position_with_class(tile_set_id, tile_class)
        tile_set = self._tile_map.get_tile_set(tile_set_id)
        return self._extract_image_from_tile_set(tile_set, class_tile_position)
