# Symbiotic Revenue Model - Hex Dashboard

Symbiotic.fi branded content and styling for Hex dashboards.

## 📁 Structure

```
├── content/           # Markdown files for Hex display
│   └── Introduction.md
├── styling/           # Python styling modules
│   ├── symbiotic_styling.py
│   ├── symbiotic_sql_data_styling.py
│   └── symbiotic_hex_dashboard.py
├── data/              # CSV data exports from Dune
│   ├── tvl_over_time.csv
│   ├── rewards_by_network.csv
│   └── ...
└── requirements.txt
```

## 🚀 Usage in Hex

### 1. Connect this repo to your Hex project
- Go to Hex project settings → Git sync
- Connect to this GitHub repository

### 2. Import styling in Cell 1
```python
from styling.symbiotic_styling import display_markdown, style_dataframe, display_section
```

### 3. Display content
```python
# Display markdown with Symbiotic branding
display_markdown('content/Introduction.md')

# Style a dataframe
import pandas as pd
df = pd.read_csv('data/tvl_over_time.csv')
display(style_dataframe(df))

# Combined: markdown + data
display_section('content/Introduction.md', df=df, title='TVL Over Time')
```

## 🎨 Brand Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Black | `#0a0a0a` | Primary text, headers |
| Green | `#00ff88` | Accent, links, highlights |
| Gray | `#3a3a3a` | Secondary text |
| Light | `#f5f5f5` | Backgrounds |

## 📊 Data Files

| File | Description |
|------|-------------|
| `tvl_over_time.csv` | Historical TVL data |
| `tvl_by_vault.csv` | TVL breakdown by vault |
| `rewards_by_network.csv` | Network reward distributions |
| `rewards_total.csv` | Total rewards over time |
| `operator_registrations.csv` | Operator registration data |

## 📦 Dependencies

```
pandas>=1.3.0
markdown>=3.3.0
IPython>=7.0.0
```

---

Built for [Hex.tech](https://hex.tech) | Styled for [Symbiotic.fi](https://symbiotic.fi)

