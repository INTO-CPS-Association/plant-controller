# Requirements

You'll need an internet connection, and a trusted LAN that you can connect
both the controller and your extra installation computer to.

## Hardware

| Qty | Component |
|----:|-----------|
| 1 | [Raspberry Pi 5, at least 4 GB RAM](../documentation/hardware/components/rpi5.md) |
| 1 | [Raspberry Pi USB-C power supply](../documentation/hardware/components/rpipsu.md) |
| 1 | [Micro SD card, at least 128 GB](../documentation/hardware/components/sdcard.md) |
| 1 | [Adafruit AS7341 light sensor](../documentation/hardware/components/ada_as7341.md) |
| 1 | [Adafruit SHT45 air temperature and humidity sensor](../documentation/hardware/components/ada_sht45.md) |
| 1 | [DF-Robot soil sensor](../documentation/hardware/components/dfr_soil_sensor.md) |
| 1 | [CS-IO404 4-channel relay module](../documentation/hardware/components/cs-io404.md) |
| 1 | [USB to RS485 module](../documentation/hardware/components/usb_to_rs485.md) |
| 1 | [12V 1A power supply with 5.5/2.1 mm barrel plug connector](../documentation/hardware/components/12v_1a_psu.md) |
| 1 | [AD20P-1230E submersible pump](../documentation/hardware/components/ad20p-1230e_pump.md) |
| 1 | [5.5/2.1 mm barrel plug with 1 m leads](../documentation/hardware/components/barrel_plug.md) |
| 1 | [5.5/2.1 mm barrel socket with 1 m leads](../documentation/hardware/components/barrel_socket.md) |
| 2 | [120 Ohm resistors](../documentation/hardware/components/term_resistor.md) |
| 1 | [STEMMA QT cable](../documentation/hardware/components/qt_cable.md) |
| 1 | [STEMMA QT to JST SH 4-pin cable](../documentation/hardware/components/qt_to_jst.md) |
| 4 | Insulated wire, each a different color (this guide uses red, black, blue and yellow), length dependent on setup |
| 4 | [2 pole, 2-to-4 lever wire connectors](../documentation/hardware/components/lever_connector.md), or similar |
| 1 | [PVC tubing, length dependent on setup](../documentation/hardware/components/pvc_tubing.md) |
| 1 | [Water reservoir, for holding water for watering](../documentation/hardware/components/water_tank.md) |

## Software

- The Raspberry Pi Imager, available from [Raspberry Pi's website](https://www.raspberrypi.com/software/)

## Tools

- One extra computer for setup and testing, able to run the Raspberry Pi
  Imager, and preferably a browser and some way to run SSH. This guide assumes
  that the extra computer is running a Linux OS.
- A way to connect a micro SD card to the above computer, either via USB
  dongle or directly in a port on the computer.
- A small flat head screwdriver.
- A pair of cutters for cutting and stripping wire.
- A container capable of holding at least a liter of water.
- A measuring cup or similar, able to measure water in milliliters in at least
  10 ml increments.
- (Optionally, a screen and keyboard able to be connected to the Raspberry Pi.
  Unless you have complete trust and control over your LAN, this is advised.)
- (Optionally, a cordless drill for twisting wire.)

---

[**Assmeble the hardware**](./qs_hardware.md)