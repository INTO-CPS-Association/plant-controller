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


def get_pin_to_actuator_map() -> dict:
    config = get_config()
    actuator_map = {}
    actuators = config.get("actuators", {})
    for name, actuator in actuators.items():
        actuator_map[actuator.get("pin")] = name
    return actuator_map

pin_to_relay_map = {
    1: "one",
    2: "two",
    3: "three",
}

pin_to_pump_map = {
    1: "pump_one",
    2: "pump_two",
    3: "pump_three",
}
