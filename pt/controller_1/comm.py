import stomp
from config import get_config, get_pin_to_actuator_map
from pump import pump_water
import time

class stompClient(stomp.ConnectionListener):
    def __init__(self, func):
        self._func = func
        config = get_config()
        config = config["services"]["external"]["stomp"]
        self._url = config["url"]
        self._user = config["user"]
        self._password = config["pass"]
        self._port = config["port"]
        self._ids = config["actuator_ids"]
        self.conn = stomp.Connection([(self._url, self._port)])
        self.conn.set_listener('', self)
        self.conn.start()
        self.conn.connect(wait=True)

    def on_connected(self, headers, message):
        print('Connected: %s' % message)
        for id in self._ids:
            queue_destination = f"actuator.{str(id)}.water"
            try:
                self.conn.subscribe(destination=queue_destination, id=1, ack='auto')
                print(f"Subscribed to {queue_destination}")
            except Exception as e:
                print(f"Error subscribing to {queue_destination}: {e}")
                continue

    def on_error(self, headers, message):
        print('Error: %s' % message)

    def on_message(self, headers, message):
        print('Message: %s' % message)
        # We need to command <pump> <time>
        command = message.split("[WATER]")[1]
        command_list = command.split(" ")
        
        if command_list[0] == "water":
            self._func(int(command_list[1]), int(command_list[2]))
        else:
            self._func(int(command_list[0]), int(command_list[1]))

    def send_message(self, destination, message):
        self.conn.send(destination=destination, body=message)

    def disconnect(self):
        self.conn.disconnect()