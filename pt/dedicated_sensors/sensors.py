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

while True:
    print(f"timestamp: {datetime.now().isoformat()}")
    temperature, relative_humidity = sht40.measurements
    print(f"SHT40 --> Temperature: {temperature:0.1f} C, Humidity: {relative_humidity:0.1f} %")
    temperature, relative_humidity = sht45.measurements
    print(f"SHT45 --> Temperature: {temperature:0.1f} C, Humidity: {relative_humidity:0.1f} %")
    print("BH1750 --> Light: %.2f Lux" % bh1750.lux)
    moisture_reading = moisture_0.moisture_read()
    temperature_reading = moisture_0.get_temp()
    print(f"Soil sensor-0 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
    moisture_reading = moisture_1.moisture_read()
    temperature_reading = moisture_1.get_temp()
    print(f"Soil sensor-1 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
    moisture_reading = moisture_2.moisture_read()
    temperature_reading = moisture_2.get_temp()
    print(f"Soil sensor-2 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
    moisture_reading = moisture_3.moisture_read()
    temperature_reading = moisture_3.get_temp()
    print(f"Soil sensor-3 --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")
    print("")
    time.sleep(10)
