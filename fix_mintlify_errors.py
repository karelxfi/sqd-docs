#!/usr/bin/env python3
"""
Fix Mintlify parsing errors in MDX files.

This script fixes:
1. Unclosed <Steps> and <details> tags
2. Unexpected closing slashes in tags
3. YAML frontmatter syntax errors (multiline descriptions)
4. Malformed JSX expressions in code blocks
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

def fix_frontmatter_yaml(content: str) -> str:
    """Fix YAML frontmatter issues."""
    lines = content.split('\n')

    if not lines or lines[0].strip() != '---':
        return content

    # Find the end of frontmatter
    frontmatter_end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            frontmatter_end = i
            break

    if frontmatter_end is None:
        return content

    # Fix the frontmatter section
    frontmatter_lines = lines[1:frontmatter_end]
    fixed_frontmatter = []

    i = 0
    while i < len(frontmatter_lines):
        line = frontmatter_lines[i]

        # Check if this is a description field with issues
        if line.strip().startswith('description:'):
            # Handle multiline descriptions properly
            if line.strip().endswith('>-'):
                # Already in proper multiline format
                fixed_frontmatter.append(line)
                i += 1
                # Get the description content
                desc_lines = []
                while i < len(frontmatter_lines) and not frontmatter_lines[i].strip().endswith('---'):
                    desc_lines.append(frontmatter_lines[i])
                    i += 1
                    # Break if we hit another field
                    if i < len(frontmatter_lines) and frontmatter_lines[i].strip() and not frontmatter_lines[i].startswith(' '):
                        break

                # Check if the last line accidentally includes ---
                if desc_lines and desc_lines[-1].strip().endswith('---'):
                    # This is the closing frontmatter marker on the same line
                    desc_lines[-1] = desc_lines[-1].replace('---', '').rstrip()
                    fixed_frontmatter.extend(desc_lines)
                    break  # We've hit the end
                else:
                    fixed_frontmatter.extend(desc_lines)
            else:
                # Single line or improperly formatted multiline
                fixed_frontmatter.append(line)
                i += 1
        else:
            fixed_frontmatter.append(line)
            i += 1

    # Reconstruct the content
    result = ['---'] + fixed_frontmatter + ['---'] + lines[frontmatter_end + 1:]
    return '\n'.join(result)

def fix_code_blocks(content: str) -> str:
    """Fix malformed code blocks and text markers."""
    # Fix ```text markers that should be closing backticks
    content = re.sub(r'```text\n', '```\n', content)

    # Fix standalone ```text that appears after code
    content = re.sub(r'\n```text\s*\n', '\n```\n', content)

    return content

def fix_unclosed_tags(content: str) -> str:
    """Fix unclosed HTML/JSX tags."""
    lines = content.split('\n')
    fixed_lines = []

    # Track open tags
    steps_open = 0
    details_open = 0

    for line in lines:
        # Count Steps tags
        steps_open += line.count('<Steps>')
        steps_open -= line.count('</Steps>')

        # Count details tags
        details_open += line.count('<details>')
        details_open -= line.count('</details>')

        fixed_lines.append(line)

    # Add missing closing tags at the end if needed
    if steps_open > 0:
        fixed_lines.append('</Steps>')
    if details_open > 0:
        fixed_lines.append('</details>')

    return '\n'.join(fixed_lines)

def fix_jsx_expressions(content: str) -> str:
    """Fix malformed JSX expressions in code blocks."""
    # Fix expressions like ${version} in code that should be escaped
    # Only fix these when they're inside code blocks or specific contexts

    # Pattern: Find code blocks and escape JSX expressions
    def escape_in_code_block(match):
        code_block = match.group(0)
        # Escape $ to prevent JSX interpretation
        code_block = code_block.replace('${', '\\${')
        return code_block

    # Apply to bash code blocks specifically
    content = re.sub(
        r'```bash.*?```',
        escape_in_code_block,
        content,
        flags=re.DOTALL
    )

    return content

def fix_closing_slashes(content: str) -> str:
    """Fix unexpected closing slashes like </details> without opening tag."""
    lines = content.split('\n')
    fixed_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check for closing details tag without proper opening
        # This happens around line 70 in logger files
        if '</details>' in line:
            # Look back to ensure there's a matching opening tag
            has_opening = False
            for j in range(i - 1, max(0, i - 50), -1):
                if '<details>' in lines[j]:
                    has_opening = True
                    break

            if not has_opening:
                # This is an orphaned closing tag, likely should be part of a details block
                # Skip it or comment it out
                i += 1
                continue

        fixed_lines.append(line)
        i += 1

    return '\n'.join(fixed_lines)

def fix_invalid_jsx_characters(content: str) -> str:
    """Fix invalid characters in JSX expressions."""
    # Fix pattern like <1 which is invalid JSX
    # This appears in faq.mdx around line 20

    # Replace < followed by a number in text with &lt;
    content = re.sub(r'<(\d)', r'&lt;\1', content)

    return content

def fix_file(filepath: Path) -> Tuple[bool, str]:
    """Fix a single MDX file. Returns (changed, error_message)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()

        content = original_content

        # Apply all fixes
        content = fix_frontmatter_yaml(content)
        content = fix_code_blocks(content)
        content = fix_unclosed_tags(content)
        content = fix_jsx_expressions(content)
        content = fix_closing_slashes(content)
        content = fix_invalid_jsx_characters(content)

        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, None

        return False, None

    except Exception as e:
        return False, str(e)

def main():
    """Main function to fix all MDX files."""
    base_dir = Path('/Users/account/sqd-docs-1')

    # Find all .mdx files
    mdx_files = list(base_dir.glob('**/*.mdx'))

    print(f"Found {len(mdx_files)} MDX files")

    fixed_count = 0
    error_count = 0

    for filepath in mdx_files:
        relative_path = filepath.relative_to(base_dir)
        changed, error = fix_file(filepath)

        if error:
            print(f"❌ Error in {relative_path}: {error}")
            error_count += 1
        elif changed:
            print(f"✅ Fixed {relative_path}")
            fixed_count += 1

    print(f"\n{'='*60}")
    print(f"Fixed {fixed_count} files")
    if error_count > 0:
        print(f"Encountered errors in {error_count} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
