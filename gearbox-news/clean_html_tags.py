#!/usr/bin/env python3
import re
import os
import glob

def clean_html_tags_only(filepath):
    """Remove only HTML tags and attributes, preserve all text content exactly"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove HTML tags but keep the text content
    # This regex removes <tag> and </tag> but preserves everything inside
    content = re.sub(r'<[^>]+>', '', content)
    
    # Remove CSS class definitions like {.class-name}
    content = re.sub(r'\{\.[^}]*\}', '', content)
    
    # Remove HTML attributes like {rel="noreferrer"}
    content = re.sub(r'\{[^}]*\}', '', content)
    
    # Clean up extra whitespace but preserve paragraph structure
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)
        else:
            # Only add empty line if previous line wasn't empty
            if cleaned_lines and cleaned_lines[-1] != '':
                cleaned_lines.append('')
    
    # Join lines back
    content = '\n'.join(cleaned_lines)
    
    # Remove excessive empty lines (more than 2 consecutive)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()

def main():
    # Get all markdown files
    md_files = glob.glob('*.md')
    
    for filepath in md_files:
        print(f"Cleaning HTML tags from {filepath}...")
        cleaned_content = clean_html_tags_only(filepath)
        
        # Write cleaned content back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"Cleaned {filepath}")

if __name__ == "__main__":
    main()



