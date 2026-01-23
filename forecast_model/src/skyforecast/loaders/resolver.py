"""Input resolution logic for monthly calculations."""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Union

from .models import ScenarioConfig, TrajectoryConfig, parse_decimal


# Default named periods
DEFAULT_PERIODS = {
    "q1": [1, 2, 3],
    "q2": [4, 5, 6],
    "q3": [7, 8, 9],
    "q4": [10, 11, 12],
    "h1": [1, 2, 3, 4, 5, 6],
    "h2": [7, 8, 9, 10, 11, 12],
}


def resolve_period_name(
    value: Union[int, str],
    periods: dict[str, list[int]],
) -> int:
    """Convert period name to month number (first month of period)."""
    if isinstance(value, int):
        return value
    # Try custom periods first, then defaults
    if value in periods:
        return periods[value][0]
    if value in DEFAULT_PERIODS:
        return DEFAULT_PERIODS[value][0]
    # Try parsing as int
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Unknown period: {value}")


def compute_trajectory_value(
    trajectory: TrajectoryConfig,
    month: int,
) -> Decimal:
    """Compute trajectory value at a given month."""
    points = trajectory.points
    sorted_months = sorted(points.keys())

    if not sorted_months:
        raise ValueError("Trajectory has no points")

    # Before first point: use first value
    if month <= sorted_months[0]:
        return parse_decimal(points[sorted_months[0]])

    # After last point: use last value
    if month >= sorted_months[-1]:
        return parse_decimal(points[sorted_months[-1]])

    # Find surrounding points
    prev_month = sorted_months[0]
    next_month = sorted_months[-1]

    for m in sorted_months:
        if m <= month:
            prev_month = m
        if m > month and next_month > m:
            next_month = m
        if m > month:
            next_month = m
            break

    prev_value = parse_decimal(points[prev_month])
    next_value = parse_decimal(points[next_month])

    if trajectory.mode == "step":
        # Step: use previous value until next point
        return prev_value

    elif trajectory.mode == "linear":
        # Linear interpolation
        if next_month == prev_month:
            return prev_value
        progress = Decimal(month - prev_month) / Decimal(next_month - prev_month)
        return prev_value + (next_value - prev_value) * progress

    else:
        raise ValueError(f"Unknown trajectory mode: {trajectory.mode}")


def normalize_month_dict(
    d: dict[Union[int, str], Any],
    periods: dict[str, list[int]],
) -> dict[int, Any]:
    """Convert dict with period names to dict with month numbers."""
    result = {}
    for key, value in d.items():
        month = resolve_period_name(key, periods)
        result[month] = value
    return result


def resolve_month_inputs(
    month: int,
    baseline: dict[str, Any],
    changes: dict[int, dict[str, Any]],
    impulses: dict[int, dict[str, Any]],
    trajectories: dict[str, TrajectoryConfig],
) -> dict[str, Any]:
    """
    Resolve all inputs for a specific month.

    Order:
    1. Start with baseline
    2. Apply trajectories (computed values)
    3. Apply cumulative changes up to this month
    4. Apply impulses for this month only
    """
    result = baseline.copy()

    # Apply trajectories
    for field, traj in trajectories.items():
        result[field] = compute_trajectory_value(traj, month)

    # Apply cumulative changes
    for m in sorted(changes.keys()):
        if m <= month:
            result.update(changes[m])

    # Apply impulses (this month only)
    if month in impulses:
        result.update(impulses[month])

    return result


def merge_scenarios(
    parent: ScenarioConfig,
    child: ScenarioConfig,
) -> ScenarioConfig:
    """Merge child scenario into parent (child overrides parent)."""
    # Start with parent values
    merged_baseline = parent.baseline.copy()
    merged_baseline.update(child.baseline)

    merged_changes = parent.changes.copy()
    for month, values in child.changes.items():
        if month in merged_changes:
            merged_changes[month] = {**merged_changes[month], **values}
        else:
            merged_changes[month] = values

    merged_impulses = parent.impulses.copy()
    for month, values in child.impulses.items():
        if month in merged_impulses:
            merged_impulses[month] = {**merged_impulses[month], **values}
        else:
            merged_impulses[month] = values

    merged_trajectories = {**parent.trajectories, **child.trajectories}
    merged_events = parent.events + child.events
    merged_agent_launches = {**parent.agent_launches, **child.agent_launches}
    merged_periods = {**DEFAULT_PERIODS, **parent.periods, **child.periods}

    return ScenarioConfig(
        name=child.name,
        description=child.description or parent.description,
        months=child.months or parent.months,
        extends=None,  # Already resolved
        periods=merged_periods,
        agent_launches=merged_agent_launches,
        baseline=merged_baseline,
        trajectories=merged_trajectories,
        changes=merged_changes,
        impulses=merged_impulses,
        events=merged_events,
    )


def process_events(
    events: list,
    changes: dict[int, dict],
    impulses: dict[int, dict],
    agent_launches: dict[str, int],
    periods: dict[str, list[int]],
) -> tuple[dict[int, dict], dict[int, dict], dict[str, int]]:
    """Process events list and merge into changes/impulses/agent_launches."""
    changes = changes.copy()
    impulses = impulses.copy()
    agent_launches = agent_launches.copy()

    for event in events:
        month = resolve_period_name(event.month, periods)

        if event.type == "set":
            if month not in changes:
                changes[month] = {}
            if event.values:
                changes[month].update(event.values)

        elif event.type == "impulse":
            if month not in impulses:
                impulses[month] = {}
            if event.values:
                impulses[month].update(event.values)

        elif event.type == "agent_launch":
            if event.agent:
                agent_launches[event.agent] = month

    return changes, impulses, agent_launches


class ResolvedScenario:
    """Fully resolved scenario ready for execution."""

    def __init__(
        self,
        name: str,
        description: str,
        months: int,
        periods: dict[str, list[int]],
        agent_launches: dict[str, int],
        baseline: dict[str, Any],
        trajectories: dict[str, TrajectoryConfig],
        changes: dict[int, dict[str, Any]],
        impulses: dict[int, dict[str, Any]],
    ):
        self.name = name
        self.description = description
        self.months = months
        self.periods = periods
        self.agent_launches = agent_launches
        self.baseline = baseline
        self.trajectories = trajectories
        self.changes = changes
        self.impulses = impulses

    def get_month_inputs(self, month: int) -> dict[str, Any]:
        """Get resolved inputs for a specific month."""
        return resolve_month_inputs(
            month=month,
            baseline=self.baseline,
            changes=self.changes,
            impulses=self.impulses,
            trajectories=self.trajectories,
        )


def resolve_scenario(
    config: ScenarioConfig,
    load_parent_fn=None,
) -> ResolvedScenario:
    """
    Resolve a scenario config into a fully resolved scenario.

    Args:
        config: The scenario configuration
        load_parent_fn: Optional function to load parent scenario by name
    """
    # Handle inheritance
    if config.extends and load_parent_fn:
        parent_config = load_parent_fn(config.extends)
        parent_resolved = resolve_scenario(parent_config, load_parent_fn)
        # Convert back to config for merging
        parent_as_config = ScenarioConfig(
            name=parent_resolved.name,
            description=parent_resolved.description,
            months=parent_resolved.months,
            periods=parent_resolved.periods,
            agent_launches={k: v for k, v in parent_resolved.agent_launches.items()},
            baseline=parent_resolved.baseline,
            trajectories=parent_resolved.trajectories,
            changes=parent_resolved.changes,
            impulses=parent_resolved.impulses,
        )
        config = merge_scenarios(parent_as_config, config)

    # Merge default periods with custom periods
    periods = {**DEFAULT_PERIODS, **config.periods}

    # Normalize agent launches (resolve period names to months)
    agent_launches = {
        name: resolve_period_name(month, periods)
        for name, month in config.agent_launches.items()
    }

    # Normalize changes and impulses (resolve period names to months)
    changes = normalize_month_dict(config.changes, periods)
    impulses = normalize_month_dict(config.impulses, periods)

    # Process events list
    changes, impulses, agent_launches = process_events(
        config.events, changes, impulses, agent_launches, periods
    )

    return ResolvedScenario(
        name=config.name,
        description=config.description,
        months=config.months,
        periods=periods,
        agent_launches=agent_launches,
        baseline=config.baseline,
        trajectories=config.trajectories,
        changes=changes,
        impulses=impulses,
    )
