#!/usr/bin/env python3
"""
Update docs.json to nest ALL EVM network pages with Overview/Schema structure.
"""

import json
import re
from pathlib import Path

# Build a complete dictionary of all available networks
catalog_dir = Path("en/data/catalog/evm")
available_networks = {}

# Check all directories in the catalog
for item in catalog_dir.iterdir():
    if item.is_dir():
        slug = item.name
        # Try to get the network name from overview.mdx
        overview_file = item / "overview.mdx"
        if overview_file.exists():
            with open(overview_file, 'r') as f:
                content = f.read()
                # Extract name from description frontmatter
                match = re.search(r'description:\s*"([^"]+?)(?:\s+data indexing)?', content)
                if match:
                    available_networks[slug] = match.group(1)
                else:
                    # Fallback: capitalize slug
                    available_networks[slug] = slug.replace('-', ' ').title()

print(f"Found {len(available_networks)} networks with nested structure")

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
                                new_pages = []
                                updated_count = 0
                                skipped_count = 0
                                
                                for page in group['pages']:
                                    # If already nested, keep it
                                    if isinstance(page, dict):
                                        new_pages.append(page)
                                        continue
                                    
                                    # Extract slug
                                    match = re.search(r'/catalog/evm/([^/]+)(?:/overview)?$', page)
                                    if not match:
                                        new_pages.append(page)
                                        skipped_count += 1
                                        continue
                                    
                                    slug = match.group(1)
                                    
                                    # Check if nested structure exists
                                    if slug in available_networks:
                                        new_pages.append({
                                            "group": available_networks[slug],
                                            "pages": [
                                                f"en/data/catalog/evm/{slug}/overview",
                                                f"en/data/catalog/evm/{slug}/schema"
                                            ]
                                        })
                                        updated_count += 1
                                    else:
                                        # Keep original if no nested structure
                                        new_pages.append(page)
                                        skipped_count += 1
                                
                                group['pages'] = new_pages
                                print(f"Updated: {updated_count} networks")
                                print(f"Skipped: {skipped_count} networks (no nested structure)")
                                print(f"Total entries: {len(new_pages)}")

# Write updated docs.json
with open('docs.json', 'w') as f:
    json.dump(docs, f, indent=2)

print("✓ docs.json navigation updated successfully")

