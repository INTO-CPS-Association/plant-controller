import adafruit_sht4x
import adafruit_tca9548a
from adafruit_as7341 import AS7341

from config import (
    precision_map,
    get_sht45_port,
    get_sht45_mode,
    get_as7341_port,
)


def init_sht45(tca: adafruit_tca9548a.TCA9548A) -> adafruit_sht4x.SHT4x:
    """Initialize the SHT45 temperature and humidity sensor."""

    # Get the port for the SHT45 sensor
    port_sht45 = get_sht45_port()

    # Get the mode string for the SHT45 sensor
    mode_str_sht45 = get_sht45_mode()

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

    return sht45


def init_as7341(tca: adafruit_tca9548a.TCA9548A) -> AS7341:
    """Initialize the AS7341 light sensor."""

    # Get the port number for the AS7341 sensor
    port_as7341 = get_as7341_port()

    return AS7341(tca[port_as7341])


def get_sht45_reading(sht45: adafruit_sht4x.SHT4x) -> dict:
    """Get the temperature and humidity readings from the SHT45 sensor."""
    try:
        temperature, relative_humidity = sht45.measurements
        return {
            "name": "sht45",
            "temperature": temperature,
            "relative_humidity": relative_humidity,
        }
    except OSError as e:
        print(f"Error reading from SHT45 sensor: {e}")
        return {"name": "sht45", "temperature": None, "relative_humidity": None}


def get_as7341_reading(light_sensor: AS7341) -> dict:
    """Get the light sensor readings from the AS7341 sensor."""
    try:
        # Read the light sensor values
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
        return measurements
    except OSError as e:
        print(f"Error reading from AS7341 sensor: {e}")
        return {
            "name": "as7341",
            "violet": None,
            "indigo": None,
            "blue": None,
            "cyan": None,
            "green": None,
            "yellow": None,
            "orange": None,
            "red": None,
        }


def print_sht45_measurements(measurements: dict) -> None:
    """Print the SHT45 temperature and humidity measurements."""
    temperature_str = (
        f"{measurements['temperature']:.1f}"
        if measurements["temperature"] is not None
        else "None"
    )
    humidity_str = (
        f"{measurements['relative_humidity']:.1f}"
        if measurements["relative_humidity"] is not None
        else "None"
    )
    print(f"SHT45 --> Temperature: {temperature_str} C, Humidity: {humidity_str} %")


def print_as7341_measurements(measurements: dict) -> None:
    """Print the AS7341 light sensor measurements."""
    violet_str = (
        f"{measurements['violet']:.1f}"
        if measurements["violet"] is not None
        else "None"
    )
    indigo_str = (
        f"{measurements['indigo']:.1f}"
        if measurements["indigo"] is not None
        else "None"
    )
    blue_str = (
        f"{measurements['blue']:.1f}" if measurements["blue"] is not None else "None"
    )
    cyan_str = (
        f"{measurements['cyan']:.1f}" if measurements["cyan"] is not None else "None"
    )
    green_str = (
        f"{measurements['green']:.1f}" if measurements["green"] is not None else "None"
    )
    yellow_str = (
        f"{measurements['yellow']:.1f}"
        if measurements["yellow"] is not None
        else "None"
    )
    orange_str = (
        f"{measurements['orange']:.1f}"
        if measurements["orange"] is not None
        else "None"
    )
    red_str = (
        f"{measurements['red']:.1f}" if measurements["red"] is not None else "None"
    )

    print("AS7341 light sensor: 415nm wavelength (Violet)  %s" % violet_str)
    print("AS7341 light sensor: 445nm wavelength (Indigo) %s" % indigo_str)
    print("AS7341 light sensor: 480nm wavelength (Blue)   %s" % blue_str)
    print("AS7341 light sensor: 515nm wavelength (Cyan)   %s" % cyan_str)
    print("AS7341 light sensor: 555nm wavelength (Green)   %s" % green_str)
    print("AS7341 light sensor: 590nm wavelength (Yellow)  %s" % yellow_str)
    print("AS7341 light sensor: 630nm wavelength (Orange)  %s" % orange_str)
    print("AS7341 light sensor: 680nm wavelength (Red)     %s" % red_str)
