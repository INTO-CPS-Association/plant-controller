"""Data structures for sensor measurements and actuation events.

This module defines the datapoint classes used throughout the system to
represent sensor readings and watering events. All data flowing to the
database passes through these structures.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Confidence:
    """Statistical confidence specification for a measurement.

    Attributes:
        interval: The uncertainty interval (e.g. 0.2 for +/- 0.2).
        level: The confidence level as a fraction (e.g. 0.95 for 95%).
    """
    interval: float
    level: float

    def str_representation(self) -> str:
        """Return a formatted string like '+-1.0000e-01 at 95.00%'."""
        return '±{:.4e} at {:.2%}'.format(self.interval, self.level)

    def __str__(self):
        return self.str_representation()


class Datapoint(ABC):
    """Abstract base class for all data that gets written to the database.

    Subclasses must implement ``to_point`` to produce a dict compatible
    with the InfluxDB line protocol structure used by DatabaseClient.
    """

    @abstractmethod
    def to_point(self, unit: str) -> dict[str, Any]:
        """Convert this datapoint to an InfluxDB-compatible dict.

        Args:
            unit: Name of the physical unit this data belongs to.

        Returns:
            Dict with 'measurement', 'tags', 'fields', and 'time' keys.
        """
        pass

    @staticmethod
    def format_for_table_name(physical_unit: str, parameter: str) -> str:
        """Generate the database table (measurement) name.

        Args:
            physical_unit: Name of the unit (e.g. 'basil_1').
            parameter: Name of the parameter (e.g. 'temperature').

        Returns:
            Lowercase string in the form '<unit>_<parameter>'.
        """
        return f'{physical_unit}_{parameter}'.lower()


class Measurement(Datapoint):
    """A single sensor measurement datapoint.

    Attributes:
        parameter: Name of the measured parameter.
        value: The measured value.
        units: Unit string (e.g. '°C', '%', 'photons/s').
        confidence: Optional uncertainty specification.
        time: Timestamp of the measurement (defaults to now).
    """

    def __init__(
        self,
        parameter: str,
        value: Any,
        units: str,
        confidence: None | Confidence = None,
        time: None | datetime = None
    ):
        self.parameter = parameter
        self.value = value
        self.units = units
        self.confidence = confidence
        if time is None:
            time = datetime.now()
        self.time = time

    def to_point(self, unit: str):
        """Convert to InfluxDB point dict.

        Args:
            unit: Name of the physical unit this measurement belongs to.
        """
        return {
            "measurement": Datapoint.format_for_table_name(unit, self.parameter),
            "tags": {
                "physical_unit": unit,
                "parameter": self.parameter
            },
            "fields": {
                "value": self.value,
                "confidence": str(self.confidence),
                "units": self.units
            },
            "time": self.time
        }


class WateringEvent(Datapoint):
    """A record of a watering actuation event.

    Attributes:
        dosage: Amount of water pumped in milliliters.
        time: Timestamp of the event (defaults to now).
    """

    def __init__(
        self,
        dosage: int,
        time: None | datetime = None
    ):
        self.dosage = dosage
        if time is None:
            time = datetime.now()
        self.time = time

    def to_point(self, unit: str):
        """Convert to InfluxDB point dict.

        Args:
            unit: Name of the physical unit this event belongs to.
        """
        return {
            "measurement": Datapoint.format_for_table_name(unit, "watering"),
            "tags": {"physical_unit": unit},
            "fields": {
                "value": self.dosage,
                "units": "ml"
            },
            "time": self.time
        }
    
