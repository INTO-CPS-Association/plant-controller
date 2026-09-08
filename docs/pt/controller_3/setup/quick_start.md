# Introduction
Following this guide will give you a fully functional minimal setup of the latet version of the Plant Controller, running on a dedicated **Raspberry Pi 5**, and monitoring and controlling **1 plant**.

## Alternative setups
The Plant Controller can be set up to monitor and control multiple plants, using different sensors, and running on alternative hardware.
If it's your first time setting up version 3 of the Plant Controller, it is advised to follow this quick start quide to get a sense of the test kit before pursuing an alternative setup.
That being said, guides for alternative setups can be found [here](custom_setups.md).

# Requirements
To follow this guide you'll need some Hardware to run the controller on, access to some Software necessary to run the controller, and a handfull of tools necessary for the construction and installation of the plant controller.

You'll also need an internet connection, and a trusted LAN that you can connect both the Controller and you extra installation computer to.

## Hardware
- 1 x [Raspberry Pi 5, with at least 4GB ram](../documentation/hardware/components/rpi5.md)
- 1 x [Raspberry Pi USB C power supply](../documentation/hardware/components/rpipsu.md)
- 1 x [micro SD card with at least 128 GB space](../documentation/hardware/components/sdcard.md)
- 1 x [Adafruit AS7341 light sensor](../documentation/hardware/components/ada_as7341.md)
- 1 x [Adafruit SHT45 air temperature and humidity sensor](../documentation/hardware/components/ada_sht45.md)
- 1 x [DF-Robot soil sensor](../documentation/hardware/components/dfr_soil_sensor.md)
- 1 x [CS-IO404 4-channel relay module](../documentation/hardware/components/cs-io404.md)
- 1 x [USB to RS485 module](../documentation/hardware/components/usb_to_rs485.md)
- 1 x [12V 1A power supply with 5.5/2.1mm barrel plug connecter](../documentation/hardware/components/12v_1a_psu.md)
- 1 x [AD20P-1230E submersible pump](../documentation/hardware/components/ad20p-1230e_pump.md)
- 1 x [5.5/2.1mm barrel plug with 1m leads](../documentation/hardware/components/barrel_plug.md)
- 1 x [5.5/2.1mm barrel socket with 1m leads](../documentation/hardware/components/barrel_socket.md)
- 2 x [120 Ohm resistors](../documentation/hardware/components/term_resistor.md)
- 1 x [STEMMA QT cable](../documentation/hardware/components/qt_cable.md)
- 1 x [STEMMA QT to JST SH 4-pin cable](../documentation/hardware/components/qt_to_jst.md)
- 4 x insulated wire, each in a different color, length dependent on setup. In this guide we use red, black, blue and yellow wire.
- 4 x [2 pole, 2 to 4 lever wire connectors](../documentation/hardware/), or similar.

## Software
- The Raspberry Pi Imager, available from [Rapsberry pi's website](https://www.raspberrypi.com/software/)

## Tools
- One extra computer for setup and testing, able to run the Raspberry Pi Imager, and preferably a browser and some way to run SSH. This guide assumes that the extra computer is running a Linux OS.
- A way to connect a micro SD card to the above computer, either via USB dongle or directly in a port in the computer
- A small flat head screwdriver
- A pair of cutters for cutting and stripping wire
- A container capable of holding at least a liter of water
- A measuring cup or similar, able to measure water in milliliters in at least 10 ml increments
- (Optionally, a screen and keyboard able to be connected to the Raspberry Pi. Unless you have complete trust and controll over you LAN, this is advised.)
- (Optionally a cordless drill for twisting wire.)

# Installation
The installation is split into two parts, installing the software on the Raspbery Pi, and assembling the hardware around the Raspberry Pi. Software installation will come with some waiting time - during these times it is possible to assemble hardware not directly connected to the Raspberry Pi.

## Software
### Install Raspberry Pi OS
Download the [Rasperry Pi Imager](https://www.raspberrypi.com/software/) to the extra computer. (See their guide on [how to use the installer](https://www.raspberrypi.com/documentation/computers/getting-started.html#imager-install), if need be.)

Connect the micro SD card to the extra computer.

Run the Raspberry Pi Imager to start the installation process.

Choose "Raspberry Pi 5" as the device.

If you have the optional screen and keyboard for the Raspberry Pi, choose "Raspberry Pi OS (64-bit)" for the OS. Otherwise choose "Raspberry Pi OS Lite (64-bit)".

Choose the connected micro SD card as the storage.

Customize your Raspberry Pi OS as desired, making sure to:
- choose a hostname for the Raspberry Pi (for example "plant-controller")
- choose your localization
- set a username and password
- input your LAN's Wi-Fi credentials (if you are not using a wired connection)
- enable SSH connectivity, if you DON'T have a screen and keyboard for the Raspberry Pi

NOTE: If you don't have a screen and keyboard for your Raspberry Pi, and can't connect to your Raspberry Pi through SSH over your LAN for some reason, enable Raspberry Pi Connect. This will allow you to connect to the Raspberry Pi over a USB connection instead.

Finally, set imager options and start writing the OS to the micro SD card. This will erase all things previously stored on the micro SD card before writing the OS and will take a couple of minutes.

When it is done, eject the micro SD card (if it hasn't already been ejected), disconnect it from the computer, and insert it into the Raspberry Pi OS.

Boot up the Raspberry Pi (connecting the screen and keyboard to it beforehand if available).

If you installed the Raspberry Pi OS with a desktop environment and have a screen and keyboard connected to it, put away the extra computer; it won't be needed for the rest of this guide. Then, open a terminal.

If you installed the Raspberry Pi OS Lite you'll have to connect to the Raspberry Pi over SSH from the extra computer. In the future, when you are instructed to open a new terminal, do it by SSH'ing in from the extra computer in a new terminal.

From the terminal, ensure that the Raspberry Pi is updated by running:

```bash
sudo apt-get update -y && sudo apt-get upgrade -y
```

When everything is updated continue to the next step.

### Install the database

The controller uses **InfluxDB 3.0 or later** to store measurements and
watering events.

The default OS kernel for the Raspberry Pi 5 uses a memory page size of
16k, but InfluxDB 3 assumes a page size of 4k. Before installing the
database on a Raspberry Pi 5, switch to the 4k kernel by setting
`kernel=kernel8.img` in `/boot/firmware/config.txt`:

```bash
echo "kernel=kernel8.img" | sudo tee -a /boot/firmware/config.txt
sudo shutdown -r now
```

This reboots the Raspberry Pi and terminates any SSH connection to the machine — give it
some time, then reconnect.

Install InfluxDB 3:

```bash
curl -O https://www.influxdata.com/d/install_influxdb3.sh \
&& sh install_influxdb3.sh
```

Choose the local install, and decline when the install script asks whether to
start the server at the end. Then start the server yourself:

```bash
influxdb3 serve --node-id node0
```

With the server running, create the admin token:

```bash
influxdb3 create token --admin
```

Note the token down — it is referred to as `<ADMIN_TOKEN>` below, and is
needed in the controller's config file. Then create the database for the
controller:

```bash
influxdb3 create database --token <ADMIN_TOKEN> --retention-period 7d plant-controller
```

Here the retention period is set to 7 days to avoid gumming up the
controller's persistent storage, and the database name to `plant-controller`,
which is the default in the config file. Both can be changed freely, as long
as the config file is updated accordingly.

!!! note
    The database server does not start automatically. Make sure
    `influxdb3 serve --node-id node0` is running whenever you run the
    controller — for example by running it in a detached terminal
    multiplexer session, or by setting it up as a systemd service.

### Install the controller software

First, get the source code onto the Raspberry Pi, either by cloning it from
GitHub or by SCP'ing it over from the extra computer:

```bash
git clone https://github.com/DisasterlyDisco/plant-controller.git
```

In the following, `<src>` refers to the full path of the cloned repository.

Install pip and venv support:

```bash
sudo apt-get install -y python3-pip python3-venv
sudo apt install --upgrade python3-setuptools
```

Create a virtual environment (here in the home directory) and activate it:

```bash
python -m venv .venv --system-site-packages
source .venv/bin/activate
```

### Install Adafruit Blinka

Adafruit Blinka provides the Python API for the Raspberry Pi's GPIO header,
which the controller uses for I2C communication with the Adafruit sensor
modules. It cannot simply be installed with pip, as it needs to configure the
machine itself — Adafruit supplies a convenience script:

```bash
cd ~
pip install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo -E env PATH=$PATH python3 raspi-blinka.py
```

### Install remaining Python dependencies

With Blinka installed, install the rest of the Python requirements as normal:

```bash
cd <src>/pt/controller_3
pip install -r requirements.txt
```

## Hardware
### Connect the air sensors to the Raspberry Pi
Using the [STEMMA QT cable](../documentation/hardware/components/qt_cable.md), connect the [Adafruit AS7341 light sensor](../documentation/hardware/components/ada_as7341.md) to the [Adafruit SHT45 air temperature and humidity sensor](../documentation/hardware/components/ada_sht45.md). It doesn't matter which of the two ports on the sensors are used.

Then, connect the [STEMMA QT to JST SH 4-pin cable](../documentation/hardware/components/qt_to_jst.md) to the final port in the [Adafruit SHT45 air temperature and humidity sensor](../documentation/hardware/components/ada_sht45.md).

Finally, with the Raspberry Pi 5 POWERED OFF, connect 4 JST pins of the [STEMMA QT to JST SH 4-pin cable](../documentation/hardware/components/qt_to_jst.md) to the Raspberry Pi's GPIO pins ([pin layout](../documentation/hardware/components/rpi5.md)), depending on their color:
- Pin 1 <-> the red wire
- Pin 3 <-> the blue wire
- pin 5 <-> the yellow wire
- pin 9 <-> the black wire

### Create the RS485 bus
Both the DF-Robots soil sensor and the CS-IO404 relay connect to the Raspberry Pi via a RS485 bus wire pair. This bus wire pair is the primary way to connect reliable peripherals to the plant controller.

Measure out how far away you want the relay from the Raspberry Pi, taking into account that the 12 DC for the pump and relay must be connected near the relay, and that the pump will be getting its power from the relay. Take this length and multiply it by 1.5 for some slack - this will be the length of the RS485 bus. As a minimum though, it should be atleast 50 cm.

Take two lengths of insulated wire, one blue, the other yellow, cutting each to be the lenght of the bus. Then, twist them together, tightly. (A cordless drill is handy for this.)

Then, take two more lengths of insulated wire, one red, one black, cutting them to be about 20 cm. Also twist these together, tightly.

Now, strip one end of each of the four wires, about 11 mm.

Connect these stripped wires to the [USB to RS485 module](../documentation/hardware/components/usb_to_rs485.md), dependent on color:
- Black to GND
- Blue to B-
- Yellow to A+
- Red to 5V

Then, connect a [120 ohm resistor](../documentation/hardware/components/term_resistor.md) between B- and A+ in the USB to RS485 module. It might be necessary to trim the resistors legs to avoid it poking too far out.

With both twisted pairs connected to the USB to RS485 module, lay them out side by side, and cut the yellow and blue pair so it is as long as the red and black pair. Put the remaining yellow and blue pair aside for later.

Strip the other ends of each of the four wires, again about 11 mm.

Take two [2 pole, 2 to 4 lever wire connectors](../documentation/hardware/).

Connect the yellow and blue wires to the 2 connection side of the first 2 pole, 2 to 4 lever wire connector, blue to blue, yellow to orange.

Connect the red and black wires to the 2 connection side of the second 2 pole, 2 to 4 lever wire connector, black to blue, red to orange.

Now, take the [DF-Robot soil sensor](../documentation/hardware/components/dfr_soil_sensor.md). Connect it to the outer connectors of the 4 connector sides of the two 2 pole, 2 to 4 lever wire connectors, depending on sensors connector wires:
- blue to blue on the first connector
- yellow to orange on the first connector
- black to blue on the second connector
- red to orange on the second connector

With the soil sensor connected, strip both ends of the remaining yellow and blue wire pair that was previously set aside, again about 11 mm.

Connect one end to the remaining connections on the first 2 pole, 2 to 4 lever wire connector, blue to blue, yellow to orange.

Connect the other end to the [CS-IO404 4-channel relay module](../documentation/hardware/components/cs-io404.md), yellow to the terminal labelled A+, blue to the terminal labelled B-.

Finally, connect a 120 Ohm resistor from the A+ to the B- terminals on the CS-IO404 relay.

### Wire up the pump relay
TODO

### Setup the pumps
TODO

# Configuration
Before use, the plant controller needs to be configured for the current setup.

Make sure that all hardware and software is installed before continuing with the configuration.

## Setup config folder

All configuration lives in the `.plant_controller` subdirectory of the user's
home directory. Initialize it from the example implementation shipped with the
source code:

```bash
cp -r <src>/pt/controller_3/impl ~/.plant_controller
mv ~/.plant_controller/config.toml.example ~/.plant_controller/config.toml
```

## Configure database connection

Edit `~/.plant_controller/config.toml` and set the `token` value to the
`<ADMIN_TOKEN>` from earlier. If the database name, host or port differ from
the defaults (for instance if the database runs on another machine), update
them here too:

```toml
[database]
name = "plant-controller"
host = "http://127.0.0.1:8181"
token = "<ADMIN_TOKEN>"
```

## Configure connected plant
Each connected plant gets its own JSON file in
`~/.plant_controller/plants/`, declaring its sensors and its pump.
An example configuration made for this quick_setup is already included in the config folder. Rename it, removing the `.example` suffix and replacing `plant_name` with a useful identifier (`<PLANT_IDENTIFIER>`)for the connected plant (note this name down for later):

```bash
mv ~/.plant_controller/plants/plant_name.toml.example ~/.plant_controller/plants/<PLANT_IDENTIFIER>.toml
```

Watering of the plant is done following a schedule. Watering schedules live in `~/.plant_controller/pump_schedules/`, one JSON file per plant. This folder comes with an example schedule just like the plant configuration. As with the plant config, rename it, removing the `.example` suffix and replacing `plant_name` with the previously chosen identifier, making sure that they are the same:

```bash
mv ~/.plant_controller/pump_schedules/plant_name.toml.example ~/.plant_controller/pump_schedules/<PLANT_IDENTIFIER>.toml
```

## Change MODBUS address of soil sensor
The connected [soil sensor](../documentation/hardware/components/dfr_soil_sensor.md) has the standard MODBUS address of 1 from the factory. This should be changed to avoid address conflicts if adding mores sensors in the future.

To do this, first disconnect the 12V DC power supply, and check that CS-IO404 is powered off (no lights on in the relay).

With that done, ensure that the InfluxDB database is running, starting it if it isn't.

Then, in a seperate terminal, source the previously setup python virtual environment and then start the plant_controller in setup mode:

```bash
cd <src>/pt/controller_3/src
python -m plant_controller setup
```

From within the setup utility, change the sensor address by writing `<PLANT_IDENTIFIER>.soil.change_id` (substituting `<PLANT_IDENTIFIER>` for the identifier previously chosen for the conencted plant), hitting enter, and following the guide as presented by the program.

If the id change was successful, exit the setup porgram, and reconnect power to the CS-IO404 relay.

## Calibrate pump
The pump needs to be calibrated after installation to ensure proper water dosage.

Before doing the calibration, the whole plant controller system should be in its final location and configuration - moving pumps and pump outlets after calibration invalidates it.

In preperation, remove the plant from under the pump outlet, and replace it with an empty vessel able to hold 1 liter of water.

When ready, make sure that the database is running and that the python virutal environment has been sourced, then start the plant_controller in setup mode:

```bash
cd <src>/pt/controller_3/src
python -m plant_controller setup
```

From here, start calibration by writing `<PLANT_IDENTIFIER>.pump.calibrate` (substituting `<PLANT_IDENTIFIER>` for the identifier previously chosen for the conencted plant), hitting enter, and following the on screen guide.

When the pump is sufficiently calibrated, replace the plant under the pump outlet.

# Running the controller
If all previous steps have been followed the controller should now be fully functional.

To run it, ensure that the database is running and that the python virtual environment has been sourced, then:

```bash
cd <src>/pt/controller_3/src
python -m plant_controller run
```

The controller now monitors and waters the connected plant, and the web interface is accesible on port 8099 of the Raspberry Pi.

If connected to the Raspebrry Pi over LAN, this interface can be found by typing in `<CONTROLLER_IP>:8099` in a browser from another computer on the same LAN, where `<CONTROLELR_IP>` is the IP of the Raspberry Pi.

If running the Raspberry Pi with a desktop environmnet and a connected screen and keyboard, the web interface is available from within the Raspberry Pi by typing in `localhost:8099` in the Raspberry Pi's browser.
