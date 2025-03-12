# Purpose

This project creates a fully-functional greenhouse of three plants.
Please see the [schematics](SCHEMATICS.md) for the physical setup.

## Development Setup

:warning: This project uses python packages that only work on Linux.
Hence, the project can only be developed on Linux OS.

This is a [poetry-based project](https://python-poetry.org/docs/).
The relevant commands to run the project are:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1     # On Windows
source .venv/bin/activate        # On Linux

pip install poetry               #Specifically install poetry to your system
# If you have poetry installed globally
poetry env activate              # shows the command to activate venv
pylint src --rcfile=.pylintrc    # runs linting checks

poetry install                   # installs all required python packages
poetry build                     # builds cp-sens package that can be published on pip
poetry run start                 # runs the main script
```

## Testing

Write tests in the _tests_ directory. Be sure to name any new files as
_test_*_.py_. To run all tests, with coverage:

```bash
pytest
```

## Use

Only MQTT client code is working at the moment.
You can use it by setting the `src/cp-sens/data/config/mqtt.json`
and executing,

```bash
python .\src\cp-sens\data\sources\mqtt.py
```
