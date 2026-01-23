"""Pydantic models for configuration."""

from __future__ import annotations

from decimal import Decimal
from typing import Literal, Union, Optional, Any

from pydantic import BaseModel, field_validator


def parse_decimal(v: Union[str, int, float, Decimal]) -> Decimal:
    """Parse value to Decimal, handling strings for precision."""
    if isinstance(v, Decimal):
        return v
    return Decimal(str(v))


class AgentConfig(BaseModel):
    """Agent definition from config."""
    name: str
    type: Literal["FARM", "SELL"]
    ownership_ratio: Decimal
    market_cap_ratio: Optional[Decimal] = None

    @field_validator("ownership_ratio", "market_cap_ratio", mode="before")
    @classmethod
    def parse_decimals(cls, v):
        if v is None:
            return None
        return parse_decimal(v)


class ModelConstants(BaseModel):
    """Model-wide constants."""
    farm_emission_rate: Decimal
    backstop_rate: Decimal

    @field_validator("*", mode="before")
    @classmethod
    def parse_all_decimals(cls, v):
        return parse_decimal(v)


class TrajectoryConfig(BaseModel):
    """Configuration for a value trajectory."""
    points: dict[int, Any]  # month -> value
    mode: Literal["step", "linear"] = "step"

    @field_validator("points", mode="before")
    @classmethod
    def parse_points(cls, v):
        if isinstance(v, dict):
            return {int(k): v for k, v in v.items()}
        return v


class EventConfig(BaseModel):
    """Single event in events list."""
    month: Union[int, str]  # month number or period name
    type: Literal["set", "impulse", "agent_launch"]
    values: Optional[dict[str, Any]] = None
    agent: Optional[str] = None  # for agent_launch type


class ScenarioConfig(BaseModel):
    """Full scenario configuration with all features."""
    name: str
    description: str = ""
    months: int = 12
    extends: Optional[str] = None  # parent scenario name

    # Named periods
    periods: dict[str, list[int]] = {}

    # Agent launches (name -> month or period name)
    agent_launches: dict[str, Union[int, str]] = {}

    # Baseline values
    baseline: dict[str, Any] = {}

    # Trajectories for interpolated values
    trajectories: dict[str, TrajectoryConfig] = {}

    # Persistent changes by month
    changes: dict[Union[int, str], dict[str, Any]] = {}

    # One-time impulses by month
    impulses: dict[Union[int, str], dict[str, Any]] = {}

    # Events list (alternative syntax)
    events: list[EventConfig] = []

    @field_validator("changes", "impulses", mode="before")
    @classmethod
    def parse_month_keys(cls, v):
        """Keep keys as-is (int or str) for later resolution."""
        if isinstance(v, dict):
            return {k: v for k, v in v.items()}
        return v

    @field_validator("trajectories", mode="before")
    @classmethod
    def parse_trajectories(cls, v):
        if isinstance(v, dict):
            return {k: TrajectoryConfig(**tv) if isinstance(tv, dict) else tv
                    for k, tv in v.items()}
        return v
