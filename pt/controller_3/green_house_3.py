from datetime import datetime
import time
import schedule
from gpiozero import LED

import adafruit_tca9548a
from adafruit_seesaw.seesaw import Seesaw
import board
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

org = "influx-org"
url = "https://influx.foo.com"
token="xxx"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="greenhouse-3"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

# Relay Channels are active low which means
#ON - turns off the output
#OFF - turns on the output

pump_1 = LED(26)
pump_2 = LED(20)
pump_3 = LED(21)
pump_1.on()
pump_2.on()
pump_3.on()

def water_plants():
    pump_1.off()
    print(f"pumps turned on at: {datetime.now().isoformat()}")
    point = (
        Point("pump-1")
        .field("status", 1)
    )
    write_api.write(bucket=bucket, org=org, record=point)

    time.sleep(5)
    
    pump_1.on()
    print(f"pumps turned off at: {datetime.now().isoformat()}")
    point = (
        Point("pump-1")
        .field("status", 0)
    )
    write_api.write(bucket=bucket, org=org, record=point)


def initialise():
    # Create I2C bus as normal
    i2c = board.I2C()  # uses board.SCL and board.SDA

    # Create the TCA9548A object and give it the I2C bus
    tca = adafruit_tca9548a.TCA9548A(i2c)

    # For each sensor, create it using the TCA9548A channel instead of the I2C object
    # moisture sensor with temperature sensing capabilities
    moisture_0 = Seesaw(tca[6], addr=0x36)
    moisture_1 = Seesaw(tca[7], addr=0x36)

def readings():

    moisture_reading = moisture_0.moisture_read()
    temperature_reading = moisture_0.get_temp()
    print(f"Soil sensor-0 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
    point = (
        Point("soil-sensor-0")
        .field("moisture", moisture_reading)
        .field("temperature", temperature_reading)
    )
    write_api.write(bucket=bucket, org=org, record=point)
    
    moisture_reading = moisture_1.moisture_read()
    temperature_reading = moisture_1.get_temp()
    print(f"Soil sensor-1 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
    point = (
        Point("soil-sensor-1")
        .field("moisture", moisture_reading)
        .field("temperature", temperature_reading)
    )
    write_api.write(bucket=bucket, org=org, record=point)

    print("")


if __name__ == "__main__":
    # Create I2C bus as normal
    i2c = board.I2C()  # uses board.SCL and board.SDA

    # Create the TCA9548A object and give it the I2C bus
    tca = adafruit_tca9548a.TCA9548A(i2c)

    # For each sensor, create it using the TCA9548A channel instead of the I2C object
    # moisture sensor with temperature sensing capabilities
    moisture_0 = Seesaw(tca[6], addr=0x36)
    moisture_1 = Seesaw(tca[7], addr=0x36)

    print("init done") 

    # Schedule the plant watering job
    schedule.every(1).minutes.do(water_plants)
    #schedule.every().day.at("10:00").do(water_plants)

    while True:
        try:
            print(f"Sample at: {datetime.now().isoformat()}")

            moisture_reading = moisture_0.moisture_read()
            temperature_reading = moisture_0.get_temp()
            print(f"Soil sensor-0 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
            point = (
                Point("soil-sensor-0")
                .field("moisture", moisture_reading)
                .field("temperature", temperature_reading)
            )
            write_api.write(bucket=bucket, org=org, record=point)
            
            moisture_reading = moisture_1.moisture_read()
            temperature_reading = moisture_1.get_temp()
            print(f"Soil sensor-1 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
            point = (
                Point("soil-sensor-1")
                .field("moisture", moisture_reading)
                .field("temperature", temperature_reading)
            )
            write_api.write(bucket=bucket, org=org, record=point)

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

        # water the plants if needed
        schedule.run_pending()
        time.sleep(60)
