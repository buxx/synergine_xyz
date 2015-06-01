from synergine_xyz.tmx.Map import Map
from synergine_xyz.exceptions import NoMatch, NotFound
from synergine_xyz.tmx.MapCollectionConfiguration import MapCollectionConfiguration
from PIL import Image


class TileMapConnector:
    """
    TODO: This class is on writing. Refactoring, split needed.
    """

    _properties = ['simulation', 'collection', 'object']
    """List of synergies object properties"""

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
        self._objects_definitions = self._get_objects_definitions()
        # self._simulations_definitions = self._get_simulations_definitions()
        # self._collections_definitions = self._get_collection_definitions()

    def _get_objects_definitions(self):
        objects = {}
        for tile_set_position, tile_set in enumerate(self._tile_map.tilesets):
            first_gid = tile_set.firstgid
            for key, tile in enumerate(tile_set.tiles):
                tile_id = first_gid + key
                objects[tile_id] = self._get_tile_properties(tile, tile_set)
                objects[tile_id]['tile_set'] = tile_set_position
        return objects

    def _get_tile_properties(self, tile, tile_set):
        properties = {}

        for property in self._properties:
            properties[property] = self._get_tile_property(property, tile, tile_set)

        properties['actions'] = self._get_node_actions(tile)
        properties['position'] = tile.id

        return properties

    def _get_tile_property(self, name, tile, tile_set):
        # Get tile property
        try:
            return self._get_property(name, tile)
        except NotFound:
            # If not, search in tile_set
            return self._get_property(name, tile_set)

    @staticmethod
    def _get_property(name, node):
        for node_property in node.properties:
            if name == node_property.name and node_property.value:
                return node_property.value
        raise NotFound('"%s" property not found' % name)

    def _get_node_actions(self, node):
        actions = []
        for node_property in node.properties:
            if 'actions' == node_property.name and node_property.value:
                actions = [action.strip() for action in node_property.value.split(',')]

        return actions

    # def _get_simulations_definitions(self):
    #     simulations_definition = {}
    #     for object_definition in self._objects_definitions:


    def create_simulations(self, config):
        simulation = {}

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
                    object_definition = dict(self._objects_definitions[tile.gid])
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

        for obj_gid in self._objects_definitions:
            object_definition = self._objects_definitions[obj_gid]
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

    def _get_object_tile_position(self, tile_set, object_position):
        absolute_start_x = tile_set.tilewidth * object_position  # 20 * 5 = 100
        y_decal = absolute_start_x // int(tile_set.image.width)  # 100 / 60 = 1
        start_y = tile_set.tileheight * y_decal  # 20 * 1 = 20
        start_x = absolute_start_x % int(tile_set.image.width)  # 100 % 60 = 40
        return int(start_x), int(start_y), int(start_x + tile_set.tilewidth), int(start_y + tile_set.tileheight)