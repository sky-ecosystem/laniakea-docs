"""Regression tests for reporting-oriented configuration."""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
sys.path.insert(0, str(ROOT / "src"))

from skyforecast.engine import create_extensions, run_scenario
from skyforecast.loaders import load_agents, load_model_constants, load_and_resolve_scenario
from skyforecast.outputs import generate_report


def load_current_scenario():
    """Load the current active scenario and extensions."""
    agents = load_agents(CONFIG_DIR / "constants" / "agents.yaml")
    constants = load_model_constants(CONFIG_DIR / "constants" / "model.yaml")
    scenario = load_and_resolve_scenario(CONFIG_DIR / "scenarios" / "q2_2026_to_q1_2027.yaml")
    with open(CONFIG_DIR / "extensions.yaml") as f:
        extensions = yaml.safe_load(f) or {}
    return scenario, agents, constants, extensions


def test_active_extensions_exclude_backstop_tracking():
    """The active model no longer wires in aggregate backstop tracking."""
    _, _, _, extensions = load_current_scenario()
    extension_names = {ext.name for ext in create_extensions(extensions)}

    assert "genesis_capital" not in extension_names
    assert "genesis_capital_spending" not in extension_names


def test_report_omits_backstop_capital_section():
    """Financial reporting output should not include aggregate backstop bookkeeping."""
    scenario, agents, constants, extensions = load_current_scenario()
    results = run_scenario(scenario, agents, constants, extensions)
    report = generate_report(scenario, results, extensions)

    assert "BACKSTOP CAPITAL" not in report
    assert "Genesis Capital:" not in report
    assert not hasattr(results.monthly[0], "displayed_backstop")
