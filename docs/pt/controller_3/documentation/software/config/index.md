# Configuration
The Plant Controller is configured with a combination of toml and json files located in `~/.plant_controller/`.
(Along these, the source code of the core python program `plant_controller` is meant to be easily extendable with custom submodules).
The general location of all config files can be seen in the diagram below.

![Deployment diagram of the custimizable files of the Plant Controller.](../../../images/deployment_diagram.png)

Config files should only ever be manually editted while the program isn't running.

- Overall configuration of the Plant Controller is described in the [`config.toml`](main_config.md).
- Each connected plant gets a seperate named config file in the directory [`plants/`](plant_config.md).
- The watering schedule for each plant is defined in the directory [`pump_schedules/`](watering_schedule.md).

The project repository contains example config files in the directory `pt/controller_3/impl/`.

