# Symbiotic Complete Brand Styling for Hex

Official Symbiotic.fi brand styling for Hex projects, unified across all Symbiotic web properties:
- 🌐 [symbiotic.fi](https://symbiotic.fi) - Main website
- 📱 [app.symbiotic.fi](https://app.symbiotic.fi) - Application interface  
- 📚 [docs.symbiotic.fi](https://docs.symbiotic.fi) - Documentation
- ✍️ [blog.symbiotic.fi](https://blog.symbiotic.fi) - Blog

## Features

- 🎨 **Dark Theme**: True to Symbiotic's brand (#0a0a0a background)
- 💚 **Symbiotic Green**: Signature #00ff88 accent color
- 🔤 **Inter Font**: Professional typography
- 📊 **App-Style Tables**: Matches app.symbiotic.fi interface
- ✨ **Gradient Headings**: Modern gradient effects
- 📱 **Fully Responsive**: Works on all devices

## Installation

### In Hex Projects

1. Upload `symbiotic_complete_styling.py` to your Hex project
2. In Cell 1:

```python
from symbiotic_complete_styling import (
    display_markdown, 
    style_dataframe, 
    display_section,
    add_divider,
    display_metric_card
)
```

## Usage

### Display Markdown

```python
# Dark theme markdown (default)
display_markdown('Introduction.md')
```

### Style DataFrames

```python
import pandas as pd

# Dark theme table (matches app.symbiotic.fi)
df = pd.read_csv('tvl_data.csv')
display(style_dataframe(df))

# Light theme option
display(style_dataframe(df, dark_mode=False))
```

### Combined Markdown + Data

```python
df = pd.read_csv('rewards.csv')
display_section('Analysis.md', df=df, title='Rewards by Network')
```

### Add Visual Elements

```python
# Section divider with gradient
add_divider()

# Metric cards (like app.symbiotic.fi)
display_metric_card("Total TVL", "$2.5B", "Across all vaults")
display_metric_card("APR", "12.5%", "Average yield")
```

## Complete Example

```python
# Cell 1: Import
from symbiotic_complete_styling import *
import pandas as pd

# Cell 2: Introduction
display_markdown('Introduction.md')
add_divider()

# Cell 3: Key metrics
display_metric_card("Total Value Locked", "$2.5B", "Across 50+ networks")
display_metric_card("Total Rewards", "$125M", "Distributed to stakers")

# Cell 4: Data analysis
tvl_df = pd.read_csv('tvl_over_time.csv')
display_section('TVL_Analysis.md', df=tvl_df, title='TVL Over Time')

add_divider()

# Cell 5: More data
rewards_df = pd.read_csv('rewards_by_network.csv')
display(style_dataframe(rewards_df))
```

## Brand Colors

### Primary Colors
- **Background**: `#0a0a0a` (Black)
- **Accent**: `#00ff88` (Symbiotic Green)
- **Text Primary**: `#ffffff` (White)
- **Text Secondary**: `#b0b0b0` (Light Gray)

### UI Elements
- **Cards**: `#1a1a1a`
- **Borders**: `#2a2a2a`
- **Hover**: `#151515`

## Typography

- **Font Family**: Inter (weights: 300-800)
- **H1**: 3.5em, 800 weight, gradient effect
- **H2**: 2.5em, 700 weight
- **H3**: 1.75em, 600 weight, green accent border
- **Body**: 1.05em, 400 weight

## Supported Markdown Features

✅ All standard markdown:
- Headings (H1-H6) with gradient effects
- Bold, italic, emphasis
- Links with green accent
- Lists with green markers
- Code blocks (dark theme with green highlights)
- Tables (app-style with gradients)
- Blockquotes (dark cards)
- Images with rounded corners
- Horizontal rules

## API Reference

### `display_markdown(file_path)`
Display markdown file with Symbiotic dark theme styling.

### `style_dataframe(df, dark_mode=True)`
Style pandas DataFrame with app.symbiotic.fi table design.

### `display_section(md_file, df=None, title=None, dark_mode=True)`
Display markdown with optional styled data table.

### `add_divider()`
Add a green gradient section divider.

### `display_metric_card(title, value, subtitle=None)`
Display a metric card matching app.symbiotic.fi interface.

## File Structure

```
symbiotic-revenue-model-content/
├── symbiotic_complete_styling.py  # Complete styling module
├── Introduction.md                 # Your content
├── *.csv                          # Your data
└── README.md                      # This file
```

## Examples from Symbiotic Properties

This styling is based on:
- **Main site gradient headings** from symbiotic.fi
- **Dark app interface** from app.symbiotic.fi
- **Documentation clarity** from docs.symbiotic.fi  
- **Blog readability** from blog.symbiotic.fi

## Dependencies

```python
markdown>=3.3.0
pandas>=1.3.0
IPython>=7.0.0
```

## Comparison: Old vs New

### Old Styling (Light)
- Light gray background (#f5f5f5)
- Basic headings
- Simple tables

### New Styling (Complete Brand)
- True Symbiotic dark theme (#0a0a0a)
- Gradient headings with brand colors
- App-style tables with hover effects
- Green accent throughout (#00ff88)
- Metric cards like the app
- Section dividers

## License

MIT License

## Links

- [Symbiotic Main Site](https://symbiotic.fi)
- [Symbiotic App](https://app.symbiotic.fi)
- [Symbiotic Docs](https://docs.symbiotic.fi)
- [Symbiotic Blog](https://blog.symbiotic.fi)
- [Brand Kit](https://symbioticfi.notion.site/Symbiotic-Brand-Kit-3934802041114e82a18e8265435b1b8b)

---

🟢 Built for Hex.tech | Styled for Symbiotic.fi
