"""
Example usage of Symbiotic styling in Hex
Copy these examples into your Hex cells
"""

# ============================================
# CELL 1: Import the styling functions
# ============================================
from symbiotic_styling import display_markdown, style_dataframe, display_section
import pandas as pd


# ============================================
# CELL 2: Display markdown introduction
# ============================================
display_markdown('Introduction.md')


# ============================================
# CELL 3: Load and display TVL data
# ============================================
tvl_df = pd.read_csv('tvl_over_time.csv')
display_section('Analysis.md', df=tvl_df, title='Total Value Locked Over Time')


# ============================================
# CELL 4: Display multiple datasets
# ============================================
# Rewards data
rewards_df = pd.read_csv('rewards_by_network.csv')
display(HTML("<h2 style='color: #0a0a0a; font-family: Inter; margin: 40px 0 20px;'>Rewards by Network</h2>"))
display(style_dataframe(rewards_df))

# Operator data
operators_df = pd.read_csv('operator_count.csv')
display(HTML("<h2 style='color: #0a0a0a; font-family: Inter; margin: 40px 0 20px;'>Operator Count</h2>"))
display(style_dataframe(operators_df))


# ============================================
# CELL 5: Custom styling for specific data
# ============================================
# Format numbers in dataframe
df = pd.read_csv('tvl_by_vault.csv')
df['TVL'] = df['TVL'].map('${:,.2f}'.format)
display(style_dataframe(df))


# ============================================
# CELL 6: Combined report
# ============================================
# Create a complete report with markdown + multiple data sections
display_markdown('Executive_Summary.md')

display(HTML("<div style='font-family: Inter; margin: 40px 0;'><h2 style='color: #0a0a0a;'>Key Metrics</h2></div>"))

# TVL
tvl = pd.read_csv('tvl_all_vaults.csv')
display(style_dataframe(tvl))

# Rewards
rewards = pd.read_csv('total_rewards.csv')
display(style_dataframe(rewards))

display_markdown('Conclusions.md')
