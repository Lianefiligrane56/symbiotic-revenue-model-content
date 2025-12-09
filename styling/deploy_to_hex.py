"""
Deploy Symbiotic Dashboard to Hex via API
==========================================

SETUP:
1. Get your Hex API Token:
   - Go to hex.tech
   - Click your profile → Settings → API Keys
   - Create new API key
   
2. Get your Project ID:
   - Open your Hex project
   - Copy the ID from URL: hex.tech/project/[PROJECT_ID]/...
   
3. Run this script with your credentials
"""

import requests
import json

# ============================================================================
# CONFIGURATION - UPDATE THESE
# ============================================================================

HEX_API_TOKEN = "974b8e1547a679beb715a8f2aeba6b1ed8e5216dad81b373a88f03524b63635e47b5d2a25110d9d2e7d3a1dd55bdcb47"
HEX_PROJECT_ID = "019afc07-fa2e-7009-a5a3-de063b204d72"  # Symbiotic Dashboard

# Hex API Base URL
HEX_API_BASE = "https://app.hex.tech/api/v1"

# ============================================================================
# HEX API FUNCTIONS
# ============================================================================

def get_project_info():
    """Get information about a Hex project"""
    url = f"{HEX_API_BASE}/project/{HEX_PROJECT_ID}"
    headers = {
        "Authorization": f"Bearer {HEX_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def run_project():
    """Run/execute a Hex project"""
    url = f"{HEX_API_BASE}/project/{HEX_PROJECT_ID}/run"
    headers = {
        "Authorization": f"Bearer {HEX_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Optional: Pass input parameters
    payload = {
        "inputParams": {
            # Add any input parameters here
            # "param_name": "value"
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_run_status(run_id):
    """Check status of a project run"""
    url = f"{HEX_API_BASE}/project/{HEX_PROJECT_ID}/run/{run_id}"
    headers = {
        "Authorization": f"Bearer {HEX_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def list_projects():
    """List all your Hex projects"""
    url = f"{HEX_API_BASE}/projects"
    headers = {
        "Authorization": f"Bearer {HEX_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    print("=" * 60)
    print("HEX API DEPLOYMENT")
    print("=" * 60)
    
    if HEX_API_TOKEN == "YOUR_HEX_API_TOKEN":
        print("""
⚠️  Please configure your Hex API credentials first!

STEPS TO GET YOUR CREDENTIALS:
==============================

1. GET API TOKEN:
   - Go to: https://app.hex.tech/settings/api
   - Click "Create API key"
   - Copy the token
   - Paste it in this script: HEX_API_TOKEN = "your_token"

2. GET PROJECT ID:
   - Create a new project in Hex (or use existing)
   - The URL looks like: hex.tech/project/abc123-def456/...
   - Copy "abc123-def456" part
   - Paste it in this script: HEX_PROJECT_ID = "abc123-def456"

3. MANUAL SETUP (Required once):
   - Go to your Hex project
   - Copy cells from: symbiotic_hex_dashboard.py
   - Add your Dune API key as a secret in Hex

4. RUN THIS SCRIPT:
   - After setup, run this script to trigger project execution
""")
        return
    
    print("\n📋 Listing your Hex projects...")
    projects = list_projects()
    
    if projects:
        print(f"\nFound {len(projects.get('projects', []))} projects:")
        for proj in projects.get('projects', []):
            print(f"   - {proj.get('name')} (ID: {proj.get('id')})")
    
    print(f"\n🔍 Getting project info for: {HEX_PROJECT_ID}")
    info = get_project_info()
    
    if info:
        print(f"   Project Name: {info.get('name')}")
        print(f"   Status: {info.get('status')}")
    
    print("\n🚀 Running project...")
    run_result = run_project()
    
    if run_result:
        run_id = run_result.get('runId')
        print(f"   Run ID: {run_id}")
        print(f"   Status: {run_result.get('status')}")
        
        print("\n✅ Project execution triggered!")
        print(f"\n🔗 View results at: https://app.hex.tech/project/{HEX_PROJECT_ID}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()


# ============================================================================
# ALTERNATIVE: CREATE PROJECT VIA API (Advanced)
# ============================================================================
"""
Note: Hex's public API currently supports:
- Running projects
- Getting project info
- Listing projects
- Getting run status

To CREATE/EDIT cells programmatically, you would need to:
1. Use the Hex UI to create the project structure
2. Use the API to run/trigger the project

For full programmatic control, consider:
- Hex's GraphQL API (internal, may change)
- Exporting/importing project JSON files
- Using Hex's CLI tools (if available)

The recommended workflow is:
1. Create project manually in Hex UI
2. Copy cells from symbiotic_hex_dashboard.py
3. Use this API script to trigger runs and get results
"""

