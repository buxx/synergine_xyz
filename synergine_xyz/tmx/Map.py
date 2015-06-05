from tmx import TileMap
from synergine_xyz.exceptions import NotFound


class Map(TileMap):

    _properties_required = ['simulation', 'collection', 'object']
    _properties_optional = ['class']
    """List of synergies object properties"""

    def __init__(self):
        super().__init__()
        self._objects_definitions = {}

    @classmethod
    def load(cls, fname):
        """

        Return a Map with tmx fname loaded and ready to use.

        :param fname:
        :return:
        """
        tile_map = super().load(fname)
        tile_map.update_objects_definitions()
        return tile_map

    def update_objects_definitions(self):
        """

        Update definition of tmx tiles objects

        :return:
        """
        self._load_objects_definitions()

    def _load_objects_definitions(self):
        """

        Compute objects definitions (see get_objects_definitions)

        :return:
        """
        self._objects_definitions = {}
        for tile_set_position, tile_set in enumerate(self.tilesets):
            first_gid = tile_set.firstgid
            for key, tile in enumerate(tile_set.tiles):
                tile_id = first_gid + key
                self._objects_definitions[tile_id] = self._get_tile_properties(tile, tile_set)
                self._objects_definitions[tile_id]['tile_set'] = tile_set_position

    def get_objects_definitions(self):
        """

        Return a dict like that: {
            GID: {
                'actions': ['action()', ...],
                'collection': 'collection_id',
                'object': 'object_id',
                'position': 'position in tileset',
                'simulation': 'simulation_id',
                'tile_set': 'tile_set_id'
            },
            ...
        }

        :return: dict of objects definitions
        """
        return self._objects_definitions

    def _get_tile_properties(self, tile, tile_set):
        """

        Return a dict with object definition: like: {
            'actions': ['action()', ...],
            'collection': 'collection_id',
            'object': 'object_id',
            'position': 'position in tileset',
            'simulation': 'simulation_id',
        }

        :param tile: tmx.Tile object
        :param tile_set: The tmx.Tileset object
        :return: dict of definition
        """
        properties = {}

        for property in self._properties_required:
            properties[property] = self._get_tile_property(property, tile, tile_set)

        for property in self._properties_optional:
            try:
                properties[property] = self._get_tile_property(property, tile, tile_set)
            except NotFound:
                properties[property] = None

        properties['actions'] = self._get_node_actions(tile)
        properties['position'] = tile.id

        return properties

    def _get_tile_property(self, name, tile, tile_set):
        """

        Return tile property value. If property not found in tile, search in tile_set.

        :param name: name of property
        :param tile: tmx.Tile
        :param tile_set:  tmx.Tileset
        :return: the property value
        :rtype: str
        """
        # Get tile property
        try:
            return self._get_property(name, tile)
        except NotFound:
            # If not, search in tile_set
            return self._get_property(name, tile_set)

    @staticmethod
    def _get_property(name, node):
        """

        Return property value of tile

        :param name: name of property
        :param node: tmx.Tile or tmx.Tileset
        :return: value of property
        """
        for node_property in node.properties:
            if name == node_property.name and node_property.value:
                return node_property.value
        raise NotFound('"%s" property not found' % name)

    def _get_node_actions(self, node):
        """

        Return list of action.
        *NOTE*: Work in progress

        :param node:
        :return:
        """
        actions = []
        for node_property in node.properties:
            if 'actions' == node_property.name and node_property.value:
                actions = [action.strip() for action in node_property.value.split(',')]

        return actions

    def get_tiles_data(self):
        """

        Return a dict with definition of synergies object in they simulation and collections.

        :return: dict with definition of simulation
        """
        tiles_data = []
        tile_set_width = self.width

        current_x_position = -1
        current_y_position = 0

        for z, layer in enumerate(self.layers):  # z: to do in future ...
            for tile in layer.tiles:

                if current_x_position == tile_set_width-1:
                    current_x_position = -1
                    current_y_position += 1

                current_x_position += 1

                position = (0, current_x_position, current_y_position)

                if tile.gid != 0:

                    object_definition = dict(self._objects_definitions[tile.gid])
                    object_definition['position'] = position

                    tiles_data.append(object_definition)

        return tiles_data

    def get_tile_set(self, key):
        """

        Return a tmx.Tileset for given key

        :param key:
        :return: tmx.Tileset
        """
        return self.tilesets[key]

    def get_tile_position_with_class(self, tile_set_id, tile_class):
        for object_gid in self._objects_definitions:
            object_definition = self._objects_definitions[object_gid]
            if object_definition['tile_set'] == tile_set_id and object_definition['class'] == tile_class:
                return object_definition['position']
        raise NotFound()