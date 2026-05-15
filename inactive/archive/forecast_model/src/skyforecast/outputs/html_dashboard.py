"""HTML dashboard generator."""

from decimal import Decimal
from typing import Any, Dict, Optional

from ..engine import ScenarioResults
from ..loaders import ResolvedScenario


# Field to extension mapping
EXTENSION_FIELDS = {
    "base": ["base_usds", "sofr", "savings_rate_spread", "gross_revenue_rate_spread",
             "security_rate", "tier2_ratio", "tier3_ratio", "tier4_ratio"],
    "psm_exposure": ["psm_amount", "psm_pct"],
    "token_farming": ["spark_market_cap", "grove_market_cap", "keel_market_cap",
                      "star4_market_cap", "star5_market_cap", "farm_yield_spread",
                      "sell_token_rate", "unrewarded_usds_user"],
}


def fmt_money(value: Decimal) -> str:
    """Format money value with M suffix."""
    millions = float(value) / 1_000_000
    return f"{millions:,.2f}M"


def fmt_pct(value: Decimal) -> str:
    """Format as percentage."""
    return f"{float(value) * 100:.2f}%"


def fmt_num(value: Any) -> str:
    """Format number with K/M/B abbreviations."""
    if isinstance(value, str):
        return value
    if isinstance(value, Decimal):
        value = float(value)
    if isinstance(value, (int, float)):
        abs_val = abs(value)
        sign = "-" if value < 0 else ""
        if abs_val >= 1_000_000_000:
            return f"{sign}{abs_val/1_000_000_000:,.1f}B"
        if abs_val >= 1_000_000:
            return f"{sign}{abs_val/1_000_000:,.0f}M"
        if abs_val >= 1_000:
            return f"{sign}{abs_val/1_000:,.0f}K"
        return f"{value:,.0f}"
    return str(value)


def get_field_extension(field: str) -> str:
    """Get which extension a field belongs to."""
    for ext, fields in EXTENSION_FIELDS.items():
        if field in fields:
            return ext
    return "other"


def group_by_extension(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Group fields by their extension."""
    grouped = {"base": {}, "psm_exposure": {}, "token_farming": {}, "other": {}}
    for key, val in data.items():
        ext = get_field_extension(key)
        if ext not in grouped:
            grouped[ext] = {}
        grouped[ext][key] = val
    return grouped


def generate_dashboard_html(
    scenario: ResolvedScenario,
    results: ScenarioResults,
    extensions: Optional[Dict[str, Any]] = None,
) -> str:
    """Generate HTML dashboard with inputs and outputs."""
    extensions = extensions or {}

    # Group baseline by extension
    grouped_baseline = group_by_extension(scenario.baseline)

    # Build base model section
    base_rows = ""
    for key, val in grouped_baseline.get("base", {}).items():
        base_rows += f"<tr><td>{key}</td><td>{fmt_num(val) if isinstance(val, (int, float, Decimal)) else val}</td></tr>\n"

    # Build trajectories section
    trajectory_rows = ""
    for key, traj in scenario.trajectories.items():
        points_str = " → ".join(f"M{m}: {fmt_num(v)}" for m, v in sorted(traj.points.items()))
        trajectory_rows += f"<tr><td>{key}</td><td>{points_str} ({traj.mode})</td></tr>\n"

    # Build PSM extension section
    psm_config = extensions.get("psm_exposure", {})
    psm_rows = ""
    psm_pct = scenario.baseline.get("psm_pct", psm_config.get("pct"))
    if psm_pct:
        psm_rows += f"<tr><td>pct</td><td>{float(psm_pct)*100:.0f}% of total USDS</td></tr>\n"
    else:
        psm_rows += f"<tr><td>amount</td><td>{fmt_num(psm_config.get('amount', 0))}</td></tr>\n"
    psm_rows += f"<tr><td>spread</td><td>{psm_config.get('spread', '-0.0030')}</td></tr>\n"

    # Build USDT subsidy section
    usdt_config = extensions.get("usdt_subsidy", {})
    usdt_rows = ""
    usdt_rows += f"<tr><td>amount</td><td>{fmt_num(usdt_config.get('amount', 0))}</td></tr>\n"

    # Build subsidized borrow section
    sub_config = extensions.get("subsidized_borrow", {})
    sub_rows = ""
    sub_rows += f"<tr><td>total_amount</td><td>{fmt_num(sub_config.get('total_amount', 0))}</td></tr>\n"
    sub_rows += f"<tr><td>duration</td><td>{sub_config.get('duration_months', 24)} months</td></tr>\n"

    # Build srUSDS cost section
    sr_config = extensions.get("srusds_cost", {})
    sr_rows = ""
    sr_rows += f"<tr><td>annual_cost</td><td>{fmt_num(sr_config.get('annual_cost', 0))}</td></tr>\n"

    # Build core vaults section
    cv_config = extensions.get("core_vaults", {})
    cv_rows = ""
    cv_rows += f"<tr><td>debt</td><td>{fmt_num(cv_config.get('debt', 0))}</td></tr>\n"
    cv_rate = cv_config.get('rate', '0.08')
    cv_rows += f"<tr><td>rate</td><td>{float(cv_rate)*100:.1f}%</td></tr>\n"

    # Build token farming section (includes agent launches)
    farm_config = extensions.get("token_farming", {})
    farm_rows = ""
    farm_rows += f"<tr><td>distribution_rate</td><td>{farm_config.get('distribution_rate', '0.175')}</td></tr>\n"
    farm_rows += f"<tr><td>farm_yield_spread</td><td>{farm_config.get('farm_yield_spread', '0.0010')}</td></tr>\n"

    # Stars from extension config
    stars_config = farm_config.get("stars", {})
    spark_mc = stars_config.get("spark", {}).get("market_cap", 0)
    for star_name, star_data in stars_config.items():
        ownership = star_data.get("ownership", "0")
        launch = star_data.get("launch_month", "?")
        if star_name == "spark":
            mc_display = fmt_num(star_data.get("market_cap", 0))
        else:
            pct = star_data.get("market_cap_pct", "0")
            mc_display = f"{float(pct)*100:.0f}% of Spark"
        farm_rows += f"<tr><td>{star_name}</td><td>{mc_display} @ {ownership} (M{launch})</td></tr>\n"

    # Build genesis prime section
    prime_config = extensions.get("genesis_prime", {})
    prime_rows = ""
    prime_rows += f"<tr><td>sell_rate</td><td>{prime_config.get('sell_rate', '0.175')}</td></tr>\n"
    primes_config = prime_config.get("primes", {})
    for prime_name, prime_data in primes_config.items():
        pct = prime_data.get("market_cap_pct", "0")
        ownership = prime_data.get("ownership", "0")
        launch = prime_data.get("launch_month", "?")
        prime_rows += f"<tr><td>{prime_name}</td><td>{float(pct)*100:.0f}% of Spark @ {ownership} (M{launch})</td></tr>\n"

    # Build changes section grouped by extension
    changes_by_ext = {"base": [], "psm_exposure": [], "token_farming": [], "other": []}
    for month in sorted(scenario.changes.keys()):
        for key, val in scenario.changes[month].items():
            ext = get_field_extension(key)
            if ext not in changes_by_ext:
                changes_by_ext[ext] = []
            changes_by_ext[ext].append((month, key, val))

    def format_changes(changes_list):
        if not changes_list:
            return ""
        rows = ""
        for month, key, val in changes_list:
            rows += f"<tr><td>M{month}</td><td>{key}</td><td>{fmt_num(val) if isinstance(val, (int, float, Decimal)) else val}</td></tr>\n"
        return rows

    base_changes = format_changes(changes_by_ext.get("base", []))
    psm_changes = format_changes(changes_by_ext.get("psm_exposure", []))
    farm_changes = format_changes(changes_by_ext.get("token_farming", []))

    # Quarterly results
    quarterly_html = ""
    for q in results.quarterly:
        month_rows = ""
        q_security = Decimal("0")
        for m in q.months:
            q_security += m.waterfall.security_budget
            net_profit = m.waterfall.net_backstop_change + m.waterfall.staking_rewards
            month_rows += f"""
            <tr>
                <td>{m.month_name}</td>
                <td>{fmt_money(m.supply.avg_usds_supply)}</td>
                <td>{fmt_money(m.revenue.gross_revenue)}</td>
                <td>{fmt_money(m.revenue.net_revenue)}</td>
                <td>{fmt_money(m.waterfall.security_budget)}</td>
                <td>{fmt_money(net_profit)}</td>
                <td>{fmt_money(m.waterfall.staking_rewards)}</td>
            </tr>"""

        q_net_profit = q.net_backstop_change + q.staking_rewards
        quarterly_html += f"""
        <div class="quarter">
            <h3>{q.quarter_name}</h3>
            <table>
                <tr><th>Month</th><th>USDS</th><th>Gross</th><th>Net Rev</th><th>Security</th><th>Profit</th><th>Stake</th></tr>
                {month_rows}
                <tr class="total">
                    <td><strong>{q.quarter_name}</strong></td>
                    <td>—</td>
                    <td><strong>{fmt_money(q.gross_revenue)}</strong></td>
                    <td><strong>{fmt_money(q.net_revenue)}</strong></td>
                    <td><strong>{fmt_money(q_security)}</strong></td>
                    <td><strong>{fmt_money(q_net_profit)}</strong></td>
                    <td><strong>{fmt_money(q.staking_rewards)}</strong></td>
                </tr>
            </table>
        </div>"""

    # Annual summary - calculate totals
    annual_security = sum(q.security_budget for q in results.quarterly)
    annual_profit = sum(q.net_backstop_change for q in results.quarterly) + results.annual_staking_rewards

    last_q = results.quarterly[-1] if results.quarterly else None
    last_m = last_q.months[-1] if last_q and last_q.months else None

    annual_rows = ""
    annual_gross = Decimal("0")
    for q in results.quarterly:
        annual_gross += q.gross_revenue
        q_profit = q.net_backstop_change + q.staking_rewards
        q_last = q.months[-1] if q.months else None
        q_end_usds = q_last.supply.avg_usds_supply if q_last else Decimal("0")
        annual_rows += f"""
        <tr>
            <td>{q.quarter_name}</td>
            <td>{fmt_money(q_end_usds)}</td>
            <td>{fmt_money(q.gross_revenue)}</td>
            <td>{fmt_money(q.net_revenue)}</td>
            <td>{fmt_money(q.security_budget)}</td>
            <td>{fmt_money(q_profit)}</td>
            <td>{fmt_money(q.staking_rewards)}</td>
        </tr>"""

    final_usds = last_m.supply.avg_usds_supply if last_m else Decimal("0")

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{results.name} - Sky Forecast</title>
    <meta http-equiv="refresh" content="5">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            padding: 20px;
            max-width: 1600px;
            margin: 0 auto;
        }}
        h1 {{ color: #fff; margin-bottom: 5px; }}
        h2 {{ color: #888; font-size: 14px; margin-bottom: 20px; font-weight: normal; }}
        h3 {{ color: #4a9eff; margin-bottom: 10px; font-size: 13px; }}
        .grid {{ display: grid; grid-template-columns: 400px 1fr; gap: 20px; }}
        .inputs {{ background: #151515; padding: 15px; border-radius: 8px; }}
        .outputs {{ background: #151515; padding: 15px; border-radius: 8px; }}
        .section {{ margin-bottom: 15px; padding: 10px; background: #1a1a1a; border-radius: 6px; }}
        .section-title {{
            font-size: 11px;
            color: #4a9eff;
            text-transform: uppercase;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }}
        .ext-title {{
            font-size: 10px;
            color: #888;
            text-transform: uppercase;
            margin-bottom: 6px;
            letter-spacing: 1px;
            border-bottom: 1px solid #333;
            padding-bottom: 4px;
        }}
        table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
        th {{ text-align: left; padding: 4px 6px; color: #666; font-weight: normal; border-bottom: 1px solid #333; }}
        td {{ padding: 4px 6px; border-bottom: 1px solid #222; }}
        tr.total td {{ border-top: 2px solid #333; background: #1a1a1a; }}
        .quarters {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }}
        .quarter {{ background: #1a1a1a; padding: 12px; border-radius: 6px; }}
        .quarter h3 {{ font-size: 14px; }}
        .annual {{ margin-top: 20px; }}
        .annual table {{ max-width: 700px; }}
        .annual tr:last-child td {{ background: #1a2a1a; font-weight: bold; }}
        .highlight {{ color: #4aff4a; }}
        .timestamp {{ color: #444; font-size: 11px; margin-top: 20px; }}
        .extensions {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
    </style>
</head>
<body>
    <h1>{results.name}</h1>
    <h2>{results.description}</h2>

    <div class="grid">
        <div class="inputs">
            <div class="section">
                <div class="section-title">Base Model</div>
                <table>{base_rows}</table>
                {"<div class='ext-title' style='margin-top:10px'>Trajectories</div><table>" + trajectory_rows + "</table>" if trajectory_rows else ""}
                {"<div class='ext-title' style='margin-top:10px'>Changes</div><table><tr><th>M</th><th>Field</th><th>Value</th></tr>" + base_changes + "</table>" if base_changes else ""}
            </div>

            <div class="extensions">
                <div class="section">
                    <div class="ext-title">PSM Exposure</div>
                    <table>{psm_rows}</table>
                    {"<div class='ext-title' style='margin-top:10px'>Changes</div><table><tr><th>M</th><th>Field</th><th>Value</th></tr>" + psm_changes + "</table>" if psm_changes else ""}
                </div>

                <div class="section">
                    <div class="ext-title">USDT Subsidy</div>
                    <table>{usdt_rows}</table>
                </div>

                <div class="section">
                    <div class="ext-title">Subsidized Borrow</div>
                    <table>{sub_rows}</table>
                </div>

                <div class="section">
                    <div class="ext-title">srUSDS Cost</div>
                    <table>{sr_rows}</table>
                </div>

                <div class="section">
                    <div class="ext-title">Core Vaults</div>
                    <table>{cv_rows}</table>
                </div>
            </div>

            <div class="section">
                <div class="ext-title">Token Farming (Stars)</div>
                <table>{farm_rows}</table>
                {"<div class='ext-title' style='margin-top:10px'>Changes</div><table><tr><th>M</th><th>Field</th><th>Value</th></tr>" + farm_changes + "</table>" if farm_changes else ""}
            </div>

            <div class="section">
                <div class="ext-title">Genesis Prime</div>
                <table>{prime_rows}</table>
            </div>
        </div>

        <div class="outputs">
            <div class="section-title">Quarterly Results</div>
            <div class="quarters">
                {quarterly_html}
            </div>

            <div class="annual">
                <div class="section-title">Annual Summary</div>
                <table>
                    <tr><th>Quarter</th><th>USDS</th><th>Gross Rev</th><th>Net Revenue</th><th>Security</th><th>Profit</th><th>Staking</th></tr>
                    {annual_rows}
                    <tr>
                        <td>Year</td>
                        <td class="highlight">{fmt_money(final_usds)}</td>
                        <td class="highlight">{fmt_money(annual_gross)}</td>
                        <td class="highlight">{fmt_money(results.annual_net_revenue)}</td>
                        <td class="highlight">{fmt_money(annual_security)}</td>
                        <td class="highlight">{fmt_money(annual_profit)}</td>
                        <td class="highlight">{fmt_money(results.annual_staking_rewards)}</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>

    <div class="timestamp">Auto-refreshes every 5s</div>
</body>
</html>"""

    return html
