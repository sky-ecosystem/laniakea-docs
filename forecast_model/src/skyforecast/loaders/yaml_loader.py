"""YAML configuration loaders."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Callable

import yaml

from .models import AgentConfig, ScenarioConfig, ModelConstants
from .resolver import ResolvedScenario, resolve_scenario


def load_yaml(path: Path) -> dict:
    """Load YAML file."""
    with open(path) as f:
        return yaml.safe_load(f)


def load_agents(path: Path) -> list[AgentConfig]:
    """Load agent definitions from YAML."""
    data = load_yaml(path)
    return [AgentConfig(**agent) for agent in data["agents"]]


def load_model_constants(path: Path) -> ModelConstants:
    """Load model constants from YAML."""
    data = load_yaml(path)
    return ModelConstants(**data)


def load_scenario(path: Path) -> ScenarioConfig:
    """Load scenario configuration from YAML."""
    data = load_yaml(path)
    return ScenarioConfig(**data)


def load_and_resolve_scenario(
    path: Path,
    scenarios_dir: Optional[Path] = None,
) -> ResolvedScenario:
    """
    Load and fully resolve a scenario, including inheritance.

    Args:
        path: Path to scenario YAML file
        scenarios_dir: Directory to search for parent scenarios (defaults to path's parent)
    """
    if scenarios_dir is None:
        scenarios_dir = path.parent

    def load_parent(name: str) -> ScenarioConfig:
        parent_path = scenarios_dir / f"{name}.yaml"
        if not parent_path.exists():
            raise FileNotFoundError(f"Parent scenario not found: {parent_path}")
        return load_scenario(parent_path)

    config = load_scenario(path)
    return resolve_scenario(config, load_parent_fn=load_parent)
