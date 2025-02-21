# Greenhouse using Pimoroni AutomationHAT

## Configure Raspberry Pi

Enable i2c interface in RPi configuration
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

## Install Libraries and Use

sudo apt-get install python3-automationhat

prefer venv install
python -m venv .venv
source .venv/bin/activate

For tutorials see the
[online guide](https://learn.pimoroni.com/article/getting-started-with-automation-hat-and-phat)

## I2C Connections

I2C addresses used in this demo are:

| I2C Address | Device | Purpose |
|:---|:---|:---|
| 0x23 (can be changed to 0x5C) | BH1750 | 16-bit light sensor |
| 0x44 | SHT40 | temperature and humidity sensor |
| 0x48 | ADS1015 | 12-bit ADC (part of Pimoroni AutomationHAT) |
| 0x54 | SN3218 | 18-channel LED driver  (part of Pimoroni AutomationHAT) |
|  | I2C Hub | Four port I2C passive hub |

Use Adafruit I2C hub to connect the required sensors to sideways
GPIO pins

See [I2C directory](https://learn.adafruit.com/i2c-addresses/the-list)

### TODO

1. For the 5V pumps, you can use the 5V supply from RPi. This supply
   is accessible on automationHAT. Otherwise, a dedicated power supply
   (just cellphone charger) works as well.

1. Make sure the connection diagram works well for the three relays and then
   check with Electronics workshop on clean up the wiring.

## Help

1. Use the class structure given in
   https://github.com/pimoroni/automation-hat/blob/main/automationhat/pins.py
   to cleanup the green house controller code.
1. AutomationHAT uses only
   [some GPIO pins](https://pinout.xyz/pinout/automation_hat).
1. See the guide on [stacking multiple HATs](https://forums.raspberrypi.com/viewtopic.php?t=382395)


