"""
Symbiotic Complete Brand Styling for Hex
=========================================
Official Symbiotic.fi brand styling matching:
- symbiotic.fi (main site)
- app.symbiotic.fi (application)
- docs.symbiotic.fi (documentation)
- blog.symbiotic.fi (blog)
"""

from IPython.display import HTML, display
import pandas as pd

# ═══════════════════════════════════════════════════════════════
# BRAND COLORS
# ═══════════════════════════════════════════════════════════════
COLORS = {
    'bg_dark': '#0a0a0a',
    'bg_card': '#1a1a1a',
    'bg_hover': '#151515',
    'border': '#2a2a2a',
    'accent': '#00ff88',
    'accent_dark': '#059669',
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0b0',
    'text_muted': '#707070',
}

# ═══════════════════════════════════════════════════════════════
# DISPLAY MARKDOWN
# ═══════════════════════════════════════════════════════════════
def display_markdown(file_path_or_text, from_github=True):
    """
    Display markdown with Symbiotic dark theme styling.
    
    Args:
        file_path_or_text: Path to .md file (from GitHub) or raw markdown text
        from_github: If True, fetches from GitHub repo. If False, treats input as raw text.
    """
    import markdown
    
    if from_github:
        import requests
        base_url = "https://raw.githubusercontent.com/Lianefiligrane56/symbiotic-revenue-model-content/main/"
        url = base_url + file_path_or_text
        content = requests.get(url).text
    else:
        content = file_path_or_text
    
    html_content = markdown.markdown(content, extensions=['tables', 'fenced_code', 'nl2br'])
    
    styled = f'''
    <div class="symbiotic-md">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            .symbiotic-md {{
                font-family: 'Inter', -apple-system, sans-serif;
                background: {COLORS['bg_dark']};
                color: {COLORS['text_primary']};
                padding: 32px 40px;
                border-radius: 12px;
                max-width: 950px;
                line-height: 1.7;
            }}
            
            .symbiotic-md h1 {{
                font-size: 2.5em;
                font-weight: 800;
                background: linear-gradient(135deg, {COLORS['text_primary']} 0%, {COLORS['accent']} 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 32px 0 24px 0;
                letter-spacing: -0.02em;
            }}
            
            .symbiotic-md h2 {{
                font-size: 1.8em;
                font-weight: 700;
                color: {COLORS['text_primary']};
                margin: 28px 0 16px 0;
                padding-bottom: 8px;
                border-bottom: 1px solid {COLORS['border']};
            }}
            
            .symbiotic-md h3 {{
                font-size: 1.4em;
                font-weight: 600;
                color: {COLORS['text_primary']};
                margin: 24px 0 12px 0;
                padding-left: 12px;
                border-left: 3px solid {COLORS['accent']};
            }}
            
            .symbiotic-md p {{
                color: {COLORS['text_secondary']};
                margin: 16px 0;
                font-size: 1.05em;
            }}
            
            .symbiotic-md a {{
                color: {COLORS['accent']};
                text-decoration: none;
                font-weight: 500;
                transition: opacity 0.2s;
            }}
            
            .symbiotic-md a:hover {{
                opacity: 0.7;
            }}
            
            .symbiotic-md ul, .symbiotic-md ol {{
                color: {COLORS['text_secondary']};
                margin: 16px 0;
                padding-left: 24px;
            }}
            
            .symbiotic-md li {{
                margin: 8px 0;
                padding-left: 8px;
            }}
            
            .symbiotic-md li::marker {{
                color: {COLORS['accent']};
            }}
            
            .symbiotic-md code {{
                background: {COLORS['bg_card']};
                color: {COLORS['accent']};
                padding: 3px 8px;
                border-radius: 4px;
                font-family: 'SF Mono', Monaco, monospace;
                font-size: 0.9em;
            }}
            
            .symbiotic-md pre {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 20px;
                overflow-x: auto;
                margin: 20px 0;
            }}
            
            .symbiotic-md pre code {{
                background: none;
                padding: 0;
                color: {COLORS['text_secondary']};
            }}
            
            .symbiotic-md table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: {COLORS['bg_card']};
                border-radius: 8px;
                overflow: hidden;
            }}
            
            .symbiotic-md th {{
                background: linear-gradient(135deg, {COLORS['bg_dark']} 0%, #151515 100%);
                color: {COLORS['text_primary']};
                padding: 14px 16px;
                text-align: left;
                font-weight: 600;
                font-size: 0.95em;
                border-bottom: 1px solid {COLORS['accent']};
            }}
            
            .symbiotic-md td {{
                padding: 12px 16px;
                color: {COLORS['text_secondary']};
                border-bottom: 1px solid {COLORS['border']};
            }}
            
            .symbiotic-md tr:hover td {{
                background: {COLORS['bg_hover']};
            }}
            
            .symbiotic-md blockquote {{
                background: {COLORS['bg_card']};
                border-left: 4px solid {COLORS['accent']};
                padding: 16px 24px;
                margin: 20px 0;
                border-radius: 0 8px 8px 0;
            }}
            
            .symbiotic-md blockquote p {{
                margin: 0;
                color: {COLORS['text_secondary']};
                font-style: italic;
            }}
            
            .symbiotic-md hr {{
                border: none;
                height: 1px;
                background: linear-gradient(90deg, transparent, {COLORS['accent']}, transparent);
                margin: 32px 0;
            }}
            
            .symbiotic-md em {{
                color: {COLORS['accent']};
                font-style: italic;
            }}
            
            .symbiotic-md strong {{
                color: {COLORS['text_primary']};
                font-weight: 600;
            }}
        </style>
        {html_content}
    </div>
    '''
    display(HTML(styled))


# ═══════════════════════════════════════════════════════════════
# STYLE DATAFRAME
# ═══════════════════════════════════════════════════════════════
def style_dataframe(df, dark_mode=True):
    """
    Style pandas DataFrame with Symbiotic app-style design.
    
    Args:
        df: pandas DataFrame
        dark_mode: Use dark theme (default True)
    """
    if dark_mode:
        return df.style.set_table_styles([
            {'selector': '', 'props': [('font-family', 'Inter, -apple-system, sans-serif')]},
            {'selector': 'table', 'props': [
                ('border-collapse', 'collapse'),
                ('width', '100%'),
                ('background', COLORS['bg_card']),
                ('border-radius', '8px'),
                ('overflow', 'hidden'),
                ('margin', '16px 0')
            ]},
            {'selector': 'th', 'props': [
                ('background', f'linear-gradient(135deg, {COLORS["bg_dark"]} 0%, #151515 100%)'),
                ('color', COLORS['text_primary']),
                ('padding', '14px 16px'),
                ('text-align', 'left'),
                ('font-weight', '600'),
                ('font-size', '0.95em'),
                ('border-bottom', f'1px solid {COLORS["accent"]}')
            ]},
            {'selector': 'td', 'props': [
                ('padding', '12px 16px'),
                ('color', COLORS['text_secondary']),
                ('border-bottom', f'1px solid {COLORS["border"]}'),
                ('font-size', '0.95em')
            ]},
            {'selector': 'tr:hover td', 'props': [
                ('background', COLORS['bg_hover'])
            ]}
        ])
    else:
        # Light mode
        return df.style.set_table_styles([
            {'selector': '', 'props': [('font-family', 'Inter, -apple-system, sans-serif')]},
            {'selector': 'table', 'props': [
                ('border-collapse', 'collapse'),
                ('width', '100%'),
                ('background', '#ffffff'),
                ('border-radius', '8px'),
                ('overflow', 'hidden'),
                ('margin', '16px 0')
            ]},
            {'selector': 'th', 'props': [
                ('background', COLORS['bg_dark']),
                ('color', '#ffffff'),
                ('padding', '14px 16px'),
                ('text-align', 'left'),
                ('font-weight', '600')
            ]},
            {'selector': 'td', 'props': [
                ('padding', '12px 16px'),
                ('color', '#3a3a3a'),
                ('border-bottom', '1px solid #e0e0e0')
            ]},
            {'selector': 'tr:nth-child(even)', 'props': [
                ('background', '#f8f8f8')
            ]},
            {'selector': 'tr:hover td', 'props': [
                ('background', '#f0f0f0')
            ]}
        ])


# ═══════════════════════════════════════════════════════════════
# DISPLAY SECTION (Markdown + Data)
# ═══════════════════════════════════════════════════════════════
def display_section(md_file, df=None, title=None, dark_mode=True):
    """
    Display markdown content with optional styled dataframe.
    
    Args:
        md_file: Path to markdown file in GitHub repo
        df: Optional pandas DataFrame to display after markdown
        title: Optional title for the data section
        dark_mode: Use dark theme (default True)
    """
    display_markdown(md_file)
    
    if df is not None:
        if title:
            title_color = COLORS['text_primary'] if dark_mode else '#0a0a0a'
            display(HTML(f'''
                <h3 style="font-family: Inter, sans-serif; color: {title_color}; 
                    font-size: 1.3em; font-weight: 600; margin: 24px 0 12px 0;
                    padding-left: 12px; border-left: 3px solid {COLORS['accent']};">
                    {title}
                </h3>
            '''))
        display(style_dataframe(df, dark_mode=dark_mode))


# ═══════════════════════════════════════════════════════════════
# METRIC CARD
# ═══════════════════════════════════════════════════════════════
def display_metric_card(title, value, subtitle=None):
    """
    Display a metric card matching app.symbiotic.fi interface.
    
    Args:
        title: Metric title (e.g., "Total TVL")
        value: Metric value (e.g., "$2.5B")
        subtitle: Optional subtitle/description
    """
    subtitle_html = f'<div class="metric-subtitle">{subtitle}</div>' if subtitle else ''
    
    card = f'''
    <div class="symbiotic-metric-card">
        <style>
            .symbiotic-metric-card {{
                font-family: 'Inter', -apple-system, sans-serif;
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                padding: 24px 28px;
                display: inline-block;
                min-width: 200px;
                margin: 8px 12px 8px 0;
                transition: all 0.2s ease;
            }}
            .symbiotic-metric-card:hover {{
                border-color: {COLORS['accent']};
                box-shadow: 0 0 20px rgba(0, 255, 136, 0.1);
            }}
            .metric-title {{
                color: {COLORS['text_muted']};
                font-size: 0.85em;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 8px;
            }}
            .metric-value {{
                color: {COLORS['text_primary']};
                font-size: 2em;
                font-weight: 700;
                letter-spacing: -0.02em;
            }}
            .metric-subtitle {{
                color: {COLORS['text_secondary']};
                font-size: 0.9em;
                margin-top: 8px;
            }}
        </style>
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {subtitle_html}
    </div>
    '''
    display(HTML(card))


# ═══════════════════════════════════════════════════════════════
# METRIC ROW (Multiple cards)
# ═══════════════════════════════════════════════════════════════
def display_metrics_row(metrics):
    """
    Display multiple metric cards in a row.
    
    Args:
        metrics: List of tuples [(title, value, subtitle), ...]
    """
    cards_html = ''
    for metric in metrics:
        title = metric[0]
        value = metric[1]
        subtitle = metric[2] if len(metric) > 2 else None
        subtitle_html = f'<div class="metric-subtitle">{subtitle}</div>' if subtitle else ''
        
        cards_html += f'''
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            {subtitle_html}
        </div>
        '''
    
    row = f'''
    <div class="symbiotic-metrics-row">
        <style>
            .symbiotic-metrics-row {{
                display: flex;
                flex-wrap: wrap;
                gap: 16px;
                margin: 20px 0;
            }}
            .symbiotic-metrics-row .metric-card {{
                font-family: 'Inter', -apple-system, sans-serif;
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                padding: 24px 28px;
                flex: 1;
                min-width: 180px;
                transition: all 0.2s ease;
            }}
            .symbiotic-metrics-row .metric-card:hover {{
                border-color: {COLORS['accent']};
                box-shadow: 0 0 20px rgba(0, 255, 136, 0.1);
            }}
            .symbiotic-metrics-row .metric-title {{
                color: {COLORS['text_muted']};
                font-size: 0.85em;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 8px;
            }}
            .symbiotic-metrics-row .metric-value {{
                color: {COLORS['text_primary']};
                font-size: 1.8em;
                font-weight: 700;
                letter-spacing: -0.02em;
            }}
            .symbiotic-metrics-row .metric-subtitle {{
                color: {COLORS['text_secondary']};
                font-size: 0.85em;
                margin-top: 8px;
            }}
        </style>
        {cards_html}
    </div>
    '''
    display(HTML(row))


# ═══════════════════════════════════════════════════════════════
# DIVIDER
# ═══════════════════════════════════════════════════════════════
def add_divider():
    """Add a gradient section divider."""
    display(HTML(f'''
        <div style="
            height: 2px;
            background: linear-gradient(90deg, transparent, {COLORS['accent']}, transparent);
            margin: 32px 0;
            max-width: 950px;
        "></div>
    '''))


# ═══════════════════════════════════════════════════════════════
# SECTION HEADER
# ═══════════════════════════════════════════════════════════════
def display_header(text, level=1):
    """
    Display a styled section header.
    
    Args:
        text: Header text
        level: 1, 2, or 3 for different sizes
    """
    if level == 1:
        header = f'''
        <h1 style="
            font-family: 'Inter', sans-serif;
            font-size: 2.5em;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, {COLORS['accent']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 32px 0 24px 0;
            letter-spacing: -0.02em;
        ">{text}</h1>
        '''
    elif level == 2:
        header = f'''
        <h2 style="
            font-family: 'Inter', sans-serif;
            font-size: 1.8em;
            font-weight: 700;
            color: {COLORS['text_primary']};
            margin: 28px 0 16px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid {COLORS['border']};
        ">{text}</h2>
        '''
    else:
        header = f'''
        <h3 style="
            font-family: 'Inter', sans-serif;
            font-size: 1.4em;
            font-weight: 600;
            color: {COLORS['text_primary']};
            margin: 24px 0 12px 0;
            padding-left: 12px;
            border-left: 3px solid {COLORS['accent']};
        ">{text}</h3>
        '''
    display(HTML(header))


# ═══════════════════════════════════════════════════════════════
# INFO/ALERT BOX
# ═══════════════════════════════════════════════════════════════
def display_info(text, type="info"):
    """
    Display an info/alert box.
    
    Args:
        text: Message text
        type: "info", "success", "warning"
    """
    colors = {
        'info': (COLORS['accent'], 'rgba(0, 255, 136, 0.1)'),
        'success': ('#10b981', 'rgba(16, 185, 129, 0.1)'),
        'warning': ('#f59e0b', 'rgba(245, 158, 11, 0.1)')
    }
    accent, bg = colors.get(type, colors['info'])
    
    display(HTML(f'''
        <div style="
            font-family: 'Inter', sans-serif;
            background: {bg};
            border-left: 4px solid {accent};
            padding: 16px 20px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
            max-width: 900px;
        ">
            <p style="margin: 0; color: {COLORS['text_secondary']}; font-size: 0.95em;">
                {text}
            </p>
        </div>
    '''))


# ═══════════════════════════════════════════════════════════════
# PRINT READY MESSAGE
# ═══════════════════════════════════════════════════════════════
print("✅ Symbiotic Complete Styling loaded!")
print("   → display_markdown('content/Introduction.md')")
print("   → style_dataframe(df)")
print("   → display_metric_card('TVL', '$2.5B')")
print("   → display_metrics_row([('TVL', '$2.5B'), ('APR', '12%')])")
print("   → add_divider()")
print("   → display_header('Title', level=1)")
print("   → display_info('Message', type='info')")

