"""Adafruit STEMMA capacitive soil moisture sensor implementation.

Reads soil moisture via an Adafruit Seesaw-based STEMMA sensor connected
through a TCA9548A I2C multiplexer. Multiple STEMMA sensors can share the
same I2C bus by using different multiplexer ports.
"""

from collections.abc import Coroutine
from typing import Any

from adafruit_seesaw.seesaw import Seesaw

from . import Sensor
from ..datapoint import Datapoint, Confidence, Measurement
from ..com_bus import BlinkaI2CBus, I2CInterface


class MultiplexedStemma(Sensor, I2CInterface):
    """Capacitive soil moisture sensor accessed via I2C multiplexer.

    Connects to an Adafruit STEMMA soil moisture sensor through a
    TCA9548A multiplexer, allowing multiple identical sensors on one bus.

    Config kwargs:
        multiplexer_address: I2C address of the TCA9548A (e.g. 0x70).
        multiplexer_port: Port number on the multiplexer (0-7).
        address: I2C address of the STEMMA sensor (e.g. 0x36).
        tbr: Time between reads in seconds.

    Attributes:
        wrapped_sensor: The Seesaw driver instance.
        time_between_reads: Interval between measurements (seconds).
        confidence: Fixed confidence specification for readings.
    """
    def __init__(
            self,
            parameter: str,
            bus: BlinkaI2CBus,
            db_save_function: Coroutine[Any, Datapoint | list[Datapoint]],
            multiplexer_address: int,
            multiplexer_port: int,
            address: int,
            tbr: int,
            **_kwargs: Any
        ):
        self.parameter = parameter
        self.wrapped_sensor = Seesaw(
            bus.ensure_multiplexer(multiplexer_address)[multiplexer_port],
            addr=address
        )
        self.db_save_function = db_save_function
        self.confidence = Confidence(interval=0.5, level=0.95)
        self.time_between_reads = tbr

    async def read(self):
        """Read moisture level and save as a percentage Measurement."""
        await self.db_save_function(
            Measurement(
                parameter=self.parameter,
                value=self.process_raw_value(
                    self.wrapped_sensor.moisture_read()
                ),
                confidence=self.confidence,
                units="%"
            )
        )
    
    def process_raw_value(self, raw_value):
        """Convert raw sensor ADC value to a percentage.

        Currently uses a simple linear mapping. Should be replaced with
        a calibrated transform for accurate volumetric water content.

        Args:
            raw_value: Raw 10-bit ADC value from the sensor (0-1023).

        Returns:
            Moisture as a percentage (0-100).
        """
        return raw_value / 1023 * 100
    
    def get_capabilities(self):
        """Return capabilities for the moisture parameter.

        Returns:
            Dict with a single entry keyed by ``self.parameter``.
        """
        return {
            self.parameter: {
                "units": "%",
                "confidence": str(self.confidence),
                "time between reads": str(self.time_between_reads) + " seconds"
             }
         }
