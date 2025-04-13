from datetime import datetime
import time

from sense_hat import SenseHat
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

org = "influx-org"
url = "https://influx.foo.com"
token="xxx"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="controller-2"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

def initialise():
    # Temperature, humidity and light readings from SenseHAT
    sense = SenseHat()
    # settings for color sensor
    sense.color.gain = 4
    sense.color.integration_cycles = 64


def readings():

    # gives temperature in degrees centigrade
    temperature = sense.get_temperature()
    # gives relative humidity in percentage terms
    relative_humidity = sense.get_humidity()
    print(f"SenseHAT --> Temperature: {temperature:0.1f} C, Humidity: {relative_humidity:0.1f} %")
    point = (
        Point("sensehat")
        .field("temperature", temperature)
        .field("relative_humidity", relative_humidity)
    )
    write_api.write(bucket=bucket, org=org, record=point)

    red, green, blue, clear = sense.color.color
    print("SenseHAT light sensor: Red     %s" % red)
    print("SenseHAT light sensor: Green   %s" % green)
    print("SenseHAT light sensor: Blue   %s" % blue)
    print("SenseHAT light sensor: Brightness %s" % clear)
    point = (
        Point("sensehat-light")
        .field("red", red)
        .field("green", green)
        .field("blue", blue)
        .field("brightness", clear)
    )
    write_api.write(bucket=bucket, org=org, record=point)
    print("light sensor read")

    print("")


if __name__ == "__main__":
    # Temperature, humidity and light readings from SenseHAT
    sense = SenseHat()
    # settings for color sensor
    sense.color.gain = 4
    sense.color.integration_cycles = 64

    print("init done") 

    while True:
        try:
            print(f"Sample at: {datetime.now().isoformat()}")
            # gives temperature in degrees forenheit
            temperature = sense.get_temperature()
            # gives relative humidity in percentage terms
            relative_humidity = sense.get_humidity()
            print(f"SenseHAT --> Temperature: {temperature:0.1f} F, Humidity: {relative_humidity:0.1f} %")
            point = (
                Point("sensehat")
                .field("temperature", temperature)
                .field("relative_humidity", relative_humidity)
            )
            write_api.write(bucket=bucket, org=org, record=point)

            red, green, blue, clear = sense.color.color
            print("SenseHAT light sensor: Red     %s" % red)
            print("SenseHAT light sensor: Green   %s" % green)
            print("SenseHAT light sensor: Blue   %s" % blue)
            print("SenseHAT light sensor: Brightness %s" % clear)
            point = (
                Point("sensehat-light")
                .field("red", red)
                .field("green", green)
                .field("blue", blue)
                .field("brightness", clear)
            )
            write_api.write(bucket=bucket, org=org, record=point)
            print("light sensor read")

            print("")

        except Exception as e:
            initialise()
            print(f"Exception at: {datetime.now().isoformat()}")
            point = (
                Point("exception")
                .field("status", 0)
            )
            write_api.write(bucket=bucket, org=org, record=point)
            time.sleep(5)
            continue

        time.sleep(60)
