import adafruit_sht4x
import yaml

precision_map = {
    "NOHEAT_HIGHPRECISION": adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION,
    "NOHEAT_MEDPRECISION": adafruit_sht4x.Mode.NOHEAT_MEDPRECISION,
    "NOHEAT_LOWPRECISION": adafruit_sht4x.Mode.NOHEAT_LOWPRECISION,
    "HIGHHEAT_1S": adafruit_sht4x.Mode.HIGHHEAT_1S,
    "HIGHHEAT_100MS": adafruit_sht4x.Mode.HIGHHEAT_100MS,
    "MEDHEAT_1S": adafruit_sht4x.Mode.MEDHEAT_1S,
    "MEDHEAT_100MS": adafruit_sht4x.Mode.MEDHEAT_100MS,
    "LOWHEAT_1S": adafruit_sht4x.Mode.LOWHEAT_1S,
    "LOWHEAT_100MS": adafruit_sht4x.Mode.LOWHEAT_100MS
}

def get_config() -> dict:
        with open("config/config.yaml", "r") as file:
            data = yaml.safe_load(file)
        return data

def get_sensor_sampling_period() -> int:
    config = get_config()
    return config["plant"]["sensors"]["sampling_period"]

def get_actuator_shedule(pump_key: str) -> dict:
    config = get_config()
    actuators = config["plant"]["actuators"]
    return actuators[pump_key]["schedule"]

def get_moisture_sensor_port(sensor_key: str) -> int:
    """
    Returns the port number for a given moisture sensor key (e.g., 'moisture_0').
    """
    config = get_config()
    seesaw = config["plant"]["sensors"]["seesaw"]
    return seesaw[sensor_key]["port"]

def get_moisture_sensor_addr(sensor_key: str) -> int:
    """
    Returns the I2C address for a given moisture sensor key (e.g., 'moisture_0').
    """
    config = get_config()
    seesaw = config["plant"]["sensors"]["seesaw"]
    return seesaw[sensor_key]["addr"]

def get_sht45_port() -> int:
    """
    Returns the port number for the SHT45 sensor.
    """
    config = get_config()
    return config["plant"]["sht45"]["port"]

def get_sht45_mode() -> str:
    """
    Returns the mode string for the SHT45 sensor.
    """
    config = get_config()
    return config["plant"]["sht45"]["mode"]

def get_as7341_port() -> int:
    """
    Returns the port number for the AS7341 sensor.
    """
    config = get_config()
    return config["plant"]["as7341"]["port"]

def get_stomp_url() -> str:
    config = get_config()
    return config["services"]["external"]["stomp"]["url"]

def get_stomp_user() -> str:
    config = get_config()
    return config["services"]["external"]["stomp"]["user"]

def get_stomp_password() -> str:
    config = get_config()
    return config["services"]["external"]["stomp"]["pass"]

def get_stomp_port() -> int:
    config = get_config()
    return config["services"]["external"]["stomp"]["port"]

def get_stomp_actuator_ids() -> list:
    config = get_config()
    return config["services"]["external"]["stomp"]["actuator_ids"]

def get_pump_id_by_pin(pin_number: int) -> str:
    """
    Returns the pump_id (e.g., 'pump_1') for a given pin number.
    """
    config = get_config()
    actuators = config["plant"]["actuators"]
    for pump_id, actuator in actuators.items():
        if actuator.get("pin") == pin_number:
            return pump_id
    raise ValueError(f"No pump_id found for pin number: {pin_number}")

def get_pin_to_actuator_map() -> dict:
    config = get_config()
    actuator_map = {}
    actuators = config.get("actuators", {})
    for name, actuator in actuators.items():
        actuator_map[actuator.get("pin")] = name
    return actuator_map

pump_id_to_relay_map = {
    "pump_1": "one",
    "pump_2": "two",
    "pump_3": "three",
}
