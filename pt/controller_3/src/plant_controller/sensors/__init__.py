"""Sensor modules for the plant monitoring system.

This package defines the abstract base class that all sensor implementations
must follow, and provides the dynamic loading mechanism used by the controller.

Writing a custom sensor module:
    1. Create a new ``.py`` file in this package (e.g. ``my_sensor.py``).
    2. Define a class that inherits from ``Sensor`` and one of the bus
       interface mixins from ``plant_controller.com_bus`` (``I2CInterface``
       or ``MODBUSInterface``).
    3. Implement the ``read`` method (async) to take a measurement and
       pass it to ``self.db_save_function``.
    4. Optionally override ``get_capabilities`` if the default
       implementation is not adequate.
    5. Reference the module and class in a plant's JSON config file::

           {
               "sensors": {
                   "my_parameter": {
                       "module": "my_sensor",
                       "class": "MySensorClass",
                       "kwargs": { ... }
                   }
               }
           }

    The ``kwargs`` dict is passed directly to the sensor's ``__init__``
    as keyword arguments (in addition to ``parameter``, ``bus``, and
    ``db_save_function`` which are always provided).

Example minimal sensor::

    from plant_controller.sensors import Sensor
    from plant_controller.com_bus import I2CInterface, BlinkaI2CBus
    from plant_controller.datapoint import Confidence, Measurement

    class MySensor(Sensor, I2CInterface):
        def __init__(self, parameter, bus, db_save_function, **kwargs):
            super().__init__(
                parameter=parameter,
                bus=bus,
                confidence=Confidence(interval=0.5, level=0.95),
                units="my_unit",
                time_between_reads=30,
                db_save_function=db_save_function,
            )

        async def read(self):
            value = ...  # read from hardware
            await self.db_save_function(
                Measurement(
                    parameter=self.parameter,
                    value=value,
                    confidence=self.confidence,
                    units=self.units,
                )
            )
"""

import logging
_logger = logging.getLogger(__name__)

from abc import ABC, abstractmethod
from typing import Any, Callable
import importlib

import anyio

from ..com_bus import Bus
from ..datapoint import Confidence, Datapoint


class Sensor(ABC):
    """Abstract base class for all sensor implementations.

    Subclasses must also inherit from a bus interface mixin
    (``I2CInterface`` or ``MODBUSInterface``) so that the dynamic loader
    can determine which bus to pass during initialization.

    Attributes:
        parameter: Name of the physical parameter being measured.
        bus: The communication bus instance assigned to this sensor.
        confidence: Measurement confidence/uncertainty specification.
        units: Unit string for the measured values (e.g. "°C", "%").
        time_between_reads: Interval in seconds between consecutive reads.
        db_save_function: Callable that persists Datapoint(s).
    """

    def __init__(
        self,
        parameter: str,
        bus: Bus,
        confidence: Confidence,
        units: str,
        time_between_reads: float,
        db_save_function: Callable[[Datapoint | list[Datapoint]], None],
        config_save_function: Callable | None = None
    ):
        """Initialize the sensor.

        Args:
            parameter: Name of the measured parameter (e.g. 'temperature').
            bus: Communication bus instance matching this sensor's bus_type().
            confidence: Measurement confidence interval specification.
            units: Unit of measurement (e.g. '°C', '%').
            time_between_reads: Seconds between automatic readings.
            db_save_function: Function to persist measurements to the DB.
            config_save_function: Callable for saving the passed arguments in the sensors config.
        """
        self.parameter = parameter
        self.bus = bus
        self.confidence = confidence
        self.units = units
        self.time_between_reads = time_between_reads
        self.db_save_function = db_save_function
        if config_save_function is not None:
            self.config_save_function = config_save_function

    @abstractmethod
    async def read(self):
        """Take a measurement and save it via db_save_function.

        Implementations should read from the hardware and call
        ``await self.db_save_function(datapoint)`` with a Measurement
        or list of Measurements.
        """
        pass

    async def reading_loop(self):
        """Run an infinite loop that calls read() at the configured interval.

        This method is started as a task by the Unit's sensing task group.
        Override only if non-uniform timing is needed.
        """
        _logger.debug(f"Started reading from sensor for parameter {self.parameter}")
        while True:
            await self.read()
            await anyio.sleep(self.time_between_reads)

    def get_capabilities(self):
        """Return a dict describing this sensor's capabilities.

        The default implementation returns a single entry keyed by
        ``self.parameter``. Override this method if the sensor produces
        multiple parameters (see GreenhouseAS7341 for an example).

        Returns:
            Dict mapping parameter names to capability info dicts.
        """
        return {
            self.parameter: {
                "units": self.units,
                "confidence": str(self.confidence),
                "time between reads": str(self.time_between_reads) + " seconds"
            }
        }

def init_sensor(
    module_name: str,
    class_name: str,
    parameter: str,
    busses: dict[str, Bus],
    db_save_function: Callable[[Datapoint | list[Datapoint]], None],
    config_save_function: Callable | None = None,
    sensor_kwargs: dict[Any] | None = None
) -> Sensor:
    """Dynamically load and instantiate a sensor from a submodule.

    This function imports ``plant_controller.sensors.<module_name>``,
    retrieves the class ``<class_name>`` from it, and instantiates it.
    The correct bus is selected automatically via the class's
    ``bus_type()`` static method.

    Args:
        module_name: Name of the Python module inside this package
            (e.g. 'stemma', 'sht45').
        class_name: Name of the Sensor subclass within that module.
        parameter: The physical parameter name for the sensor.
        busses: Dict mapping bus type strings to Bus instances.
        db_save_function: Callable for persisting datapoints.
        config_save_function: Callable for saving the passed arguments in the sensors config.
        sensor_kwargs: Extra keyword arguments forwarded to the sensor's
            ``__init__`` (from the config's "kwargs" field).

    Returns:
        An initialized Sensor instance ready for use.

    Raises:
        ModuleNotFoundError: If the module cannot be imported.
        AttributeError: If the class doesn't exist in the module.
    """
    if sensor_kwargs is None:
        sensor_kwargs = {}
    sensor_module = importlib.import_module(__name__ + "." + module_name)
    sensor_class = getattr(sensor_module, class_name)
    return sensor_class(
        parameter=parameter,
        bus=busses[sensor_class.bus_type()],
        db_save_function=db_save_function,
        config_save_function=config_save_function,
        **sensor_kwargs
    )
