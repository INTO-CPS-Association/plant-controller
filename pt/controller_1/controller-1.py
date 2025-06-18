from datetime import datetime
from schedule import every, repeat
import schedule

import adafruit_sht4x
import adafruit_tca9548a
from adafruit_as7341 import AS7341
from adafruit_seesaw.seesaw import Seesaw
import automationhat
import board
import os, time
from influxdb_client import Point
from typing import Sequence, Tuple, Any
import yaml

from store import InfluxDBStore

from config import (
    precision_map,
    get_config,
    get_sensor_sampling_period,
    get_moisture_sensor_port,
    get_moisture_sensor_addr,
    get_sht45_port,
    get_sht45_mode,
    get_as7341_port,
    get_actuator_shedule,
    RESTART_DELAY
)
from pump import water_plant, water_plant_1, water_plant_2, water_plant_3

store_influx = InfluxDBStore()

from comm import stompClient

def init_moisture_sensor(moisture_name: str) -> Seesaw:
    """Initialize a moisture sensor based on its name."""
    port = get_moisture_sensor_port(sensor_key=moisture_name)
    addr = get_moisture_sensor_addr(sensor_key=moisture_name)

    # Create I2C bus as normal
    i2c = board.I2C()  # uses board.SCL and board.SDA

    # Create the TCA9548A object and give it the I2C bus
    tca = adafruit_tca9548a.TCA9548A(i2c)
    try:
        # Initialize the Seesaw moisture sensor
        return Seesaw(tca[port], addr=addr)
    except ValueError as e:
        print(f"ValueError initializing {moisture_name} sensor: {e}")
        return None
    except OSError as e:
        print(f"OSError initializing {moisture_name} sensor: {e}")
        return None

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
        print(f"Error reading from moisture sensor: {e}")
        return None, None

def create_point(measurements: dict) -> Point:
    """Create a point for the measurement.
    Args:
        measurements (dict): A dictionary containing the measurement data.
        The dictionary should have a "name" key for the measurement name
        and other keys for the measurement fields.
    Returns:
        Point: An InfluxDB Point object with the measurement data.
    """
    point = Point(measurements["name"])
    for key, value in measurements.items():
        if key != "name":
            point.field(key, value)
    return point


def print_sht45_measurements(measurements: dict) -> None:
    """Print the SHT45 temperature and humidity measurements."""
    print(
        f"SHT45 --> Temperature: {measurements['temperature']:0.1f} C, Humidity: {measurements['relative_humidity']:0.1f} %"
    )


def print_as7341_measurements(measurements: dict) -> None:
    """Print the AS7341 light sensor measurements."""
    print("AS7341 light sensor: 415nm wavelength (Violet)  %s" % measurements["violet"])
    print("AS7341 light sensor: 445nm wavelength (Indigo) %s" % measurements["indigo"])
    print("AS7341 light sensor: 480nm wavelength (Blue)   %s" % measurements["blue"])
    print("AS7341 light sensor: 515nm wavelength (Cyan)   %s" % measurements["cyan"])
    print("AS7341 light sensor: 555nm wavelength (Green)   %s" % measurements["green"])
    print("AS7341 light sensor: 590nm wavelength (Yellow)  %s" % measurements["yellow"])
    print("AS7341 light sensor: 630nm wavelength (Orange)  %s" % measurements["orange"])
    print("AS7341 light sensor: 680nm wavelength (Red)     %s" % measurements["red"])


def print_soil_sensor_measurements(measurements: dict) -> None:
    """Print the soil sensor measurements."""
    moisture_str = f"{measurements['moisture']:.1f}" if measurements['moisture'] is not None else "None"
    temperature_str = f"{measurements['temperature']:.1f} C" if measurements['temperature'] is not None else "None"
    print(
        f"{measurements['name']} --> Moisture: {moisture_str}, Temperature: {temperature_str} C"
    )


def create_exception_point(e: Exception) -> Point:
    """Create a point for the exception measurement."""
    point = Point("exception").field("status", 0)
    return point


def initialise() -> Sequence[Any]:
    """Initializes the sensor objects for the TCA9548A multiplexer."""

    # Get the port for the SHT45 sensor
    port_sht45 = get_sht45_port()

    # Get the mode string for the SHT45 sensor
    mode_str_sht45 = get_sht45_mode()

    # Get the port number for the AS7341 sensor
    port_as7341 = get_as7341_port()

    # Create I2C bus as normal
    i2c = board.I2C()  # uses board.SCL and board.SDA

    # Create the TCA9548A object and give it the I2C bus
    tca = adafruit_tca9548a.TCA9548A(i2c)

    # For each sensor, create it using the TCA9548A channel instead of the I2C object
    # moisture sensor with temperature sensing capabilities
    moisture_0 = init_moisture_sensor(moisture_name="moisture_0")
    moisture_1 = init_moisture_sensor(moisture_name="moisture_1")
    moisture_2 = init_moisture_sensor(moisture_name="moisture_2")

    # SHT45 is a temperature and humidity sensor
    sht45 = adafruit_sht4x.SHT4x(tca[port_sht45])

    if mode_str_sht45 in precision_map:
        # Set the sensor mode based on the string value
        mode_value = precision_map[mode_str_sht45]
        sht45.mode = mode_value
    else:
        raise ValueError(f"Invalid mode string: {mode_str_sht45}")

    # Can also set the mode to enable heater
    # sht45.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
    print("Current mode for SHT45 is: ", adafruit_sht4x.Mode.string[sht45.mode])

    # AS7341 is a ten-channel (eight color) light sensor
    light_sensor = AS7341(tca[port_as7341])

    return moisture_0, moisture_1, moisture_2, sht45, light_sensor


def initialise_actuators() -> None:
    """Initializes the actuators."""

    # Get actuator configuration from the config file
    schedule_pump_1 = get_actuator_shedule(pump_key="pump_1")
    schedule_pump_2 = get_actuator_shedule(pump_key="pump_2")
    schedule_pump_3 = get_actuator_shedule(pump_key="pump_3")

    # Set the schedule for the actuators
    if schedule_pump_1:
        every().monday.at(schedule_pump_1).do(
            lambda: water_plant_1(store_influx=store_influx)
        )
        every().wednesday.at(schedule_pump_1).do(
            lambda: water_plant_1(store_influx=store_influx)
        )
        every().friday.at(schedule_pump_1).do(
            lambda: water_plant_1(store_influx=store_influx)
        )
    if schedule_pump_2:
        # Set the schedule for pump 2
        every().day.at(schedule_pump_2).do(
            lambda: water_plant_2(store_influx=store_influx)
        )
    if schedule_pump_3:
        # Set the schedule for pump 3
        every().monday.at(schedule_pump_3).do(
            lambda: water_plant_3(store_influx=store_influx)
        )
        every().wednesday.at(schedule_pump_3).do(
            lambda: water_plant_3(store_influx=store_influx)
        )
        every().friday.at(schedule_pump_3).do(
            lambda: water_plant_3(store_influx=store_influx)
        )


def readings(moisture_0, moisture_1, moisture_2, sht45, light_sensor):
    print(f"Sample at: {datetime.now().isoformat()}")
    temperature, relative_humidity = sht45.measurements
    # Create a dict from the measurements
    measurements = {
        "name": "sht45",
        "temperature": temperature,
        "relative_humidity": relative_humidity,
    }
    print_sht45_measurements(measurements=measurements)
    point = create_point(measurements=measurements)
    store_influx.write(record=point)

    # Create a dict from the measurements
    measurements = {
        "name": "as7341",
        "violet": light_sensor.channel_415nm,
        "indigo": light_sensor.channel_445nm,
        "blue": light_sensor.channel_480nm,
        "cyan": light_sensor.channel_515nm,
        "green": light_sensor.channel_555nm,
        "yellow": light_sensor.channel_590nm,
        "orange": light_sensor.channel_630nm,
        "red": light_sensor.channel_680nm,
    }
    print_as7341_measurements(measurements=measurements)
    point = create_point(measurements=measurements)
    store_influx.write(record=point)

    moisture_reading, temperature_reading = get_moisture_sensor_reading(moisture_0)
    # Create a dict from the measurements
    measurements = {
        "name": "soil-sensor-0",
        "moisture": moisture_reading,
        "temperature": temperature_reading,
    }
    point = create_point(measurements=measurements)
    print_soil_sensor_measurements(measurements=measurements)

    store_influx.write(record=point)

    moisture_reading, temperature_reading = get_moisture_sensor_reading(moisture_1)
    # Create a dict from the measurements
    measurements = {
        "name": "soil-sensor-1",
        "moisture": moisture_reading,
        "temperature": temperature_reading,
    }
    point = create_point(measurements=measurements)
    print_soil_sensor_measurements(measurements=measurements)

    store_influx.write(record=point)

    moisture_reading, temperature_reading = get_moisture_sensor_reading(moisture_2)
    # Create a dict from the measurements
    measurements = {
        "name": "soil-sensor-2",
        "moisture": moisture_reading,
        "temperature": temperature_reading,
    }
    point = create_point(measurements=measurements)
    print_soil_sensor_measurements(measurements=measurements)

    store_influx.write(record=point)

    print("")


if __name__ == "__main__":
    # Initialize the actuators
    initialise_actuators()
    # Initialize the sensors
    moisture_0, moisture_1, moisture_2, sht45, light_sensor = initialise()

    # reading interval
    # Set up schedule for sensors
    sampling_period = get_sensor_sampling_period()
    if sampling_period:
        pass
    else:
        raise ValueError(
            f"No sampling_period given in config file for sensors: {sampling_period}"
        )

    # Create STOMP client
    stomp_client = stompClient(
        lambda relay, duration, pump_id: water_plant(
            store_influx=store_influx, pump_id=pump_id, relay=relay, duration=duration
        )
    )

    print("init done")

    while True:
        try:
            readings(moisture_0, moisture_1, moisture_2, sht45, light_sensor)

            # time.sleep(5)
            # raise Exception("I2C device error")

        except Exception as e:
            time.sleep(RESTART_DELAY)
            moisture_0, moisture_1, moisture_2, sht45, light_sensor = initialise()
            print(f"Exception at: {datetime.now().isoformat()}")

            point = create_exception_point(e)
            store_influx.write(record=point)
            continue

        # water the plants if needed
        schedule.run_pending()
        time.sleep(sampling_period)
