"""
Symbiotic Protocol P&L Calculator
=================================
Calculate Protocol Profit & Loss from rewards data.

Usage in Hex:
    from scripts.protocol_pl import calculate_pl, display_pl, PLConfig
"""

import pandas as pd
from dataclasses import dataclass
from typing import Optional, Dict

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

@dataclass
class PLConfig:
    """P&L Configuration - adjust these for different scenarios"""
    
    # Protocol fee assumptions by vault type
    vault_fees: Dict[str, float] = None
    
    # Default protocol fee if no vault breakdown
    default_fee_rate: float = 0.10
    
    # Monthly operating costs (from GPRP financials)
    monthly_opex: float = 474000
    
    # OpEx breakdown (from actual GPRP P&L)
    opex_personnel: float = 0.54      # 54% - Personnel/Contractors
    opex_audit: float = 0.23          # 23% - Audit & Security
    opex_marketing: float = 0.11      # 11% - Marketing & BD
    opex_legal: float = 0.03          # 3% - Legal & Professional
    opex_other: float = 0.09          # 9% - Other
    
    # Number of months to calculate
    months: int = 6
    
    def __post_init__(self):
        if self.vault_fees is None:
            self.vault_fees = {
                'Relay': 0.05,       # 5% - High volume, competitive
                'Staking': 0.10,     # 10% - Standard restaking
                'Insurance': 0.15,   # 15% - Premium product
                'LRT': 0.08,         # 8% - Competitive with others
                'Liquid': 0.10,      # 10% - Standard
                'Default': 0.10      # 10% - Fallback
            }


# Default configuration
DEFAULT_CONFIG = PLConfig()


# ═══════════════════════════════════════════════════════════════
# P&L CALCULATION
# ═══════════════════════════════════════════════════════════════

def calculate_pl(df_rewards, config: PLConfig = None, amount_col: str = None):
    """
    Calculate Protocol P&L from rewards data.
    
    Args:
        df_rewards: DataFrame with rewards data
        config: PLConfig object (uses defaults if None)
        amount_col: Column name for reward amounts (auto-detected if None)
    
    Returns:
        dict with P&L metrics
    """
    if config is None:
        config = DEFAULT_CONFIG
    
    # Auto-detect amount column
    if amount_col is None:
        for col in ['total_rewards_usd', 'amount_usd', 'rewards_usd', 'amount', 'value']:
            if col in df_rewards.columns:
                amount_col = col
                break
        
        if amount_col is None:
            numeric_cols = df_rewards.select_dtypes(include=['float64', 'int64']).columns
            amount_col = numeric_cols[0] if len(numeric_cols) > 0 else None
    
    if amount_col is None:
        raise ValueError("Could not find amount column in data")
    
    # Calculate gross rewards
    gross_rewards = df_rewards[amount_col].sum()
    
    # Calculate protocol revenue
    protocol_revenue = gross_rewards * config.default_fee_rate
    staker_rewards = gross_rewards - protocol_revenue
    
    # Calculate operating expenses
    total_opex = config.monthly_opex * config.months
    personnel = total_opex * config.opex_personnel
    audit = total_opex * config.opex_audit
    marketing = total_opex * config.opex_marketing
    legal = total_opex * config.opex_legal
    other = total_opex * config.opex_other
    
    # Calculate net income
    net_income = protocol_revenue - total_opex
    gross_margin = (protocol_revenue / gross_rewards * 100) if gross_rewards > 0 else 0
    net_margin = (net_income / protocol_revenue * 100) if protocol_revenue > 0 else 0
    
    return {
        'gross_rewards': gross_rewards,
        'staker_rewards': staker_rewards,
        'protocol_revenue': protocol_revenue,
        'total_opex': total_opex,
        'opex_personnel': personnel,
        'opex_audit': audit,
        'opex_marketing': marketing,
        'opex_legal': legal,
        'opex_other': other,
        'net_income': net_income,
        'gross_margin': gross_margin,
        'net_margin': net_margin,
        'months': config.months,
        'fee_rate': config.default_fee_rate,
    }


def build_pl_dataframe(pl_metrics: dict) -> pd.DataFrame:
    """
    Build a formatted P&L DataFrame for display.
    
    Args:
        pl_metrics: dict from calculate_pl()
    
    Returns:
        pandas DataFrame
    """
    m = pl_metrics
    
    pl_data = {
        'Line Item': [
            'REVENUE',
            'Gross Rewards Generated',
            f'Less: Staker Distribution ({(1-m["fee_rate"])*100:.0f}%)',
            '─────────────────────────',
            f'Protocol Revenue ({m["fee_rate"]*100:.0f}%)',
            '',
            'OPERATING EXPENSES',
            'Personnel & Contractors (54%)',
            'Audit & Security (23%)',
            'Marketing & BD (11%)',
            'Legal & Professional (3%)',
            'Other Operating (9%)',
            '─────────────────────────',
            'Total Operating Expenses',
            '',
            '═════════════════════════',
            'NET INCOME',
            '',
            'MARGINS',
            'Gross Margin',
            'Net Margin',
        ],
        'Amount': [
            '',
            f'${m["gross_rewards"]:,.0f}',
            f'(${m["staker_rewards"]:,.0f})',
            '',
            f'${m["protocol_revenue"]:,.0f}',
            '',
            '',
            f'(${m["opex_personnel"]:,.0f})',
            f'(${m["opex_audit"]:,.0f})',
            f'(${m["opex_marketing"]:,.0f})',
            f'(${m["opex_legal"]:,.0f})',
            f'(${m["opex_other"]:,.0f})',
            '',
            f'(${m["total_opex"]:,.0f})',
            '',
            '',
            f'${m["net_income"]:,.0f}',
            '',
            '',
            f'{m["gross_margin"]:.1f}%',
            f'{m["net_margin"]:.1f}%',
        ]
    }
    
    return pd.DataFrame(pl_data)


def display_pl(df_rewards, config: PLConfig = None, style_func=None):
    """
    Calculate and display P&L with styling.
    
    Args:
        df_rewards: DataFrame with rewards data
        config: PLConfig object
        style_func: Optional styling function (e.g., style_df)
    
    Returns:
        tuple (pl_metrics dict, pl_dataframe)
    """
    from IPython.display import display
    
    # Calculate
    metrics = calculate_pl(df_rewards, config)
    df_pl = build_pl_dataframe(metrics)
    
    # Display
    print("=" * 60)
    print("         SYMBIOTIC PROTOCOL P&L")
    print("=" * 60)
    
    if style_func:
        display(style_func(df_pl))
    else:
        display(df_pl)
    
    # Print summary
    print(f"\n📊 SUMMARY ({metrics['months']} months)")
    print(f"   Gross Rewards:    ${metrics['gross_rewards']/1e6:.2f}M")
    print(f"   Protocol Revenue: ${metrics['protocol_revenue']/1e6:.2f}M")
    print(f"   Operating Costs:  ${metrics['total_opex']/1e6:.2f}M")
    print(f"   Net Income:       ${metrics['net_income']/1e6:.2f}M")
    print(f"   Net Margin:       {metrics['net_margin']:.1f}%")
    
    print(f"\n⚠️  Assumptions:")
    print(f"   • Protocol fee: {metrics['fee_rate']*100:.0f}% (currently 0% in growth phase)")
    print(f"   • Monthly OpEx: ${config.monthly_opex if config else DEFAULT_CONFIG.monthly_opex:,.0f}")
    
    return metrics, df_pl


# ═══════════════════════════════════════════════════════════════
# SCENARIO ANALYSIS
# ═══════════════════════════════════════════════════════════════

def scenario_analysis(df_rewards, fee_rates=[0.05, 0.10, 0.15, 0.20]):
    """
    Run P&L scenarios with different fee rates.
    
    Args:
        df_rewards: DataFrame with rewards data
        fee_rates: List of fee rates to test
    
    Returns:
        DataFrame with scenario comparison
    """
    scenarios = []
    
    for rate in fee_rates:
        config = PLConfig(default_fee_rate=rate)
        metrics = calculate_pl(df_rewards, config)
        
        scenarios.append({
            'Fee Rate': f'{rate*100:.0f}%',
            'Protocol Revenue': f'${metrics["protocol_revenue"]/1e6:.2f}M',
            'Net Income': f'${metrics["net_income"]/1e6:.2f}M',
            'Net Margin': f'{metrics["net_margin"]:.1f}%',
            'Breakeven': '✅' if metrics['net_income'] > 0 else '❌'
        })
    
    return pd.DataFrame(scenarios)


# Print available functions when imported
print("📊 Protocol P&L Calculator loaded!")
print("   → calculate_pl(df_rewards, config)")
print("   → build_pl_dataframe(metrics)")
print("   → display_pl(df_rewards, config, style_func)")
print("   → scenario_analysis(df_rewards, fee_rates)")
print("   → PLConfig (configuration class)")

