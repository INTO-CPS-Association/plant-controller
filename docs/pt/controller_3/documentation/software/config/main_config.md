# Main Configuration
The main config file should be located at `~/.plant_controller/config.toml`.

Currently, it is only used to setup the database connection.

It should contain this:
```toml
[database]
name = "<DATABASE_NAME>"
host = "<HOST_ADDRESS>"
token = "<DATABASE_TOKEN>"
```

- `<DATABASE_NAME>` is the name of the InfluxDB database meant to house the controllers sensor and actuation data-
- `<HOST_ADDRESS>` is the address of the InfluxDB server serving the database. If installed locally in the Plant Controller Raspberry Pi, this is usually `http://127.0.0.1:8181`.
- `<DATABASE_TOKEN>` is an InfluxDB token with read and write access to the database.