"""Dynamic pump schedule implementation.

Waters the plant based on a linked sensor reading, maintaining the sensed
parameter between a low point and a high point. When the reading drops
below the low point the schedule enters a "climbing" phase — dosing water
at regular intervals until the reading exceeds the high point, then it
switches to a "falling" phase where it simply polls the sensor until the
reading drops again.

Schedule JSON format::

    {
        "type": "dynamic",
        "details": {
            "linked_sensed_parameter": "soil_moisture",
            "high_point": 44,
            "low_point": 15,
            "watering_dose_increment_when_climbing_in_milliliters": 50,
            "time_in_seconds_between_watering_when_climbing": 600,
            "time_in_seconds_between_sensing_when_falling": 600
        }
    }
"""

import logging
_logger = logging.getLogger(__name__)

from collections.abc import Coroutine
from typing import Any

import anyio

from . import PumpSchedule

LINKED_PARAMETER = "linked_sensed_parameter"
HIGH_POINT = "high_point"
LOW_POINT = "low_point"
CLIMBING_DOSE = "watering_dose_increment_when_climbing_in_milliliters"
CLIMBING_REST_TIME = "time_in_seconds_between_watering_when_climbing"
FALLING_TBS = "time_in_seconds_between_sensing_when_falling"

class Schedule(PumpSchedule):
    """Sensor-driven watering schedule.

    Maintains a sensed parameter (e.g. soil moisture) between two
    thresholds by alternating between *climbing* and *falling* phases:

    * **Falling** — the sensor value is above the low point. The schedule
      polls the sensor at ``falling_tbs`` intervals and takes no action.
    * **Climbing** — the sensor value dropped below the low point. The
      schedule doses water every ``climbing_rest_time`` seconds until the
      reading exceeds the high point, then returns to falling.

    Attributes:
        linked_parameter: Name of the sensed parameter to track.
        high_point: Upper threshold; stop watering when exceeded.
        low_point: Lower threshold; start watering when reading drops below.
        climbing_dose: Milliliters of water to deliver per dose while climbing.
        climbing_rest_time: Seconds to wait between doses while climbing.
        falling_tbs: Seconds between sensor polls while falling.
        climbing: Whether the schedule is currently in the climbing phase.
    """

    def __init__(self, details: Any | None):
        """Parse dynamic schedule configuration.

        Args:
            details: Dict containing the six required configuration keys
                (see module docstring for the expected JSON shape).
        """
        self.linked_parameter = details[LINKED_PARAMETER]
        self.high_point = details[HIGH_POINT]
        self.low_point = details[LOW_POINT]
        self.climbing_dose = details[CLIMBING_DOSE]
        self.climbing_rest_time = details[CLIMBING_REST_TIME]
        self.falling_tbs = details[FALLING_TBS]
        self.climbing = False

    def register_plant(self, plant):
        """Bind the schedule to a plant so it can read sensor data.

        Args:
            plant: The plant instance whose ``db_client`` will be queried
                for the linked sensed parameter.
        """
        self._get_current_moisture_level = lambda: plant.db_client.read_measurements(
            physical_unit=plant.name,
            parameter=self.linked_parameter,
            limit=1
        ).value[0]

    def get_type(self) -> str:
        return "dynamic"

    def get_description(self):
        return "Dynamic watering schedule. Waters the plant dynamically, making the plant soil vacillate between the high point and the low point. The schedule is linked to a sensed parameter, and will water the plant when the sensed parameter drops below the low point, and will stop watering when the sensed parameter exceeds the high point. On controller startup, the schedule starts in the falling phase, and will not water the plant until the sensed parameter drops below the low point."
    
    def get_details(self) -> dict:
        """Return the schedule configuration as a dict suitable for JSON serialization."""
        return {
            LINKED_PARAMETER: self.linked_parameter,
            HIGH_POINT: self.high_point,
            LOW_POINT: self.low_point,
            CLIMBING_DOSE: self.climbing_dose,
            CLIMBING_REST_TIME: self.climbing_rest_time,
            FALLING_TBS: self.falling_tbs
        }
    
    async def run_schedule(self, pump_function: Coroutine[Any, int]):
        """Alternate between climbing and falling phases forever.

        Args:
            pump_function: Async callback to activate the pump with a
                dosage in milliliters.
        """
        while True:
            if self.climbing:
                if self._get_current_moisture_level() > self.high_point:
                    self.climbing = False
                else:
                    await pump_function(self.climbing_dose)
                    await anyio.sleep(self.climbing_rest_time)
            else:
                if self._get_current_moisture_level() < self.low_point:
                    self.climbing = True
                else:
                    await anyio.sleep(self.falling_tbs)

    @staticmethod
    def validate_schedule_details(schedule_details: Any):
        """Validate that schedule_details contains all required keys.

        Args:
            schedule_details: The "details" field from the config JSON.

        Raises:
            ValueError: If format requirements are not met.
        """
        if not isinstance(schedule_details, dict):
            raise ValueError("A schedule of type 'dynamic' needs a dictionary with configuration parameters in the 'details' value.")
        
        if LINKED_PARAMETER not in schedule_details:
            raise ValueError(f"Dynamic schedule 'details' must contain a '{LINKED_PARAMETER}' entry.")

        if not isinstance(schedule_details[LINKED_PARAMETER], str):
            raise ValueError(f"'{LINKED_PARAMETER}' must be a string.")

        if HIGH_POINT not in schedule_details:
            raise ValueError(f"Dynamic schedule 'details' must contain a '{HIGH_POINT}' entry.")

        if not isinstance(schedule_details[HIGH_POINT], (int, float)):
            raise ValueError(f"'{HIGH_POINT}' must be a number.")

        if LOW_POINT not in schedule_details:
            raise ValueError(f"Dynamic schedule 'details' must contain a '{LOW_POINT}' entry.")

        if not isinstance(schedule_details[LOW_POINT], (int, float)):
            raise ValueError(f"'{LOW_POINT}' must be a number.")

        if schedule_details[LOW_POINT] >= schedule_details[HIGH_POINT]:
            raise ValueError(f"'{LOW_POINT}' must be less than '{HIGH_POINT}'.")

        if CLIMBING_DOSE not in schedule_details:
            raise ValueError(f"Dynamic schedule 'details' must contain a '{CLIMBING_DOSE}' entry.")

        if not isinstance(schedule_details[CLIMBING_DOSE], int):
            raise ValueError(f"'{CLIMBING_DOSE}' must be an integer.")

        if CLIMBING_REST_TIME not in schedule_details:
            raise ValueError(f"Dynamic schedule 'details' must contain a '{CLIMBING_REST_TIME}' entry.")

        if not isinstance(schedule_details[CLIMBING_REST_TIME], (int, float)):
            raise ValueError(f"'{CLIMBING_REST_TIME}' must be a number.")

        if FALLING_TBS not in schedule_details:
            raise ValueError(f"Dynamic schedule 'details' must contain a '{FALLING_TBS}' entry.")

        if not isinstance(schedule_details[FALLING_TBS], (int, float)):
            raise ValueError(f"'{FALLING_TBS}' must be a number.")

