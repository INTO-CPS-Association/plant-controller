# Configure the controller

Before use, the plant controller needs to be configured for the current setup.
Make sure that all hardware and software is installed before continuing.

## Set up the config folder

All configuration lives in the `.plant_controller` subdirectory of the user's
home directory. Initialize it from the example implementation shipped with the
source code:

```bash
cp -r <src>/pt/controller_3/impl ~/.plant_controller
mv ~/.plant_controller/config.toml.example ~/.plant_controller/config.toml
```

## Configure the database connection

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

## Configure the connected plant

Each connected plant gets its own JSON file in
`~/.plant_controller/plants/`, declaring its sensors and its pump.
An example configuration made for this quick start is already included in the
config folder. Rename it, removing the `.example` suffix and replacing
`plant_name` with a useful identifier (`<PLANT_IDENTIFIER>`) for the connected
plant (note this name down for later):

```bash
mv ~/.plant_controller/plants/plant_name.json.example ~/.plant_controller/plants/<PLANT_IDENTIFIER>.json
```

Watering of the plant is done following a schedule. Watering schedules live in
`~/.plant_controller/pump_schedules/`, one JSON file per plant. This folder
comes with an example schedule just like the plant configuration. As with the
plant config, rename it, removing the `.example` suffix and replacing
`plant_name` with the previously chosen identifier, making sure that they are
the same:

```bash
mv ~/.plant_controller/pump_schedules/plant_name.json.example ~/.plant_controller/pump_schedules/<PLANT_IDENTIFIER>.json
```

## Change the MODBUS address of the soil sensor

The connected
[soil sensor](../documentation/hardware/components/dfr_soil_sensor.md) has the
standard MODBUS address of 1 from the factory. This should be changed to avoid
address conflicts if adding more sensors in the future.

To do this, first disconnect the 12V DC power supply, and check that CS-IO404
is powered off (no lights on in the relay).

With that done, ensure that the InfluxDB database is running, starting it if
it isn't.

Then, in a separate terminal, source the previously set up Python virtual
environment and then start the plant_controller in setup mode:

```bash
source ~/.venv/bin/activate
cd <src>/pt/controller_3/src
python -m plant_controller setup
```

From within the setup utility, change the sensor address by writing
`<PLANT_IDENTIFIER>.sensor.soil.change_device_id` (substituting `<PLANT_IDENTIFIER>` for the
identifier previously chosen for the connected plant), hitting enter, and
following the guide as presented by the program.

Make sure that the address chosen is not the same as the CS-IO404 relay; choosing an address above 32 will ensure that there is no conflict if following this guide.

If the id change was successful, exit the setup program, and reconnect power
to the CS-IO404 relay.

## Calibrate the pump

The pump needs to be calibrated after installation to ensure proper water
dosage.

!!! warning
    The whole plant controller system should be in its final location and
    configuration before calibrating — moving pumps and pump outlets after
    calibration invalidates it.

In preparation, remove the plant from under the pump outlet, and replace it
with an empty vessel able to hold 1 liter of water.

When ready, make sure that the database is running and that the Python virtual
environment has been sourced, then start the plant_controller in setup mode:

```bash
source ~/.venv/bin/activate
cd <src>/pt/controller_3/src
python -m plant_controller setup
```

From here, start calibration by writing
`<PLANT_IDENTIFIER>.pump.calibrate` (substituting `<PLANT_IDENTIFIER>` for the
identifier previously chosen for the connected plant), hitting enter, and
following the on screen guide.

When the pump is sufficiently calibrated, replace the plant under the pump
outlet.

---

[**Run the controller**](qs_run.md)