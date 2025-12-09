"""
================================================================================
SYMBIOTIC CASE STUDY - HEX DASHBOARD (GitHub Synced)
================================================================================
This dashboard automatically syncs content from your GitHub repos:
- Case-Study: Dune queries, Python code, data analysis
- symbiotic-revenue-model-content: Introduction & documentation

Copy each CELL into Hex.tech as separate Python cells.
================================================================================
"""

# ============================================================================
# CELL 1: GITHUB SYNC SETUP
# ============================================================================
# Copy this into a Python cell in Hex

import requests
import base64
import json
import time
import pandas as pd
from IPython.display import Markdown, display, HTML

# Your GitHub repos
CASE_STUDY_REPO = "Lianefiligrane56/Case-Study"
CONTENT_REPO = "Lianefiligrane56/symbiotic-revenue-model-content"
GITHUB_API = "https://api.github.com"

def fetch_github_file(repo, path, decode=True):
    """Fetch a file from GitHub (works with public repos)"""
    url = f"{GITHUB_API}/repos/{repo}/contents/{path}"
    response = requests.get(url, params={"t": int(time.time())})  # Cache bust
    
    if response.status_code == 200:
        data = response.json()
        if decode:
            content = base64.b64decode(data['content']).decode('utf-8')
            return content
        return data
    else:
        print(f"⚠️ Could not fetch {path}: {response.status_code}")
        return None

def fetch_github_raw(repo, path):
    """Fetch raw file content (faster, no base64 decode needed)"""
    url = f"https://raw.githubusercontent.com/{repo}/main/{path}?t={int(time.time())}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def list_github_dir(repo, path=""):
    """List files in a GitHub directory"""
    url = f"{GITHUB_API}/repos/{repo}/contents/{path}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

print("✅ GitHub sync functions loaded")
print(f"📦 Case Study Repo: {CASE_STUDY_REPO}")
print(f"📄 Content Repo: {CONTENT_REPO}")


# ============================================================================
# CELL 2: LOAD INTRODUCTION FROM GITHUB
# ============================================================================
# Copy this into a Python cell in Hex

# Fetch Introduction.md from your content repo
intro_content = fetch_github_raw(CONTENT_REPO, "Introduction.md")

if intro_content:
    # Apply Symbiotic styling
    styled_intro = f"""
    <style>
        .intro-section {{
            font-family: 'Inter', -apple-system, sans-serif;
            max-width: 900px;
            padding: 30px;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            border-radius: 12px;
            color: #e0e0e0;
            margin: 20px 0;
        }}
        .intro-section h1 {{ color: #00ff88; font-size: 2em; margin-bottom: 20px; }}
        .intro-section h2 {{ color: #00ff88; font-size: 1.5em; margin-top: 30px; }}
        .intro-section a {{ color: #00ff88; text-decoration: none; }}
        .intro-section a:hover {{ opacity: 0.8; }}
        .intro-section table {{ 
            width: 100%; 
            border-collapse: collapse; 
            margin: 20px 0;
            background: #1a1a2e;
        }}
        .intro-section th {{ 
            background: #00ff88; 
            color: #0a0a0a; 
            padding: 12px; 
            text-align: left;
            font-weight: 600;
        }}
        .intro-section td {{ 
            padding: 12px; 
            border-bottom: 1px solid #333;
            color: #e0e0e0;
        }}
        .intro-section ul {{ padding-left: 20px; }}
        .intro-section li {{ margin: 8px 0; }}
    </style>
    <div class="intro-section">
    """
    
    import markdown
    html_content = markdown.markdown(intro_content, extensions=['tables', 'extra'])
    display(HTML(styled_intro + html_content + "</div>"))
    print("✅ Introduction loaded from GitHub")
else:
    print("⚠️ Could not load Introduction.md")


# ============================================================================
# CELL 3: LOAD SQL QUERIES FROM GITHUB
# ============================================================================
# Copy this into a Python cell in Hex

# Fetch SQL queries from Case-Study repo
sql_queries = {}

# List of SQL files to fetch
sql_files = [
    "dune_queries/symbiotic_vault_onchain.sql",
    "dune_queries/symbiotic_vault_simulation.sql"
]

print("📥 Loading SQL queries from GitHub...")
for sql_file in sql_files:
    content = fetch_github_raw(CASE_STUDY_REPO, sql_file)
    if content:
        name = sql_file.split("/")[-1].replace(".sql", "")
        sql_queries[name] = content
        print(f"   ✅ {name}")

print(f"\n📊 Loaded {len(sql_queries)} SQL queries")

# Display a preview
if sql_queries:
    for name, sql in sql_queries.items():
        display(HTML(f"""
        <details style="margin: 10px 0; padding: 15px; background: #1a1a2e; border-radius: 8px; border-left: 3px solid #00ff88;">
            <summary style="color: #00ff88; cursor: pointer; font-weight: 600;">📄 {name}.sql</summary>
            <pre style="background: #0a0a0a; color: #e0e0e0; padding: 15px; margin-top: 10px; border-radius: 4px; overflow-x: auto; font-size: 12px;">{sql[:1000]}{'...' if len(sql) > 1000 else ''}</pre>
        </details>
        """))


# ============================================================================
# CELL 4: LOAD DUNE CLIENT FROM GITHUB
# ============================================================================
# Copy this into a Python cell in Hex

# Fetch the Dune client code from GitHub
dune_client_code = fetch_github_raw(CASE_STUDY_REPO, "dune_client/symbiotic_dune_client.py")

if dune_client_code:
    # Execute the code to make SymbioticDuneClient available
    exec(dune_client_code, globals())
    print("✅ SymbioticDuneClient loaded from GitHub")
else:
    print("⚠️ Could not load Dune client")


# ============================================================================
# CELL 5: FETCH LIVE DATA FROM DUNE
# ============================================================================
# Copy this into a Python cell in Hex
# NOTE: Add your DUNE_API_KEY as a Hex Secret first!

import os

# Get API key from Hex secrets
# DUNE_API_KEY = os.environ.get('DUNE_API_KEY')  # Uncomment in Hex
DUNE_API_KEY = "YOUR_DUNE_API_KEY_HERE"  # Replace or use Hex secrets

# Query IDs from Symbiotic Dune dashboards
QUERY_IDS = {
    "rewards_v1": 5734268,
    "network_rewards": 5845829,
    "tvl_all_vaults": 4627837,
    "tvl_over_time": 4921148,
    "tvl_by_collateral": 4921564,
    "operators": 4543572,
}

# Initialize client and fetch data
try:
    from dune_client.client import DuneClient
    dune = DuneClient(DUNE_API_KEY)
    
    dataframes = {}
    print("📊 Fetching Dune data...")
    
    for name, query_id in QUERY_IDS.items():
        try:
            result = dune.get_latest_result(query_id)
            df = pd.DataFrame(result.result.rows)
            dataframes[name] = df
            print(f"   ✅ {name}: {len(df)} rows")
        except Exception as e:
            print(f"   ⚠️ {name}: {e}")
    
    print(f"\n✅ Loaded {len(dataframes)} datasets")
    
except Exception as e:
    print(f"⚠️ Dune client not available: {e}")
    print("   Using sample data instead...")
    dataframes = {}


# ============================================================================
# CELL 6: STYLED DATA DISPLAY
# ============================================================================
# Copy this into a Python cell in Hex

def style_dataframe(df, title=""):
    """Apply Symbiotic styling to dataframes"""
    
    styled = df.style.set_table_styles([
        {'selector': 'table', 'props': [
            ('font-family', 'Inter, sans-serif'),
            ('border-collapse', 'collapse'),
            ('width', '100%'),
            ('margin', '20px 0'),
        ]},
        {'selector': 'th', 'props': [
            ('background-color', '#00ff88'),
            ('color', '#0a0a0a'),
            ('font-weight', '600'),
            ('padding', '12px 16px'),
            ('text-align', 'left'),
        ]},
        {'selector': 'td', 'props': [
            ('padding', '10px 16px'),
            ('border-bottom', '1px solid #333'),
            ('color', '#e0e0e0'),
            ('background-color', '#1a1a2e'),
        ]},
        {'selector': 'tr:hover td', 'props': [
            ('background-color', '#2a2a4e'),
        ]},
    ])
    
    if title:
        display(HTML(f"<h3 style='color: #00ff88; font-family: Inter, sans-serif;'>{title}</h3>"))
    
    return styled

# Display loaded data
if dataframes:
    for name, df in list(dataframes.items())[:3]:  # Show first 3
        display(style_dataframe(df.head(10), f"📊 {name.replace('_', ' ').title()}"))
else:
    print("No data loaded. Add your DUNE_API_KEY to fetch live data.")


# ============================================================================
# CELL 7: ANALYSIS SUMMARY FROM GITHUB
# ============================================================================
# Copy this into a Python cell in Hex

# Fetch the analysis summary from Case-Study repo
analysis_md = fetch_github_raw(CASE_STUDY_REPO, "dune_client/output/analysis_summary.md")

if analysis_md:
    import markdown
    html = markdown.markdown(analysis_md, extensions=['tables', 'extra'])
    
    display(HTML(f"""
    <div style="
        font-family: Inter, sans-serif;
        max-width: 900px;
        padding: 30px;
        background: #1a1a2e;
        border-radius: 12px;
        color: #e0e0e0;
        margin: 20px 0;
        border-left: 4px solid #00ff88;
    ">
        <h2 style="color: #00ff88; margin-top: 0;">📈 Analysis Summary</h2>
        {html}
    </div>
    """))
    print("✅ Analysis summary loaded from GitHub")


# ============================================================================
# CELL 8: REPO FILE BROWSER
# ============================================================================
# Copy this into a Python cell in Hex

def display_repo_structure(repo, path=""):
    """Display the repository file structure"""
    files = list_github_dir(repo, path)
    
    html = f"""
    <div style="
        font-family: monospace;
        background: #0a0a0a;
        padding: 20px;
        border-radius: 8px;
        color: #e0e0e0;
    ">
        <h3 style="color: #00ff88; margin-top: 0;">📁 {repo}</h3>
    """
    
    for item in files:
        icon = "📁" if item['type'] == 'dir' else "📄"
        color = "#00ff88" if item['type'] == 'dir' else "#e0e0e0"
        html += f"<div style='margin: 4px 0; color: {color};'>{icon} {item['name']}</div>"
    
    html += "</div>"
    display(HTML(html))

# Show both repo structures
print("📦 Your GitHub Repositories:")
display_repo_structure(CASE_STUDY_REPO)
display_repo_structure(CONTENT_REPO)


# ============================================================================
# USAGE NOTES
# ============================================================================
"""
🔄 HOW THE GITHUB SYNC WORKS:
1. All content is fetched directly from your GitHub repos
2. When you push changes to GitHub, just re-run the cells to get updates
3. No local files needed - everything comes from the cloud!

📝 TO UPDATE YOUR DASHBOARD:
1. Edit files in Obsidian (Introduction.md) or VS Code (SQL queries)
2. Commit and push to GitHub
3. Re-run the Hex cells to see the changes

🔑 SETUP IN HEX:
1. Go to Settings > Secrets
2. Add DUNE_API_KEY with your Dune API key
3. Copy each CELL above into separate Python cells
4. Run all cells!
"""

