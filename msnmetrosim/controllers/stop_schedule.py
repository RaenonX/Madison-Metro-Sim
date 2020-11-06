"""
Controller of the MMT GTFS stop schedule data.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from datetime import timedelta, datetime
from typing import List, Iterable, Dict, Tuple

from msnmetrosim.models import MMTStopSchedule, MMTStopScheduleSim
from .base import CSVLoadableController

__all__ = ("MMTStopScheduleController",)


class MMTStopScheduleController(CSVLoadableController):
    """
    MMT stop schedule data controller.

    Data file that will use this controller:
    - mmt_gtfs/stop_times.csv
    """

    def _init_by_arrival_hr(self, stop_schedules: List[MMTStopSchedule]):
        """Initialize a :class:`list` which index is the hour of arrival time of the stop schedule."""
        for stop_schedule in stop_schedules:
            self._by_arrival_hr[stop_schedule.arrival_time.hour].append(stop_schedule)

    def _init_by_trip_id_len(self, stop_schedules: List[MMTStopSchedule]):
        """
        Initialize ``self._by_trip_id`` which key is the trip ID and the value is the stops arranged sequentially.

        This assumes ``stop_schedules`` is already sorted by the trip ID first, then the stop sequence.

        This also initializes ``self._by_trip_len`` to store the stop count of a trip.
        The key of this dict is the trip ID, and the value of this dict is the stop count of that trip.
        """
        for stop_schedule in stop_schedules:
            trip_id = stop_schedule.trip_id

            if trip_id not in self._by_trip_id:
                self._by_trip_id[trip_id] = [stop_schedule]
                self._by_trip_len[trip_id] = 1
            else:
                self._by_trip_id[trip_id].append(stop_schedule)
                self._by_trip_len[trip_id] += 1

    def __init__(self, stop_schedules: List[MMTStopSchedule]):
        super().__init__(stop_schedules)

        self._by_arrival_hr: List[List[MMTStopSchedule]] = [[] for _ in range(24)]
        self._init_by_arrival_hr(stop_schedules)

        self._by_trip_id: Dict[int, List[MMTStopSchedule]] = {}
        self._by_trip_len: Dict[int, int] = {}
        self._init_by_trip_id_len(stop_schedules)

    def _get_stop_schedules(self, arrival_hr: int, trip_ids: Iterable[int] = None) -> List[MMTStopSchedule]:
        """
        Get the stop schedules which the hour of arrival time is ``arrival_hr``.

        If ``trip_ids`` is given,
        the return will only contain the stop schedules which trip ID is contained in ``trip_ids``.
        """
        if arrival_hr < 0 or arrival_hr > 23:
            raise ValueError(f"Invalid `arrival_hr`: {arrival_hr}")

        ret: List[MMTStopSchedule]

        if trip_ids:
            ret = [data for trip_id in trip_ids
                   for data in self._by_trip_id[trip_id] if data.arrival_time.hour == arrival_hr]
        else:
            ret = [stop_schedule for stop_schedule in self._by_arrival_hr[arrival_hr]
                   if stop_schedule in trip_ids]

        return ret

    def get_stop_schedule_sim_by_arrival(self, start_dt: datetime, time_range: float, /,
                                         trip_ids: Iterable[int] = None) \
            -> List[MMTStopScheduleSim]:
        """
        Get all stop schedules which arrival time is between ``start_dt`` and ``(start_dt + time_range)``.

        ``time_range`` is in seconds.

        The return will be sorted by the arrival time.

        If ``trip_ids`` is set, only stop schedules which trip ID is in ``trip_ids`` will be returned.
        """
        ret: List[MMTStopScheduleSim] = []

        # Blocks to "include all"
        for hr in range(start_dt.hour, start_dt.hour + int(time_range // 3600)):
            # Modding 24 since the start time and the end time is cross-day is possible
            data_block = self._get_stop_schedules(hr % 24, trip_ids)

            start_date = start_dt.date()
            if hr > 23:
                start_date += timedelta(days=1)

            # --- Find the next stop and add it if exists

            # Cache to store the converted next :class:`MMTStopScheduleSim`
            # Key is (trip_id, stop_sequence), value is the next stop for the corresponding stop
            next_cache: Dict[Tuple[int, int]] = {}

            # In-line function to fill the next stop cache
            def fill_next_cache(tid, seq):
                if seq >= self._by_trip_len[tid]:
                    return None

                next_raw = self._by_trip_id[tid][seq]

                # Check if the arrival time is in the range
                if next_raw.arrival_time.hour == hr:
                    next_sim = fill_next_cache(tid, seq + 1)
                    next_cache[(tid, seq)] = MMTStopScheduleSim.from_raw(next_raw, start_date, next_stop=next_sim)

                    return next_sim

                return None

            for stop_schedule in data_block:
                trip_id = stop_schedule.trip_id
                trip_stops = self._by_trip_len[trip_id]
                next_seq = stop_schedule.stop_sequence
                next_cache_key = (trip_id, stop_schedule.stop_sequence)

                # If the next stop is not yet generated, generate it and store it to the cache for later use
                if next_cache_key not in next_cache and next_seq < trip_stops:
                    fill_next_cache(trip_id, next_seq)

                next_stop = next_cache.get(next_cache_key)
                ret.append(MMTStopScheduleSim.from_raw(stop_schedule, start_date, next_stop=next_stop))

        # Blocks to selectively included
        end_time = start_dt + timedelta(seconds=time_range)

        for data in self._get_stop_schedules(end_time.hour, trip_ids):
            schedule_sim = MMTStopScheduleSim.from_raw(data, end_time.date())
            if schedule_sim.arrival_time <= end_time:
                ret.append(schedule_sim)

        return list(sorted(ret, key=lambda s_sim: s_sim.arrival_time))

    @staticmethod
    def on_row_read(row: List[str]) -> object:
        return MMTStopSchedule.parse_from_row(row)
