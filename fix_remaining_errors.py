#!/usr/bin/env python3

import os
import re
import glob

def fix_frontmatter_issues(file_path):
    """Fix remaining frontmatter syntax issues"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has frontmatter
        if not content.startswith('---\n'):
            return False
            
        lines = content.split('\n')
        fixed = False
        
        # Fix missing newlines before closing ---
        for i, line in enumerate(lines):
            if line.strip() == '---' and i > 0:
                # Check if previous line doesn't end with newline
                if i > 0 and lines[i-1].strip() and not lines[i-1].endswith('\n'):
                    # Add newline before closing ---
                    lines[i-1] = lines[i-1].rstrip()
                    lines.insert(i, '')
                    fixed = True
                    break
        
        # Fix concatenated frontmatter fields
        for i, line in enumerate(lines):
            if '---' in line and line.strip() != '---':
                # Split concatenated fields
                if 'title:' in line and 'description:' in line:
                    # This is a concatenated line, split it
                    parts = line.split('description:')
                    if len(parts) == 2:
                        lines[i] = parts[0].strip()
                        lines.insert(i+1, 'description:' + parts[1])
                        fixed = True
                        break
        
        if fixed:
            # Write back the fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            return True
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False
    
    return False

def fix_escaped_curly_braces(file_path):
    """Fix escaped curly braces in JSX attributes"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix escaped curly braces in JSX attributes
        original_content = content
        
        # Fix style attributes
        content = re.sub(r'style=\\{\{([^}]+)\\}\\}', r'style={{\1}}', content)
        
        # Fix other JSX attributes with escaped braces
        content = re.sub(r'(\w+)=\\{\{([^}]+)\\}\\}', r'\1={{\2}}', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False
    
    return False

def main():
    # Find all MDX files
    mdx_files = glob.glob('en/**/*.mdx', recursive=True)
    
    fixed_count = 0
    
    for file_path in mdx_files:
        print(f"Processing {file_path}...")
        
        # Fix frontmatter issues
        if fix_frontmatter_issues(file_path):
            print(f"  Fixed frontmatter in {file_path}")
            fixed_count += 1
        
        # Fix escaped curly braces
        if fix_escaped_curly_braces(file_path):
            print(f"  Fixed curly braces in {file_path}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    main()