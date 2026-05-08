"""AS7341 10-channel spectral light sensor implementation.

Measures photon flux across 9 spectral bands (415nm to 910nm) using
the AMS AS7341 sensor IC. Readings are converted from raw photon counts
to flux (photons/s) using the configured integration time.
"""

from typing import Any, Callable

import adafruit_as7341

from . import Sensor
from ..datapoint import Datapoint, Confidence, Measurement
from ..com_bus import BlinkaI2CBus, I2CInterface


class LightConfidence(Confidence):
    """Confidence specification for spectral light measurements.

    Instead of a simple +/- interval, spectral sensors have channel-specific
    uncertainty expressed as center wavelength variance and full width at
    half maximum (FWHM).

    Attributes:
        center_wavelength_variance: Uncertainty in peak wavelength (nm).
        full_width_half_maximum: Channel bandwidth at half sensitivity (nm).
    """
    def __init__(
        self,
        center_wavelenght_variance: int,
        full_width_half_maximum: int
    ):
        self.center_wavelength_variance = center_wavelenght_variance
        self.full_width_half_maximum = full_width_half_maximum

    def str_representation(self) -> str:
        return f"Center wavelength ±{self.center_wavelength_variance}nm, FWHM ±{self.full_width_half_maximum}nm"


class GreenhouseAS7341(Sensor, I2CInterface):
    """AS7341 spectral light sensor for greenhouse-level measurements.

    Reads 9 spectral channels (415nm through 910nm NIR) and reports
    photon flux in photons/s. Uses 64x gain by default.

    This sensor does not use the standard Sensor.__init__ because it
    reports multiple parameters from a single physical device.

    Attributes:
        wrapped_sensor: The adafruit_as7341.AS7341 driver instance.
        time_between_reads: Interval between measurement cycles (seconds).
        integration_time: Computed integration time per reading (seconds).
    """
    def __init__(
        self,
        parameter: str,
        bus: BlinkaI2CBus,
        db_save_function: Callable[[Datapoint | list[Datapoint]], None],
        **kwargs: Any
    ):
        self.parameter = parameter
        self.wrapped_sensor = adafruit_as7341.AS7341(bus.wrapped_bus)
        self.wrapped_sensor.gain = adafruit_as7341.Gain.GAIN_64X
        self.db_save_function = db_save_function
        self.time_between_reads = 15
        self.integration_time = (
            (self.wrapped_sensor.atime + 1)
            * (self.wrapped_sensor.astep + 1)
            * 2.78e-6
        )

    def photon_count_to_flux(self, count):
        """Convert a raw photon count to flux (photons/s).

        Args:
            count: Raw channel count from the sensor.

        Returns:
            Photon flux in photons per second.
        """
        return count / self.integration_time

    async def read(self):
        """Read all 9 spectral channels and save as Measurements."""
        self.db_save_function(
            [
                Measurement(
                    parameter=self.parameter + "_415nm",
                    value=self.photon_count_to_flux(
                        self.wrapped_sensor.channel_415nm
                    ),
                    confidence=LightConfidence(
                        center_wavelenght_variance=10,
                        full_width_half_maximum=26
                    ),
                    units="photons/s"
                ),
                Measurement(
                    parameter=self.parameter + "_445nm",
                    value=self.photon_count_to_flux(
                        self.wrapped_sensor.channel_445nm
                    ),
                    confidence=LightConfidence(
                        center_wavelenght_variance=10,
                        full_width_half_maximum=30
                    ),
                    units="photons/s"
                ),
                Measurement(
                    parameter=self.parameter + "_480nm",
                    value=self.photon_count_to_flux(
                        self.wrapped_sensor.channel_480nm
                    ),
                    confidence=LightConfidence(
                        center_wavelenght_variance=10,
                        full_width_half_maximum=36
                    ),
                    units="photons/s"
                ),
                Measurement(
                    parameter=self.parameter + "_515nm",
                    value=self.photon_count_to_flux(
                        self.wrapped_sensor.channel_515nm
                    ),
                    confidence=LightConfidence(
                        center_wavelenght_variance=10,
                        full_width_half_maximum=39
                    ),
                    units="photons/s"
                ),
                Measurement(
                    parameter=self.parameter + "_555nm",
                    value=self.photon_count_to_flux(
                        self.wrapped_sensor.channel_555nm
                    ),
                    confidence=LightConfidence(
                        center_wavelenght_variance=10,
                        full_width_half_maximum=39
                    ),
                    units="photons/s"
                ),
                Measurement(
                    parameter=self.parameter + "_590nm",
                    value=self.photon_count_to_flux(
                        self.wrapped_sensor.channel_590nm
                    ),
                    confidence=LightConfidence(
                        center_wavelenght_variance=10,
                        full_width_half_maximum=40
                    ),
                    units="photons/s"
                ),
                Measurement(
                    parameter=self.parameter + "_630nm",
                    value=self.photon_count_to_flux(
                        self.wrapped_sensor.channel_630nm
                    ),
                    confidence=LightConfidence(
                        center_wavelenght_variance=10,
                        full_width_half_maximum=50
                    ),
                    units="photons/s"
                ),
                Measurement(
                    parameter=self.parameter + "_680nm",
                    value=self.photon_count_to_flux(
                        self.wrapped_sensor.channel_680nm
                    ),
                    confidence=LightConfidence(
                        center_wavelenght_variance=10,
                        full_width_half_maximum=52
                    ),
                    units="photons/s"
                ),
                Measurement(
                    parameter=self.parameter + "_infrared_910nm",
                    value=self.photon_count_to_flux(
                        self.wrapped_sensor.channel_nir
                    ),
                    units="photons/s"
                )
            ]
        )

    def get_capabilities(self):
        """Return capabilities for all 9 spectral channels."""
        return {
            self.parameter + "_415nm": {
                "units": "photons/s",
                "time between reads": str(self.time_between_reads) + " seconds",
                "integration time": str(self.integration_time) + " seconds"
            },
            self.parameter + "_445nm": {
                "units": "photons/s",
                "time between reads": str(self.time_between_reads) + " seconds",
                "integration time": str(self.integration_time) + " seconds"
            },
            self.parameter + "_480nm": {
                "units": "photons/s",
                "time between reads": str(self.time_between_reads) + " seconds",
                "integration time": str(self.integration_time) + " seconds"
            },
            self.parameter + "_515nm": {
                "units": "photons/s",
                "time between reads": str(self.time_between_reads) + " seconds",
                "integration time": str(self.integration_time) + " seconds"
            },
            self.parameter + "_555nm": {
                "units": "photons/s",
                "time between reads": str(self.time_between_reads) + " seconds",
                "integration time": str(self.integration_time) + " seconds"
            },
            self.parameter + "_590nm": {
                "units": "photons/s",
                "time between reads": str(self.time_between_reads) + " seconds",
                "integration time": str(self.integration_time) + " seconds"
            },
            self.parameter + "_630nm": {
                "units": "photons/s",
                "time between reads": str(self.time_between_reads) + " seconds",
                "integration time": str(self.integration_time) + " seconds"
            },
            self.parameter + "_680nm": {
                "units": "photons/s",
                "time between reads": str(self.time_between_reads) + " seconds",
                "integration time": str(self.integration_time) + " seconds"
            },
            self.parameter + "_infrared_910nm": {
                "units": "photons/s",
                "time between reads": str(self.time_between_reads) + " seconds",
                "integration time": str(self.integration_time) + " seconds"
            }
        }