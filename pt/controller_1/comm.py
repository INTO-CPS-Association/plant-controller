import stomp
from config import (
    get_stomp_url,
    get_stomp_user,
    get_stomp_password,
    get_stomp_port,
    get_stomp_actuator_ids,
)
from pump import pump_water
import time


class stompClient(stomp.ConnectionListener):
    def __init__(self, func):
        self._func = func
        self._url = get_stomp_url()
        self._user = get_stomp_user()
        self._password = get_stomp_password()
        self._port = get_stomp_port()
        self._ids = get_stomp_actuator_ids()
        self.heartbeats = (
            15000,
            15000,
        )  # Heartbeat interval in milliseconds (from client to server, from server to client)
        self.conn = stomp.Connection(
            [(self._url, self._port)], heartbeats=self.heartbeats
        )
        self.conn.set_listener("", self)
        self.conn.start()
        self.conn.connect(self._user, self._password, wait=True)

    def on_connected(self, frame):
        print("Connected: %s" % frame.body)
        for index, id in enumerate(self._ids):
            queue_destination = f"actuator.{str(id)}.water"
            try:
                self.conn.subscribe(destination=queue_destination, id=index, ack="auto")
                print(f"Subscribed to {queue_destination} with id {index}")
            except Exception as e:
                print(f"Error subscribing to {queue_destination}: {e}")
                continue

    def on_error(self, frame):
        print("Error: %s" % frame)

    def on_message(self, frame):
        print("STOMP Command Message: %s" % frame.body)
        # We need to command [WATER]<pump_pin> <duration>
        command = frame.body.split("[WATER]")[1]
        command_list = command.split(" ")

        if command_list[0] == "water":
            self._func(int(command_list[1]), int(command_list[2]))
        else:  # pin, duration
            self._func(int(command_list[1]), int(command_list[0]))

    def send_message(self, destination, message):
        self.conn.send(destination=destination, body=message)

    def disconnect(self):
        self.conn.disconnect()
