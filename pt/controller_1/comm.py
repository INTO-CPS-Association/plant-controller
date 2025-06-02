import stomp
import automationhat
from config import (
    get_stomp_url,
    get_stomp_user,
    get_stomp_password,
    get_stomp_port,
    get_STOMP_destination_topics,
    get_pump_id_by_topic,
    get_relay_by_pump_id,
)

HEARTBEAT_CLIENT = 0  # Heartbeat interval from client to server in milliseconds
HEARTBEAT_SERVER = 0  # Heartbeat interval from server to client in milliseconds


class stompClient(stomp.ConnectionListener):
    def __init__(self, func):
        self._func = func
        self._url = get_stomp_url()
        self._user = get_stomp_user()
        self._password = get_stomp_password()
        self._port = get_stomp_port()
        self._topics = get_STOMP_destination_topics()
        self.heartbeats = (
            HEARTBEAT_CLIENT,
            HEARTBEAT_SERVER,
        )
        self.conn = stomp.Connection(
            [(self._url, self._port)], heartbeats=self.heartbeats
        )
        self.conn.set_listener("", self)
        self.conn.connect(self._user, self._password, wait=True)

    def on_connected(self, frame):
        print("Connected: %s" % frame.body)
        for index, topic in enumerate(self._topics):
            queue_destination = topic
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
        topic = frame.headers["destination"]
        command = frame.body.split("[WATER]")[1]
        command_list = command.split(" ")
        # Get pump id from topic
        try:
            pump_id = get_pump_id_by_topic(topic)
            relay_str = get_relay_by_pump_id(pump_id)
            # Convert string to actual relay object
            relay = getattr(automationhat.relay, relay_str)
        except ValueError as e:
            print(f"[ValueError] Error: {e}")
            return
        # duration, pump_id
        self._func(relay, int(command_list[1]), pump_id)

    def send_message(self, destination, message):
        self.conn.send(destination=destination, body=message)

    def disconnect(self):
        self.conn.disconnect()
