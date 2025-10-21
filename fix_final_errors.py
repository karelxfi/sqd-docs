#!/usr/bin/env python3
"""Fix specific remaining errors."""

from pathlib import Path
import re

def fix_file(filepath: Path) -> bool:
    """Fix a specific file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Fix 1: description line with ---  at the end (factory-contracts.mdx)
        # Pattern: "description: >-\n  Text---"
        content = re.sub(r'(description:\s*>-\s*\n\s+.+?)---\n', r'\1\n---\n', content)

        # Fix 2: Unclosed <details> tags - add closing tags if missing
        # Count opening and closing
        open_count = content.count('<details>')
        close_count = content.count('</details>')

        if open_count > close_count:
            # Add missing closing tags at the end
            content += '\n' + '</details>\n' * (open_count - close_count)

        # Fix 3: Orphan closing </Tip> tags (logs.mdx line 121)
        # Remove closing tags without opening
        lines = content.split('\n')
        tip_count = 0
        new_lines = []

        for line in lines:
            # Count tips on this line
            opens = line.count('<Tip>')
            closes = line.count('</Tip>')

            # Update balance
            new_balance = tip_count + opens

            # If we're trying to close more than we have open, skip those closes
            if closes > new_balance:
                # Remove the extra closing tags
                for _ in range(closes - new_balance):
                    line = line.replace('</Tip>', '', 1)
                closes = new_balance

            tip_count = new_balance - closes
            new_lines.append(line)

        content = '\n'.join(new_lines)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

    return False

def main():
    base = Path('/Users/account/sqd-docs-1')

    # Files with known issues
    files_to_fix = [
        'en/sdk/evm/reference/factory-contracts.mdx',
        'en/sdk/evm/reference/logs.mdx',
        'en/api/reference/evm-api.mdx',
        'en/api/reference/starknet-api.mdx',
        'en/api/reference/substrate-api.mdx',
        'en/cloud/reference/rpc-proxy-networks.mdx',
    ]

    fixed = 0
    for rel_path in files_to_fix:
        filepath = base / rel_path
        if filepath.exists():
            if fix_file(filepath):
                print(f"✅ Fixed {rel_path}")
                fixed += 1
        else:
            print(f"⚠️  Not found: {rel_path}")

    print(f"\nFixed {fixed} files")

if __name__ == '__main__':
    main()
