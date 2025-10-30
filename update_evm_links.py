#!/usr/bin/env python3
"""
Update all View → links in evm.mdx to point to /overview pages.
"""

import re

# Read evm.mdx
with open('en/data/networks/evm.mdx', 'r') as f:
    content = f.read()

# Pattern to match View → links
# Match: [View →](/en/data/catalog/evm/SLUG)
# Replace with: [View →](/en/data/catalog/evm/SLUG/overview)
pattern = r'\[View →\]\(/en/data/catalog/evm/([^/)]+)\)'
replacement = r'[View →](/en/data/catalog/evm/\1/overview)'

# Count replacements
original_content = content
content = re.sub(pattern, replacement, content)

count = len(re.findall(pattern, original_content))
print(f"Found {count} View → links to update")

# Write updated content
with open('en/data/networks/evm.mdx', 'w') as f:
    f.write(content)

print(f"✓ Updated all {count} View → links in evm.mdx")

