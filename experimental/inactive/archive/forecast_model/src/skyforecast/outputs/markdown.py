"""Markdown output formatter."""

from decimal import Decimal

from ..engine import MonthResults, QuarterResults, ScenarioResults


def fmt_money(value: Decimal, decimals: int = 2) -> str:
    """Format money value with M suffix."""
    millions = value / Decimal("1_000_000")
    return f"{millions:,.{decimals}f}M"


def fmt_pct(value: Decimal, decimals: int = 2) -> str:
    """Format as percentage."""
    pct = value * 100
    return f"{pct:.{decimals}f}%"


def format_quarter_table(quarter: QuarterResults) -> str:
    """Format a quarter's monthly results as a table."""
    lines = [
        f"## {quarter.quarter_name}",
        "",
        "| Month | USDS Supply | Gross Rev | Net Rev | Staking |",
        "|-------|-------------|-----------|---------|---------|",
    ]

    for m in quarter.months:
        lines.append(
            f"| {m.month_name} | {fmt_money(m.supply.avg_usds_supply)} | "
            f"{fmt_money(m.revenue.gross_revenue)} | {fmt_money(m.revenue.net_revenue)} | "
            f"{fmt_money(m.waterfall.staking_rewards)} |"
        )

    # Quarter total row
    lines.append(
        f"| **{quarter.quarter_name}** | — | "
        f"**{fmt_money(quarter.gross_revenue)}** | **{fmt_money(quarter.net_revenue)}** | "
        f"**{fmt_money(quarter.staking_rewards)}** |"
    )

    return "\n".join(lines)


def format_annual_summary(results: ScenarioResults) -> str:
    """Format annual summary table."""
    lines = [
        "## Annual Summary",
        "",
        "| Quarter | Gross Revenue | Net Revenue | Staking Rewards |",
        "|---------|---------------|-------------|-----------------|",
    ]

    for q in results.quarterly:
        lines.append(
            f"| {q.quarter_name} | {fmt_money(q.gross_revenue)} | "
            f"{fmt_money(q.net_revenue)} | {fmt_money(q.staking_rewards)} |"
        )

    lines.append(
        f"| **Year** | **{fmt_money(results.annual_gross_revenue)}** | "
        f"**{fmt_money(results.annual_net_revenue)}** | "
        f"**{fmt_money(results.annual_staking_rewards)}** |"
    )

    return "\n".join(lines)


def format_detailed_month(m: MonthResults) -> str:
    """Format detailed output for a single month."""
    lines = [
        f"### {m.month_name} (Month {m.month})",
        "",
        "**Rates:**",
        f"- SOFR: {fmt_pct(m.rates.sofr)}",
        f"- Savings Rate: {fmt_pct(m.rates.savings_rate)}",
        f"- Gross Revenue Rate: {fmt_pct(m.rates.gross_revenue_rate)}",
        f"- Farm Yield: {fmt_pct(m.rates.farm_yield)}",
        "",
        "**Agents:**",
        f"- Farmable Tokens: {fmt_money(m.farmable_tokens)}",
        f"- Sellable Tokens: {fmt_money(m.sellable_tokens)}",
        "",
        "**Supply:**",
        f"- USDS Supply: {fmt_money(m.supply.avg_usds_supply)}",
        f"- sUSDS Supply: {fmt_money(m.supply.avg_susds_supply)}",
        "",
        "**Revenue:**",
        f"- Gross Revenue: {fmt_money(m.revenue.gross_revenue)}",
        f"- Savings Expense: {fmt_money(m.revenue.savings_expense)}",
        f"- Net Revenue: {fmt_money(m.revenue.net_revenue)}",
        "",
        "**Waterfall:**",
        f"- Security Budget: {fmt_money(m.waterfall.security_budget)}",
        f"- Backstop Contribution: {fmt_money(m.waterfall.backstop_contribution)}",
        f"- Staking Rewards: {fmt_money(m.waterfall.staking_rewards)}",
    ]
    return "\n".join(lines)


def format_scenario_markdown(results: ScenarioResults, detailed: bool = False) -> str:
    """Format complete scenario results as markdown."""
    lines = [
        f"# {results.name}",
        "",
    ]

    if results.description:
        lines.extend([results.description, ""])

    lines.append("---")
    lines.append("")

    # Quarterly summaries with monthly details
    for quarter in results.quarterly:
        lines.append(format_quarter_table(quarter))
        lines.append("")
        lines.append("---")
        lines.append("")

    # Annual summary
    lines.append(format_annual_summary(results))

    # Detailed monthly output (optional)
    if detailed:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Monthly Details")
        lines.append("")
        for m in results.monthly:
            lines.append(format_detailed_month(m))
            lines.append("")

    return "\n".join(lines)
