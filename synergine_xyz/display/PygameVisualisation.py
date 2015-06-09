import pygame
from synergine.display.Visualisation import Visualisation as BaseVisualisation
from synergine_xyz.display.object.pygame.PygameImage import PygameImage


class PygameVisualisation(BaseVisualisation):

    def __init__(self, visualisation_config):
        super().__init__(visualisation_config)
        self._oriented_images = {}

    def add_oriented_objects(self, oriented_object_class):
        self._oriented_objects.append(oriented_object_class)

    def _update_object_config(self, object_class, object_image):
        super()._update_object_config(object_class, object_image)
        pil_image = self._get_object_default_image(object_class)
        image_bytes = pil_image.tobytes()
        pygame_surface = pygame.image.fromstring(image_bytes, pil_image.size, pil_image.mode)
        pygame_image = PygameImage(pygame_surface)
        self._visualisation_config['objects'][object_class]['default'] = pygame_image

    def _get_object_default_image(self, object_class):
        return self._visualisation_config['objects'][object_class]['default']

    def add_callback(self, object_class, callback):
        self._visualisation_config['objects'][object_class]['callbacks'].append(callback)

    def add_modifier(self, object_class, callback):
        self._visualisation_config['objects'][object_class]['modifiers'].append(callback)
