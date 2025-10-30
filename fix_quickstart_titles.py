#!/usr/bin/env python3
"""
Fix Quick Start card titles in all non-EVM network overview pages.
Change "CLI Cheatsheet" to "Quick Start"
"""

import os
from pathlib import Path

# Directories to process
DIRS = [
    "en/data/catalog/substrate",
    "en/data/catalog/fuel",
    "en/data/catalog/tron",
    "en/data/catalog/starknet",
    "en/data/catalog/solana"
]

count = 0

for dir_path in DIRS:
    catalog_dir = Path(dir_path)
    if not catalog_dir.exists():
        continue
    
    # Find all overview.mdx files
    for overview_file in catalog_dir.glob("*/overview.mdx"):
        with open(overview_file, 'r') as f:
            content = f.read()
        
        # Replace the card title
        if 'title="CLI Cheatsheet"' in content:
            content = content.replace(
                'title="CLI Cheatsheet"',
                'title="Quick Start"'
            )
            
            with open(overview_file, 'w') as f:
                f.write(content)
            
            count += 1
            print(f"✓ {overview_file}")

print(f"\n✓ Updated {count} overview pages")

