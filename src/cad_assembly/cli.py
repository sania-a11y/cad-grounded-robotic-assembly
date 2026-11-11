import json
from pathlib import Path

import typer
from rich import print

from cad_assembly.graph.schema import AssemblySpec
from cad_assembly.graph.validate import validate_assembly

app = typer.Typer(help="Tools for CAD-grounded robotic assembly research.")


@app.command()
def validate_graph(input: Path = typer.Option(..., exists=True, readable=True)):
    """Validate an assembly graph specification stored as JSON."""
    spec = AssemblySpec.model_validate_json(input.read_text(encoding="utf-8"))
    errors = validate_assembly(spec)
    if errors:
        print("[bold red]Validation failed[/bold red]")
        for error in errors:
            print(f"- {error}")
        raise typer.Exit(code=1)
    print("[bold green]Assembly specification is structurally valid.[/bold green]")


if __name__ == "__main__":
    app()
