"""Progress tracker."""
from dataclasses import dataclass, field
from datetime import datetime, timedelta

__all__ = ("Progress",)

from typing import Optional


@dataclass
class Progress:
    """
    An object for tracking the progress.

    Call ``start()`` upon starting the task.

    Usage
    -----

    >>> count = 10
    >>>
    >>> progress = Progress(count)
    >>> progress.start()
    >>> for i in range(count):
    >>>     # Task
    >>>     progress.rec_completed_one()
    >>>     print(progress)
    """

    total: int
    completed: int = field(default=0)

    dt_start: datetime = field(default=None)
    dt_last_rec: datetime = field(default=None)

    def start(self):
        """
        Record that the task has started.

        If the task is already started, calling this method won't do anything.
        """
        if not self.dt_start:
            self.dt_start = datetime.now()

    def rec_completed_one(self):
        """
        Record that one unit of the task is completed.

        :raises ValueError: if the task is completed, i.e. `total` == `completed`
        """
        if self.total == self.completed:
            raise ValueError("Already completed")

        self.completed += 1
        self.dt_last_rec = datetime.now()

    @property
    def current_progress(self) -> float:
        """Current progress in ratio: 0 <= x <= 1."""
        return self.completed / self.total

    @property
    def estimated_time_left(self) -> Optional[float]:
        """
        Estimated time left for completing the task in seconds.

        Returns ``None`` if the task has not yet been started.
        """
        if not self.dt_start:
            return None

        secs_all = (self.dt_last_rec - self.dt_start).total_seconds() / self.current_progress
        secs_past = (datetime.now() - self.dt_start).total_seconds()
        secs_left = secs_all - secs_past

        return secs_left

    @property
    def estimated_completion_dt(self) -> Optional[datetime]:
        """
        Estimate completion timestamp of the task.

        Returns ``None`` if the task has not yet been started.
        """
        if not self.dt_start:
            return None

        return datetime.now() + timedelta(seconds=self.estimated_time_left)

    def __str__(self):
        if not self.dt_start:
            return f"{self.total} units of tasks to do. Task not yet started."

        return f"{self.completed} / {self.total} ({self.current_progress:.2%}) - " \
               f"Estimated to complete at {self.estimated_completion_dt.strftime('%Y-%m-%d %H:%M:%S')} " \
               f"({self.estimated_time_left:.2f} secs left)"

    def __repr__(self):
        return str(self)
