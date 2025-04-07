# Green House - I

Please see the [SCHEMATICS](SCHEMATICS.md) to get an overview of
the electrical and physical layout of the plants system.

## Initial Setup

Enable i2c interface in RPi OS configuration.

```bash
sudo raspi-config nonint do_i2c 0
```

You can check the list of I2C devices connected to a RPi using

```bash
sudo apt-get install i2c-tools
i2cdetect -y 1
```

## Run

Please execute the following commands to start the controller.

```sh
pip install -r requirements.txt
python controller-1.py
```

## Note

1. Accessing the I2C bus in parallel in two programs leads to errors. Use multiplexer for such a purpose.
1. The I2C bus communication may not be very robust.
   The sensors produce errors sometimes in an hour and sometimes in a day. So python exception checking is required.
