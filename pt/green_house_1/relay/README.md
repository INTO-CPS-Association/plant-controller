
The GPIO pin layout has changed in RPi 5. Only "gpiozero" package
works correctly.

The board works correctly but the software is outdated.
It only works upto RPi 4.
https://www.waveshare.com/wiki/RPi_Relay_Board

However, we can use python gpiozero pip package to use the board


Install gpiozero at the system level (don't use venv)
$sudo apt install python3-gpiozero
This installs gpiozero==2.0.1 in the system site packages

Do not use virtual environment

The GPIO pins are:

channel_1 = GPIO26
channel_2 = GPIO20
channel_3 = GPIO21

# Channels are active low which means
#ON - turns off the output
#OFF - turns on the output

One channel can control all the motors.
It takes more current to drive all channels.


TODO:
---
At the moment LEDs are being used to control the channels but
LEDs draw a lot of current. Is there a low-power way to
activate the channels?



Useful references:
---
https://gpiozero.readthedocs.io/en/stable/recipes.html
https://www.waveshare.com/wiki/RPi_Relay_Board
https://www.sunfounder.com/blogs/news/comprehensive-guide-to-the-pin-diagram-of-raspberry-pi-5-understanding-gpio-pins-and-their-functions
https://www.twicea.com/blog/learn-raspberry-pi-5-pinout-in-this-in-depth-comprehensive-guide

Note:
---
gpiod library doesn't work
https://www.acmesystems.it/libgpiod
