# Relays for Greenhouses

The GPIO pin layout has changed in
[RPi 5](https://www.sunfounder.com/blogs/news/comprehensive-guide-to-the-pin-diagram-of-raspberry-pi-5-understanding-gpio-pins-and-their-functions).
Only
[gpiozero](https://gpiozero.readthedocs.io/en/stable/recipes.html) package.
works correctly with RPi 5.

## Digitlogger IoT Relay

This works really well without any static leakage problems, but has
only one effective relay. For the controlling the relay, we are using
one control signal. The control signal is connected to RPi 5 as follows.

* Pin-43: ground
* pin-36: control signal to IoT Relay

One channel can control all the motors.
It takes more current to drive all channels.

### TODO

At the moment LEDs are being used to control the channels but
LEDs draw a lot of current. Is there a low-power way to
activate the channels?

## References

* [RPi 5 pinout guide](https://www.twicea.com/blog/learn-raspberry-pi-5-pinout-in-this-in-depth-comprehensive-guide)
