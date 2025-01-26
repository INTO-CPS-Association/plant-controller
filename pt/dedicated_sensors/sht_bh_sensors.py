# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using two TSL2491 light sensors attached to TCA9548A channels 0 and 1.
# Use with other I2C sensors would be similar.

import time
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
# BH1750 is light sensor
bh1750 = adafruit_bh1750.BH1750(tca[4])
# SHT40 and SHT45 are temperature and humidity sensors
sht40 = adafruit_sht4x.SHT4x(tca[5])
sht45 = adafruit_sht4x.SHT4x(tca[7])

# After initial setup, can just use sensors as normal.

sht45.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
# Can also set the mode to enable heater
# sht45.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
print("Current mode for SHT45 is: ", adafruit_sht4x.Mode.string[sht45.mode])

while True:
    temperature, relative_humidity = sht40.measurements
    print(f"SHT40 --> Temperature: {temperature:0.1f} C, Humidity: {relative_humidity:0.1f} %")
    temperature, relative_humidity = sht45.measurements
    print(f"SHT45 --> Temperature: {temperature:0.1f} C, Humidity: {relative_humidity:0.1f} %")
    print("BH1750 --> Light: %.2f Lux" % bh1750.lux)
    print("")
    time.sleep(1)
