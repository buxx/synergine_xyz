from synergine_xyz.cst import POSITION
from synergine.core.simulation.mechanism.Mechanism import Mechanism
import numpy as np


class BinaryGridMechanism(Mechanism):
    """
    TODO: Cercle de point au lieu de carre ?
    """

    def _get_computed_object_event_parameters(self, object_id, context):
        radius = self._get_grid_radius(object_id, context)
        object_position = context.metas.value.get(POSITION, object_id)
        around_grid_points = self._get_around_grid_points(context, object_position, radius)
        around_grid = self._points_to_binary_grid(context, around_grid_points)
        return {
            'grid': around_grid,
            'points': around_grid_points,
            'center_point': (radius, radius),
            'start_position': object_position
        }

    def _get_grid_radius(self, object_id, context):
        # TODO Maintenir un rayon (calculé en fonction de la taille de la colonie + ratio en fonction de ce qui
        # est smelling)
        # pour le moment ...valeur hardcode
        return 6

    def _get_around_grid_points(self, context, start_position, radius):
        around_points = context.get_around_points_of(start_position, radius, exclude_start_point=False)
        real_diameter = radius*2+1  # (+1 because get_around_points_of compute around reference point)
        return np.array(around_points).reshape(real_diameter, real_diameter, 3)  # 3: 3d

    def _points_to_binary_grid(self, context, grid_points):
        binary_grid = []
        for line in grid_points:
            binary_grid.append(list(map(lambda position: self._position_is(position, context), line)))
        return np.array(binary_grid).reshape(len(grid_points[0]+1), len(grid_points[0]+1))
        return binary_grid

    def _position_is(self, position, context):
        """

        :param position:
        :param context:
        :return: 0 or 1
        :rtype: int
        """
        raise NotImplementedError()
