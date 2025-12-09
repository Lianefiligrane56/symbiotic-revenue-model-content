from IPython.display import HTML, display
import pandas as pd

# Symbiotic-styled function for displaying dataframes and SQL results
def style_dataframe(df):
    """Apply Symbiotic.fi styling to pandas dataframes (for Dune data)"""
    
    styled = df.style.set_table_styles([
        # Table container
        {'selector': 'table', 
         'props': [
             ('font-family', 'Inter, -apple-system, sans-serif'),
             ('border-collapse', 'collapse'),
             ('width', '100%'),
             ('margin', '20px 0'),
             ('background', '#ffffff'),
             ('border-radius', '8px'),
             ('overflow', 'hidden')
         ]},
        
        # Headers - Symbiotic black with white text
        {'selector': 'th', 
         'props': [
             ('background-color', '#0a0a0a !important'),
             ('color', '#ffffff !important'),
             ('font-weight', '600'),
             ('padding', '14px 16px'),
             ('text-align', 'left'),
             ('font-size', '0.95em'),
             ('border', 'none')
         ]},
        
        # Cells
        {'selector': 'td', 
         'props': [
             ('padding', '12px 16px'),
             ('border-bottom', '1px solid #e0e0e0'),
             ('color', '#3a3a3a'),
             ('font-size', '0.9em')
         ]},
        
        # Alternating rows
        {'selector': 'tbody tr:nth-child(even)', 
         'props': [
             ('background-color', '#f8f8f8')
         ]},
        
        # Hover effect
        {'selector': 'tbody tr:hover', 
         'props': [
             ('background-color', '#f0f0f0'),
             ('transition', 'background-color 0.2s')
         ]}
    ])
    
    return styled


# Function to display styled markdown + data together
def display_section(md_file, df=None, title=None):
    """Display markdown content with optional styled dataframe"""
    
    import markdown
    
    # Read and convert markdown
    with open(md_file, 'r') as f:
        md_content = f.read()
    html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
    
    # Symbiotic CSS
    css = """<style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        .symbiotic-section { 
            font-family: 'Inter', sans-serif !important; 
            max-width: 1200px; 
            margin: 20px auto; 
            padding: 40px !important; 
            background: #f5f5f5 !important;
            border-radius: 8px;
        }
        .symbiotic-section h1 { color: #0a0a0a !important; font-size: 3em; font-weight: 700; margin-bottom: 30px; }
        .symbiotic-section h2 { color: #0a0a0a !important; font-size: 2em; font-weight: 600; margin-top: 40px; margin-bottom: 20px; }
        .symbiotic-section h3 { color: #1a1a1a !important; font-size: 1.5em; font-weight: 600; margin-top: 30px; }
        .symbiotic-section p { color: #3a3a3a !important; line-height: 1.8; margin: 16px 0; }
        .symbiotic-section a { color: #00ff88 !important; text-decoration: none; font-weight: 500; }
        .symbiotic-section a:hover { opacity: 0.7; }
        .symbiotic-section ul, .symbiotic-section ol { color: #3a3a3a !important; margin: 16px 0; }
        .symbiotic-section li { color: #3a3a3a !important; margin: 8px 0; line-height: 1.6; }
        .symbiotic-section code { background: #0a0a0a !important; color: #00ff88 !important; padding: 4px 8px; border-radius: 4px; font-size: 0.9em; }
        .symbiotic-section pre { background: #0a0a0a !important; color: #e0e0e0 !important; padding: 20px; border-radius: 8px; margin: 20px 0; overflow-x: auto; }
        .symbiotic-section pre code { background: none !important; padding: 0; }
        .symbiotic-section table { background: #ffffff !important; border-radius: 8px; overflow: hidden; }
        .symbiotic-section blockquote { border-left: 3px solid #00ff88; padding: 16px 24px; background: #ffffff; margin: 20px 0; }
        .data-title { color: #0a0a0a !important; font-size: 1.5em; font-weight: 600; margin: 30px 0 16px 0; }
    </style>"""
    
    # Display markdown
    display(HTML(f"{css}<div class='symbiotic-section'>{html_content}</div>"))
    
    # Display dataframe if provided
    if df is not None:
        if title:
            display(HTML(f"<div class='symbiotic-section'><h3 class='data-title'>{title}</h3></div>"))
        display(style_dataframe(df))


# Usage examples:

# 1. Display markdown only
# display_section('Introduction.md')

# 2. Display markdown with Dune data
# df = pd.read_csv('tvl_over_time.csv')
# display_section('Introduction.md', df=df, title='TVL Over Time')

# 3. Just style a dataframe
# df = pd.read_csv('rewards_by_network.csv')
# display(style_dataframe(df))
