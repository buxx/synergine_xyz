from synergine_xyz.tmx.TileMapConnector import TileMapConnector
from tests.tmx.src.TmxMap import TmxMap
from tests.tmx.src.TmxMap import AntCollection, EnvCollection, AntObj, FoodObj, RockObj


class TestLoadMap(TmxMap):

    def _get_set_up_simulations(self):
        tile_map_connector = self._get_import()
        return tile_map_connector.create_simulations()

    def _get_import(self):
        return TileMapConnector.from_file(self._map_file_path, dict(self._map_config))

    def test_import(self):
        self._get_import()

    def test_get_simulations(self):
        # We have to launch simulation to check synergies objects states
        synergy_object_manager = self._get_synergy_object_manager_for_cycle(cycles=0, main_process=True)
        simulations = synergy_object_manager.get_simulations()

        # Test simulations contents
        self.assertEquals(1, len(simulations))
        self.assertTrue(isinstance(simulations[0], self._map_config['simulation']['base']))

        collections = simulations[0].get_collections()
        self.assertEquals(3, len(collections))

        self.assertIsInstance(collections[0], AntCollection)
        self.assertIsInstance(collections[1], AntCollection)
        self.assertIsInstance(collections[2], EnvCollection)

        collection_0_objects = collections[0].get_objects()
        self.assertEquals(1, len(collection_0_objects))
        self.assertIsInstance(collection_0_objects[0], AntObj)
        self.assertEquals((0, 2, 3), collection_0_objects[0].get_position())

        collection_1_objects = collections[1].get_objects()
        self.assertEquals(1, len(collection_1_objects))
        self.assertIsInstance(collection_1_objects[0], AntObj)
        self.assertEquals((0, 3, 1), collection_1_objects[0].get_position())

        collection_2_objects = collections[2].get_objects()
        self.assertEquals(8, len(collection_2_objects))
        self.assertIsInstance(collection_2_objects[0], RockObj)
        self.assertIsInstance(collection_2_objects[1], RockObj)
        self.assertIsInstance(collection_2_objects[2], RockObj)
        self.assertIsInstance(collection_2_objects[3], RockObj)
        self.assertIsInstance(collection_2_objects[4], RockObj)
        self.assertIsInstance(collection_2_objects[5], FoodObj)
        self.assertIsInstance(collection_2_objects[6], RockObj)
        self.assertIsInstance(collection_2_objects[7], RockObj)
        self.assertEquals((0, 0, 0), collection_2_objects[0].get_position())
        self.assertEquals((0, 1, 0), collection_2_objects[1].get_position())
        self.assertEquals((0, 2, 0), collection_2_objects[2].get_position())
        self.assertEquals((0, 3, 0), collection_2_objects[3].get_position())
        self.assertEquals((0, 0, 1), collection_2_objects[4].get_position())
        self.assertEquals((0, 1, 1), collection_2_objects[5].get_position())
        self.assertEquals((0, 0, 2), collection_2_objects[6].get_position())
        self.assertEquals((0, 0, 3), collection_2_objects[7].get_position())
