# References

## UIO case study

**Ref Paper**: Eduard Kamburjan et al., GreenhouseDT: An Exemplar for Digital Twins...

### Physical Twin Description

The physical twin of GreenhouseDT consists of a greenhouse with three shelves. On each of the two top shelves there are two plants, each equipped with a moisture sensor. Each shelf is equipped with a combined humidity/temperature sensor, and the whole greenhouse has a light sensor.
As for actuators, each plant is connected to one water pump, which pumps water from a basin at the bottom shelf of the greenhouse.
Each shelf has a Raspberry Pi, which collects and relays data from the sensors on this shelf. to a time-series database that acts as an interface to the digital twin. Similarly, each pump is connected to a Raspberry Pi that receives commands to water its associated plant.
The connections of the Raspberry Pi can be configured locally, but must adhere to the information of the asset model. The light sensor is handled by the minicomputer of the top shelf.

**Additional Information Sources**: discussion with Riccardo Sieve and Einar Johnsen

repositories are:

1. [complete codebase](https://github.com/N-essuno/greenhouse_twin_project)
   -- comprehensive docs and code base (but last updated in Feb, 2024)
2. [PT setup](https://github.com/sievericcardo/greenhouse_dt_project)
3. [water pump code](https://github.com/MarcoAmato/greenhouse_actuator)
4. [data collector for PT](https://github.com/N-essuno/greenhouse-data-collector)
   -- really good quality; see
   [sample data](https://github.com/sievericcardo/greenhousedt_frontend/blob/main/basic_data.csv);
   [InfluxDB config](https://github.com/sievericcardo/greenhouse-data-collector/blob/master/collector/config.ini.example)
5. [frontend website](https://github.com/sievericcardo/greenhousedt_frontend)
6. [create greenhouse DT from SMOL program](https://github.com/N-essuno/smol_scheduler)

### Blogs, Vlogs etc

1. [Using DF Robot Products](https://community.dfrobot.com/makelog-313566.html?tracking=660bd90501412)