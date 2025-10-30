#!/usr/bin/env python3
"""
Update docs.json navigation to include nested Overview/Schema pages for ALL EVM networks.
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

# Create a lookup dictionary of all networks
all_networks_dict = {n["slug"]: n["name"] for n in networks}
all_networks_dict["ethereum-mainnet"] = "Ethereum Mainnet"
all_networks_dict["arbitrum-one"] = "Arbitrum One"

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
                                updated_count = 0
                                
                                for page in group['pages']:
                                    # If already nested (dict/object), keep it
                                    if isinstance(page, dict):
                                        new_pages.append(page)
                                        continue
                                    
                                    # Extract slug from path
                                    # Patterns: /catalog/evm/SLUG or /catalog/evm/SLUG/overview
                                    match = re.search(r'/catalog/evm/([^/]+)(?:/overview)?$', page)
                                    if not match:
                                        new_pages.append(page)
                                        continue
                                    
                                    slug = match.group(1)
                                    
                                    # Check if we have this network
                                    if slug in all_networks_dict:
                                        # Create nested structure
                                        new_pages.append({
                                            "group": all_networks_dict[slug],
                                            "pages": [
                                                f"en/data/catalog/evm/{slug}/overview",
                                                f"en/data/catalog/evm/{slug}/schema"
                                            ]
                                        })
                                        updated_count += 1
                                    else:
                                        # Keep as is if not in our list
                                        new_pages.append(page)
                                
                                group['pages'] = new_pages
                                print(f"Updated {updated_count} EVM network entries in navigation")
                                print(f"Total navigation entries: {len(new_pages)}")

# Write updated docs.json
with open('docs.json', 'w') as f:
    json.dump(docs, f, indent=2)

print("✓ docs.json navigation updated successfully")

