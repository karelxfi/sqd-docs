#!/usr/bin/env python3
"""
Validate details tags in MDX files.
"""

import re

def validate_details_tags(file_path):
    """Validate details tags in a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all details tags
    details_pattern = r'<details[^>]*>'
    closing_pattern = r'</details>'
    
    opening_tags = re.findall(details_pattern, content)
    closing_tags = re.findall(closing_pattern, content)
    
    print(f"File: {file_path}")
    print(f"Opening tags: {len(opening_tags)}")
    print(f"Closing tags: {len(closing_tags)}")
    
    for i, tag in enumerate(opening_tags):
        print(f"  Opening {i+1}: {tag}")
    
    for i, tag in enumerate(closing_tags):
        print(f"  Closing {i+1}: {tag}")
    
    if len(opening_tags) != len(closing_tags):
        print(f"  ❌ Mismatch: {len(opening_tags)} opening, {len(closing_tags)} closing")
    else:
        print(f"  ✅ Balanced: {len(opening_tags)} opening, {len(closing_tags)} closing")
    
    print()

if __name__ == "__main__":
    validate_details_tags('en/api-reference/reference/substrate-api.mdx')
    validate_details_tags('en/api-reference/reference/starknet-api.mdx')
