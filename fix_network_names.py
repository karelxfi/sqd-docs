#!/usr/bin/env python3
"""
Fix network names in docs.json to remove description text.
"""

import json
import re
from pathlib import Path

# Build proper network names from overview files
network_names = {}
catalog_dir = Path("en/data/catalog/evm")

for network_dir in catalog_dir.iterdir():
    if network_dir.is_dir():
        slug = network_dir.name
        # Read the original .mdx file for the title
        old_file = catalog_dir / f"{slug}.mdx"
        if old_file.exists():
            with open(old_file, 'r') as f:
                content = f.read()
                match = re.search(r'title:\s*"([^"]+)"', content)
                if match:
                    network_names[slug] = match.group(1)

print(f"Loaded {len(network_names)} network names from original files")

# Read docs.json
with open('docs.json', 'r') as f:
    docs = json.load(f)

# Fix network names in navigation
fixed = 0
for lang in docs['navigation']['languages']:
    if lang['language'] == 'en':
        for tab in lang['tabs']:
            if tab.get('tab') == 'Data Catalog':
                for dropdown in tab.get('dropdowns', []):
                    if dropdown.get('dropdown') == 'EVM Data':
                        for group in dropdown['groups']:
                            if group['group'] == 'Supported Networks':
                                for page in group['pages']:
                                    if isinstance(page, dict) and 'group' in page:
                                        # Extract slug from the first page path
                                        if page['pages'] and '/catalog/evm/' in page['pages'][0]:
                                            slug = page['pages'][0].split('/catalog/evm/')[-1].split('/')[0]
                                            if slug in network_names:
                                                old_name = page['group']
                                                new_name = network_names[slug]
                                                if old_name != new_name:
                                                    page['group'] = new_name
                                                    fixed += 1
                                                    print(f"✓ {slug}: {old_name[:50]}... → {new_name}")

# Write back
with open('docs.json', 'w') as f:
    json.dump(docs, f, indent=2)

print(f"\n✓ Fixed {fixed} network names in docs.json")

