"""
Symbiotic Dune Data Fetcher
===========================
Fetch data from Dune Analytics API for Symbiotic Protocol analysis.

Usage in Hex:
    from scripts.fetch_dune_data import fetch_query, fetch_latest, SYMBIOTIC_QUERIES
"""

import requests
import time
import pandas as pd
from io import StringIO

# ═══════════════════════════════════════════════════════════════
# SYMBIOTIC DUNE QUERY IDs
# ═══════════════════════════════════════════════════════════════
SYMBIOTIC_QUERIES = {
    'rewards_dashboard': 4289365,      # Main rewards dashboard
    'tvl_over_time': 4284521,          # TVL historical data
    'operators': 4285123,               # Operator registrations
    'networks': 4286789,                # Network overview
    'vault_stats': 4287456,             # Vault statistics
}


def fetch_query(query_id, api_key, timeout=60):
    """
    Execute a Dune query and return results as DataFrame.
    
    Args:
        query_id: Dune query ID (int)
        api_key: Dune API key (str)
        timeout: Max seconds to wait (default 60)
    
    Returns:
        pandas DataFrame with query results
    """
    if not api_key:
        raise ValueError("❌ DUNE_API_KEY required. Get it at: https://dune.com/settings/api")
    
    headers = {"X-Dune-API-Key": api_key}
    
    # Execute query
    print(f"🔄 Executing Dune query {query_id}...")
    execute_url = f"https://api.dune.com/api/v1/query/{query_id}/execute"
    
    response = requests.post(execute_url, headers=headers)
    response.raise_for_status()
    execution_id = response.json()['execution_id']
    
    print(f"   Execution ID: {execution_id}")
    
    # Poll for results
    results_url = f"https://api.dune.com/api/v1/execution/{execution_id}/results"
    max_attempts = timeout // 2
    
    for attempt in range(max_attempts):
        time.sleep(2)
        response = requests.get(results_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data['state'] == 'QUERY_STATE_COMPLETED':
            rows = data['result']['rows']
            df = pd.DataFrame(rows)
            print(f"✅ Loaded {len(df):,} rows")
            return df
        
        if data['state'] == 'QUERY_STATE_FAILED':
            raise Exception(f"Query failed: {data.get('error', 'Unknown error')}")
        
        print(f"   Waiting... ({attempt + 1}/{max_attempts})")
    
    raise TimeoutError(f"Query timed out after {timeout} seconds")


def fetch_latest(query_id, api_key):
    """
    Get the latest cached results for a query (doesn't re-execute).
    Faster but may have stale data.
    
    Args:
        query_id: Dune query ID
        api_key: Dune API key
    
    Returns:
        pandas DataFrame
    """
    if not api_key:
        raise ValueError("❌ DUNE_API_KEY required")
    
    headers = {"X-Dune-API-Key": api_key}
    url = f"https://api.dune.com/api/v1/query/{query_id}/results"
    
    print(f"📥 Fetching latest results for query {query_id}...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    rows = data['result']['rows']
    df = pd.DataFrame(rows)
    
    print(f"✅ Loaded {len(df):,} rows (cached)")
    return df


def fetch_csv_from_github():
    """
    Fetch pre-exported CSV data from GitHub repo.
    Use this when you don't have a Dune API key.
    
    Returns:
        dict of DataFrames
    """
    BASE_URL = "https://raw.githubusercontent.com/Lianefiligrane56/symbiotic-revenue-model-content/main/data/"
    
    datasets = {
        'rewards_total': 'rewards_total.csv',
        'rewards_by_network': 'rewards_by_network.csv',
        'tvl_over_time': 'tvl_over_time.csv',
        'tvl_by_vault': 'tvl_by_vault.csv',
        'tvl_by_collateral': 'tvl_by_collateral.csv',
        'operator_count': 'operator_count.csv',
        'operator_registrations': 'operator_registrations.csv',
        'network_rewards': 'network_rewards.csv',
    }
    
    data = {}
    print("📥 Fetching data from GitHub...")
    
    for name, filename in datasets.items():
        try:
            url = BASE_URL + filename
            df = pd.read_csv(url)
            data[name] = df
            print(f"   ✅ {name}: {len(df)} rows")
        except Exception as e:
            print(f"   ⚠️  {name}: Failed ({e})")
            data[name] = pd.DataFrame()
    
    return data


# ═══════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def load_all_data(api_key=None):
    """
    Load all Symbiotic data - from Dune API if key provided, else from GitHub.
    
    Args:
        api_key: Optional Dune API key
    
    Returns:
        dict of DataFrames
    """
    if api_key:
        print("🔑 Using Dune API...")
        return {
            'rewards': fetch_latest(SYMBIOTIC_QUERIES['rewards_dashboard'], api_key),
            'tvl': fetch_latest(SYMBIOTIC_QUERIES['tvl_over_time'], api_key),
        }
    else:
        print("📁 Using GitHub cached data...")
        return fetch_csv_from_github()


# Print available functions when imported
print("📊 Symbiotic Dune Data Fetcher loaded!")
print("   → fetch_query(query_id, api_key)")
print("   → fetch_latest(query_id, api_key)")
print("   → fetch_csv_from_github()")
print("   → load_all_data(api_key=None)")
print(f"   → SYMBIOTIC_QUERIES: {list(SYMBIOTIC_QUERIES.keys())}")

