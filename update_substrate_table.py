#!/usr/bin/env python3
"""
Add Details column with links to substrate.mdx network table.
"""

import re

# Read the file
with open('en/data/networks/substrate.mdx', 'r') as f:
    content = f.read()

# Find the table and add Details column
# First, update the header
content = re.sub(
    r'\|\s*Network\s*\|\s*Gateway URL\s*\|',
    '| Network | Gateway URL | Details |',
    content
)

# Update the separator line
content = re.sub(
    r'\|\s*:[-]+:\s*\|\s*:[-]+:\s*\|',
    '| :-------------------------: | :-----------------------------------------------------------: | :-----: |',
    content
)

# Add link column to each network row
def add_link(match):
    network_name = match.group(1)
    gateway_url = match.group(2)
    slug = match.group(3)
    
    return f'| {network_name} | {gateway_url} | [View →](/en/data/catalog/substrate/{slug}/overview) |'

# Match table rows and add the link column
pattern = r'\|(\s*[^|]+?\s*)\|(https://v2\.archive\.subsquid\.io/network/([a-z0-9\-]+))\s*\|'
content = re.sub(pattern, add_link, content)

# Write back
with open('en/data/networks/substrate.mdx', 'w') as f:
    f.write(content)

print("✓ Added Details column with links to substrate.mdx")

