# Plant Configurations
For each plant connected the Plant Controller, a config file should be located in the `plants/` directory (see the [config overview](index.md) for its location).

The names of each of these files (which should end in `.json`) are used by the Plant Controller to identify the plant an all associated sensor readings and actuations.

In abstract it contains a list of all connected sensors and actuators associated with the named plant. A Generalized view of this can be seen below

```json
{
    "sensors": {
        "<SENSOR_NAME>": {
            "module": "<PYTHON_MODULE_NAME>",
            "class": "<PYTHON_CLASS_NAME>",
            "kwargs": { ... }
        },
        ...
    },
    "actuators": {
        "<ACTUATOR_NAME>": { ... },
        ...
    }
}
```

Each sensor is given a descriptive, plant unique name (`<SENSOR_NAME>`), the name of the python module and class containing the sensors driver source code (`<PYTHON_MODULE_NAME>` and `<PYTHON_CLASS_NAME>`, see the diagram in the [config overview](index.md) for where they are located), and any sensor specific key word args needed to initialize it. A plant can be configured with as little as no sensors (leave the `sensors` liste empty), and there is no upper bound (other than reason and the Plant Controllers physical limitations) for the number of sensors that can be configured for each plant.

Each actuator is defined similarly to the sensors, with a plant unique name, and actuator specific configuration. Currently, only one type of actuator is possible for the Plant Controller, the hardcoded `water_pump`. Each plant must contain this one actuator, and no other apart from it.

Below is an example config for a plant with a single sensor using the standard module and class for the [DFRobort soil sensor](../../hardware/components/dfr_soil_sensor.md), here named `soil`.

```json
{
    "sensors": {
        "soil": {
            "module": "df_robot_temp_moist_ec",
            "class": "DFRobotRS485SoilTemperatureHumidityECSensor",
            "kwargs": {
                "device_id": 1,
                "tbr": 10
            }
        }
    },
    "actuators": {
        "water_pump": {
            "calibration": {
                "slope": 0.02,
                "offset": 1.5
            },
            "coil_number": 0,
            "relay_address": 2
        }
    }
}
```

## Sensor configurations

### In build sensors
The source code for the Plant Controller comes with two standard sensor drivers, one each for the [DF Robot soil sensor](../../hardware/components/dfr_soil_sensor.md) and [STEMMA soil sensor](../../hardware/components/stemma_soil_sensor.md).

#### DF Robot soil sensor
When connecting a [DF Robot soil sensor](../../hardware/components/dfr_soil_sensor.md) to a plant, set its module to `df_robot_temp_moist_ec` and its class to `DFRobotRS485SoilTemperatureHumidityECSensor` ([source code docs](../../../../../api/plant_controller/sensors/df_robot_temp_moist_ec.md)).

The sensor accepts two `kwargs`:

- `device_id`: The MODBUS id of the sensor. Ranges from 1 to 253. If installing a newly bought sensor, this should be set to `1`.
- `tbr`: Time Between Reads of the sensor, in seconds. In practice, the time between finishing one read and beginning the next. Thus, if the sensor takes `read_time` to read from the sensor, the actual read frequency becomes 1 / (`tbr` + `read_time`).

!!! warning "Multiple newly bought DF Robot sensors"
    If multiple newly bought DF Robot soil sensors are to be connected to the plant controller it is important that each be configured, connected and setup ONE AT A TIME.
    Multiple devices cannot be connected to the MODBUS with the same device id.

    When configuring and connecting a newly bought DF Robot soil sensor, make sure to change its id using the [setup utility](../plant_controller/cli.md) of the Plant Controller.

#### STEMMA soil sensor
When connecting a [STEMMA soil sensor](../../hardware/components/stemma_soil_sensor.md) to a plant, set its module to `stemma` and its class to `MultiplexedStemma` ([source code docs](../../../../../api/plant_controller/sensors/stemma.md)).

The sensor accepts four `kwargs`:

- `multiplexer_address`: I2C address of the [STEMMA multiplexer](../../hardware/components/stemma_multiplexer.md) the STEMMA soil sensor is connected to.
- `multiplexer_port`: Port number of the port on the STEMMA multiplexer that the STEMMA soil sensor is connected to.
- `address`: I2C address of the STEMMA soil sensor.
- `tbr`: Time Between Reads of the sensor, in seconds. In practice, the time between finishing one read and beginning the next. Thus, if the sensor takes `read_time` to read from the sensor, the actual read frequency becomes 1 / (`tbr` + `read_time`).

### Custom sensors
Custom sensor drivers can be added to the Plant Controller, either by adding new module files with classes to the appropriate directory (see the diagram in the [config overview](index.md)), or by adding new classes to the already existing modules for the DFRobot and STEMMA soil sensors.

To use these custom drivers, simply set their module name and class name in the config for the sensor, and add any necessarry `kwargs` as needed for your custom module.

It is advised to read the documentation for the source code of the [sensor modules](../../../../../api/plant_controller/sensors/index.md) and [communication busses](../../../../../api/plant_controller/com_bus.md) before creating new custom sensor driver code.

## Pump configurations
Each plant must contain configuration for one pump, and each pump config must contain three parameters:

- `calibration`: Contains the parameters for the linear function used to map water dosage in ml to pumping time in seconds. Should be set to an initial value, and can afterwards be calibrated further with the [setup utility](../plant_controller/cli.md).
- `coil_number`: The number of the coil that this pump is connected to on the [relay](../../hardware/components/cs-io404.md).
- `relay_address`: MODBUS address/id of the relay that this pump is connected to.