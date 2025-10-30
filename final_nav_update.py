#!/usr/bin/env python3
"""
Final update: convert all simple EVM network paths to nested structure in docs.json.
"""

import json
import re
from pathlib import Path

# Build map of available networks with proper names
network_names = {}
catalog_dir = Path("en/data/catalog/evm")

for network_dir in catalog_dir.iterdir():
    if network_dir.is_dir():
        slug = network_dir.name
        overview = network_dir / "overview.mdx"
        if overview.exists():
            with open(overview, 'r') as f:
                content = f.read()
                # Get description
                match = re.search(r'description:\s*"([^"]+)', content)
                if match:
                    desc = match.group(1)
                    # Remove common suffixes
                    name = desc.replace(' data indexing and API access', '')
                    name = name.replace(' data indexing', '')
                    network_names[slug] = name

print(f"Loaded {len(network_names)} network names")

# Read docs.json
with open('docs.json', 'r') as f:
    docs = json.load(f)

# Update EVM networks in navigation
updated = 0
for lang in docs['navigation']['languages']:
    if lang['language'] == 'en':
        print(f"Processing language: {lang['language']}")
        for tab in lang['tabs']:
            print(f"  Tab: {tab.get('tab', 'NO TAB KEY')}")
            if tab.get('tab') == 'Data Catalog':
                for dropdown in tab.get('dropdowns', []):
                    if dropdown.get('dropdown') == 'EVM Data':
                        for group in dropdown['groups']:
                            if group['group'] == 'Supported Networks':
                                new_pages = []
                                print(f"Found {len(group['pages'])} pages in Supported Networks")
                                for page in group['pages']:
                                    # Already nested? Keep it
                                    if isinstance(page, dict):
                                        new_pages.append(page)
                                        print(f"  • Kept nested: {page.get('group', 'unknown')}")
                                        continue
                                    
                                    # Simple path? Try to convert
                                    if '/catalog/evm/' in page:
                                        # Extract slug
                                        slug = page.split('/catalog/evm/')[-1].replace('/overview', '')
                                        
                                        if slug in network_names:
                                            new_pages.append({
                                                "group": network_names[slug],
                                                "pages": [
                                                    f"en/data/catalog/evm/{slug}/overview",
                                                    f"en/data/catalog/evm/{slug}/schema"
                                                ]
                                            })
                                            updated += 1
                                            print(f"  ✓ {slug} → {network_names[slug]}")
                                        else:
                                            new_pages.append(page)
                                            print(f"  ⚠ Kept {slug} (no nested structure found)")
                                    else:
                                        new_pages.append(page)
                                
                                group['pages'] = new_pages

# Write back
with open('docs.json', 'w') as f:
    json.dump(docs, f, indent=2)

print(f"\n✓ Updated {updated} networks in docs.json")

