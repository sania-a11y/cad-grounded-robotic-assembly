from pathlib import Path
import sys

import typer

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cad_assembly.cli import validate_graph

if __name__ == "__main__":
    typer.run(validate_graph)
