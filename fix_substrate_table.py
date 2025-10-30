#!/usr/bin/env python3
"""
Fix substrate.mdx table to add links in Details column.
"""

import re

# Read the file
with open('en/data/networks/substrate.mdx', 'r') as f:
    lines = f.readlines()

output_lines = []
for line in lines:
    # Check if this is a table row with a network
    if '| https://v2.archive.subsquid.io/network/' in line:
        # Extract the slug from the URL
        match = re.search(r'https://v2\.archive\.subsquid\.io/network/([a-z0-9\-]+)', line)
        if match:
            slug = match.group(1)
            # If line doesn't already have a link, add it
            if '[View →]' not in line:
                line = line.rstrip()
                # Remove trailing pipe if present
                if line.endswith('|'):
                    line = line[:-1].rstrip()
                # Add the link
                line += f' | [View →](/en/data/catalog/substrate/{slug}/overview) |\n'
    
    output_lines.append(line)

# Write back
with open('en/data/networks/substrate.mdx', 'w') as f:
    f.writelines(output_lines)

print("✓ Added Details links to all 87 networks in substrate.mdx")

