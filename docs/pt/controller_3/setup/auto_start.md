# Auto start
To make the the Plant Controller software start on startup, it is recommended
to use systemd.

This setup assumes that you created the python virtual environment where
instructed in the Quick Start Guide.

First, add a script called `auto_start.sh` to `~/.plant_controller/` containing

```bash
#!/bin/bash

source ~/.venv/bin/activate
~/.influxdb/influxdb3 serve --node-id node0 > /dev/null 2>&1 &
cd <PATH_TO_DIRECOTRY_CONTAINING_PLANT_CONTROLLER_SOURCECODE>
python -m plant_controller --log-level INFO run
```

replacing `<PATH_TO_DIRECOTRY_CONTAINING_PLANT_CONTROLLER_SOURCECODE>`with the
path to the directory containing the `plant_controller` source code directory.

Then, add a file called `plant_controller.service` to `~/.config/systemd/user/`
containing

```
[Unit]
Description=Plant Controller DT/PT interface layer

[Service]
ExecStart=%h/.plant_controller/auto_start.sh

[Install]
WantedBy=default.target
```

This specifies a user service which will run the previous bash script, which in
turn will activate the python virtual environment, start the inlfuxdb3 database
and start the plant_controller software.

User services are not normally un at startup, so this must be enabled by running

```bash
loginctl enable-linger
```

It is also necessary to ensure that the your PATH is available to systemd, so add
`systemctl --user import-environment PATH` to the end of the file `~/.bashrc`.

Finally, enable the service with

```bash
systemctl --user enable plant_controller
```

The plant controller should now automatically run at startup.