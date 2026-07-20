"""Generate API reference pages from plant_controller docstrings.

Writes mkdocstrings stub pages to docs/api/. Run before `zensical build`.
New modules also need a nav entry in zensical.toml.
"""

import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src = root / "pt" / "controller_3" / "src"
out = root / "docs" / "api"

shutil.rmtree(out, ignore_errors=True)

for path in sorted(src.glob("plant_controller/**/*.py")):
    module_path = path.relative_to(src).with_suffix("")
    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = module_path.parent / "index.md"
    elif parts[-1] == "__main__" or parts[-1].startswith("_"):
        continue
    else:
        doc_path = module_path.with_suffix(".md")

    target = out / doc_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"::: {'.'.join(parts)}\n")
