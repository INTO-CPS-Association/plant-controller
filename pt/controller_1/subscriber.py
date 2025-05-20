import stomp
import json
import time

class Subscriber(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn
        self.count = 0
        self.start = time.time()

    def on_error(self, frame):
        print(f'received an error {frame.body}')

    def on_message(self, frame):
        # We need to command <pump> <time>
        command = frame.body.split("[WATER]")[1]
        command_list = command.split(" ")

        if command_list[0] == "water":
            pump_water(int(command_list[1]), int(command_list[2]))
        else:
            pump_water(int(command_list[0]), int(command_list[1]))