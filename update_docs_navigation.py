#!/usr/bin/env python3
"""
Update docs.json navigation to include nested Overview/Schema pages for all EVM networks.
"""

import json
import re

# Load processed networks
with open('processed_networks.json', 'r') as f:
    networks = json.load(f)

# Add the already completed networks to the list
completed_networks = [
    {"slug": "ethereum-mainnet", "name": "Ethereum Mainnet"},
    {"slug": "arbitrum-one", "name": "Arbitrum One"}
]

# Merge with processed networks
all_networks = []
# Add ethereum-mainnet first
all_networks.append(completed_networks[0])
# Add other networks in order, inserting arbitrum-one in the right place
for network in networks:
    if network["slug"] == "arbitrum-nova":
        # Insert arbitrum-one before arbitrum-nova
        all_networks.append(completed_networks[1])
    all_networks.append(network)

networks = all_networks

# Read docs.json
with open('docs.json', 'r') as f:
    docs = json.load(f)

# Find the EVM data section in navigation
for lang in docs['navigation']['languages']:
    if lang['language'] == 'en':
        for tab in lang['tabs']:
            if tab.get('tab') == 'Data':
                for dropdown in tab.get('dropdowns', []):
                    if dropdown.get('dropdown') == 'EVM Data':
                        for group in dropdown['groups']:
                            if group['group'] == 'Supported Networks':
                                # Update pages to use nested structure
                                new_pages = []
                                for page in group['pages']:
                                    # Skip if already nested (dict/object)
                                    if isinstance(page, dict):
                                        new_pages.append(page)
                                        continue
                                    
                                    # Extract slug from path
                                    match = re.search(r'/([^/]+)(?:/overview)?$', page)
                                    if not match:
                                        new_pages.append(page)
                                        continue
                                    
                                    slug = match.group(1)
                                    
                                    # Find network name
                                    network = next((n for n in networks if n['slug'] == slug), None)
                                    if not network:
                                        # Keep as is if not in our processed list
                                        new_pages.append(page)
                                        continue
                                    
                                    # Create nested structure
                                    new_pages.append({
                                        "group": network['name'],
                                        "pages": [
                                            f"en/data/catalog/evm/{slug}/overview",
                                            f"en/data/catalog/evm/{slug}/schema"
                                        ]
                                    })
                                
                                group['pages'] = new_pages
                                print(f"Updated {len(new_pages)} EVM network entries in navigation")

# Write updated docs.json
with open('docs.json', 'w') as f:
    json.dump(docs, f, indent=2)

print("✓ docs.json navigation updated successfully")

