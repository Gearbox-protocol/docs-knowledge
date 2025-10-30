#!/usr/bin/env python3
import re
import os
import glob

def final_cleanup(filepath):
    """Final cleanup to remove remaining markup artifacts"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove remaining CSS-like syntax
    content = re.sub(r':::*\s*', '', content)
    content = re.sub(r':::.*?:::', '', content, flags=re.DOTALL)
    
    # Remove image references and alt text
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    
    # Remove empty lines with just colons
    content = re.sub(r'^:+$', '', content, flags=re.MULTILINE)
    
    # Clean up extra whitespace
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith(':::'):
            cleaned_lines.append(line)
        elif not line and cleaned_lines and cleaned_lines[-1] != '':
            cleaned_lines.append('')
    
    # Join lines back
    content = '\n'.join(cleaned_lines)
    
    # Remove excessive empty lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()

def main():
    # Get all markdown files
    md_files = glob.glob('*.md')
    
    for filepath in md_files:
        print(f"Final cleanup of {filepath}...")
        cleaned_content = final_cleanup(filepath)
        
        # Write cleaned content back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"Final cleanup completed for {filepath}")

if __name__ == "__main__":
    main()



