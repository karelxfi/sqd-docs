#!/usr/bin/env python3
"""
Fix substrate.mdx table to add links in Details column.
"""

import re

# Read the file
with open('en/data/networks/substrate.mdx', 'r') as f:
    content = f.read()

# Process each line with a network entry
lines = content.split('\n')
output_lines = []

for line in lines:
    # Check if this is a table row with a gateway URL
    if '| https://v2.archive.subsquid.io/network/' in line or 'https://v2.archive.subsquid.io/network/' in line:
        # Extract the slug from the URL
        match = re.search(r'https://v2\.archive\.subsquid\.io/network/([a-z0-9\-]+)', line)
        if match and '[View →]' not in line:
            slug = match.group(1)
            # Replace the pattern: "url          |" with "url          | [View →](/link) |"
            line = re.sub(
                r'(https://v2\.archive\.subsquid\.io/network/[a-z0-9\-]+\s*)\|$',
                rf'\1 | [View →](/en/data/catalog/substrate/{slug}/overview) |',
                line
            )
    
    output_lines.append(line)

# Write back
with open('en/data/networks/substrate.mdx', 'w') as f:
    f.write('\n'.join(output_lines))

print("✓ Fixed Details links for all networks in substrate.mdx")

