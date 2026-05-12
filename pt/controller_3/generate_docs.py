"""Generate API documentation for plant_controller using pdoc.

Mocks hardware-specific modules (Adafruit Blinka, board, sensors) so that
pdoc can import the package in CI without physical hardware attached.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Hardware modules that require physical I2C/GPIO hardware to import.
# We replace them with mocks so pdoc can introspect the rest of the code.
HARDWARE_MODULES = [
    "board",
    "busio",
    "digitalio",
    "microcontroller",
    "adafruit_tca9548a",
    "adafruit_as7341",
    "adafruit_sht4x",
    "adafruit_seesaw",
    "adafruit_seesaw.seesaw",
]

for mod_name in HARDWARE_MODULES:
    sys.modules[mod_name] = MagicMock()

# Now we can safely import pdoc and generate docs
import pdoc  # noqa: E402

if __name__ == "__main__":

    here = Path(__file__).parent
    src_dir = here / "src"
    out_dir = here / "docs_build"

    sys.path.insert(0, str(src_dir))

    pdoc.pdoc(
        "plant_controller",
        output_directory=out_dir,
    )
    print(f"Documentation generated in {out_dir}")
