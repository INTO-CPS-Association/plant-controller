# Install the software
Software installation will come with some waiting time — during these times it
is possible to [assemble hardware](./qs_hardware.md) not directly connected to the Raspberry Pi.

## Install Raspberry Pi OS

Download the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to
the extra computer. (See their guide on
[how to use the installer](https://www.raspberrypi.com/documentation/computers/getting-started.html#imager-install),
if need be.)

Connect the micro SD card to the extra computer.

Run the Raspberry Pi Imager to start the installation process.

Choose **"Raspberry Pi 5"** as the device.

If you have the optional screen and keyboard for the Raspberry Pi, choose
**"Raspberry Pi OS (64-bit)"** for the OS. Otherwise choose
**"Raspberry Pi OS Lite (64-bit)"**.

Choose the connected micro SD card as the storage.

Customize your Raspberry Pi OS as desired, making sure to:

- choose a hostname for the Raspberry Pi (for example "plant-controller")
- choose your localization
- set a username and password
- input your LAN's Wi-Fi credentials (if you are not using a wired connection)
- enable SSH connectivity, if you DON'T have a screen and keyboard for the
  Raspberry Pi

!!! tip "No screen or keyboard?"
    If you can't connect to your Raspberry Pi through SSH over your LAN for
    some reason, enable **Raspberry Pi Connect**. This will allow you to
    connect to the Raspberry Pi over a USB connection instead.

Finally, set imager options and start writing the OS to the micro SD card.
This will erase all things previously stored on the micro SD card before
writing the OS and will take a couple of minutes.

When it is done, eject the micro SD card (if it hasn't already been ejected),
disconnect it from the computer, and insert it into the Raspberry Pi.

Boot up the Raspberry Pi (connecting the screen and keyboard to it beforehand
if available).

If you installed the Raspberry Pi OS with a desktop environment and have a
screen and keyboard connected to it, put away the extra computer; it won't be
needed for the rest of this guide. Then, open a terminal.

If you installed the Raspberry Pi OS Lite you'll have to connect to the
Raspberry Pi over SSH from the extra computer. In the future, when you are
instructed to open a new terminal, do it by SSH'ing in from the extra computer
in a new terminal.

From the terminal, ensure that the Raspberry Pi is updated by running:

```bash
sudo apt-get update -y && sudo apt-get upgrade -y
```

When everything is updated, continue to the next step.

---

## Install the database

The controller uses **InfluxDB 3.0 or later** to store measurements and
watering events.

!!! warning "Raspberry Pi 5 page size"
    The default OS kernel for the Raspberry Pi 5 uses a memory page size of
    16k, but InfluxDB 3 assumes a page size of 4k. Before installing the
    database on a Raspberry Pi 5, switch to the 4k kernel by setting
    `kernel=kernel8.img` in `/boot/firmware/config.txt`:

    ```bash
    echo "kernel=kernel8.img" | sudo tee -a /boot/firmware/config.txt
    sudo shutdown -r now
    ```

    This reboots the Raspberry Pi and terminates any SSH connection to the
    machine — give it some time, then reconnect.

Install InfluxDB 3:

```bash
curl -O https://www.influxdata.com/d/install_influxdb3.sh \
&& sh install_influxdb3.sh
```

Choose the local install, and decline when the install script asks whether to
start the server at the end. Then start the server yourself:

```bash
influxdb3 serve --node-id node0
```

With the server running, open a new terminal (or SSH session) and create the
admin token:

```bash
influxdb3 create token --admin
```

Note the token down — it is referred to as `<ADMIN_TOKEN>` below, and is
needed in the controller's config file. Then create the database for the
controller:

```bash
influxdb3 create database --token <ADMIN_TOKEN> --retention-period 7d plant-controller
```

Here the retention period is set to 7 days to avoid gumming up the
controller's persistent storage, and the database name to `plant-controller`,
which is the default in the config file. Both can be changed freely, as long
as the config file is updated accordingly.

### Start InfluxDB automatically

To ensure the database starts automatically, create a systemd service:

```bash
sudo tee /etc/systemd/system/influxdb3.service > /dev/null << 'EOF'
[Unit]
Description=InfluxDB 3
After=network.target

[Service]
ExecStart=/usr/local/bin/influxdb3 serve --node-id node0
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now influxdb3
```

!!! note
    If `influxdb3` was installed to a different path, update the
    `ExecStart` line accordingly. You can find the path with
    `which influxdb3`.

---

## Install the controller software

First, get the source code onto the Raspberry Pi, either by cloning it from
GitHub or by SCP'ing it over from the extra computer:

```bash
git clone https://github.com/DisasterlyDisco/plant-controller.git
```

In the following, `<src>` refers to the full path of the cloned repository.

Install pip and venv support:

```bash
sudo apt-get install -y python3-pip python3-venv python3-setuptools
```

Create a virtual environment (here in the home directory) and activate it:

```bash
cd ~
python -m venv .venv --system-site-packages
source .venv/bin/activate
```

### Install Adafruit Blinka

Adafruit Blinka provides the Python API for the Raspberry Pi's GPIO header,
which the controller uses for I2C communication with the Adafruit sensor
modules. It cannot simply be installed with pip, as it needs to configure the
machine itself — Adafruit supplies a convenience script:

```bash
cd ~
pip install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo -E env PATH=$PATH python3 raspi-blinka.py
```

### Install remaining Python dependencies

With Blinka installed, install the rest of the Python requirements as normal:

```bash
cd <src>/pt/controller_3
pip install -r requirements.txt
```

---

[**Configure the controller**](./qs_config.md)
