"""SHT45 temperature and humidity sensor implementation.

Measures air temperature (°C) and relative humidity (%) using the
Sensirion SHT45 sensor. Confidence intervals are condition-dependent
for humidity.
"""

from typing import Any, Callable

import adafruit_sht4x

from . import Sensor
from ..datapoint import Datapoint, Confidence, Measurement
from ..com_bus import BlinkaI2CBus, I2CInterface


class GreenhouseSHT45(Sensor, I2CInterface):
    """SHT45 temperature and humidity sensor for greenhouse monitoring.

    Reports two parameters: 'temperature' (°C) and 'humidity' (%).
    Uses high-precision mode with no heater. Humidity confidence varies
    with operating conditions per the datasheet specifications.

    This sensor does not use the standard Sensor.__init__ because it
    reports multiple parameters from a single physical device.

    Attributes:
        wrapped_sensor: The adafruit_sht4x.SHT4x driver instance.
        time_between_reads: Interval between measurements (seconds).
        temperature_confidence: Fixed confidence for temperature readings.
    """
    def __init__(
        self,
        parameter: str,
        bus: BlinkaI2CBus,
        db_save_function: Callable[[Datapoint | list[Datapoint]], None],
        **kwargs: Any
    ):
        self.parameter = parameter
        self.wrapped_sensor = adafruit_sht4x.SHT4x(bus.wrapped_bus)
        self.wrapped_sensor.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
        self.db_save_function = db_save_function
        self.time_between_reads=15
        self.temperature_confidence = Confidence(interval=0.2, level=0.95)

    @staticmethod
    def humidity_confidence(temperature, humidity):
        """Compute condition-dependent confidence interval for humidity.

        The SHT45 datasheet specifies wider tolerances at extreme
        temperature or humidity values.

        Args:
            temperature: Current temperature reading in °C.
            humidity: Current humidity reading in %.

        Returns:
            A Confidence instance with the appropriate interval.
        """
        if humidity > 95:
            return Confidence(interval=1.75, level=0.95)
        elif humidity > 75 or humidity < 15 or temperature > 55 or temperature < 15:
            return Confidence(interval=1.5, level=0.95)
        else:
            return Confidence(interval=1, level=0.95)

    async def read(self):
        """Read temperature and humidity, saving both as Measurements."""
        temperature, humidity = self.wrapped_sensor.measurements
        self.db_save_function(
            [
                Measurement(
                    parameter=self.parameter + ".temperature",
                    value=temperature,
                    confidence=self.temperature_confidence,
                    units="°C"
                ),
                Measurement(
                    parameter=self.parameter + ".humidity",
                    value=humidity,
                    confidence=GreenhouseSHT45.humidity_confidence(temperature, humidity),
                    units="%"
                )
            ]
        )

    def get_capabilities(self):
        """Return capabilities for temperature and humidity parameters."""
        return {
            self.parameter + ".temperature": {
                "units": "°C",
                "confidence": str(self.temperature_confidence),
                "time between reads": str(self.time_between_reads) + " seconds"
            },
            self.parameter + ".humidity": {
                "units": "%",
                "confidence": "Varies based on temperature and humidity",
                "time between reads": str(self.time_between_reads) + " seconds"
            }
        }
