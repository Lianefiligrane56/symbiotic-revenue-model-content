"""
Symbiotic Historic Data Analysis
================================
Display historic P&L, rewards trends, and TVL over time.

Usage in Hex:
    from scripts.historic_data import display_historic_pl, display_rewards_trends, display_tvl_trends
"""

import pandas as pd
from IPython.display import HTML, display


# ═══════════════════════════════════════════════════════════════
# 1. HISTORIC P&L OVER TIME
# ═══════════════════════════════════════════════════════════════

def calculate_monthly_pl(df_rewards, time_col='time', amount_col=None, 
                         fee_rate=0.10, monthly_opex=474000):
    """
    Calculate monthly P&L from rewards data.
    
    Args:
        df_rewards: DataFrame with rewards data
        time_col: Column name for timestamp
        amount_col: Column name for amounts (auto-detected if None)
        fee_rate: Protocol fee rate (default 10%)
        monthly_opex: Monthly operating costs
    
    Returns:
        DataFrame with monthly P&L
    """
    df = df_rewards.copy()
    
    # Auto-detect amount column
    if amount_col is None:
        for col in ['total_rewards_usd', 'amount_usd', 'rewards_usd', 'amount', 'value']:
            if col in df.columns:
                amount_col = col
                break
        if amount_col is None:
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            amount_col = numeric_cols[0] if len(numeric_cols) > 0 else None
    
    # Convert to datetime
    df[time_col] = pd.to_datetime(df[time_col])
    df['month'] = df[time_col].dt.to_period('M')
    
    # Aggregate by month
    monthly = df.groupby('month').agg({
        amount_col: 'sum'
    }).reset_index()
    
    monthly.columns = ['Month', 'Gross Rewards']
    
    # Calculate P&L components
    monthly['Protocol Revenue'] = monthly['Gross Rewards'] * fee_rate
    monthly['Staker Rewards'] = monthly['Gross Rewards'] * (1 - fee_rate)
    monthly['Operating Costs'] = monthly_opex
    monthly['Net Income'] = monthly['Protocol Revenue'] - monthly['Operating Costs']
    monthly['Net Margin %'] = (monthly['Net Income'] / monthly['Protocol Revenue'] * 100).round(1)
    
    # Format month
    monthly['Month'] = monthly['Month'].astype(str)
    
    return monthly


def display_historic_pl(df_rewards, time_col='time', amount_col=None,
                        fee_rate=0.10, monthly_opex=474000):
    """
    Display historic P&L table.
    """
    monthly = calculate_monthly_pl(df_rewards, time_col, amount_col, fee_rate, monthly_opex)
    
    # Create display version with formatting
    display_df = monthly.copy()
    display_df['Gross Rewards'] = display_df['Gross Rewards'].apply(lambda x: f'${x:,.0f}')
    display_df['Protocol Revenue'] = display_df['Protocol Revenue'].apply(lambda x: f'${x:,.0f}')
    display_df['Staker Rewards'] = display_df['Staker Rewards'].apply(lambda x: f'${x:,.0f}')
    display_df['Operating Costs'] = display_df['Operating Costs'].apply(lambda x: f'(${x:,.0f})')
    display_df['Net Income'] = monthly['Net Income'].apply(lambda x: f'${x:,.0f}' if x >= 0 else f'(${abs(x):,.0f})')
    display_df['Net Margin %'] = display_df['Net Margin %'].apply(lambda x: f'{x}%')
    
    print("═" * 80)
    print("                    HISTORIC P&L BY MONTH")
    print("═" * 80)
    display(display_df)
    
    # Summary
    total_revenue = monthly['Protocol Revenue'].sum()
    total_costs = monthly['Operating Costs'].sum()
    total_net = monthly['Net Income'].sum()
    
    print(f"\n📊 PERIOD TOTALS")
    print(f"   Total Protocol Revenue: ${total_revenue:,.0f}")
    print(f"   Total Operating Costs:  ${total_costs:,.0f}")
    print(f"   Total Net Income:       ${total_net:,.0f}")
    
    return monthly


# ═══════════════════════════════════════════════════════════════
# 2. HISTORIC REWARDS TRENDS
# ═══════════════════════════════════════════════════════════════

def calculate_rewards_by_month(df_rewards, time_col='time', amount_col=None):
    """
    Calculate rewards trends by month.
    """
    df = df_rewards.copy()
    
    # Auto-detect amount column
    if amount_col is None:
        for col in ['total_rewards_usd', 'amount_usd', 'rewards_usd', 'amount', 'value']:
            if col in df.columns:
                amount_col = col
                break
    
    df[time_col] = pd.to_datetime(df[time_col])
    df['month'] = df[time_col].dt.to_period('M')
    
    monthly = df.groupby('month').agg({
        amount_col: ['sum', 'count', 'mean']
    }).reset_index()
    
    monthly.columns = ['Month', 'Total Rewards', 'Transactions', 'Avg Reward']
    monthly['Month'] = monthly['Month'].astype(str)
    
    # Calculate MoM growth
    monthly['MoM Growth %'] = monthly['Total Rewards'].pct_change() * 100
    
    return monthly


def calculate_rewards_by_network(df_rewards, network_col='network', amount_col=None):
    """
    Calculate rewards breakdown by network.
    """
    df = df_rewards.copy()
    
    # Auto-detect columns
    if amount_col is None:
        for col in ['total_rewards_usd', 'amount_usd', 'rewards_usd', 'amount']:
            if col in df.columns:
                amount_col = col
                break
    
    if network_col not in df.columns:
        for col in ['network', 'vault', 'vault_name', 'protocol']:
            if col in df.columns:
                network_col = col
                break
    
    if network_col not in df.columns:
        return pd.DataFrame({'Note': ['No network column found']})
    
    by_network = df.groupby(network_col).agg({
        amount_col: 'sum'
    }).reset_index()
    
    by_network.columns = ['Network', 'Total Rewards']
    by_network = by_network.sort_values('Total Rewards', ascending=False)
    by_network['% of Total'] = (by_network['Total Rewards'] / by_network['Total Rewards'].sum() * 100).round(1)
    
    return by_network


def display_rewards_trends(df_rewards, df_rewards_network=None, time_col='time', amount_col=None):
    """
    Display rewards trends over time and by network.
    """
    print("═" * 80)
    print("                    HISTORIC REWARDS TRENDS")
    print("═" * 80)
    
    # Monthly trends
    print("\n📈 REWARDS BY MONTH")
    monthly = calculate_rewards_by_month(df_rewards, time_col, amount_col)
    
    display_df = monthly.copy()
    display_df['Total Rewards'] = display_df['Total Rewards'].apply(lambda x: f'${x:,.0f}')
    display_df['Transactions'] = display_df['Transactions'].apply(lambda x: f'{x:,}')
    display_df['Avg Reward'] = display_df['Avg Reward'].apply(lambda x: f'${x:,.2f}')
    display_df['MoM Growth %'] = display_df['MoM Growth %'].apply(lambda x: f'{x:+.1f}%' if pd.notna(x) else '-')
    
    display(display_df)
    
    # Network breakdown
    if df_rewards_network is not None:
        print("\n📊 REWARDS BY NETWORK")
        by_network = df_rewards_network.copy()
    else:
        print("\n📊 REWARDS BY NETWORK (from main data)")
        by_network = calculate_rewards_by_network(df_rewards, amount_col=amount_col)
    
    if 'Total Rewards' in by_network.columns:
        display_network = by_network.head(10).copy()
        if by_network['Total Rewards'].dtype in ['float64', 'int64']:
            display_network['Total Rewards'] = display_network['Total Rewards'].apply(lambda x: f'${x:,.0f}')
        display(display_network)
    else:
        display(by_network.head(10))
    
    return monthly


# ═══════════════════════════════════════════════════════════════
# 3. HISTORIC TVL TRENDS
# ═══════════════════════════════════════════════════════════════

def calculate_tvl_trends(df_tvl, time_col='time', tvl_col='tvl'):
    """
    Calculate TVL trends over time.
    """
    df = df_tvl.copy()
    
    # Auto-detect columns
    if tvl_col not in df.columns:
        for col in ['tvl', 'total_tvl', 'tvl_usd', 'value', 'amount']:
            if col in df.columns:
                tvl_col = col
                break
    
    if time_col not in df.columns:
        for col in ['time', 'date', 'timestamp', 'block_time']:
            if col in df.columns:
                time_col = col
                break
    
    df[time_col] = pd.to_datetime(df[time_col])
    df = df.sort_values(time_col)
    
    # Get daily/weekly snapshots
    df['date'] = df[time_col].dt.date
    daily = df.groupby('date').agg({
        tvl_col: 'last'  # End of day TVL
    }).reset_index()
    
    daily.columns = ['Date', 'TVL']
    
    # Calculate changes
    daily['Change'] = daily['TVL'].diff()
    daily['Change %'] = daily['TVL'].pct_change() * 100
    
    return daily


def display_tvl_trends(df_tvl, time_col='time', tvl_col='tvl'):
    """
    Display TVL trends over time.
    """
    print("═" * 80)
    print("                    HISTORIC TVL TRENDS")
    print("═" * 80)
    
    daily = calculate_tvl_trends(df_tvl, time_col, tvl_col)
    
    # Summary stats
    current_tvl = daily['TVL'].iloc[-1] if len(daily) > 0 else 0
    max_tvl = daily['TVL'].max()
    min_tvl = daily['TVL'].min()
    avg_tvl = daily['TVL'].mean()
    
    print(f"\n📊 TVL SUMMARY")
    print(f"   Current TVL:  ${current_tvl/1e9:.2f}B")
    print(f"   Peak TVL:     ${max_tvl/1e9:.2f}B")
    print(f"   Lowest TVL:   ${min_tvl/1e9:.2f}B")
    print(f"   Average TVL:  ${avg_tvl/1e9:.2f}B")
    
    # Show recent data
    print(f"\n📈 RECENT TVL (Last 20 days)")
    recent = daily.tail(20).copy()
    recent['TVL'] = recent['TVL'].apply(lambda x: f'${x/1e9:.3f}B')
    recent['Change'] = recent['Change'].apply(lambda x: f'${x/1e6:+,.1f}M' if pd.notna(x) else '-')
    recent['Change %'] = recent['Change %'].apply(lambda x: f'{x:+.2f}%' if pd.notna(x) else '-')
    
    display(recent)
    
    return daily


# ═══════════════════════════════════════════════════════════════
# COMBINED DISPLAY
# ═══════════════════════════════════════════════════════════════

def display_all_historic(df_rewards, df_tvl, df_rewards_network=None,
                        fee_rate=0.10, monthly_opex=474000):
    """
    Display all historic data: P&L, Rewards, and TVL.
    """
    print("\n" + "█" * 80)
    print("                    SYMBIOTIC HISTORIC DATA ANALYSIS")
    print("█" * 80 + "\n")
    
    # 1. Historic P&L
    display_historic_pl(df_rewards, fee_rate=fee_rate, monthly_opex=monthly_opex)
    
    print("\n")
    
    # 2. Rewards Trends
    display_rewards_trends(df_rewards, df_rewards_network)
    
    print("\n")
    
    # 3. TVL Trends
    display_tvl_trends(df_tvl)


# Print available functions
print("📊 Historic Data Analysis loaded!")
print("   → display_historic_pl(df_rewards)")
print("   → display_rewards_trends(df_rewards, df_rewards_network)")
print("   → display_tvl_trends(df_tvl)")
print("   → display_all_historic(df_rewards, df_tvl)")

