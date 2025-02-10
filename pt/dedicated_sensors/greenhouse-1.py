# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using two TSL2491 light sensors attached to TCA9548A channels 0 and 1.
# Use with other I2C sensors would be similar.

from datetime import datetime
import numpy as np
import time
from adafruit_seesaw.seesaw import Seesaw
import board
import adafruit_bh1750
import adafruit_sht4x
import adafruit_tca9548a
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from gpiozero import LED
import schedule

org = "influx-org"
url = "https://influx.foo.com"
token="xxx"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="plants"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

#use GPIO16 (pin-36 on RPi5)
aquarium_pumps = LED(16)

aquarium_pumps.off()

def water_plants():
    aquarium_pumps.on()
    print(f"pump turned on at: {datetime.now().isoformat()}")
    point = (
        Point("water_pumps")
        .field("status", 1)
    )
    write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)
    time.sleep(10)
    aquarium_pumps.off()
    print(f"pump turned off at: {datetime.now().isoformat()}")
    point = (
        Point("water_pumps")
        .field("status", 0)
    )
    write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)

# Schedule the plant watering job
#schedule.every().day.at("14:50").do(water_plants)
#schedule.every(3).minutes.do(water_plants)

def initialise():
    # Create I2C bus as normal
    i2c = board.I2C()  # uses board.SCL and board.SDA

    # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    # Create the TCA9548A object and give it the I2C bus

    tca = adafruit_tca9548a.TCA9548A(i2c)

    # For each sensor, create it using the TCA9548A channel instead of the I2C object
    # moisture sensor with temperature sensing capabilities
    moisture_0 = Seesaw(tca[0], addr=0x36)
    moisture_1 = Seesaw(tca[1], addr=0x36)
    moisture_2 = Seesaw(tca[2], addr=0x36)
    moisture_3 = Seesaw(tca[3], addr=0x36)

    # SHT40 and SHT45 are temperature and humidity sensors
    sht40 = adafruit_sht4x.SHT4x(tca[5])
    sht45 = adafruit_sht4x.SHT4x(tca[6])
    # BH1750 is light sensor
    bh1750 = adafruit_bh1750.BH1750(tca[7])

    # After initial setup, can just use sensors as normal.

    sht45.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
    # Can also set the mode to enable heater
    # sht45.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
    print("Current mode for SHT45 is: ", adafruit_sht4x.Mode.string[sht45.mode])
    
def readings():
    print(f"timestamp: {datetime.now().isoformat()}")
    temperature, relative_humidity = sht40.measurements
    print(f"SHT40 --> Temperature: {temperature:0.1f} C, Humidity: {relative_humidity:0.1f} %")
    point = (
        Point("sht40")
        .field("temperature", temperature)
        .field("relative_humidity", relative_humidity)
    )
    write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)

    temperature, relative_humidity = sht45.measurements
    print(f"SHT45 --> Temperature: {temperature:0.1f} C, Humidity: {relative_humidity:0.1f} %")
    point = (
        Point("sht45")
        .field("temperature", temperature)
        .field("relative_humidity", relative_humidity)
    )
    write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)

    print("BH1750 --> Light: %.2f Lux" % bh1750.lux)
    point = (
        Point("bht1750")
        .field("light", bh1750.lux)
    )
    write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)

    moisture_reading = moisture_0.moisture_read()
    temperature_reading = moisture_0.get_temp()
    print(f"Soil sensor-0 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
    point = (
        Point("soil-sensor-0")
        .field("moisture", moisture_reading)
        .field("temperature", temperature_reading)
    )
    write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)
    
    moisture_reading = moisture_1.moisture_read()
    temperature_reading = moisture_1.get_temp()
    print(f"Soil sensor-1 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
    point = (
        Point("soil-sensor-1")
        .field("moisture", moisture_reading)
        .field("temperature", temperature_reading)
    )
    write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)

    moisture_reading = moisture_2.moisture_read()
    temperature_reading = moisture_2.get_temp()
    print(f"Soil sensor-2 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
    point = (
        Point("soil-sensor-2")
        .field("moisture", moisture_reading)
        .field("temperature", temperature_reading)
    )
    write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)

    moisture_reading = moisture_3.moisture_read()
    temperature_reading = moisture_3.get_temp()
    print(f"Soil sensor-3 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
    point = (
        Point("soil-sensor-3")
        .field("moisture", moisture_reading)
        .field("temperature", temperature_reading)
    )
    write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)

    print("")


if __name__ == "__main__":
    # Create I2C bus as normal
    i2c = board.I2C()  # uses board.SCL and board.SDA

    # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    # Create the TCA9548A object and give it the I2C bus

    tca = adafruit_tca9548a.TCA9548A(i2c)

    # For each sensor, create it using the TCA9548A channel instead of the I2C object
    # moisture sensor with temperature sensing capabilities
    moisture_0 = Seesaw(tca[0], addr=0x36)
    moisture_1 = Seesaw(tca[1], addr=0x36)
    moisture_2 = Seesaw(tca[2], addr=0x36)
    moisture_3 = Seesaw(tca[3], addr=0x36)

    # SHT40 and SHT45 are temperature and humidity sensors
    sht40 = adafruit_sht4x.SHT4x(tca[5])
    sht45 = adafruit_sht4x.SHT4x(tca[6])
    # BH1750 is light sensor
    bh1750 = adafruit_bh1750.BH1750(tca[7])

    # After initial setup, can just use sensors as normal.

    sht45.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
    # Can also set the mode to enable heater
    # sht45.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
    print("Current mode for SHT45 is: ", adafruit_sht4x.Mode.string[sht45.mode])
    print("init done") 

    # Schedule the plant watering job
    schedule.every(1).minutes.do(water_plants)

    while True:
        try:
            print(f"timestamp: {datetime.now().isoformat()}")
            temperature, relative_humidity = sht40.measurements
            print(f"SHT40 --> Temperature: {temperature:0.1f} C, Humidity: {relative_humidity:0.1f} %")
            point = (
                Point("sht40")
                .field("temperature", temperature)
                .field("relative_humidity", relative_humidity)
            )
            write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)

            temperature, relative_humidity = sht45.measurements
            print(f"SHT45 --> Temperature: {temperature:0.1f} C, Humidity: {relative_humidity:0.1f} %")
            point = (
                Point("sht45")
                .field("temperature", temperature)
                .field("relative_humidity", relative_humidity)
            )
            write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)

            print("BH1750 --> Light: %.2f Lux" % bh1750.lux)
            point = (
                Point("bht1750")
                .field("light", bh1750.lux)
            )
            write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)

            moisture_reading = moisture_0.moisture_read()
            temperature_reading = moisture_0.get_temp()
            print(f"Soil sensor-0 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
            point = (
                Point("soil-sensor-0")
                .field("moisture", moisture_reading)
                .field("temperature", temperature_reading)
            )
            write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)
            
            moisture_reading = moisture_1.moisture_read()
            temperature_reading = moisture_1.get_temp()
            print(f"Soil sensor-1 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
            point = (
                Point("soil-sensor-1")
                .field("moisture", moisture_reading)
                .field("temperature", temperature_reading)
            )
            write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)

            moisture_reading = moisture_2.moisture_read()
            temperature_reading = moisture_2.get_temp()
            print(f"Soil sensor-2 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
            point = (
                Point("soil-sensor-2")
                .field("moisture", moisture_reading)
                .field("temperature", temperature_reading)
            )
            write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)

            moisture_reading = moisture_3.moisture_read()
            temperature_reading = moisture_3.get_temp()
            print(f"Soil sensor-3 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
            point = (
                Point("soil-sensor-3")
                .field("moisture", moisture_reading)
                .field("temperature", temperature_reading)
            )
            write_api.write(bucket=bucket, org="TestUserDTaaS", record=point)

            print("")
            #time.sleep(5)
            #raise Exception("I2C device error")

        except Exception as e:
            initialise()
            continue

        # water the plants if needed
        schedule.run_pending()
        time.sleep(10)
