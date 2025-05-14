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