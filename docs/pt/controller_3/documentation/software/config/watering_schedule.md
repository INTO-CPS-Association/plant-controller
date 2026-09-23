# Watering schedules
Each plant connected to the Plant Controller must have a schedule that defines when and how the plant is to be watered by the Controller.

This schedule is located in the `pump_schedules/` subdirectory of the config directory (see the [config overview](index.md) for its location) and must be named the same as the related plants [plant config file](plant_config.md).

Each schedule is a JSON file which must contain at least a `type` and a `schedule` field. The `type` field describes which type of schedule it is, and is used to load the correct schedule driver code at runtime. The contents of the `schedule` field is type specific, and is used define the plant specific schedule parameters.

Currently, only one type of schedule comes prepackaged with the `plant_controller` source code, the `daily` schedule ([source code docs](../../../../../api/plant_controller/pump_schedules/daily.md)). When using this schedule, the plant is watered at the set times for the set amounts of ml each day. An example of the config for this schedule can be seen below.

```json
{
    "type": "daily",
    "schedule": [
        {
            "time": "09:16:00",
            "dose": 100
        },
        {
            "time": "17:05:30",
            "dose": 120
        }
    ]
}
```

This schedule can be changed, either by editting the schedule file while the [`plant_controller`](../plant_controller/index.md) isn't running OR by using the [Web API](../web_api/index.md) during normal operation.

## Custom schedules
New schedule modules can be added to the `plant_controller` source code to allow for other types of schedules than the standard `daily` type. To do this, add a module with the type name and the necessary code to the `pump_schedules/` directory ***in the source code directory*** (see the [config overview](index.md) for its location) and update the schedule config file with the new type and necessary schedule parameters as needed for the new module.

It is advised to read the documentation for the source code of [schedules in general](../../../../../api/plant_controller/pump_schedules/index.md) and the [`daily` schedule specifically](../../../../../api/plant_controller/pump_schedules/daily.md) before creating your own custom schedules.
