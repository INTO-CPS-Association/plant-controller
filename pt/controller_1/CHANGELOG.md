# Updates

## 28-March-2025

The projects have been renamed from **greenhouse** to **controller**.

## 17-Feb-2025

The demo setup has been updated to include three Adafruit I2C soil sensors,
one temperature and humidity sensors - SHT45;
and light sensor (AS7341). The sensors are connected to Adafruit
PCA9548A (8-ch multiplexer) as follows:

The connections to the ports are:

port 0,1 and 2 --> soil moisture sensors
port 6 --> SHT45 temperature and humidity sensor
port 7 --> AS7341 light sensor

The IoT relay has been replaced with Pimoroni AutomationHAT

With this setup, execute the following commands.

```sh
pip install -r requirements.txt
python controller-1.py
```

The data is being written to InfluxDB database with the following details.

```txt
URL: https://dtl-server-2.st.lab.au.dk
Org: TestUserDTaaS
Bucket: greenhouse-1
```

A Pi Juice UPS has been added to the RPi. As a result, we have
a stack of the following.

* AutomationHAT on top of Pi Juice HAT
* Pi Juice HAT on top of Raspberry Pi 5

## 13-Feb-2025

The green house configuration changed.
The three large plants are being monitored and watered.
The watering is temporarily turned off to monitor the long-term
stability of the code.

## 8-Feb-2025

The small basil plants died. The large large basil plants are still ok.
Moisture sensors 0 and 1 are placed in one plant and
moisture sensors 2 and 3 are placed in another plant

## 3-Feb-2025

The four moisture sensors are placed in four basil plants.
Two large plants and two small plants.
The large plants are large by about 3X vis-a-vis small ones.

## 31-Jan-2025

The demo setup has been updated to include four Adafruit I2C soil sensors,
two temperature and humidity sensors - SH40 and SHT45;
and light sensor (BH1750). The sensors are connected to Adafruit
8-ch multiplexer as follows:


The PCA9548A is connected to I2C pins of RPi 5 using Stemma QT
connector.

The pins are:

1 - RED, 3 - BLUE, 5 - YELLOW, 9 - GND

The Multiplexer is available at port x70 and it has 8 ports.
The connections to the ports are:

port 0,1 and 3 --> soil moisture sensors
port 2 --> faulty soil moisture sensor
port 5 --> SHT45 temperature and humidity sensor
port 7 --> AS7341 light sensor

Also the IoT relay is connected to ports 34 (gnd) and 36 (signal).

With this setup, execute three programs.

1. controller-1 (inside python venv)
1. relay.py (outside python venv)
1. sht_bh_3_moisture_sensors.py (inside python venv)
1. sht_bh_3_moisture_sensors_influxdb.py (inside python venv)

