from datetime import datetime
import time
import schedule

import adafruit_sht4x
import adafruit_tca9548a
from adafruit_as7341 import AS7341
from adafruit_seesaw.seesaw import Seesaw
import board
from influxdb_client import Point

import store
from motors import water_plants

store_influx = store.influx()

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

    # Schedule the plant watering job
    schedule.every(1).minutes.do(water_plants)
    #schedule.every().day.at("10:00").do(water_plants)

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
            point = (
                Point("exception")
                .field("status", 0)
            )
            store_influx.write(record=point)
            #time.sleep(5)
            #raise Exception("I2C device error")

        except Exception as e:
            initialise()
            print(f"Exception at: {datetime.now().isoformat()}")
            point = (
                Point("exception")
                .field("status", 1)
            )
            store_influx.write(record=point)
            time.sleep(5)
            continue

        # water the plants if needed
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    print("Starting greenhouse-1")