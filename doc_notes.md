### index
Make it clear where 

# Setup

## General notes
Make steps as info scarce as possible. No undue info, tell users only what they need to know at each step, no more.
Give context as necessary, don't fronload.

Specify that this setup is meant for a clean installation of Raspbian on a Rpi 5, and that mileage may vary with other setups.

Consider renaming the home directory from .plant_controller to .plant-controller (hyphen instead of underscore)

## Overview
Have splash page be quicker to introduce building,
relegate project pitch to own page,
use simpler idealized example setup (either iconographic/diagram or low noise image)

## Assmebly

### Notes for wiring diagram

#### High level (currenlty missing)
Add a very high level overview of how things are connected. Same names as IBD blocks, but simpler connections.
Refer to PT-electrical-schematic.png in docs/pt/controller_2 for regerence

#### Low level (IBD)
Check if COM ports should be 0V or 12V
Give full names for colored wires
More descriptive connection names

### I2C connection
Give a diagram of where pins are on Rpi.
Give diagram of cable colors for Qwiik/QT connectors
Specify that STEMMA soil sensors can be connected to any port of the multiplexer BUT that the portnumber must be noted for later.

### MODBUS
Need link to indepth description of twisting, witring, wirechoices, end termination, n such.
A close up diagram and/or table for the connections from MODBUS sensor to RS485 to USB module.
Instruct that users connect the MODBUS bus and Soil sensors to RS485 to USB module BEFORE connecting the module to the Rpi.
Divide up into the mandatory steps (module to CSIO404), and peripheral steps (module to sensor)
"Just twist it and forget it"

### Power wiring for CSIO-404
It is very unclear from the explanation how this should be done. It can be done in many ways, but the ambiguity makes it frustrating to put together.

## Software Installation

Installation of Influx db unclear - what to do (start, custom config, install only)
Also, tell users to source bashrc after install.
Add that after starting server, token should be created in another tab.

Add systemd startup service to the pull request - explain its use in the installation.

Make sure user nows that plant name, plant config name and plant schedul name has to be the same for each plant.

### 4. Configure
How does the user configure the plant to use the DFRobot soil sensor?

### 5. Calibrate
Specify that the name "purple_ufo" in the setup example is the name given to a plant in the plant config.

### 6. Run
Mistakenly refers to the docs for the web_api python module as a way to understand the controllers REST API.

## the final step
Guidance through the webapi.
It is unclear what the "sensing" endpoint tells the user.
It is uncelar what "parameter" is for the /sensing/{unit}/{parameter} endpoint





