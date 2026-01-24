"""Plain text report generator - quarterly breakdown with monthly details."""

from decimal import Decimal
from typing import Any, Dict, Optional

from ..engine import ScenarioResults
from ..loaders import ResolvedScenario


def fmt_money(value: Decimal, decimals: int = 1) -> str:
    """Format money value with M/B suffix."""
    val = float(value)
    if abs(val) >= 1_000_000_000:
        return f"${val / 1_000_000_000:,.{decimals}f}B"
    return f"${val / 1_000_000:,.{decimals}f}M"


def fmt_num(value: Any) -> str:
    """Format number with K/M/B abbreviations."""
    if isinstance(value, str):
        return value
    if isinstance(value, Decimal):
        value = float(value)
    if isinstance(value, (int, float)):
        abs_val = abs(value)
        if abs_val >= 1_000_000_000:
            return f"{abs_val/1_000_000_000:,.1f}B"
        if abs_val >= 1_000_000:
            return f"{abs_val/1_000_000:,.0f}M"
        if abs_val >= 1_000:
            return f"{abs_val/1_000:,.0f}K"
        return f"{value:,.2f}"
    return str(value)


def fmt_pct(value: Decimal) -> str:
    """Format rate as percentage."""
    return f"{float(value) * 100:.2f}%"


def format_inputs_section(
    scenario: ResolvedScenario,
    extensions: Optional[Dict[str, Any]] = None,
) -> list:
    """Format the inputs section of the report."""
    extensions = extensions or {}
    lines = []

    lines.append("=" * 80)
    lines.append("SCENARIO INPUTS")
    lines.append("=" * 80)
    lines.append("")

    # Base Model
    lines.append("BASE MODEL")
    lines.append("-" * 40)
    base_fields = ["base_usds", "sofr", "savings_rate_spread", "gross_revenue_rate_spread",
                   "security_rate", "tier2_ratio", "tier3_ratio", "tier4_ratio"]
    for key in base_fields:
        if key in scenario.baseline:
            val = scenario.baseline[key]
            lines.append(f"  {key}: {fmt_num(val)}")
    lines.append("")

    # Trajectories
    if scenario.trajectories:
        lines.append("TRAJECTORIES")
        lines.append("-" * 40)
        for key, traj in scenario.trajectories.items():
            points_str = " → ".join(f"M{m}: {fmt_num(v)}" for m, v in sorted(traj.points.items()))
            lines.append(f"  {key}: {points_str} ({traj.mode})")
        lines.append("")

    # Changes
    if scenario.changes:
        lines.append("SCHEDULED CHANGES")
        lines.append("-" * 40)
        for month in sorted(scenario.changes.keys()):
            for key, val in scenario.changes[month].items():
                lines.append(f"  M{month}: {key} = {fmt_num(val)}")
        lines.append("")

    # Extensions
    lines.append("EXTENSIONS")
    lines.append("-" * 40)

    # PSM Exposure
    psm = extensions.get("psm_exposure", {})
    if psm:
        lines.append("  PSM Exposure:")
        if psm.get('pct'):
            lines.append(f"    pct: {float(psm['pct'])*100:.0f}% of total USDS")
        elif psm.get('amount'):
            lines.append(f"    amount: {fmt_num(psm['amount'])}")
        if psm.get('spread'):
            lines.append(f"    spread: {psm['spread']}")

    # USDT Subsidy
    usdt = extensions.get("usdt_subsidy", {})
    if usdt:
        lines.append("  USDT Subsidy:")
        lines.append(f"    amount: {fmt_num(usdt.get('amount', 0))}")
        rate_factor = usdt.get('rate_factor', '0.50')
        lines.append(f"    rate: {float(rate_factor)*100:.0f}% of SSR")

    # Subsidized Borrow
    sub = extensions.get("subsidized_borrow", {})
    if sub:
        lines.append("  Subsidized Borrow:")
        lines.append(f"    total_amount: {fmt_num(sub.get('total_amount', 0))}")
        lines.append(f"    duration: {sub.get('duration_months', 24)} months")

    # srUSDS Cost
    sr = extensions.get("srusds_cost", {})
    if sr:
        lines.append("  srUSDS Cost:")
        lines.append(f"    annual_cost: {fmt_num(sr.get('annual_cost', 0))}")

    # Core Vaults
    cv = extensions.get("core_vaults", {})
    if cv:
        lines.append("  Core Vaults:")
        lines.append(f"    debt: {fmt_num(cv.get('debt', 0))}")
        lines.append(f"    rate: {float(cv.get('rate', 0.08))*100:.1f}%")

    # Token Farming
    farm = extensions.get("token_farming", {})
    if farm:
        lines.append("  Token Farming:")
        lines.append(f"    distribution_rate: {farm.get('distribution_rate', '0.175')}")
        lines.append(f"    farm_yield_spread: {farm.get('farm_yield_spread', '0.0010')}")
        stars = farm.get("stars", {})
        for star_name, star_data in stars.items():
            ownership = star_data.get("ownership", "0")
            launch = star_data.get("launch_month", "?")
            if star_name == "spark":
                mc_display = fmt_num(star_data.get("market_cap", 0))
            else:
                pct = star_data.get("market_cap_pct", "0")
                mc_display = f"{float(pct)*100:.0f}% of Spark"
            lines.append(f"    {star_name}: {mc_display} @ {ownership} (M{launch})")

    # Genesis Capital
    gen = extensions.get("genesis_capital", {})
    if gen:
        lines.append("  Genesis Capital:")
        lines.append(f"    core_buffer: {fmt_num(gen.get('core_buffer', 0))}")
        lines.append(f"    min_threshold: {fmt_num(gen.get('min_backstop_threshold', 0))}")
        gen_stars = gen.get("stars", {})
        for star_name, star_data in gen_stars.items():
            gc = star_data.get("genesis_capital", 0)
            lines.append(f"    {star_name}: {fmt_num(gc)}")

    # Genesis Prime
    prime = extensions.get("genesis_prime", {})
    if prime:
        lines.append("  Genesis Prime:")
        lines.append(f"    sell_rate: {prime.get('sell_rate', '0.175')}")
        primes = prime.get("primes", {})
        for prime_name, prime_data in primes.items():
            pct = prime_data.get("market_cap_pct", "0")
            ownership = prime_data.get("ownership", "0")
            launch = prime_data.get("launch_month", "?")
            lines.append(f"    {prime_name}: {float(pct)*100:.0f}% of Spark @ {ownership} (M{launch})")

    lines.append("")
    return lines


def generate_report(
    scenario: ResolvedScenario,
    results: ScenarioResults,
    extensions: Optional[Dict[str, Any]] = None,
) -> str:
    """Generate plain text report with quarters broken down by month."""
    lines = []

    # Header
    lines.extend([
        results.name.upper(),
        results.description,
        "",
    ])

    # Inputs section
    lines.extend(format_inputs_section(scenario, extensions))

    lines.extend([
        "=" * 80,
        "FORECAST RESULTS",
        "=" * 80,
        "",
        "COLUMN DEFINITIONS",
        "SSR: Sky Savings Rate (annualized)",
        "USDS: Total USDS supply",
        "Gross Rev: Total revenue before savings rate expenses",
        "Net Rev: Revenue after savings rate expenses",
        "Security: Security operational expenses",
        "Profit: Net profit after operational expenses",
        "Staking: Funds distributed to SKY stakers as staking rewards",
        "",
    ])

    # Column widths
    col = [8, 8, 10, 10, 10, 10, 10, 10]  # Month, SSR, USDS, GrossRev, NetRev, Security, Profit, Staking
    header = f"{'Month':<{col[0]}} {'SSR':>{col[1]}} {'USDS':>{col[2]}} {'Gross Rev':>{col[3]}} {'Net Rev':>{col[4]}} {'Security':>{col[5]}} {'Profit':>{col[6]}} {'Staking':>{col[7]}}"
    divider = "-" * len(header)

    # Generate each quarter with monthly breakdown
    for q in results.quarterly:
        lines.extend([
            q.quarter_name,
            divider,
            header,
        ])

        for m in q.months:
            profit = m.waterfall.net_backstop_change + m.waterfall.staking_rewards

            lines.append(
                f"{m.month_name:<{col[0]}} "
                f"{fmt_pct(m.rates.savings_rate):>{col[1]}} "
                f"{fmt_money(m.supply.avg_usds_supply):>{col[2]}} "
                f"{fmt_money(m.revenue.gross_revenue):>{col[3]}} "
                f"{fmt_money(m.revenue.net_revenue):>{col[4]}} "
                f"{fmt_money(m.waterfall.security_budget):>{col[5]}} "
                f"{fmt_money(profit):>{col[6]}} "
                f"{fmt_money(m.waterfall.staking_rewards):>{col[7]}}"
            )

        # Quarter total row
        q_last = q.months[-1]
        q_profit = q.net_backstop_change + q.staking_rewards

        lines.append(
            f"{q.quarter_name:<{col[0]}} "
            f"{fmt_pct(q_last.rates.savings_rate):>{col[1]}} "
            f"{fmt_money(q_last.supply.avg_usds_supply):>{col[2]}} "
            f"{fmt_money(q.gross_revenue):>{col[3]}} "
            f"{fmt_money(q.net_revenue):>{col[4]}} "
            f"{fmt_money(q.security_budget):>{col[5]}} "
            f"{fmt_money(q_profit):>{col[6]}} "
            f"{fmt_money(q.staking_rewards):>{col[7]}}"
        )
        lines.append("")

    # Annual Summary (broken down by quarter)
    lines.extend([
        "ANNUAL SUMMARY",
        divider,
        f"{'Quarter':<{col[0]}} {'SSR':>{col[1]}} {'USDS':>{col[2]}} {'Gross Rev':>{col[3]}} {'Net Rev':>{col[4]}} {'Security':>{col[5]}} {'Profit':>{col[6]}} {'Staking':>{col[7]}}",
    ])

    for q in results.quarterly:
        q_last = q.months[-1]
        q_usds = q_last.supply.avg_usds_supply
        q_profit = q.net_backstop_change + q.staking_rewards

        lines.append(
            f"{q.quarter_name:<{col[0]}} "
            f"{fmt_pct(q_last.rates.savings_rate):>{col[1]}} "
            f"{fmt_money(q_usds):>{col[2]}} "
            f"{fmt_money(q.gross_revenue):>{col[3]}} "
            f"{fmt_money(q.net_revenue):>{col[4]}} "
            f"{fmt_money(q.security_budget):>{col[5]}} "
            f"{fmt_money(q_profit):>{col[6]}} "
            f"{fmt_money(q.staking_rewards):>{col[7]}}"
        )

    # Annual total
    last_month = results.monthly[-1]
    annual_gross = sum(q.gross_revenue for q in results.quarterly)
    annual_security = sum(q.security_budget for q in results.quarterly)
    cumulative_contrib = sum(m.waterfall.net_backstop_change for m in results.monthly)
    annual_profit = cumulative_contrib + results.annual_staking_rewards

    lines.append(
        f"{'Year':<{col[0]}} "
        f"{fmt_pct(last_month.rates.savings_rate):>{col[1]}} "
        f"{fmt_money(last_month.supply.avg_usds_supply):>{col[2]}} "
        f"{fmt_money(annual_gross):>{col[3]}} "
        f"{fmt_money(results.annual_net_revenue):>{col[4]}} "
        f"{fmt_money(annual_security):>{col[5]}} "
        f"{fmt_money(annual_profit):>{col[6]}} "
        f"{fmt_money(results.annual_staking_rewards):>{col[7]}}"
    )

    return "\n".join(lines)
