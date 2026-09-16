# Custom sensors
The Plant Controller is by default able to be connected to and [configured for](../documentation/software/config/plant_config.md) the [DF Robot soil sensor](../documentation/hardware/components/dfr_soil_sensor.md) and the [STEMMA soil sensor](../documentation/hardware/components/stemma_soil_sensor.md). It is possible though to add new custom sensors to the Plant Controller.

This can be done by adding new drivers for the already existing sensor types (see [plant configuration](../documentation/software/config/plant_config.md) and the source code docs for the [sensor modules](../../../api/plant_controller/sensors/index.md)), but it is also possible to add entirely new nesor hardware to the as long as it adheres to a couple of restrictions.

## Custom sensor communication protocol
All new sensors connected to the Plant Controller must either communicate via the MODUS RTU protocol or the I2C protocol.

If communicating over MODBUS RTU, make sure that the new sensor is configured with

- a baudrate of 9600
- a bytesize of 8
- no parity
- 1 stopbit

If communicating over I2C, make sure that you have the correct cable to connect it to the STEMMA QT port on the greenhouse sensors, and that the new sensors address doesn't conflict with that of the [greenhouse light sensor](../documentation/hardware/components/ada_as7341.md) and [greenhouse air sensor](../documentation/hardware/components/ada_sht45.md).

## Custom sensor power draw
If MODBUS RTU based sensors need 5V power, either make sure that the total power of all sensors connected to the Plant Controllers 5V power line doesn't exceed 5W OR supply the sensor with power externally.

## Coding the custom sensor module
There is a standard API for new sensor modules that should be followed to ensure proper functionality. See the source code doces for [sensor modules](../../../api/plant_controller/sensors/index.md) and the other sensors for API guidance and inspiration, and the source docs for [communication procotols](../../../api/plant_controller/com_bus.md) for understanding of the communication busses.