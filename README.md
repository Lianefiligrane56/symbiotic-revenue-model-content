# Symbiotic Revenue Model - Hex Dashboard

Complete Symbiotic.fi branded dashboard for Hex with data fetching, styling, and P&L calculations.

## 📁 Structure

```
symbiotic-revenue-model-content/
├── content/              # Markdown content for display
│   └── Introduction.md
├── styling/              # Hex display styling
│   ├── symbiotic_styling.py
│   └── symbiotic_complete_styling.py
├── scripts/              # Data fetching & calculations
│   ├── fetch_dune_data.py
│   └── protocol_pl.py
├── data/                 # CSV exports from Dune
│   ├── rewards_total.csv
│   ├── tvl_over_time.csv
│   └── ...
└── README.md
```

## 🚀 Quick Start in Hex

### Option 1: Paste Styling Directly (Recommended)

```python
# Cell 1: Styling
from IPython.display import HTML, display
import pandas as pd
import requests
import markdown

def display_markdown(path):
    url = "https://raw.githubusercontent.com/Lianefiligrane56/symbiotic-revenue-model-content/main/" + path
    htm = markdown.markdown(requests.get(url).text, extensions=['tables'])
    css = "<style>.s{font-family:Inter;background:#0a0a0a;color:#fff;padding:32px;border-radius:12px}.s h1{color:#00ff88}.s p{color:#b0b0b0}.s a{color:#059669}.s table{background:#1a1a1a;width:100%}.s th{background:#0a0a0a;color:#fff;padding:12px;border-bottom:1px solid #00ff88}.s td{padding:12px;color:#b0b0b0;border-bottom:1px solid #2a2a2a}</style>"
    display(HTML(css + "<div class='s'>" + htm + "</div>"))

def style_df(df):
    return df.style.set_table_styles([
        {'selector':'th','props':[('background','#0a0a0a'),('color','#fff'),('padding','12px')]},
        {'selector':'td','props':[('padding','12px'),('color','#b0b0b0'),('background','#1a1a1a')]}
    ])

def display_metric_card(title, value):
    h = "<div style='font-family:Inter;background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:24px;display:inline-block;margin:8px'>"
    h += "<div style='color:#707070;font-size:0.85em'>" + str(title) + "</div>"
    h += "<div style='color:#fff;font-size:2em'>" + str(value) + "</div></div>"
    display(HTML(h))

print("Done!")
```

### Option 2: Load Data from GitHub

```python
# Cell 2: Load Data
import pandas as pd

BASE = "https://raw.githubusercontent.com/Lianefiligrane56/symbiotic-revenue-model-content/main/data/"

df_rewards = pd.read_csv(BASE + "rewards_total.csv")
df_tvl = pd.read_csv(BASE + "tvl_over_time.csv")
df_networks = pd.read_csv(BASE + "rewards_by_network.csv")

print(f"✅ Loaded {len(df_rewards)} reward rows")
```

### Option 3: Display Content

```python
# Cell 3: Show Introduction
display_markdown('content/Introduction.md')
```

## 📊 P&L Calculation

```python
# Calculate Protocol P&L
gross_rewards = df_rewards['amount'].sum()  # Adjust column name
protocol_fee = 0.10  # 10% protocol take
protocol_revenue = gross_rewards * protocol_fee

monthly_opex = 474000  # From GPRP financials
months = 6
total_opex = monthly_opex * months

net_income = protocol_revenue - total_opex
net_margin = (net_income / protocol_revenue * 100)

# Display
display_metric_card("Gross Rewards", f"${gross_rewards/1e6:.2f}M")
display_metric_card("Protocol Revenue", f"${protocol_revenue/1e6:.2f}M")
display_metric_card("Net Income", f"${net_income/1e6:.2f}M")
display_metric_card("Net Margin", f"{net_margin:.1f}%")
```

## 🎨 Brand Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Background | `#0a0a0a` | Dark theme base |
| Cards | `#1a1a1a` | Card backgrounds |
| Accent | `#00ff88` | Symbiotic green |
| Text Primary | `#ffffff` | Headers |
| Text Secondary | `#b0b0b0` | Body text |
| Links | `#059669` | Clickable links |

## 📁 Data Files

| File | Description |
|------|-------------|
| `rewards_total.csv` | Total rewards over time |
| `rewards_by_network.csv` | Rewards breakdown by network |
| `tvl_over_time.csv` | Historical TVL data |
| `tvl_by_vault.csv` | TVL by vault type |
| `operator_count.csv` | Operator metrics |
| `operator_registrations.csv` | Registration history |

## 🔗 Links

- [Symbiotic.fi](https://symbiotic.fi)
- [Symbiotic App](https://app.symbiotic.fi)
- [Dune Dashboard](https://dune.com/symbiotic/symbiotic-rewards)

---

Built for [Hex.tech](https://hex.tech) | Styled for [Symbiotic.fi](https://symbiotic.fi)
