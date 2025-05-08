from datetime import datetime
from schedule import every, repeat
import schedule

import adafruit_sht4x
import adafruit_tca9548a
from adafruit_as7341 import AS7341
from adafruit_seesaw.seesaw import Seesaw
import automationhat
import board
import os, time
from influxdb_client import Point
from typing import Sequence, Tuple, Any
import yaml

from store import InfluxDBStore

store_influx = InfluxDBStore()

precision_map = {
    "NOHEAT_HIGHPRECISION": adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION,
    "NOHEAT_MEDPRECISION": adafruit_sht4x.Mode.NOHEAT_MEDPRECISION,
    "NOHEAT_LOWPRECISION": adafruit_sht4x.Mode.NOHEAT_LOWPRECISION,
    "HIGHHEAT_1S": adafruit_sht4x.Mode.HIGHHEAT_1S,
    "HIGHHEAT_100MS": adafruit_sht4x.Mode.HIGHHEAT_100MS,
    "MEDHEAT_1S": adafruit_sht4x.Mode.MEDHEAT_1S,
    "MEDHEAT_100MS": adafruit_sht4x.Mode.MEDHEAT_100MS,
    "LOWHEAT_1S": adafruit_sht4x.Mode.LOWHEAT_1S,
    "LOWHEAT_100MS": adafruit_sht4x.Mode.LOWHEAT_100MS
}

def get_config() -> dict:
        with open("config/config.yaml", "r") as file:
            data = yaml.safe_load(file)
        return data

def create_sht45_point_measurement(measurements: Tuple[float, float]) -> Point:
    '''Create a point for the SHT45 temperature and humidity measurement.'''
    temperature, relative_humidity = measurements
    point = (
                Point("sht45")
                .field("temperature", temperature)
                .field("relative_humidity", relative_humidity)
            )
    return point

def print_sht45_measurements(measurements: Tuple[float, float]) -> None:
    '''Print the SHT45 temperature and humidity measurements.'''
    temperature, relative_humidity = measurements
    print(f"SHT45 --> Temperature: {temperature:0.1f} C, Humidity: {relative_humidity:0.1f} %")

def create_as7341_point_measurement(light_sensor: AS7341) -> Point:
    '''Create a point for the AS7341 light sensor measurement.'''
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
    return point

def print_as7341_measurements(light_sensor: AS7341) -> None:
    '''Print the AS7341 light sensor measurements.'''
    print("AS7341 light sensor: 415nm wavelength (Violet)  %s" % light_sensor.channel_415nm)
    print("AS7341 light sensor: 445nm wavelength (Indigo) %s" % light_sensor.channel_445nm)
    print("AS7341 light sensor: 480nm wavelength (Blue)   %s" % light_sensor.channel_480nm)
    print("AS7341 light sensor: 515nm wavelength (Cyan)   %s" % light_sensor.channel_515nm)
    print("AS7341 light sensor: 555nm wavelength (Green)   %s" % light_sensor.channel_555nm)
    print("AS7341 light sensor: 590nm wavelength (Yellow)  %s" % light_sensor.channel_590nm)
    print("AS7341 light sensor: 630nm wavelength (Orange)  %s" % light_sensor.channel_630nm)
    print("AS7341 light sensor: 680nm wavelength (Red)     %s" % light_sensor.channel_680nm)

def create_soil_sensor_point_measurement(moisture_reading: float, temperature_reading: float, sensor_id: int) -> Point:
    '''Create a point for the soil sensor measurement.'''
    point = (
                Point(f"soil-sensor-{sensor_id}")
                .field("moisture", moisture_reading)
                .field("temperature", temperature_reading)
            )
    return point

def print_soil_sensor_measurements(moisture_reading: float, temperature_reading: float, sensor_id: int) -> None:
    '''Print the soil sensor measurements.'''
    print(f"Soil sensor-{sensor_id} --> Moisture: {moisture_reading:0.1f}, Temperature: {temperature_reading:0.1f} C")

def create_exception_point(e: Exception) -> Point:
    '''Create a point for the exception measurement.'''
    point = (
                Point("exception")
                .field("status", 0)
            )
    return point

def create_pump_point(pump_id: str, status: int) -> Point:
    '''Create a point for the pump measurement.'''
    point = (
                Point(f"pump-{pump_id}")
                .field("status", status)
            )
    return point

def water_plant_1():
    automationhat.relay.one.on()
    print(f"pump-1 turned on at: {datetime.now().isoformat()}")
    point = create_pump_point(pump_id="1", status=1)
    
    store_influx.write(record=point)


    time.sleep(15)
    
    automationhat.relay.one.off()
    print(f"pump-1 turned off at: {datetime.now().isoformat()}")
    point = create_pump_point(pump_id="1", status=0)
    
    store_influx.write(record=point)

def water_plant_2():
    automationhat.relay.two.on()
    print(f"pump-2 turned on at: {datetime.now().isoformat()}")
    point = create_pump_point(pump_id="2", status=1)
    
    store_influx.write(record=point)

    time.sleep(6)
    
    automationhat.relay.two.off()
    print(f"pump-2 turned off at: {datetime.now().isoformat()}")
    point = create_pump_point(pump_id="2", status=0)
    
    store_influx.write(record=point)

def water_plant_3():
    automationhat.relay.three.on()
    print(f"pump-3 turned on at: {datetime.now().isoformat()}")
    point = create_pump_point(pump_id="3", status=1)
    
    store_influx.write(record=point)

    time.sleep(10)
    
    automationhat.relay.three.off()
    print(f"pump-3 turned off at: {datetime.now().isoformat()}")
    point = create_pump_point(pump_id="3", status=0)
    
    store_influx.write(record=point)  

def initialise(config: dict) -> Sequence[Any]:
    '''Initializes the sensor objects for the TCA9548A multiplexer.'''

    # Get actuator configuration from the config file
    config = config["plant"]["sensors"]

    # Get the moisture sensor port numbers
    port_moisture_0 = config["seesaw"]["moisture_0"]["port"]
    port_moisture_1 = config["seesaw"]["moisture_1"]["port"]
    port_moisture_2 = config["seesaw"]["moisture_2"]["port"]

    # Get the moisture sensor addresses
    addr_moisture_0 = config["seesaw"]["moisture_0"]["addr"]
    addr_moisture_1 = config["seesaw"]["moisture_1"]["addr"]
    addr_moisture_2 = config["seesaw"]["moisture_2"]["addr"]

    # Get the port for the SHT45 sensor
    port_sht45 = config["sht45"]["port"]

    # Get the mode string for the SHT45 sensor
    mode_str_sht45 = config["sht45"]["mode"]

    # Get the port number for the AS7341 sensor
    port_as7341 = config["as7341"]["port"]

    # Create I2C bus as normal
    i2c = board.I2C()  # uses board.SCL and board.SDA

    # Create the TCA9548A object and give it the I2C bus
    tca = adafruit_tca9548a.TCA9548A(i2c)

    # For each sensor, create it using the TCA9548A channel instead of the I2C object
    # moisture sensor with temperature sensing capabilities
    moisture_0 = Seesaw(tca[port_moisture_0], addr=addr_moisture_0)
    moisture_1 = Seesaw(tca[port_moisture_1], addr=addr_moisture_1)
    moisture_2 = Seesaw(tca[port_moisture_2], addr=addr_moisture_2)

    # SHT45 is a temperature and humidity sensor
    sht45 = adafruit_sht4x.SHT4x(tca[port_sht45])

    if mode_str_sht45 in precision_map:
        # Set the sensor mode based on the string value
        mode_value = precision_map[mode_str_sht45]
        sht45.mode = mode_value
    else:
        raise ValueError(f"Invalid mode string: {mode_str_sht45}")
    
    # Can also set the mode to enable heater
    # sht45.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
    print("Current mode for SHT45 is: ", adafruit_sht4x.Mode.string[sht45.mode])

    # AS7341 is a ten-channel (eight color) light sensor
    light_sensor = AS7341(tca[port_as7341])
        
    return moisture_0, moisture_1, moisture_2, sht45, light_sensor

def initialise_actuators(config: dict) -> None:
    '''Initializes the actuators.'''

    # Get actuator configuration from the config file
    config = config["plant"]["actuators"]

    # Get the scedules for the actuators
    schedule_pump_1 = config["pump_1"]["schedule"]
    schedule_pump_2 = config["pump_2"]["schedule"]
    schedule_pump_3 = config["pump_3"]["schedule"]

    # Set the schedule for the actuators
    if schedule_pump_1:
        every().monday.at(schedule_pump_1).do(water_plant_1)
        every().wednesday.at(schedule_pump_1).do(water_plant_1)
        every().friday.at(schedule_pump_1).do(water_plant_1)
    if schedule_pump_2:
        # Set the schedule for pump 2
        every().day.at(schedule_pump_2).do(water_plant_2)
    if schedule_pump_3:
        # Set the schedule for pump 3
        every().monday.at(schedule_pump_3).do(water_plant_3)
        every().wednesday.at(schedule_pump_3).do(water_plant_3)
        every().friday.at(schedule_pump_3).do(water_plant_3)

def readings(moisture_0, moisture_1, moisture_2, sht45, light_sensor):
    print(f"Sample at: {datetime.now().isoformat()}")
    print_sht45_measurements(measurements = sht45.measurements)
    point = create_sht45_point_measurement(measurements = sht45.measurements)
    
    store_influx.write(record=point)

    print_as7341_measurements(light_sensor = light_sensor)
    point = create_as7341_point_measurement(light_sensor = light_sensor)
    
    store_influx.write(record=point)

    moisture_reading = moisture_0.moisture_read()
    temperature_reading = moisture_0.get_temp()
    point = create_soil_sensor_point_measurement(moisture_reading = moisture_reading, temperature_reading = temperature_reading, sensor_id = 0)
    print_soil_sensor_measurements(moisture_reading = moisture_reading, temperature_reading = temperature_reading, sensor_id = 0)
    
    store_influx.write(record=point)
    
    moisture_reading = moisture_1.moisture_read()
    temperature_reading = moisture_1.get_temp()
    point = create_soil_sensor_point_measurement(moisture_reading = moisture_reading, temperature_reading = temperature_reading, sensor_id = 1)
    print_soil_sensor_measurements(moisture_reading = moisture_reading, temperature_reading = temperature_reading, sensor_id = 1)
    
    store_influx.write(record=point)

    moisture_reading = moisture_2.moisture_read()
    temperature_reading = moisture_2.get_temp()
    point = create_soil_sensor_point_measurement(moisture_reading = moisture_reading, temperature_reading = temperature_reading, sensor_id = 2)
    print_soil_sensor_measurements(moisture_reading = moisture_reading, temperature_reading = temperature_reading, sensor_id = 2)
    
    store_influx.write(record=point)

    print("")


if __name__ == "__main__": 
    # Get the configuration from the config file
    config = get_config()
    # Initialize the actuators
    initialise_actuators(config)
    # Initialize the sensors
    moisture_0, moisture_1, moisture_2, sht45, light_sensor = initialise(config)
    
    # reading interval
    # Set up schedule for sensors
    schedule_sensors = config["plant"]["sensors"]["schedule"]
    if schedule_sensors:
        pass
    else:
        raise ValueError(f"No schedule given in config file for sensors: {schedule_sensors}")
    
    print("init done") 

    while True:
        try:
            readings(moisture_0, moisture_1, moisture_2, sht45, light_sensor)

            #time.sleep(5)
            #raise Exception("I2C device error")

        except Exception as e:
            moisture_0, moisture_1, moisture_2, sht45, light_sensor = initialise(config)
            print(f"Exception at: {datetime.now().isoformat()}")

            point = create_exception_point(e)
            store_influx.write(record=point)
            time.sleep(5)
            continue

        # water the plants if needed
        schedule.run_pending()
        time.sleep(schedule_sensors)
