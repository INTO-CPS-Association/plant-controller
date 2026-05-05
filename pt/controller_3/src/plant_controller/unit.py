"""Base unit module defining the Unit class.

A Unit represents a physical entity (plant or greenhouse) that has sensors
attached to it and optionally actuators. Units are the primary organizational
abstraction: each unit has its own database namespace and sensor set.
"""

import anyio

from .database import DatabaseClient
from .datapoint import Datapoint
from .setup_actions import HasSetupFunctionsMixin

class Unit(HasSetupFunctionsMixin):
    """A physical unit with attached sensors and optional actuation.

    This is the base class for Plant and Greenhouse. It manages sensor
    registration, the sensing loop, and database persistence.

    Attributes:
        name: Unique identifier for this unit (used as DB namespace).
        db_client: Database client for persisting measurements.
        db_lock: Async lock ensuring serialized DB writes.
        sensors: List of registered Sensor instances.
    """

    def __init__(self, name: str, db_client: DatabaseClient):
        """Initialize the unit.

        Args:
            name: Unique name identifying this unit.
            db_client: Database client for measurement persistence.
        """
        self.name = name
        self.db_client = db_client
        self.db_lock = anyio.Lock()
        self.sensors = []

    def register_sensor(self, new_sensor):
        """Register a sensor with this unit.

        Ensures no two sensors report the same parameter name within a unit.

        Args:
            new_sensor: A Sensor instance to attach to this unit.

        Raises:
            ValueError: If a parameter name conflicts with an existing sensor.
        """
        for sensor in self.sensors:
            for parameter in list(sensor.get_capabilities()):
                if parameter in new_sensor.get_capabilities():
                    raise ValueError(f"Sensor with parameter '{parameter}' already exists in unit '{self.name}'. Each sensor must have unique parameters. If two sensors have overlapping parameters, consider combining them into a single sensor, or specifying the differences in their parameters.")
        self.sensors.append(new_sensor)

    async def start_sensing(self):
        """Start all sensor reading loops concurrently.

        Each sensor's reading_loop is launched as a task in a task group.
        This coroutine runs indefinitely.
        """
        async with anyio.create_task_group() as tg:
            for sensor in self.sensors:
                tg.start_soon(sensor.reading_loop)

    async def db_save_function(self, data: Datapoint | list[Datapoint]):
        """Persist measurement data to the database (thread-safe).

        This method is passed to sensors and pumps as their save callback.

        Args:
            data: A single Datapoint or list of Datapoints to persist.
        """
        async with self.db_lock:
            self.db_client.write_measurements(self.name, data)

    def get_sensing_capabilites(self):
        """Return combined capabilities of all registered sensors.

        Returns:
            Dict mapping parameter names to their capability info dicts.
        """
        capabilities = {}
        for sensor in self.sensors:
            capabilities = {**capabilities, **sensor.get_capabilities()}
        return capabilities

    def has_actuation(self) -> bool:
        """Return whether this unit has actuation capabilities.

        Override in subclasses that have pumps or other actuators.
        """
        return False