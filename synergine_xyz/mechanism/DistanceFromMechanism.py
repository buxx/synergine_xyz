from synergine_xyz.cst import POSITION
from synergine.core.simulation.mechanism.Mechanism import Mechanism


class DistanceFromMechanism(Mechanism):
    """

    """

    def _get_computed_object_event_parameters(self, object_id, context):
        max_distance = self._get_maximum_distance(object_id, context)
        object_position = context.metas.value.get(POSITION, object_id)
        around_points_distance = self._get_distances_for_points(context, object_position, max_distance)
        return {'points_distances': around_points_distance}

    def _get_maximum_distance(self, object_id, context):
        raise NotImplementedError()

    def _get_distances_for_points(self, context, object_position, max_distance):
        points_distances = {object_position: 0}
        points_to_looks = [object_position]

        for current_distance in range(max_distance):
            new_points_to_looks = []
            for looked_point in points_to_looks:
                around_points = context.get_around_points_of_point(looked_point)
                for around_point in around_points:
                    if around_point not in points_distances and self._point_is_computable(context, around_point):
                        points_distances[around_point] = current_distance+1
                        new_points_to_looks.append(around_point)
            points_to_looks = new_points_to_looks

        return points_distances

    def _point_is_computable(self, context, point):
        return True
