#!/usr/bin/env python3
"""
Update docs.json navigation:
1. Add all 87 Substrate networks sorted A-Z
2. Sort all EVM networks alphabetically A-Z
"""

import json
import re
from pathlib import Path

def parse_substrate_networks():
    """Extract network names and slugs from substrate.mdx table."""
    with open('en/data/networks/substrate.mdx', 'r') as f:
        content = f.read()
    
    networks = []
    pattern = r'\|\s*([^|]+?)\s*\|\s*https://v2\.archive\.subsquid\.io/network/([a-z0-9\-]+)\s*\|'
    matches = re.findall(pattern, content)
    
    for name, slug in matches:
        name = name.strip()
        # Remove footnote markers
        name = re.sub(r'\s*\(\*+\)\s*$', '', name)
        networks.append({'name': name, 'slug': slug})
    
    # Sort alphabetically by name
    networks.sort(key=lambda x: x['name'].lower())
    return networks

def get_evm_networks_from_nav(nav_pages):
    """Extract EVM network entries from navigation."""
    evm_networks = []
    for entry in nav_pages:
        if isinstance(entry, dict) and 'group' in entry:
            network_name = entry['group']
            pages = entry.get('pages', [])
            if len(pages) == 2 and 'evm' in str(pages):
                evm_networks.append(entry)
    return evm_networks

# Read docs.json
with open('docs.json', 'r') as f:
    docs = json.load(f)

# Get Substrate networks
substrate_networks = parse_substrate_networks()
print(f"Found {len(substrate_networks)} Substrate networks")

# Find and update navigation
for lang in docs['navigation']['languages']:
    if lang['language'] == 'en':
        for tab in lang['tabs']:
            if tab.get('tab') == 'Data Catalog':
                for dropdown in tab.get('dropdowns', []):
                    
                    # Update Substrate Data
                    if dropdown.get('dropdown') == 'Substrate Data':
                        for group in dropdown['groups']:
                            if group['group'] == 'Networks':
                                # Create sorted network entries
                                new_pages = []
                                for network in substrate_networks:
                                    new_pages.append({
                                        "group": network['name'],
                                        "pages": [
                                            f"en/data/catalog/substrate/{network['slug']}/overview",
                                            f"en/data/catalog/substrate/{network['slug']}/schema"
                                        ]
                                    })
                                group['pages'] = new_pages
                                print(f"✓ Updated Substrate networks: {len(new_pages)} networks sorted A-Z")
                    
                    # Sort EVM Data
                    elif dropdown.get('dropdown') == 'EVM Data':
                        for group in dropdown['groups']:
                            if group['group'] == 'Supported Networks':
                                # Extract current EVM networks
                                evm_networks = get_evm_networks_from_nav(group['pages'])
                                
                                # Sort alphabetically by group name
                                evm_networks.sort(key=lambda x: x['group'].lower())
                                
                                group['pages'] = evm_networks
                                print(f"✓ Sorted EVM networks: {len(evm_networks)} networks sorted A-Z")

# Write back
with open('docs.json', 'w') as f:
    json.dump(docs, f, indent=2)

print(f"\n✓ Navigation updated successfully")

