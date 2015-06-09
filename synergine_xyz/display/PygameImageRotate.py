from pygame.transform import rotate
from synergine_xyz.display.object.pygame.PygameImage import PygameImage


class PygameImageRotate:

    def __init__(self):
        self._cache = {}

    def get_for_direction(self, pygame_image, direction):
        pygame_image_id = id(pygame_image)

        if pygame_image_id not in self._cache:
            self._cache[pygame_image_id] = {}

        if direction not in self._cache[pygame_image_id]:
            self._cache[pygame_image_id][direction] = self._rotate_image(pygame_image, direction)

        return self._cache[pygame_image_id][direction]

    @staticmethod
    def _rotate_image(pygame_image, direction):
        image_surface = pygame_image.get_surface()
        if direction == 10:
            return PygameImage(rotate(image_surface, 45))
        if direction == 11 or direction == 14:
            return PygameImage(image_surface)
        if direction == 12:
            return PygameImage(rotate(image_surface, -45))
        if direction == 13:
            return PygameImage(rotate(image_surface, 90))
        if direction == 14:
            return PygameImage(image_surface)
        if direction == 15:
            return PygameImage(rotate(image_surface, -90))
        if direction == 16:
            return PygameImage(rotate(image_surface, 135))
        if direction == 17:
            return PygameImage(rotate(image_surface, 180))
        if direction == 18:
            return PygameImage(rotate(image_surface, -135))

        raise Exception('Direction unknown')
