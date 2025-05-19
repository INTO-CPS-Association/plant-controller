import automationhat
import time

from config import pin_to_relay_map, pin_to_pump_map
from datetime import datetime


def pump_water(sec: int, pump_pin: int):
    """
    Pump water for a given number of seconds.
    :param sec: Number of seconds to pump water
    :param relay_name: Name of the relay to use
    """
    print("Pumping water for {} seconds...".format(sec))
    # Get the relay object from the relay name
    relay_str = pin_to_relay_map[pump_pin]
    relay = getattr(automationhat.relay, relay_str)

    pump_id = pin_to_pump_map[pump_pin]

    relay.on()
    print(f"{pump_id} turned on at: {datetime.now().isoformat()}")

    time.sleep(sec)

    relay.off()
    print(f"{pump_id} turned off at: {datetime.now().isoformat()}")

    