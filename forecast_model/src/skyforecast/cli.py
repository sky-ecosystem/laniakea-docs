"""Command-line interface."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

try:
    import typer
    from rich.console import Console
    HAS_CLI_DEPS = True
except ImportError:
    HAS_CLI_DEPS = False

import yaml

from .loaders import load_agents, load_model_constants, load_and_resolve_scenario
from .engine import run_scenario
from .outputs import format_scenario_markdown
from .outputs.html_dashboard import generate_dashboard_html


def load_extensions(path: Path) -> dict:
    """Load extensions config from YAML."""
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


if HAS_CLI_DEPS:
    app = typer.Typer(help="Sky protocol forecast model")
    console = Console()

    @app.command()
    def run(
        scenario: str = typer.Argument(..., help="Scenario name (without .yaml extension)"),
        config_dir: Path = typer.Option(
            Path("config"),
            "--config-dir", "-c",
            help="Configuration directory",
        ),
        output: Optional[Path] = typer.Option(
            None,
            "--output", "-o",
            help="Output file (default: stdout)",
        ),
        detailed: bool = typer.Option(
            False,
            "--detailed", "-d",
            help="Include detailed monthly output",
        ),
    ):
        """Run a forecast scenario and output markdown."""
        agents_path = config_dir / "constants" / "agents.yaml"
        model_path = config_dir / "constants" / "model.yaml"
        scenario_path = config_dir / "scenarios" / f"{scenario}.yaml"
        extensions_path = config_dir / "extensions.yaml"

        if not agents_path.exists():
            console.print(f"[red]Error: agents config not found at {agents_path}[/red]")
            raise typer.Exit(1)

        if not model_path.exists():
            console.print(f"[red]Error: model config not found at {model_path}[/red]")
            raise typer.Exit(1)

        if not scenario_path.exists():
            console.print(f"[red]Error: scenario not found at {scenario_path}[/red]")
            raise typer.Exit(1)

        agents = load_agents(agents_path)
        constants = load_model_constants(model_path)
        resolved_scenario = load_and_resolve_scenario(scenario_path)
        extensions = load_extensions(extensions_path)

        results = run_scenario(resolved_scenario, agents, constants, extensions)
        markdown = format_scenario_markdown(results, detailed=detailed)

        if output:
            output.write_text(markdown)
            console.print(f"[green]Results written to {output}[/green]")
        else:
            console.print(markdown)

    @app.command()
    def dashboard(
        scenario: str = typer.Argument(..., help="Scenario name (without .yaml extension)"),
        config_dir: Path = typer.Option(
            Path("config"),
            "--config-dir", "-c",
            help="Configuration directory",
        ),
        output: Path = typer.Option(
            Path("dashboard.html"),
            "--output", "-o",
            help="Output HTML file",
        ),
    ):
        """Generate HTML dashboard for a scenario."""
        agents_path = config_dir / "constants" / "agents.yaml"
        model_path = config_dir / "constants" / "model.yaml"
        scenario_path = config_dir / "scenarios" / f"{scenario}.yaml"
        extensions_path = config_dir / "extensions.yaml"

        if not agents_path.exists():
            console.print(f"[red]Error: agents config not found at {agents_path}[/red]")
            raise typer.Exit(1)

        if not model_path.exists():
            console.print(f"[red]Error: model config not found at {model_path}[/red]")
            raise typer.Exit(1)

        if not scenario_path.exists():
            console.print(f"[red]Error: scenario not found at {scenario_path}[/red]")
            raise typer.Exit(1)

        agents = load_agents(agents_path)
        constants = load_model_constants(model_path)
        resolved_scenario = load_and_resolve_scenario(scenario_path)
        extensions = load_extensions(extensions_path)

        results = run_scenario(resolved_scenario, agents, constants, extensions)
        html = generate_dashboard_html(resolved_scenario, results, extensions)

        output.write_text(html)
        console.print(f"[green]Dashboard written to {output}[/green]")

    @app.command()
    def validate(
        config_dir: Path = typer.Option(
            Path("config"),
            "--config-dir", "-c",
            help="Configuration directory",
        ),
    ):
        """Validate configuration files without running."""
        agents_path = config_dir / "constants" / "agents.yaml"
        model_path = config_dir / "constants" / "model.yaml"
        scenarios_dir = config_dir / "scenarios"
        extensions_path = config_dir / "extensions.yaml"

        errors = []

        # Validate agents
        if agents_path.exists():
            try:
                agents = load_agents(agents_path)
                console.print(f"[green]✓[/green] agents.yaml: {len(agents)} agents")
            except Exception as e:
                errors.append(f"agents.yaml: {e}")
        else:
            errors.append(f"agents.yaml not found at {agents_path}")

        # Validate model constants
        if model_path.exists():
            try:
                load_model_constants(model_path)
                console.print("[green]✓[/green] model.yaml: valid")
            except Exception as e:
                errors.append(f"model.yaml: {e}")
        else:
            errors.append(f"model.yaml not found at {model_path}")

        # Validate extensions
        if extensions_path.exists():
            try:
                extensions = load_extensions(extensions_path)
                console.print(f"[green]✓[/green] extensions.yaml: {len(extensions)} extensions")
            except Exception as e:
                errors.append(f"extensions.yaml: {e}")
        else:
            console.print("[yellow]⚠[/yellow] extensions.yaml: not found (optional)")

        # Validate scenarios
        if scenarios_dir.exists():
            for scenario_path in scenarios_dir.glob("*.yaml"):
                try:
                    resolved = load_and_resolve_scenario(scenario_path)
                    console.print(
                        f"[green]✓[/green] {scenario_path.name}: "
                        f"{resolved.months} months"
                    )
                except Exception as e:
                    errors.append(f"{scenario_path.name}: {e}")
        else:
            console.print(f"[yellow]Warning: no scenarios directory at {scenarios_dir}[/yellow]")

        if errors:
            console.print("\n[red]Validation errors:[/red]")
            for err in errors:
                console.print(f"  - {err}")
            raise typer.Exit(1)
        else:
            console.print("\n[green]All configs valid![/green]")


def main():
    """Entry point for the CLI."""
    if not HAS_CLI_DEPS:
        print("Error: CLI dependencies not installed.")
        print("Install with: pip install typer rich")
        print("Or use run_dashboard.py directly for dashboard generation.")
        return 1
    app()
    return 0


if __name__ == "__main__":
    exit(main())
