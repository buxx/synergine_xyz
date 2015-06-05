import pygame
from synergine.display.Visualisation import Visualisation as BaseVisualisation
from synergine_xyz.display.object.pygame.PygameImage import PygameImage
from synergine_xyz.display.object.pygame.DirectionnedImage import DirectionnedImage
from synergine_xyz.cst import PREVIOUS_DIRECTION


class PygameVisualisation(BaseVisualisation):

    def __init__(self, visualisation_config):
        super().__init__(visualisation_config)
        self._oriented_objects = []
        self._oriented_images = {}

    def set_oriented_objects(self, oriented_object_classes):
        self._oriented_objects = oriented_object_classes

    def add_oriented_objects(self, oriented_object_class):
        self._oriented_objects.append(oriented_object_class)

    def _update_object_config(self, object_class, object_image):
        super()._update_object_config(object_class, object_image)
        pil_image = self._get_object_default_image(object_class)
        image_bytes = pil_image.tobytes()
        pygame_surface = pygame.image.fromstring(image_bytes, pil_image.size, pil_image.mode)
        pygame_image = PygameImage(pygame_surface)
        self._visualisation_config['objects'][object_class]['default'] = pygame_image

    def _is_oriented_object(self, object_class):
        for oriented_object_class in self._oriented_objects:
            if issubclass(object_class, oriented_object_class) or object_class == oriented_object_class:
                return True
        return False

    def _get_object_default_image(self, object_class):
        return self._visualisation_config['objects'][object_class]['default']

    def _add_oriented_callback(self, object_class):
        default_image = self._get_object_default_image(object_class)
        direction_image = DirectionnedImage(default_image)
        self._oriented_images[object_class] = direction_image
        # TODO: Peut-on se passer de that ?
        that = self
        self._visualisation_config['objects'][object_class]['callbacks'].append(
            lambda obj, context: that.get_oriented_image(object_class, obj, context)
        )

    def get_oriented_image(self, object_class, obj, context):
        try:
            previous_direction = context.metas.value.get(PREVIOUS_DIRECTION, obj.get_id())
        # TODO: KeyError: berk
        except KeyError:
            previous_direction = 14
        directionned_image = self._oriented_images[object_class]
        return directionned_image.get_for_direction(previous_direction)

    def add_callback(self, object_class, callback):
        self._visualisation_config['objects'][object_class]['callbacks'].append(callback)

    def add_oriented_callbacks(self):
        for object_class in self._visualisation_config['objects']:
            if self._is_oriented_object(object_class):
                self._add_oriented_callback(object_class)
