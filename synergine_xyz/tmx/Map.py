from tmx import TileMap
from synergine_xyz.exceptions import NotFound


class Map(TileMap):

    _properties = ['simulation', 'collection', 'object']
    """List of synergies object properties"""

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
        objects_definitions = {}
        for tile_set_position, tile_set in enumerate(self.tilesets):
            first_gid = tile_set.firstgid
            for key, tile in enumerate(tile_set.tiles):
                tile_id = first_gid + key
                objects_definitions[tile_id] = self._get_tile_properties(tile, tile_set)
                objects_definitions[tile_id]['tile_set'] = tile_set_position
        return objects_definitions


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

        for property in self._properties:
            properties[property] = self._get_tile_property(property, tile, tile_set)

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
