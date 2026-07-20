# Plant Controller

A project to develop edge controllers and digital twins for plants.

This site collects documentation for the plant controller hardware and
the accompanying software.

## Hardware

Build documentation for each controller revision:

- [Controller 1](pt/controller_1/PARTS.md) — parts list,
  [assembly guide](pt/controller_1/assembly/ASSEMBLE.md) and
  [references](pt/controller_1/REFERENCES.md)
- [Controller 2](pt/controller_2/PARTS.md) — parts list
- [Controller 3](pt/controller_3/index.md) — the current revision

## Software

The controller 3 software (`plant_controller`) is documented in the
[API Reference](api/plant_controller/index.md). It is built around a
modular extension model: new sensors, pumps and pump schedules are added
as drop-in modules under `plant_controller.sensors`,
`plant_controller.pumps` and `plant_controller.pump_schedules`.
