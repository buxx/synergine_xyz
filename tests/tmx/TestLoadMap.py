from synergine_xyz.tmx.TileMapConnector import TileMapConnector
from tests.tmx.src.TmxMap import TmxMap


class TestLoadMap(TmxMap):

    def test_import(self):
        TileMapConnector.from_file(self._map_file_path)

    def test_get_simulations(self):
        tile_map_connector = TileMapConnector.from_file(self._map_file_path)
        simulations = tile_map_connector.create_simulations(dict(self._map_config))

        self.assertEquals(1, len(simulations))
        self.assertTrue(isinstance(simulations[0], self._map_config['simulation']['base']))