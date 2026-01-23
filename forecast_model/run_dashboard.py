#!/usr/bin/env python3
"""Quick runner to generate dashboard."""

from pathlib import Path

import yaml

from skyforecast.loaders import load_agents, load_model_constants, load_and_resolve_scenario
from skyforecast.engine import run_scenario
from skyforecast.outputs.html_dashboard import generate_dashboard_html

CONFIG_DIR = Path(__file__).parent / "config"
OUTPUT_FILE = Path(__file__).parent / "dashboard.html"


def load_extensions(path: Path) -> dict:
    """Load extensions config from YAML."""
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def run(scenario_name: str = "base_2026"):
    agents = load_agents(CONFIG_DIR / "constants" / "agents.yaml")
    constants = load_model_constants(CONFIG_DIR / "constants" / "model.yaml")
    scenario = load_and_resolve_scenario(CONFIG_DIR / "scenarios" / f"{scenario_name}.yaml")
    extensions = load_extensions(CONFIG_DIR / "extensions.yaml")

    results = run_scenario(scenario, agents, constants, extensions)
    html = generate_dashboard_html(scenario, results, extensions)

    OUTPUT_FILE.write_text(html)
    print(f"Dashboard updated: {OUTPUT_FILE}")


if __name__ == "__main__":
    import sys
    scenario = sys.argv[1] if len(sys.argv) > 1 else "base_2026"
    run(scenario)
