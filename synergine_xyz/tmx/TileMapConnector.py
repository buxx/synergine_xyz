from synergine_xyz.tmx.Map import Map
from synergine_xyz.exceptions import NoMatch, NotFound
from synergine_xyz.tmx.MapCollectionConfiguration import MapCollectionConfiguration
from PIL import Image


class TileMapConnector:
    """
    TODO: This class is on writing. Refactoring, split needed.
    """

    @classmethod
    def from_file(cls, file_name):
        """

        Return TileMapConnector instance with file_name tmx map as reference.

        :param file_name:
        :return:
        """
        return cls(Map.load(file_name))

    def __init__(self, tile_map: Map):
        """

        :param tile_map: Map
        :return:
        """
        self._tile_map = tile_map

    def create_simulations(self, config):
        simulation = {}
        objects_definitions = self._tile_map.get_objects_definitions()

        width = self._tile_map.width
        height = self._tile_map.height

        current_x_position = -1
        current_y_position = 0

        for z, layer in enumerate(self._tile_map.layers):
            for tile in layer.tiles:

                if current_x_position == width-1:
                    current_x_position = -1
                    current_y_position += 1

                current_x_position += 1

                position = (0, current_x_position, current_y_position)

                if tile.gid != 0:

                    # TODO: check and raise
                    object_definition = dict(objects_definitions[tile.gid])
                    object_definition['position'] = position

                    object_tile_set = object_definition['tile_set']

                    # TODO: Check and raise
                    object_simulation_class = config['simulation'][object_definition['simulation']]
                    if object_simulation_class not in simulation:
                        simulation[object_simulation_class] = {}

                    if object_tile_set not in simulation[object_simulation_class]:
                        simulation[object_simulation_class][object_tile_set] = {}

                    object_collection_class = config['collection'][object_definition['collection']]
                    if object_collection_class not in simulation[object_simulation_class][object_tile_set]:
                        simulation[object_simulation_class][object_tile_set][object_collection_class] = []

                    simulation[object_simulation_class][object_tile_set][object_collection_class].append(
                        object_definition)

        simulations = []
        for simulation_class in simulation:
            collections_list = simulation[simulation_class]
            collections = []
            for collection_key in collections_list:
                collections_definitions = collections_list[collection_key]
                for collection_class in collections_definitions:
                    objects_definitions = collections_definitions[collection_class]
                    map_collection_configuration = MapCollectionConfiguration(objects_definitions, config)
                    collection = collection_class(map_collection_configuration)
                    collections.append(collection)
            simulation = simulation_class(collections)
            simulations.append(simulation)

        return simulations

    def extract_objects_images(self, config):
        """

        :param config:
        :return: dict of {object_class: PIL.Image._ImageCrop, ...}
        """
        objects_images = {}
        objects_definitions = self._tile_map.get_objects_definitions()

        for obj_gid in objects_definitions:
            object_definition = objects_definitions[obj_gid]
            object_tile_set = self._get_tile_set(object_definition['tile_set'])
            image = self._extract_image_from_tile_set(object_tile_set, object_definition['position'])

            obj_class = config['object'][object_definition['object']]
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
        absolute_start_x = tile_set.tilewidth * object_position  # 20 * 5 = 100
        y_decal = absolute_start_x // int(tile_set.image.width)  # 100 / 60 = 1
        start_y = tile_set.tileheight * y_decal  # 20 * 1 = 20
        start_x = absolute_start_x % int(tile_set.image.width)  # 100 % 60 = 40
        return int(start_x), int(start_y), int(start_x + tile_set.tilewidth), int(start_y + tile_set.tileheight)
