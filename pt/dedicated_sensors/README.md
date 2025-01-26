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

## Note

1. Accessing the I2C bus in parallel in two programs leads to errors. Use multiplexer for such a purpose.
1. The I2C bus communication may not be very robust.
   The sensors produce errors sometimes in an hour and sometimes in a day. So python exception checking is required.
