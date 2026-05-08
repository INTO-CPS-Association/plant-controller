"""Pump control modules for the plant watering system.

This package defines the abstract base class for pump implementations and
provides concrete implementations for supported hardware.

Included implementations:
    - ``ad20p_1230e.CS_IO404_Based_AD20P_1230E``: AD20P-1230E pump
      controlled via a CS-IO404 Modbus relay module.

Writing a custom pump module:
    1. Create a new ``.py`` file in this package (e.g. ``my_pump.py``).
    2. Define a class that inherits from ``Pump`` and a bus interface mixin
       from ``plant_controller.com_bus`` (``I2CInterface`` or
       ``MODBUSInterface``).
    3. Implement the ``pumping_callback`` method to activate the pump for
       the calculated duration and then record the event via
       ``self.db_save_function``.
    4. The pump is instantiated by the Plant class. To use a custom pump,
       modify the Plant initialization or extend the config parsing.

Calibration:
    Pumps convert a dosage in milliliters to a pumping duration using
    linear calibration parameters (slope and offset). The relationship is::

        time_seconds = slope * dosage_ml + offset

    The ``calibration_parameters`` dict must contain 'slope' and 'offset'
    keys. Use the setup utility's calibration procedure to determine these.

Example minimal pump::

    from plant_controller.pumps import Pump
    from plant_controller.com_bus import MODBUSInterface, MODBUS
    from plant_controller.datapoint import WateringEvent

    class MyPump(Pump, MODBUSInterface):
        def __init__(self, bus, db_save_function, calibration_parameters,
                     **kwargs):
            super().__init__(bus, db_save_function, calibration_parameters)
            # ... hardware-specific setup ...

        async def pumping_callback(self, dosage: int):
            pump_time = self.calibration_parameters["slope"] * dosage \\
                        + self.calibration_parameters["offset"]
            # ... activate pump for pump_time seconds ...
            await self.db_save_function(WateringEvent(dosage=dosage))
"""

from abc import ABC, abstractmethod
from typing import Any, Callable

from ..com_bus import Bus
from ..datapoint import Datapoint


class Pump(ABC):
    """Abstract base class for all pump implementations.

    Subclasses must also inherit from a bus interface mixin
    (``I2CInterface`` or ``MODBUSInterface``) so that the controller
    can determine which bus to pass during initialization.

    Attributes:
        bus: The communication bus instance for hardware control.
        db_save_function: Callable to persist WateringEvent datapoints.
        calibration_parameters: Dict containing at minimum 'slope' (sec/ml)
            and 'offset' (sec) for dosage-to-time conversion.
    """

    def __init__(
        self,
        bus: Bus,
        db_save_function: Callable[[Datapoint | list[Datapoint]], None],
        calibration_parameters: dict[str, Any]
    ):
        """Initialize the pump.

        Args:
            bus: Communication bus instance (I2C or MODBUS).
            db_save_function: Function to save watering events to DB.
            calibration_parameters: Dict with 'slope' (sec/ml) and 'offset'
                (sec) for the linear dosage-to-time model.
        """
        self.bus = bus
        self.db_save_function = db_save_function
        self.calibration_parameters = calibration_parameters

    @abstractmethod
    async def pumping_callback(self, dosage: int):
        """Activate the pump to deliver the specified dosage.

        This method is called by the pump schedule and must block (await)
        until pumping is complete to ensure accurate dosage delivery.
        After pumping, implementations should record the event via
        ``await self.db_save_function(WateringEvent(dosage=dosage))``.

        Args:
            dosage: Amount to pump in milliliters.
        """
        pass
