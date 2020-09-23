"""Base class(es) of the controller which can data can be loaded from CSV file."""
import csv
import os
from abc import ABC, abstractmethod
from typing import List

from msnmetrosim.static import DATA_DIR

__all__ = ("CSVLoadableController",)


class CSVLoadableController(ABC):
    """Base class of the controller which can data can be loaded from CSV file."""

    def __init__(self, data: list):
        self._data = data

    @staticmethod
    def get_csv_file_abs_path(file_path: str):
        """
        Get the absolute path of ``file_path``.

        This assumes that the data file ``file_path`` is inside the directory configured in ``msnmetrosim.static``.
        """
        return os.path.join(DATA_DIR, file_path)

    @staticmethod
    @abstractmethod
    def on_row_read(row: List[str]) -> object:
        """
        Method to be called upon a row of csv being read.

        This should return a data entry object for initialization.
        """
        raise NotImplementedError()

    @classmethod
    def load_csv(cls, file_path: str, delimiter: str = ",", has_header: bool = True):
        """
        Load a csv file to be a controller.

        Note that ``file_path`` should be a relative path of the data file under the data directory.

        Data directory can be configured in ``msnmetrosim.static``.
        """
        routes = []

        with open(cls.get_csv_file_abs_path(file_path), "r") as file:
            csv_reader = csv.reader(file, delimiter=delimiter)

            if has_header:
                next(csv_reader, None)  # Dump header

            for row in csv_reader:
                routes.append(cls.on_row_read(row))

        return cls(routes)
