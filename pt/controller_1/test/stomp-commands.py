import stomp
import sys
#import time
from ..config import (
    get_stomp_url,
    get_stomp_user,
    get_stomp_password,
    get_stomp_port
)

url = get_stomp_url()
port = get_stomp_port()
user = get_stomp_user()
password = get_stomp_password()


class MyListener(stomp.ConnectionListener):
  def on_connected(self, frame):
    print(f"Connected to broker: {frame}")
  def on_disconnected(self):
    print("Disconnected from broker.")
  def on_error(self, frame):
    print(f"Broker error: {frame}")

conn = stomp.Connection([(url, port)])
conn.set_listener('', MyListener())
conn.connect(user, password, wait=True)

while True:
  if not conn.is_connected():
    print("Connection lost, reconnecting...")
    conn.connect(user, password, wait=True)
  else:
    print("Sending message...")
    conn.send(destination='actuator.3.water', body='[WATER]0 5')
  #time.sleep(10)
  sys.exit(0)