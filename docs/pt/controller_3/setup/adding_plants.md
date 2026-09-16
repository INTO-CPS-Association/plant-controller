# Adding plants to the Plant Controller
The Plant Controller is designed to support up to 4 plants. A "plant" in this case is something that is senseable and needs watering, and can, in theory, be anything from a single small house plant, to a bed of multiple plants of varying sizes and species. The physicality of the biological plant or plants is up to the implementer and the use case.

The Plant Controller really only knows about connected sensors and actuators, which is what defines the plant to it.

So, to add a new plant, connect a new [pump](../documentation/hardware/components/ad20p-1230e_pump.md) to an empty coil in the [relay](../documentation/hardware/components/cs-io404.md), connect any [new sensors](custom_sensors.md) to the MODBUS bus and/or the I2C bus as needed, and add new [plant](../documentation/software/config/plant_config.md) and [watering schedule](../documentation/software/config/watering_schedule.md) configs in the config directories. Then, if need be, run any neccesary setup actions with the [setup utility](../documentation/software/plant_controller/cli.md).

With all that done, the new plant is connected.