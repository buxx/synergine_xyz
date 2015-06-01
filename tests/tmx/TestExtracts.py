import PIL
from synergine_xyz.tmx.TileMapConnector import TileMapConnector
from tests.tmx.src.TmxMap import TmxMap
from tests.tmx.src.TmxMap import FoodObj, AntObj, EggObj, RockObj
from tests.tmx.src.tiles_string import ant, egg, food, rock


class TestExtracts(TmxMap):

    def test_objects_images(self):
        tile_map_connector = TileMapConnector.from_file(self._map_file_path)
        object_images = tile_map_connector.extract_objects_images(dict(self._map_config))

        self.assertTrue(FoodObj in object_images)
        self.assertIsInstance(object_images[FoodObj], PIL.Image._ImageCrop)
        self.assertEquals(food, object_images[FoodObj].tostring())

        self.assertTrue(AntObj in object_images)
        self.assertIsInstance(object_images[AntObj], PIL.Image._ImageCrop)
        self.assertEquals(ant, object_images[AntObj].tostring())

        self.assertTrue(EggObj in object_images)
        self.assertIsInstance(object_images[EggObj], PIL.Image._ImageCrop)
        self.assertEquals(egg, object_images[EggObj].tostring())

        self.assertTrue(RockObj in object_images)
        self.assertIsInstance(object_images[RockObj], PIL.Image._ImageCrop)
        self.assertEquals(rock, object_images[RockObj].tostring())


