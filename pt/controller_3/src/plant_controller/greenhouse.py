"""Greenhouse unit module.

The Greenhouse is a Unit representing the shared greenhouse environment.
It has light and temperature/humidity sensors but no actuation.
"""

from typing import Any

from .database import DatabaseClient
from .sensors import init_sensor
from .unit import Unit


class Greenhouse(Unit):
    """The greenhouse environment unit.

    Automatically registers the AS7341 spectral light sensor and the
    SHT45 temperature/humidity sensor. There is one Greenhouse instance
    per controller.
    """

    def __init__(self, db_client: DatabaseClient, busses: dict[str, Any]):
        """Initialize the greenhouse with its fixed sensor set.

        Args:
            db_client: Database client for persisting measurements.
            busses: Dict of available bus instances.
        """
        super().__init__(name="greenhouse", db_client=db_client)
        self.register_sensor(init_sensor(
            module_name="as7341",
            class_name="GreenhouseAS7341",
            parameter="light_level", # Defined by sensor 
            busses=busses,
            db_save_function=self.db_save_function
        ))
        self.register_sensor(init_sensor(
            module_name="sht45",
            class_name="GreenhouseSHT45",
            parameter="air", # Defined by sensor
            busses=busses,
            db_save_function=self.db_save_function
        ))
