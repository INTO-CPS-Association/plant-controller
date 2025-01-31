# Dedicated Sensors

The approach taken here is to use one good sensor for
each physical variable measurement.
All the sensors selected use [I2C communication protocol](https://www.nxp.com/docs/en/user-guide/UM10204.pdf).

There is only one I2C port on GPIO of Raspberry Pi 5.
An Adafruit
[PCA9548A multiplexer](https://learn.adafruit.com/adafruit-pca9548-8-channel-stemma-qt-qwiic-i2c-multiplexer)
setup is used to connect
multiple I2C sensors to the Raspberry Pi (RPi) 5.

It is useful to be familiar with the RPi 5 [GPIO pins](https://pinout.xyz/).
The I2C pins of RPi 5 are.

| Pin No | Pin Name | Suggested Wire Color |
|:---|:---|:---|
| 1 | 3.3 | RED |
| 2 or 4 | 5V | RED |
| 3 | SDA | BLUE |
| 5 | SCL | YELLOW |
| 6 or 9 | GND | BLACK |

The multiplexer can work with both 3.3V and 5V.
The Multiplexer is available at **I2C address x70** and it has 8 ports.

You can check the list of I2C devices connected to a RPi using

```bash
sudo apt-get install i2c-tools
i2cdetect -y 1
```

The temperature and humidity sensor (SHT45) and light sensor (BH1750)
are connected to the multiplexer.
Sometimes these sensors work only when connected
on certain multiplexer ports (probably a bug).
The trial run worked successfully when was BH1750 connected to port 4 and SH45 to port 7 (with starting port number being 0).

## Updates

### 31-Jan-2025

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

port 0 to 3 --> I2C soil moisture sensors
port 4 --> empty
port 5 --> SHT40
port 6 --> SHT45
port 7 --> BH1750

Also the IoT relay is connected to ports 34 and 36.

With this setup, execute two programs.

1. relay-Rune.py (outside python venv)
1. sht_bh_3_moisture_sensors.py (inside python venv)


## Note

1. Accessing the I2C bus in parallel in two programs leads to errors. Use multiplexer for such a purpose.
1. The I2C bus communication may not be very robust.
   The sensors produce errors sometimes in an hour and sometimes in a day. So python exception checking is required.
