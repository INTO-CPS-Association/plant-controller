# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using two TSL2491 light sensors attached to TCA9548A channels 0 and 1.
# Use with other I2C sensors would be similar.

from datetime import datetime
import numpy as np
import time
#import schedule
from schedule import every, repeat
import schedule

import adafruit_sht4x
import adafruit_tca9548a
from adafruit_as7341 import AS7341
from adafruit_seesaw.seesaw import Seesaw
import automationhat
import board
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from store import InfluxDBStore

store_influx = InfluxDBStore()

@repeat(every().monday.at("10:15")) #run at 10:15 hours
@repeat(every().wednesday.at("10:15"))
@repeat(every().friday.at("10:15"))
def water_plant_1():
    automationhat.relay.one.on()
    point = (
        Point("pump-1")
        .field("status", 1)
    )
    
    store_influx.write(record=point)
    print(f"pump-1 turned on at: {datetime.now().isoformat()}")


    time.sleep(15)
    
    automationhat.relay.one.off()
    print(f"pump-1 turned off at: {datetime.now().isoformat()}")
    point = (
        Point("pump-1")
        .field("status", 0)
    )
    
    store_influx.write(record=point)


@repeat(every().day.at("10:15")) #run at 10:15 hours
#@repeat(every().minute.at(":10")) #run at 10th second of each minute
def water_plant_2():
    automationhat.relay.two.on()
    point = (
        Point("pump-2")
        .field("status", 1)
    )
    
    store_influx.write(record=point)
    print(f"pump-2 turned on at: {datetime.now().isoformat()}")

    time.sleep(6)
    
    automationhat.relay.two.off()
    point = (
        Point("pump-2")
        .field("status", 0)
    )
    
    store_influx.write(record=point)
    print(f"pump-2 turned off at: {datetime.now().isoformat()}")


@repeat(every().monday.at("10:15")) #run at 10:15 hours
@repeat(every().wednesday.at("10:15"))
@repeat(every().friday.at("10:15"))
def water_plant_3():
    automationhat.relay.three.on()
    print(f"pump-3 turned on at: {datetime.now().isoformat()}")
    point = (
        Point("pump-3")
        .field("status", 1)
    )
    
    store_influx.write(record=point)
    print(f"pump-3 turned off at: {datetime.now().isoformat()}")

    time.sleep(10)
    
    automationhat.relay.three.off()
    point = (
        Point("pump-3")
        .field("status", 0)
    )
    
    store_influx.write(record=point)


def initialise():
    # Create I2C bus as normal
    i2c = board.I2C()  # uses board.SCL and board.SDA

    # Create the TCA9548A object and give it the I2C bus
    tca = adafruit_tca9548a.TCA9548A(i2c)

    # For each sensor, create it using the TCA9548A channel instead of the I2C object
    # moisture sensor with temperature sensing capabilities
    moisture_0 = Seesaw(tca[0], addr=0x36)
    moisture_1 = Seesaw(tca[1], addr=0x36)
    moisture_2 = Seesaw(tca[2], addr=0x36)

    # SHT45 is a temperature and humidity sensor
    sht45 = adafruit_sht4x.SHT4x(tca[6])
    sht45.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
    # Can also set the mode to enable heater
    # sht45.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
    print("Current mode for SHT45 is: ", adafruit_sht4x.Mode.string[sht45.mode])
    
    # AS7341 is a ten-channel (eight color) light sensor
    light_sensor = AS7341(tca[7])    

def readings():

    temperature, relative_humidity = sht45.measurements
    print(f"SHT45 --> Temperature: {temperature:0.1f} C, Humidity: {relative_humidity:0.1f} %")
    point = (
        Point("sht45")
        .field("temperature", temperature)
        .field("relative_humidity", relative_humidity)
    )
    
    store_influx.write(record=point)

    print("AS7341 light sensor: 415nm wavelength (Violet)  %s" % light_sensor.channel_415nm)
    print("AS7341 light sensor: 445nm wavelength (Indigo) %s" % light_sensor.channel_445nm)
    print("AS7341 light sensor: 480nm wavelength (Blue)   %s" % light_sensor.channel_480nm)
    print("AS7341 light sensor: 515nm wavelength (Cyan)   %s" % light_sensor.channel_515nm)
    print("AS7341 light sensor: 555nm wavelength (Green)   %s" % light_sensor.channel_555nm)
    print("AS7341 light sensor: 590nm wavelength (Yellow)  %s" % light_sensor.channel_590nm)
    print("AS7341 light sensor: 630nm wavelength (Orange)  %s" % light_sensor.channel_630nm)
    print("AS7341 light sensor: 680nm wavelength (Red)     %s" % light_sensor.channel_680nm)
    point = (
        Point("as7341")
        .field("violet", light_sensor.channel_415nm)
        .field("indigo", light_sensor.channel_445nm)
        .field("blue", light_sensor.channel_480nm)
        .field("cyan", light_sensor.channel_515nm)
        .field("green", light_sensor.channel_555nm)
        .field("yellow", light_sensor.channel_590nm)
        .field("orange", light_sensor.channel_630nm)
        .field("red", light_sensor.channel_680nm)
    )
    
    store_influx.write(record=point)
    print("light sensor read")

    moisture_reading = moisture_0.moisture_read()
    temperature_reading = moisture_0.get_temp()
    print(f"Soil sensor-0 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
    point = (
        Point("soil-sensor-0")
        .field("moisture", moisture_reading)
        .field("temperature", temperature_reading)
    )
    
    store_influx.write(record=point)
    
    moisture_reading = moisture_1.moisture_read()
    temperature_reading = moisture_1.get_temp()
    print(f"Soil sensor-1 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
    point = (
        Point("soil-sensor-1")
        .field("moisture", moisture_reading)
        .field("temperature", temperature_reading)
    )
    
    store_influx.write(record=point)

    moisture_reading = moisture_2.moisture_read()
    temperature_reading = moisture_2.get_temp()
    print(f"Soil sensor-2 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
    point = (
        Point("soil-sensor-2")
        .field("moisture", moisture_reading)
        .field("temperature", temperature_reading)
    )
    
    store_influx.write(record=point)

    print("")


if __name__ == "__main__":
    # Create I2C bus as normal
    i2c = board.I2C()  # uses board.SCL and board.SDA

    # Create the TCA9548A object and give it the I2C bus
    tca = adafruit_tca9548a.TCA9548A(i2c)

    # For each sensor, create it using the TCA9548A channel instead of the I2C object
    # moisture sensor with temperature sensing capabilities
    moisture_0 = Seesaw(tca[0], addr=0x36)
    moisture_1 = Seesaw(tca[1], addr=0x36)
    moisture_2 = Seesaw(tca[2], addr=0x36)

    # SHT45 is a temperature and humidity sensor
    sht45 = adafruit_sht4x.SHT4x(tca[6])
    sht45.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
    # Can also set the mode to enable heater
    # sht45.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
    print("Current mode for SHT45 is: ", adafruit_sht4x.Mode.string[sht45.mode])

    # AS7341 is a ten-channel (eight color) light sensor
    light_sensor = AS7341(tca[7])    

    print("init done") 

    while True:
        try:
            print(f"Sample at: {datetime.now().isoformat()}")
            temperature, relative_humidity = sht45.measurements
            print(f"SHT45 --> Temperature: {temperature:0.1f} C, Humidity: {relative_humidity:0.1f} %")
            point = (
                Point("sht45")
                .field("temperature", temperature)
                .field("relative_humidity", relative_humidity)
            )
            
            store_influx.write(record=point)

            print("AS7341 light sensor: 415nm wavelength (Violet)  %s" % light_sensor.channel_415nm)
            print("AS7341 light sensor: 445nm wavelength (Indigo) %s" % light_sensor.channel_445nm)
            print("AS7341 light sensor: 480nm wavelength (Blue)   %s" % light_sensor.channel_480nm)
            print("AS7341 light sensor: 515nm wavelength (Cyan)   %s" % light_sensor.channel_515nm)
            print("AS7341 light sensor: 555nm wavelength (Green)   %s" % light_sensor.channel_555nm)
            print("AS7341 light sensor: 590nm wavelength (Yellow)  %s" % light_sensor.channel_590nm)
            print("AS7341 light sensor: 630nm wavelength (Orange)  %s" % light_sensor.channel_630nm)
            print("AS7341 light sensor: 680nm wavelength (Red)     %s" % light_sensor.channel_680nm)
            point = (
                Point("as7341")
                .field("violet", light_sensor.channel_415nm)
                .field("indigo", light_sensor.channel_445nm)
                .field("blue", light_sensor.channel_480nm)
                .field("cyan", light_sensor.channel_515nm)
                .field("green", light_sensor.channel_555nm)
                .field("yellow", light_sensor.channel_590nm)
                .field("orange", light_sensor.channel_630nm)
                .field("red", light_sensor.channel_680nm)
            )
            
            store_influx.write(record=point)

            moisture_reading = moisture_0.moisture_read()
            temperature_reading = moisture_0.get_temp()
            print(f"Soil sensor-0 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
            point = (
                Point("soil-sensor-0")
                .field("moisture", moisture_reading)
                .field("temperature", temperature_reading)
            )
            
            store_influx.write(record=point)
            
            moisture_reading = moisture_1.moisture_read()
            temperature_reading = moisture_1.get_temp()
            print(f"Soil sensor-1 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
            point = (
                Point("soil-sensor-1")
                .field("moisture", moisture_reading)
                .field("temperature", temperature_reading)
            )
            
            store_influx.write(record=point)

            moisture_reading = moisture_2.moisture_read()
            temperature_reading = moisture_2.get_temp()
            print(f"Soil sensor-2 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
            point = (
                Point("soil-sensor-2")
                .field("moisture", moisture_reading)
                .field("temperature", temperature_reading)
            )
            
            store_influx.write(record=point)

            print("")
            #time.sleep(5)
            #raise Exception("I2C device error")

        except Exception as e:
            initialise()
            print(f"Exception at: {datetime.now().isoformat()}")
            point = (
                Point("exception")
                .field("status", 0)
            )
            
            store_influx.write(record=point)
            time.sleep(5)
            continue

        # water the plants if needed
        schedule.run_pending()
        time.sleep(60)
