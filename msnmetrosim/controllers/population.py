"""Controller of the population data."""
from typing import List, Tuple

from msnmetrosim.models import PopulationWard
from msnmetrosim.utils import get_plane, generate_points
from .base import CSVLoadableController, LocationalDataController

__all__ = ("PopulationDataController",)


class PopulationDataController(LocationalDataController, CSVLoadableController):
    """
    Population data controller.

    Data file that will use this controller:
    - population.csv
    """

    def __init__(self, pop_ward: List[PopulationWard]):
        super().__init__(pop_ward)

    def get_population_points(self, lat: float, lon: float, range_km: float, interval_km: float) \
            -> Tuple[List[Tuple[float, float]], List[float]]:
        """
        Get the coordinates of dummy wards with weights as the population density around the corresponding point.

        Both ``range_km`` and ``interval_km`` will be used for generating dummy wards.

        This method gets 3 closest ward points centered around ``(lat, lon)``,
        then use these to construct a plane to project the population density,
        which will be returned as the second element.
        """
        pop_points = self.find_closest_data_num(lat, lon, 3)
        pop_project_plane = get_plane(((pop_points[0].data.lat, pop_points[0].data.lon, pop_points[0].data.total),
                                       (pop_points[1].data.lat, pop_points[1].data.lon, pop_points[1].data.total),
                                       (pop_points[2].data.lat, pop_points[2].data.lon, pop_points[2].data.total)))

        ret_pop_points: List[Tuple[float, float]] = []
        ret_pop_density: List[float] = []

        wards = generate_points((lat, lon), range_km, interval_km)

        for ward in wards:
            ret_pop_points.append(ward)
            ret_pop_density.append(pop_project_plane.get_z(*ward, 1))

        return ret_pop_points, ret_pop_density

    @staticmethod
    def on_row_read(row: List[str]) -> object:
        return PopulationWard.parse_from_row(row)
