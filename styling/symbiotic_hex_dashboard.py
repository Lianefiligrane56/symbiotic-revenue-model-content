"""
================================================================================
SYMBIOTIC REVENUE MODEL - HEX DASHBOARD
================================================================================
Copy this into Hex.tech as Python cells

HOW TO USE IN HEX:
1. Go to hex.tech and create a new project
2. Add your Dune API key as a secret: Settings > Secrets > DUNE_API_KEY
3. Copy each section below into separate Python cells
4. Run all cells to generate the dashboard
================================================================================
"""

# ============================================================================
# CELL 0: DISPLAY INTRODUCTION FROM GITHUB (Markdown Cell)
# ============================================================================
# Copy this into a Python cell in Hex - displays your Obsidian content

import requests
import time
from IPython.display import Markdown, display

# Fetch Introduction.md from your GitHub repo (cache-busted)
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Lianefiligrane56/symbiotic-revenue-model-content/main/Introduction.md"
response = requests.get(f"{GITHUB_RAW_URL}?t={int(time.time())}")

if response.status_code == 200:
    display(Markdown(response.text))
    print("✅ Introduction loaded from GitHub")
else:
    print(f"⚠️ Could not fetch Introduction.md (Status: {response.status_code})")


# ============================================================================
# CELL 1: IMPORTS AND CONFIGURATION
# ============================================================================
# Copy this into a Python cell in Hex

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# Get API key from Hex secrets (or use directly for testing)
# DUNE_API_KEY = hex.env.get('DUNE_API_KEY')
DUNE_API_KEY = "R0AXtXn3orSdCiylk2dY72XWs95Q4Hg7"

print("✅ Imports loaded successfully")


# ============================================================================
# CELL 2: FETCH LIVE DATA FROM DUNE
# ============================================================================
# Copy this into a Python cell in Hex

from dune_client.client import DuneClient

dune = DuneClient(DUNE_API_KEY)

# Fetch all queries
print("📊 Fetching Dune data...")

try:
    # V1 Rewards
    rewards_data = dune.get_latest_result(5734268)
    df_rewards = pd.DataFrame(rewards_data.result.rows)
    print(f"   ✅ Rewards: {len(df_rewards)} rows")
    
    # Network Rewards
    network_data = dune.get_latest_result(5845829)
    df_networks = pd.DataFrame(network_data.result.rows)
    print(f"   ✅ Networks: {len(df_networks)} rows")
    
    # TVL All Vaults
    tvl_data = dune.get_latest_result(4627837)
    df_tvl = pd.DataFrame(tvl_data.result.rows)
    print(f"   ✅ TVL: {len(df_tvl)} rows")
    
    # TVL Over Time
    tvl_time_data = dune.get_latest_result(4921148)
    df_tvl_time = pd.DataFrame(tvl_time_data.result.rows)
    print(f"   ✅ TVL Over Time: {len(df_tvl_time)} rows")
    
    # TVL By Collateral
    collateral_data = dune.get_latest_result(4921564)
    df_collateral = pd.DataFrame(collateral_data.result.rows)
    print(f"   ✅ Collateral: {len(df_collateral)} rows")
    
    # Operators
    operator_data = dune.get_latest_result(4543572)
    df_operators = pd.DataFrame(operator_data.result.rows)
    print(f"   ✅ Operators: {len(df_operators)} rows")
    
    data_loaded = True
    print("\n✅ All data loaded successfully!")
    
except Exception as e:
    print(f"⚠️ Error fetching data: {e}")
    data_loaded = False


# ============================================================================
# CELL 3: CALCULATE LIVE METRICS
# ============================================================================
# Copy this into a Python cell in Hex

# Calculate current metrics from live data
if data_loaded:
    # TVL
    if 'tvl' in df_tvl.columns:
        current_tvl = df_tvl['tvl'].sum() / 1e9
    else:
        current_tvl = 1.0
    
    # Networks
    unique_networks = len(df_networks) if len(df_networks) > 0 else 3
    
    # Total Rewards
    if 'rewards_usd' in df_rewards.columns:
        total_rewards = df_rewards['rewards_usd'].sum() / 1e6
    elif 'total_distributed_usd' in df_rewards.columns:
        total_rewards = df_rewards['total_distributed_usd'].sum() / 1e6
    else:
        total_rewards = 1.0
    
    # Operators
    if 'registered_operators' in df_operators.columns:
        operator_count = df_operators['registered_operators'].max()
    else:
        operator_count = len(df_operators)
else:
    current_tvl = 1.32
    unique_networks = 3
    total_rewards = 1.41
    operator_count = 181

print(f"""
================================================================================
📊 LIVE METRICS
================================================================================
   Current TVL:        ${current_tvl:.2f}B
   Active Networks:    {unique_networks}
   Total Rewards:      ${total_rewards:.2f}M
   Operator Count:     {operator_count}
================================================================================
""")


# ============================================================================
# CELL 4: REVENUE MODEL PARAMETERS (INPUT CELL)
# ============================================================================
# In Hex, make this an INPUT CELL so users can adjust parameters

# Base Parameters (from live data)
tvl_base = current_tvl  # $B
networks_year1 = max(unique_networks, 3)
tvl_growth_yoy = 0.30  # 30% annual growth

# Network Growth
networks_year2 = int(networks_year1 * 1.8)
networks_year3 = int(networks_year1 * 2.5)

# Revenue Parameters
relay_fee_rate = 0.10  # 10%
relay_revenue_per_network = 0.6  # $M per network
insurance_premium_rate = 0.02  # 2%
insurance_protocol_take = 0.15  # 15%
credit_vault_pct_tvl = 0.20  # 20%
credit_net_margin = 0.005  # 0.5%
credit_protocol_take = 0.25  # 25%
da_revenue_year1 = 2.0  # $M
da_growth_yoy = 0.40  # 40%
derivatives_volume = 100  # $M
derivatives_fee = 0.0005  # 0.05%

# Operating Expenses ($M annual)
opex_contractors = 3.06
opex_it_audit = 1.28
opex_marketing = 0.70
opex_legal = 0.18
opex_other = 0.41
opex_annual = opex_contractors + opex_it_audit + opex_marketing + opex_legal + opex_other

print(f"📋 Model Parameters Set")
print(f"   Base TVL: ${tvl_base:.2f}B")
print(f"   Networks Y1/Y2/Y3: {networks_year1}/{networks_year2}/{networks_year3}")
print(f"   Annual OpEx: ${opex_annual:.2f}M")


# ============================================================================
# CELL 5: BUILD SCENARIO MODEL
# ============================================================================
# Copy this into a Python cell in Hex

def build_scenario(scenario_type, year):
    """Build revenue projections for a scenario"""
    
    if scenario_type == "Downside":
        tvl_mult, net_mult, fee_mult, da_growth = 0.70, 0.70, 0.90, 0.20
    elif scenario_type == "Base":
        tvl_mult, net_mult, fee_mult, da_growth = 1.0, 1.0, 1.0, da_growth_yoy
    else:  # Upside
        tvl_mult, net_mult, fee_mult, da_growth = 1.30, 1.20, 1.15, 0.50
    
    # Calculate TVL
    tvl = tvl_base * (1 + tvl_growth_yoy) ** (year - 1) * tvl_mult
    
    # Calculate Networks
    if year == 1:
        networks = networks_year1 * net_mult
    elif year == 2:
        networks = networks_year2 * net_mult
    else:
        networks = networks_year3 * net_mult
    
    # Revenue Streams
    relay = networks * relay_revenue_per_network * (1 + relay_fee_rate * fee_mult)
    insurance = tvl * 1000 * insurance_premium_rate * insurance_protocol_take
    credit = tvl * 1000 * credit_vault_pct_tvl * credit_net_margin * credit_protocol_take
    da = da_revenue_year1 * ((1 + da_growth) ** (year - 1))
    derivatives = derivatives_volume * tvl_mult * derivatives_fee
    
    total_revenue = relay + insurance + credit + da + derivatives
    opex = opex_annual * (1 + (year - 1) * 0.20)
    ebitda = total_revenue - opex
    
    return {
        'Scenario': scenario_type,
        'Year': year,
        'TVL_B': round(tvl, 2),
        'Networks': int(networks),
        'Relay': round(relay, 2),
        'Insurance': round(insurance, 2),
        'Credit': round(credit, 2),
        'DA': round(da, 2),
        'Derivatives': round(derivatives, 2),
        'Total_Revenue': round(total_revenue, 2),
        'OpEx': round(opex, 2),
        'EBITDA': round(ebitda, 2),
        'EBITDA_Margin': round(ebitda / total_revenue * 100, 1) if total_revenue > 0 else 0,
    }

# Build full model
results = []
for scenario in ['Downside', 'Base', 'Upside']:
    for year in [1, 2, 3]:
        results.append(build_scenario(scenario, year))

# Add stress test
stress = {
    'Scenario': 'Stress',
    'Year': 1,
    'TVL_B': round(tvl_base * 0.56, 2),
    'Networks': int(networks_year1 * 0.6),
    'Relay': round(networks_year1 * 0.6 * relay_revenue_per_network * 0.35, 2),
    'Insurance': round(tvl_base * 0.56 * 1000 * insurance_premium_rate * 0.25 * insurance_protocol_take, 2),
    'Credit': round(tvl_base * 0.56 * 1000 * credit_vault_pct_tvl * 0.3 * credit_net_margin * credit_protocol_take, 2),
    'DA': round(da_revenue_year1 * 0.5, 2),
    'Derivatives': round(derivatives_volume * 0.3 * derivatives_fee, 2),
}
stress['Total_Revenue'] = round(stress['Relay'] + stress['Insurance'] + stress['Credit'] + stress['DA'] + stress['Derivatives'], 2)
stress['OpEx'] = opex_annual
stress['EBITDA'] = round(stress['Total_Revenue'] - opex_annual, 2)
stress['EBITDA_Margin'] = round(stress['EBITDA'] / stress['Total_Revenue'] * 100, 1) if stress['Total_Revenue'] > 0 else 0
results.append(stress)

df_model = pd.DataFrame(results)
print("✅ Revenue model built")
df_model


# ============================================================================
# CELL 6: SUMMARY TABLE (Display in Hex)
# ============================================================================
# Copy this into a Python cell in Hex

# Create summary for Year 3 + Stress
summary_data = []
for scenario in ['Downside', 'Base', 'Upside']:
    row = df_model[(df_model['Scenario'] == scenario) & (df_model['Year'] == 3)].iloc[0]
    vs_target = (row['Total_Revenue'] / 20 - 1) * 100
    summary_data.append({
        'Scenario': scenario,
        'Year': 3,
        'TVL': f"${row['TVL_B']:.1f}B",
        'Networks': row['Networks'],
        'Revenue': f"${row['Total_Revenue']:.1f}M",
        'EBITDA': f"${row['EBITDA']:.1f}M",
        'Margin': f"{row['EBITDA_Margin']:.0f}%",
        'vs Target': f"{vs_target:+.0f}%"
    })

# Add stress
stress_row = df_model[df_model['Scenario'] == 'Stress'].iloc[0]
vs_target = (stress_row['Total_Revenue'] / 20 - 1) * 100
summary_data.append({
    'Scenario': 'Stress',
    'Year': 1,
    'TVL': f"${stress_row['TVL_B']:.1f}B",
    'Networks': stress_row['Networks'],
    'Revenue': f"${stress_row['Total_Revenue']:.1f}M",
    'EBITDA': f"${stress_row['EBITDA']:.1f}M",
    'Margin': f"{stress_row['EBITDA_Margin']:.0f}%",
    'vs Target': f"{vs_target:+.0f}%"
})

df_summary = pd.DataFrame(summary_data)
print("📊 SCENARIO SUMMARY")
df_summary


# ============================================================================
# CELL 7: CHART - REVENUE BY SCENARIO OVER TIME
# ============================================================================
# Copy this into a Python cell in Hex

df_main = df_model[df_model['Scenario'] != 'Stress']

fig_scenario = px.line(
    df_main, 
    x='Year', 
    y='Total_Revenue', 
    color='Scenario',
    markers=True,
    title='📈 Revenue Projections by Scenario',
    labels={'Total_Revenue': 'Revenue ($M)', 'Year': 'Year'},
    color_discrete_map={'Downside': '#EF4444', 'Base': '#3B82F6', 'Upside': '#10B981'}
)

fig_scenario.add_hline(y=20, line_dash="dash", line_color="red", 
                       annotation_text="$20M Target")

fig_scenario.update_layout(
    height=500,
    template='plotly_white',
    font=dict(size=14)
)

fig_scenario.show()


# ============================================================================
# CELL 8: CHART - REVENUE WATERFALL (BASE YEAR 3)
# ============================================================================
# Copy this into a Python cell in Hex

base_y3 = df_model[(df_model['Scenario'] == 'Base') & (df_model['Year'] == 3)].iloc[0]

streams = ['Relay', 'Insurance', 'Credit', 'DA', 'Derivatives']
values = [base_y3[s] for s in streams]

fig_waterfall = go.Figure(go.Waterfall(
    name="Revenue",
    orientation="v",
    measure=["relative"] * len(streams) + ["total"],
    x=['Relay Fees', 'Insurance', 'Private Credit', 'Data Availability', 'Derivatives', 'Total'],
    y=values + [base_y3['Total_Revenue']],
    text=[f"${v:.1f}M" for v in values] + [f"${base_y3['Total_Revenue']:.1f}M"],
    textposition="outside",
    connector={"line": {"color": "rgb(63, 63, 63)"}},
    increasing={"marker": {"color": "#10B981"}},
    totals={"marker": {"color": "#3B82F6"}}
))

fig_waterfall.update_layout(
    title="💰 Revenue Breakdown - Base Case Year 3",
    height=500,
    template='plotly_white',
    showlegend=False
)

fig_waterfall.show()


# ============================================================================
# CELL 9: CHART - TVL BY COLLATERAL (LIVE DATA)
# ============================================================================
# Copy this into a Python cell in Hex

if data_loaded and len(df_collateral) > 0:
    # Find TVL column
    tvl_col = None
    for col in df_collateral.columns:
        if 'tvl' in col.lower() or 'usd' in col.lower():
            tvl_col = col
            break
    
    symbol_col = None
    for col in df_collateral.columns:
        if 'symbol' in col.lower():
            symbol_col = col
            break
    
    if tvl_col and symbol_col:
        df_plot = df_collateral[[symbol_col, tvl_col]].copy()
        df_plot.columns = ['Symbol', 'TVL']
        df_plot['TVL'] = pd.to_numeric(df_plot['TVL'], errors='coerce')
        df_plot = df_plot.nlargest(10, 'TVL')
        
        fig_collateral = px.bar(
            df_plot,
            x='Symbol',
            y='TVL',
            title='🏦 TVL by Collateral Type (Top 10)',
            labels={'TVL': 'TVL (USD)', 'Symbol': 'Collateral'},
            color='TVL',
            color_continuous_scale='Greens'
        )
        
        fig_collateral.update_layout(height=500, template='plotly_white')
        fig_collateral.show()
else:
    print("⚠️ Collateral data not available")


# ============================================================================
# CELL 10: CHART - EBITDA COMPARISON
# ============================================================================
# Copy this into a Python cell in Hex

df_y3 = df_model[(df_model['Year'] == 3) & (df_model['Scenario'] != 'Stress')]

fig_ebitda = go.Figure()

fig_ebitda.add_trace(go.Bar(
    name='Revenue',
    x=df_y3['Scenario'],
    y=df_y3['Total_Revenue'],
    marker_color='#3B82F6'
))

fig_ebitda.add_trace(go.Bar(
    name='EBITDA',
    x=df_y3['Scenario'],
    y=df_y3['EBITDA'],
    marker_color='#10B981'
))

fig_ebitda.update_layout(
    title='📊 Year 3: Revenue vs EBITDA by Scenario',
    barmode='group',
    height=500,
    template='plotly_white',
    yaxis_title='$M'
)

fig_ebitda.show()


# ============================================================================
# CELL 11: CHART - STRESS TEST COMPARISON
# ============================================================================
# Copy this into a Python cell in Hex

base_y1 = df_model[(df_model['Scenario'] == 'Base') & (df_model['Year'] == 1)].iloc[0]
stress = df_model[df_model['Scenario'] == 'Stress'].iloc[0]

streams = ['Relay', 'Insurance', 'Credit', 'DA', 'Derivatives']

fig_stress = go.Figure(data=[
    go.Bar(name='Base Case Y1', x=streams, y=[base_y1[s] for s in streams], marker_color='#3B82F6'),
    go.Bar(name='Stress Test', x=streams, y=[stress[s] for s in streams], marker_color='#EF4444')
])

fig_stress.update_layout(
    title='⚠️ Stress Test vs Base Case (Year 1)',
    barmode='group',
    height=500,
    template='plotly_white',
    yaxis_title='Revenue ($M)'
)

fig_stress.show()


# ============================================================================
# CELL 12: KEY INSIGHTS
# ============================================================================
# Copy this into a Python cell in Hex

base_y3 = df_model[(df_model['Scenario'] == 'Base') & (df_model['Year'] == 3)].iloc[0]
stress = df_model[df_model['Scenario'] == 'Stress'].iloc[0]

print("""
================================================================================
🎯 KEY INSIGHTS
================================================================================
""")

print(f"✅ Base case reaches ${base_y3['Total_Revenue']:.1f}M by Year 3 (vs $20M target)")
print(f"✅ Base case EBITDA margin: {base_y3['EBITDA_Margin']:.0f}%")
print(f"✅ Relay represents {base_y3['Relay'] / base_y3['Total_Revenue'] * 100:.0f}% of Year 3 revenue")
print(f"✅ Stress test maintains ${stress['Total_Revenue']:.1f}M revenue")
print(f"✅ Current TVL (${current_tvl:.2f}B) tracking {'above' if current_tvl > tvl_base * 0.7 else 'below'} downside scenario")

print("""
================================================================================
📋 MARKET SIZING
================================================================================
""")

tam_data = pd.DataFrame({
    'Revenue Stream': ['Relay Fees', 'Insurance', 'Private Credit', 'Data Availability', 'Derivatives'],
    'TAM ($B)': [2.0, 7.4, 1700, 0.5, 62],
    'Year 1 Rev ($M)': [
        df_model[(df_model['Scenario']=='Base') & (df_model['Year']==1)].iloc[0]['Relay'],
        df_model[(df_model['Scenario']=='Base') & (df_model['Year']==1)].iloc[0]['Insurance'],
        df_model[(df_model['Scenario']=='Base') & (df_model['Year']==1)].iloc[0]['Credit'],
        df_model[(df_model['Scenario']=='Base') & (df_model['Year']==1)].iloc[0]['DA'],
        df_model[(df_model['Scenario']=='Base') & (df_model['Year']==1)].iloc[0]['Derivatives']
    ],
    'Key Driver': ['34% devs multi-chain', 'ETF/institutional', 'BTC restaking', '100+ rollups', 'LST adoption']
})

print(tam_data.to_string(index=False))

print("""
================================================================================
""")

