from synergine_xyz.tmx.Map import Map
from synergine_xyz.exceptions import NoMatch, NotFound
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

    def create_simulations(self):
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

        return self._get_simulation_from_definition(simulation_definition)

    def _get_simulation_class(self, simulation_name):
        if simulation_name not in self._config['simulation']:
            raise Exception('Unknown simulation %s' % simulation_name)
        return self._config['simulation'][simulation_name]

    def _get_collection_class(self, collection_name):
        if collection_name not in self._config['collection']:
            raise Exception('Unknown collection %s' % collection_name)
        return self._config['collection'][collection_name]

    def _get_object_class(self, object_name):
        if object_name not in self._config['object']:
            raise Exception('Unknown object %s' % object_name)
        return self._config['object'][object_name]

    def _get_simulation_from_definition(self, definition):
        simulations = []
        for simulation_class in definition:
            collections_list = definition[simulation_class]
            collections = []
            for collection_key in collections_list:
                collections_definitions = collections_list[collection_key]
                for collection_class in collections_definitions:
                    objects_definitions = collections_definitions[collection_class]
                    map_collection_configuration = MapCollectionConfiguration(objects_definitions, dict(self._config))
                    collection = collection_class(map_collection_configuration)
                    collections.append(collection)
            simulation = simulation_class(collections)
            simulations.append(simulation)

        return simulations

    def extract_objects_images(self):
        """

        :return: dict of {object_class: PIL.Image._ImageCrop, ...}
        """
        objects_images = {}
        objects_definitions = self._tile_map.get_objects_definitions()

        for obj_gid in objects_definitions:
            object_definition = objects_definitions[obj_gid]
            object_tile_set = self._get_tile_set(object_definition['tile_set'])
            image = self._extract_image_from_tile_set(object_tile_set, object_definition['position'])

            obj_class = self._get_object_class(object_definition['object'])
            if obj_class not in objects_images:
                objects_images[obj_class] = image

        return objects_images

    def _get_tile_set(self, key):
        return self._tile_map.tilesets[key]

    def _extract_image_from_tile_set(self, tile_set, object_position):
        tile_set_image = Image.open(tile_set.image.source)
        x1, y1, x2, y2 = self._get_object_tile_position(tile_set, object_position)
        return tile_set_image.crop((x1, y1, x2, y2))

    @staticmethod
    def _get_object_tile_position(tile_set, object_position):
        absolute_start_x = tile_set.tilewidth * object_position
        y_decal = absolute_start_x // int(tile_set.image.width)
        start_y = tile_set.tileheight * y_decal
        start_x = absolute_start_x % int(tile_set.image.width)
        return int(start_x), int(start_y), int(start_x + tile_set.tilewidth), int(start_y + tile_set.tileheight)
