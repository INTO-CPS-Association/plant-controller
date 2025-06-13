from datetime import datetime
import time
import automationhat
from influxdb_client import Point
from store import InfluxDBStore

from config import (
  get_relay_by_pump_id,
  get_pump_config)


def create_pump_point(pump_id: str, status: int) -> Point:
    """Create a point for the pump measurement."""
    point = Point(f"{pump_id}").field("status", status)
    return point


def water_plant(store_influx: InfluxDBStore, pump_id: str, relay, duration: int):
    """
    Activates a pump for a specified duration and logs the status to InfluxDB.

    Args:
        pump_id (str): The ID of the pump (e.g., "1", "2", "3").
        relay: The relay object to control the pump.
        duration (int): The duration in seconds to keep the pump on.
    """
    relay.on()
    print(f"{pump_id} turned on at: {datetime.now().isoformat()}")
    point = create_pump_point(pump_id=pump_id, status=1)
    store_influx.write(record=point)

    time.sleep(duration)

    relay.off()
    print(f"{pump_id} turned off at: {datetime.now().isoformat()}")
    point = create_pump_point(pump_id=pump_id, status=0)
    store_influx.write(record=point)


# Update the specific plant watering functions to use the refactored function
def water_plant_1(store_influx: InfluxDBStore):
    water_plant(
        store_influx,
        pump_id="pump_1",
        relay=automationhat.relay.one,
        duration=get_pump_config("pump_1").get("on_duration", 15)
    )


def water_plant_2(store_influx: InfluxDBStore):
    water_plant(
        store_influx,
        pump_id="pump_2",
        relay=automationhat.relay.two,
        duration=get_pump_config("pump_2").get("on_duration", 6)
    )


def water_plant_3(store_influx: InfluxDBStore):
    water_plant(
        store_influx,
        pump_id="pump_3",
        relay=automationhat.relay.three,
        duration=get_pump_config("pump_1").get("on_duration", 10)
    )
