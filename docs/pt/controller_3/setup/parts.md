# Parts

The parts for the controller are divided into two groups: the mandatory
**core controller**, and the **peripherals**. The core is everything needed to
connect one or more plants to the system, along with the sensors for the
greenhouse. Peripherals are the sensors and actuators connected per plant —
you'll need one pump and at least one soil sensor per plant you intend to
connect.

Wiring for the RS485 MODBUS bus, optional balancing resistors and terminal
blocks for connecting raw wires are not included in the lists below.

!!! note "Prices"
    Prices were collected in mid-2026 from the listed (mostly Danish/EU)
    vendors and converted to DKK at $1 = 6.44 DKK and €1 = 7.47 DKK. Expect
    them to have drifted, and substitute local vendors as convenient — apart
    from the specific sensor and relay modules, most parts are generic.

## Choosing peripherals

For soil sensing there are two supported options:

- **Adafruit STEMMA Soil Sensor** (I2C) — cheapest option, measures soil
  moisture only. All STEMMA soil sensors share the same I2C address, so
  connecting more than one requires a TCA9548A I2C multiplexer (one
  multiplexer serves up to 7 soil sensors, as one port is used for the bus).
  Getting the multiplexer is recommended even for a single sensor, as it also
  keeps the setup extendable with other I2C peripherals.
- **DFRobot RS485 Soil Sensor** (MODBUS) — measures soil temperature,
  moisture *and* electrical conductivity. More expensive, but the recommended
  choice for Digital Twin work, as it gives multiple sensed parameters per
  plant and the sensors sit on the shared RS485 bus without extra hardware.

For watering, each plant needs one **AD20P-1230E 12V submersible pump**,
switched by the CS-IO404 relay module in the core, plus PVC tubing from the
water tank to the plant.

The controller software is modular: other I2C or MODBUS sensors and pumps can
be used by writing a small driver module — see the
[Software API Reference](../../../api/plant_controller/index.md).

## Core controller

| Qty | Name | Description | Vendor | Unit Price | Cost (DKK) |
|-----|------|-------------|--------|------------|------------|
| 1 | [Raspberry Pi 5 - 4GB](https://raspberrypi.dk/produkt/raspberry-pi-5-4-gb/) | Single board computer - core processing unit | RaspberryPi.dk | 909.00 DKK | 909.00 |
| 1 | [Raspberry Pi 27W USB-C PSU](https://raspberrypi.dk/produkt/raspberry-pi-stroemforsyning-usb-c-eu-5v-5a-hvid/) | Power supply for Raspberry Pi 5 | RaspberryPi.dk | 119.00 DKK | 119.00 |
| 1 | [SANDISK Ultra microSD - 128GB](https://www.proshop.dk/Hukommelseskort/SANDISK-Ultra-microSDSD-140MBs-128GB/3120859) | Removable persistent memory for the Raspberry Pi 5 | PROSHOP | 169.00 DKK | 169.00 |
| 1 | [Adafruit AS7341](https://www.adafruit.com/product/4698) | Light spectrum sensor for sensing greenhouse light | Adafruit | $18.95 | 122.04 |
| 1 | [Adafruit SHT45](https://www.adafruit.com/product/5665) | Air temperature and humidity sensor for sensing greenhouse environment | Adafruit | $12.50 | 80.50 |
| 1 | [CS-IO404](https://www.dfrobot.com/product-2349.html) | 4-channel relay module for pump actuation | DFRobot | $27.90 | 179.68 |
| 1 | [USB to RS485 Module](https://www.dfrobot.com/product-2189.html) | RS485 connection for the Raspberry Pi 5 | DFRobot | $8.50 | 54.74 |
| 1 | [12V/1A PSU](https://www.proshop.dk/Baerbar-Oplader/Deltaco-power-adapter/3370145) | Power supply for relay and water pumps | PROSHOP | 62.00 DKK | 62.00 |
| 1 | [STEMMA QT cable - 50mm](https://www.adafruit.com/product/4399) | I2C bus cable for daisy chaining greenhouse sensors | Adafruit | $0.95 | 6.12 |
| 1 | [STEMMA QT JST SH 4-pin cable](https://www.adafruit.com/product/4397) | I2C cable for connection to the Raspberry Pi 5's GPIO pins | Adafruit | $0.95 | 6.12 |
| 1 | [DC socket 5.5/2.1mm 1m](https://botland.store/dc-plugs/3507-dc-socket-5521mm-with-1-m-wire-5904422349295.html) | DC socket for connecting 12V PSU to CS-IO404 and pumps | BOTLAND | €1.50 | 11.21 |

Total: **1719.41 DKK**

## Peripherals (per plant)

### Pump

| Qty | Name | Description | Vendor | Unit Price | Cost (DKK) |
|-----|------|-------------|--------|------------|------------|
| 1 | [AD20P-1230E](https://botland.store/pumps/14873-electric-liquid-pump-ad20p-1230e-12v-240lh-5904422342739.html) | Submersible 12V pump | BOTLAND | €10.90 | 81.42 |
| 1 | [DC plug 5.5/2.1mm 1.5m](https://botland.store/wires-and-power-connectors/1831-plug-dc-55-21mm-with-cable-15m-5904422356163.html) | DC plug for connecting pump to relay | BOTLAND | €0.90 | 6.72 |
| 1m* | [PVC tube, 5m x 8mm](https://www.biltema.dk/baad/vvs/slanger/pvc-slanger/pvc-slange-5-m-x-8-mm-2000060031) | PVC tubing for moving water | Biltema | 32.90 DKK | 6.58* |

*Assumes the pump must move the water 1 meter from water tank to plant. For
each 5 m of tubing needed across all pumps, a cost of 32.90 DKK is incurred.

Total, one pump: **121.04 DKK**
Total, three pumps, max 1.6 m pumping distance: **297.32 DKK**

### STEMMA Soil Moisture Sensor

| Qty | Name | Description | Vendor | Unit Price | Cost (DKK) |
|-----|------|-------------|--------|------------|------------|
| 1 | [Adafruit STEMMA Soil Sensor](https://www.adafruit.com/product/4026) | Moisture sensor for plant soil | Adafruit | $7.50 | 48.30 |
| 1 | [Sparkfun Flexible Qwiic to STEMMA Cable - 500mm](https://opencircuit.dk/product/flexible-qwiic-to-stemma-cable-500mm) | Soil sensor connector | Opencircuit | €4.20 | 31.37 |
| (1) | [Adafruit PCA9548](https://www.adafruit.com/product/5626) | I2C multiplexer | Adafruit | $6.95 | (44.76) |
| (1) | [STEMMA QT cable - 50mm](https://www.adafruit.com/product/4399) | I2C bus connector to multiplexer | Adafruit | $0.95 | (6.12) |

The multiplexer (parenthesized) is necessary when connecting more than one
STEMMA soil sensor, and recommended in any case for extendability — one
multiplexer per 7 soil sensors.

Total, one sensor: **79.67 DKK**
Total, one sensor, extendable: **130.55 DKK**
Total, seven sensors: **608.57 DKK**

### RS485 Soil Temperature, Moisture, EC Sensor

| Qty | Name | Description | Vendor | Unit Price | Cost (DKK) |
|-----|------|-------------|--------|------------|------------|
| 1 | [RS485 Soil Temperature, Moisture, EC Sensor](https://www.dfrobot.com/product-2817.html) | Multiparameter sensor for plant soil | DFRobot | $39.00 | 251.16 |

Total: **251.16 DKK**

## Example configurations

### Single plant, moisture only, unextendable

- Core controller: 1719.41 DKK
- 1x Pump: 121.04 DKK
- 1x STEMMA Soil Sensor: 79.67 DKK

Total: **1920.12 DKK**

### Single plant, moisture only

- Core controller: 1719.41 DKK
- 1x Pump: 121.04 DKK
- 1x STEMMA Soil Sensor, extendable: 130.55 DKK

Total: **1971 DKK**

### Single plant, multiple sensed parameters

*(Recommended minimal configuration)*

- Core controller: 1719.41 DKK
- 1x Pump: 121.04 DKK
- 1x RS485 Soil Sensor: 251.16 DKK

Total: **2091.61 DKK**

### Three plants, moisture only

- Core controller: 1719.41 DKK
- 3x Pump: 297.32 DKK
- 3x STEMMA Soil Sensor: 289.89 DKK

Total: **2306.62 DKK**

### Three plants, multiple sensed parameters

*(Recommended 3 plant configuration)*

- Core controller: 1719.41 DKK
- 3x Pump: 297.32 DKK
- 3x RS485 Soil Sensor: 753.48 DKK

Total: **2770.21 DKK**

---

Once the parts have arrived, continue to [Assembly](assembly.md).
