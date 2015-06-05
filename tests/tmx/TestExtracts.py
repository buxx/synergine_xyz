import PIL
from synergine_xyz.exceptions import NotFound
from synergine_xyz.tmx.TileMapConnector import TileMapConnector
from tests.tmx.src.TmxMap import TmxMap
from tests.tmx.src.TmxMap import FoodObj, AntObj, EggObj, RockObj
from tests.tmx.src.tiles_string import ant, egg, food, rock


class TestExtracts(TmxMap):

    def test_objects_images(self):
        tile_map_connector = TileMapConnector.from_file(self._map_file_path, dict(self._map_config))
        object_images = tile_map_connector.extract_objects_images()

        self.assertTrue(self._class_in_list(FoodObj, object_images))
        production_class = self._get_first_matching_class(FoodObj, object_images)
        self.assertIsInstance(object_images[production_class], PIL.Image._ImageCrop)
        self.assertEquals(food, object_images[production_class].tostring())

        self.assertTrue(self._class_in_list(AntObj, object_images))
        production_class = self._get_first_matching_class(AntObj, object_images)
        self.assertIsInstance(object_images[production_class], PIL.Image._ImageCrop)
        self.assertEquals(ant, object_images[production_class].tostring())

        self.assertTrue(self._class_in_list(EggObj, object_images))
        production_class = self._get_first_matching_class(EggObj, object_images)
        self.assertIsInstance(object_images[production_class], PIL.Image._ImageCrop)
        self.assertEquals(egg, object_images[production_class].tostring())

        self.assertTrue(self._class_in_list(RockObj, object_images))
        production_class = self._get_first_matching_class(RockObj, object_images)
        self.assertIsInstance(object_images[production_class], PIL.Image._ImageCrop)
        self.assertEquals(rock, object_images[production_class].tostring())

    def _class_in_list(self, class_to_find, list_of_classes):
        try:
            self._get_first_matching_class(class_to_find, list_of_classes)
            return True
        except NotFound:
            return False

    def _get_first_matching_class(self, class_to_find, list_of_classes):
        for class_to_test in list_of_classes:
            if issubclass(class_to_test, class_to_find) or class_to_find == class_to_test:
                return class_to_test
        raise NotFound()