# Plant Controller - I

Please see the [SCHEMATICS](SCHEMATICS.md) to get an overview of
the electrical and physical layout of the plant controller system.

## Initial Setup

Enable I2C interface in RPi OS configuration.

```bash
sudo raspi-config nonint do_i2c 0
```

You can check the list of I2C devices connected to a RPi using

```bash
sudo apt-get install i2c-tools
i2cdetect -y 1
```

## Configuration

The controller is configured using the `config.yaml` file. A template is provided in config/config.yaml.template.
You can copy it to `config/config.yaml` and edit it according to your setup.

The configuration file contains the following sections:

- Services: containing influxdb and STOMP services.
- Plant: containing sensors and actuators.

### Configuration Details

The `config.yaml.template` file contains the following structure:

```yaml
services:
  internal:
    influxdb:               # InfluxDB configuration for storing sensor data
      bucket: "controller-1"
      token: "xxxx"         # Your InfluxDB access token
      url: "https://influxdb.example.com"
      org: "plants"
  external:
    stomp:                  # STOMP message broker configuration
      url: "localhost.com"
      user: "admin"
      pass: "admin"
      port: "1234"
      topics:               # Map of STOMP topics to pump IDs
          "actuator.1.water": pump_1
          "actuator.2.water": pump_2
          "actuator.3.water": pump_3

plant:
  sensors:
    seesaw:                 # Adafruit Seesaw soil moisture sensors
      moisture_0:           # First moisture sensor
        port: 0             # TCA9548A multiplexer port
        addr: 0x36          # I2C address
      moisture_1:           # Second moisture sensor
        port: 1
        addr: 0x36
      moisture_2:           # Third moisture sensor
        port: 2
        addr: 0x36
    sht45:                  # Temperature & humidity sensor
      port: 6               # TCA9548A multiplexer port
      mode: NOHEAT_HIGHPRECISION  # Sensor operation mode
    as7341:                 # Light spectrum sensor
      port: 7               # TCA9548A multiplexer port
    sampling_period: 60     # Sensor reading interval in seconds
    
  actuators:
    pump_1:                 # First water pump
      relay: one            # Relay name on the Automation HAT
      schedule: "10:15"     # Daily watering time (HH:MM)
      on_duration: 15       # Pump turn on time
    pump_2:                 # Second water pump
      relay: two
      schedule: "14:30"
      on_duration: 6        # Pump turn on time
    pump_3:                 # Third water pump
      relay: three
      schedule: "10:15"
      on_duration: 10       # Pump turn on time
```

### Configuration Sections

1. **Services**
   - **internal/influxdb**: Configuration for InfluxDB time series database.
   - **external/stomp**: Configuration for STOMP message broker to receive remote commands.

2. **Plant**
   - **sensors**: Configuration for all connected sensors.
     - **seesaw**: Soil moisture sensors.
     - **sht45**: Temperature and humidity sensor.
     - **as7341**: Light spectrum sensor.
     - **sampling_period**: How often sensors are read (in seconds).
   - **actuators**: Configuration for water pumps.
     - Each pump has a relay name and watering schedule.

### Note

- The I2C addresses must match your physical hardware configuration.
- Valid relay names are "one", "two", and "three" as defined by the Automation HAT.
- Relay names must match the actual relay that the pump is connected to.
- A sensor's port corresponds to the TCA9548A multiplexer port it is connected to.

## Run

Please execute the following commands to start the controller.

```sh
# create and load virtual environment
pip install -r requirements.txt
python controller-1.py
```

### Caveat

1. Accessing the I2C bus in parallel in two programs leads to errors.
   Use multiplexer for such a purpose.
1. The I2C bus communication may not be very robust.
   The sensors produce errors sometimes in an hour and sometimes in
   a day. So python exception checking is required.

## Process Manager

PM2 is a process manager for applications, which allows them to stay alive,
if they exits unexpectedly due to errors. The output and errors get stored
in a log file.

To install PM2, run the following command:

```bash
npm install -g pm2
```

Then you can start the controller using PM2:

```bash
# create but do not load it
pm2 start controller-1.py --interpreter .venv/bin/python --restart-delay=60000 --log controller-1.log
```

The above command starts the `controller-1.py` script using
the Python interpreter from the virtual environment (`.venv`) and
restarts it after 60 seconds if it exits unexpectedly. The logs will
be stored in controller-1.log.
