from adafruit_seesaw.seesaw import Seesaw
import adafruit_tca9548a
from typing import Tuple

from config import (
    get_moisture_sensor_port,
    get_moisture_sensor_addr,
    get_moisture_sensors,
)


def init_moisture_sensors(tca: adafruit_tca9548a.TCA9548A) -> dict:
    """Initialize a moisture sensor based on its name."""

    # empty moisture sensors dict with name as key and Seesaw object as value
    moisture_sensors_dict = {}

    moisture_sensors = get_moisture_sensors()
    for moisture_name, moisture_value in moisture_sensors.items():
        addr = moisture_value["addr"]
        port = moisture_value["port"]
        try:
            # Initialize the Seesaw moisture sensor
            moisture_sensors_dict[moisture_name] = Seesaw(tca[port], addr=addr)
        except ValueError as e:
            print(f"[ValueError] initializing {moisture_name} sensor: {e}")
            moisture_sensors_dict[moisture_name] = None
        except OSError as e:
            print(f"[OSError] initializing {moisture_name} sensor: {e}")
            moisture_sensors_dict[moisture_name] = None
    
    return moisture_sensors_dict


def get_moisture_sensor_reading(moisture_sensor: Seesaw) -> Tuple[float, float]:
    """Get the moisture and temperature readings from a Seesaw moisture sensor."""
    if moisture_sensor is None:
        return None, None

    try:
        # Read the moisture level
        moisture = moisture_sensor.moisture_read()
        # Read the temperature
        temperature = moisture_sensor.get_temp()
        return moisture, temperature
    except OSError as e:
        print(f"[OSError] reading from moisture sensor: {e}")
        return None, None


def print_soil_sensor_measurements(measurements: dict) -> None:
    """Print the soil sensor measurements."""
    moisture_str = (
        f"{measurements['moisture']:.1f}"
        if measurements["moisture"] is not None
        else "None"
    )
    temperature_str = (
        f"{measurements['temperature']:.1f} C"
        if measurements["temperature"] is not None
        else "None"
    )
    print(
        f"{measurements['name']} --> Moisture: {moisture_str}, Temperature: {temperature_str} C"
    )
