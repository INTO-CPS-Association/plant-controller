# Waveshare Relay for Greenhouses

The GPIO pin layout has changed in
[RPi 5](https://www.sunfounder.com/blogs/news/comprehensive-guide-to-the-pin-diagram-of-raspberry-pi-5-understanding-gpio-pins-and-their-functions).
Only
[gpiozero](https://gpiozero.readthedocs.io/en/stable/recipes.html) package.
works correctly with RPi 5 and also with older RPi models.

## Waveshare 3-Relay HAT

The GPIO pins for the three-relays are:

* channel_1 = GPIO26
* channel_2 = GPIO20
* channel_3 = GPIO21

Remember, the channels to the relays are active low which means

* ON - turns off the output
* OFF - turns on the output

The board works correctly but the software is outdated.
The [provided software](https://www.waveshare.com/wiki/RPi_Relay_Board)
only works upto RPi 4.
This outdated software uses
[gpiod library](https://www.acmesystems.it/libgpiod)
which doesn't work for RPi 5.

However, we can use python gpiozero pip package to use the board

The package can either be installed at the system level or
inside python virtual environment.

```bash
$sudo apt install python3-gpiozero
This installs gpiozero==2.0.1 in the system site packages
```

### TODO

At the moment LEDs are being used to control the channels but
LEDs draw a lot of current. Is there a low-power way to
activate the channels?

## References

* [RPi 5 pinout guide](https://www.twicea.com/blog/learn-raspberry-pi-5-pinout-in-this-in-depth-comprehensive-guide)

### Note

[gpiod library doesn't work](https://www.acmesystems.it/libgpiod).
Use **gpiozero** package instead.
