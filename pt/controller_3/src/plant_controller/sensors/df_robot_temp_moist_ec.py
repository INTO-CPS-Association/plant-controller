"""DFRobot RS485 soil temperature, humidity, and EC sensor implementation.

Reads soil moisture (%RH), temperature (°C), and electrical conductivity
(μS/cm) from a DFRobot RS485/MODBUS soil sensor. Communication uses MODBUS
RTU holding registers.

Each physical sensor has a configurable MODBUS device ID (2–253). Sensors
ship with a default ID of 1, which should be changed before deployment to
avoid address collisions. The ``change_id`` setup action handles this.

Config kwargs:
    device_id: MODBUS device ID of the sensor (2–253 recommended).
    tbr: Time between reads in seconds.
"""

import logging
_logger = logging.getLogger(__name__)

from typing import Any, Callable

import anyio

from . import Sensor
from ..datapoint import Datapoint, Measurement
from ..cli_helpers import clear_screen
from ..com_bus import MODBUS, MODBUSInterface
from ..setup_actions import HasSetupFunctionsMixin

_DEFAULT_DF_HUM_TEMP_EC_ID=1
_DF_HUM_TEMP_EC_MOISTURE_ADDRESS=0x0000
_DF_HUM_TEMP_EC_TEMPERATURE_ADDRESS=0x0001
_DF_HUM_TEMP_EC_CONDUCTIVITY_ADDRESS=0x0002
_DF_HUM_TEMP_EC_ID_ADDRESS=0x07D0

class DFRobotRS485SoilTemperatureHumidityECSensor(Sensor, MODBUSInterface, HasSetupFunctionsMixin):
    """DFRobot RS485 soil sensor measuring moisture, temperature, and EC.

    Communicates over MODBUS RTU, reading three holding registers per
    measurement cycle. Reports three sub-parameters named
    ``<parameter>.moisture``, ``<parameter>.temperature``, and
    ``<parameter>.electrical_conductivity``.

    This sensor includes a setup action (``change_device_id``) for
    reassigning the sensor's MODBUS address, which is necessary before
    deploying multiple sensors on the same bus.

    Attributes:
        parameter: Base parameter name (sub-parameters are derived from it).
        bus: The MODBUS bus instance used for communication.
        db_save_function: Async callable for persisting measurements.
        config_save_function: Callable for saving config changes to disk.
        device_id: MODBUS device address of this sensor.
        time_between_reads: Interval between measurement cycles (seconds).
    """

    def __init__(
        self,
        parameter: str,
        bus: MODBUS,
        db_save_function: Callable[[Datapoint | list[Datapoint]], None],
        config_save_function: Callable,
        device_id: int,
        tbr: int,
        **_kwargs: Any
    ):
        """Initialize the DFRobot soil sensor.

        Args:
            parameter: Base name for the measured parameters (e.g. 'soil').
            bus: MODBUS bus instance for register reads/writes.
            db_save_function: Async function to persist measurements to the DB.
            config_save_function: Callable for saving config changes (e.g.
                updated device_id) back to the plant's JSON config file.
            device_id: MODBUS device address (2–253 recommended; 1 is the
                factory default and triggers a warning).
            tbr: Time between reads in seconds.
            **_kwargs: Ignored; allows forward-compatible config expansion.
        """
        self.parameter = parameter
        self.bus = bus
        self.db_save_function = db_save_function
        self.config_save_function = config_save_function
        self.device_id = device_id
        self.time_between_reads = tbr
        if self.device_id == _DEFAULT_DF_HUM_TEMP_EC_ID:
            _logger.warning(f"DF Robot RS485 Soil Temperature Humidity EC Sensor, parameter '{self.parameter}' is configured with default device id {_DEFAULT_DF_HUM_TEMP_EC_ID}. This should be changed to an other non default value (2-253) in setup before running the controller.")
    
    async def read(self):
        """Read moisture, temperature, and EC registers and save as Measurements.

        The blocking MODBUS register reads are offloaded to a worker thread
        to avoid stalling the async event loop.
        """
        def _blocking_read():
            _logger.debug(f"Fetching readings from sensor [{self.parameter}]")
            try:
                return [
                    Measurement(
                        parameter=f"{self.parameter}_moisture",
                        value=self.bus.convert_from_registers(
                            registers=self.bus.read_holding_registers(
                                address=_DF_HUM_TEMP_EC_MOISTURE_ADDRESS,
                                device_id=self.device_id
                            ).registers,
                            data_type=self.bus.DATATYPE.UINT16
                        ) / 10,
                        units="%RH"
                    ),
                    Measurement(
                        parameter=f"{self.parameter}_temperature",
                        value=self.bus.convert_from_registers(
                            registers=self.bus.read_holding_registers(
                                address=_DF_HUM_TEMP_EC_TEMPERATURE_ADDRESS,
                                device_id=self.device_id
                            ).registers,
                            data_type=self.bus.DATATYPE.INT16
                        ) / 10,
                        units="°C"
                    ),
                    Measurement(
                        parameter=f"{self.parameter}_electrical_conductivity",
                        value=self.bus.convert_from_registers(
                            registers=self.bus.read_holding_registers(
                                address=_DF_HUM_TEMP_EC_CONDUCTIVITY_ADDRESS,
                                device_id=self.device_id
                            ).registers,
                            data_type=self.bus.DATATYPE.UINT16
                        ),
                        units="μS/cm"
                    )
                ]
            except Exception as e:
                _logger.error(f"Failed to fetch sensor values for parameter [{self.parameter}]: {e}")
                raise e
        _logger.debug(f"Starting blocking sensing for parameter [{self.parameter}] in seperate thread.")
        measurements = await anyio.to_thread.run_sync(_blocking_read)
        _logger.debug(f"Saving for parameter [{self.parameter}] in database the measurements {measurements}")
        self.db_save_function(measurements)

    def get_capabilities(self):
        """Return capabilities for the three sub-parameters.

        Returns:
            Dict with entries for ``<parameter>.moisture``,
            ``<parameter>.temperature``, and
            ``<parameter>.electrical_conductivity``.
        """
        return {
            f"{self.parameter}_moisture": {
                "units": "%RH (Relative Humidity)",
                "time between reads": str(self.time_between_reads) + " seconds"
            },
            f"{self.parameter}_temperature": {
                "units": "°C",
                "time between reads": str(self.time_between_reads) + " seconds"
            },
            f"{self.parameter}_electrical_conductivity": {
                "units": "μS/cm",
                "time between reads": str(self.time_between_reads) + " seconds"
            }
        }
    
    async def change_id(self):
        """Interactive procedure to change the sensor's MODBUS device ID.

        Guides the user through safely reassigning the sensor's address on
        the MODBUS bus. Validates that the new ID is in the range 2–253 and
        writes it to the sensor's ID register. On success, updates the
        in-memory device_id and persists the change via config_save_function.
        """
        clear_screen()
        print(f"Ensure that no other MODBUS device with id {self.device_id} is connected to the controller before proceding.")
        if self.device_id == _DEFAULT_DF_HUM_TEMP_EC_ID:
            print("WARNING: This sensor has device id 1. This is the default id for this sensor type, and generally the default value for unconfigured MODBUS devices.")
            print("It is recommended that all other MODBUS devices are disconnected from the Controller before proceding.")
        print("If any other connected MODBUS device has this id, please cancel this command, turn off the Controller, unplug that device, restart the Controller and then rerun this command.")
        print("")
        print(f"Are you certain that no other connected device has device id {self.device_id}")
        print("[y/N]")
        if input() not in ["y" , "Y" , "yes" , "Yes" , "YES"]:
            clear_screen()
            print("Aborting command")
            print("")
            return
        
        clear_screen()
        while True:
            print("Please input new device id (valid values are integers from 2 to 253 inclusive):")
            response = input()
            clear_screen()
            match response:
                case 'stop' | 'cancel' | 'quit':
                    print("Command aborted.")
                    return
            try:
                response = int(response)
                if response < 2:
                    print("The id cannot be less than 2.")
                elif response > 253:
                    print("The id cannot be higher than 253")
                else:
                    break
                    
            except Exception:
                print(f"The given input '{response}' wasn't a whole number!")
        try:
            self.bus.write_register(
                address=_DF_HUM_TEMP_EC_ID_ADDRESS,
                value=response,
                device_id=self.device_id
            )
        except Exception as e:
            print(f"FAILED TO WRITE NEW ID [{response}]: {e}")
            print("Aborting command!")
            return

        self.device_id = response
        self.config_save_function(device_id=response)
        print(f"The sensor was updated with the new id '{response}'.")
        print("")
        return

    def setup_functions(self) -> dict[str, dict[str, Any]]:
        """Return available setup actions for this sensor.

        Returns:
            Dict with a ``change_device_id`` entry for reassigning the
            sensor's MODBUS address.
        """
        return {
            "change_device_id": {
                "description": "Change the MODBUS device id of the sensor.",
                "function": self.change_id
            }
        }
        