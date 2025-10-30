#!/usr/bin/env python3
import re
import os
import glob
from bs4 import BeautifulSoup

def clean_html_to_markdown(filepath):
    """Convert HTML to clean Markdown preserving all original text content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the main article content
    article_content = soup.find('div', class_='gh-content') or soup.find('article') or soup.find('main')
    
    if not article_content:
        # Fallback: try to find content by other means
        article_content = soup.find('div', {'class': re.compile(r'.*content.*')})
    
    if not article_content:
        # Last resort: use the whole body
        article_content = soup.find('body') or soup
    
    # Convert to markdown using pandoc-like approach but preserving text
    markdown_content = ""
    
    # Process each element
    for element in article_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'span', 'strong', 'em', 'a', 'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'br']):
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(element.name[1])
            markdown_content += f"{'#' * level} {element.get_text().strip()}\n\n"
        elif element.name == 'p':
            text = element.get_text().strip()
            if text:
                markdown_content += f"{text}\n\n"
        elif element.name == 'strong' or element.name == 'b':
            text = element.get_text().strip()
            if text:
                markdown_content += f"**{text}**"
        elif element.name == 'em' or element.name == 'i':
            text = element.get_text().strip()
            if text:
                markdown_content += f"*{text}*"
        elif element.name == 'a':
            text = element.get_text().strip()
            href = element.get('href', '')
            if text and href:
                markdown_content += f"[{text}]({href})"
            elif text:
                markdown_content += text
        elif element.name == 'ul':
            markdown_content += "\n"
            for li in element.find_all('li', recursive=False):
                text = li.get_text().strip()
                if text:
                    markdown_content += f"- {text}\n"
            markdown_content += "\n"
        elif element.name == 'ol':
            markdown_content += "\n"
            for i, li in enumerate(element.find_all('li', recursive=False), 1):
                text = li.get_text().strip()
                if text:
                    markdown_content += f"{i}. {text}\n"
            markdown_content += "\n"
        elif element.name == 'li':
            # Handle nested lists
            text = element.get_text().strip()
            if text and not any(parent.name in ['ul', 'ol'] for parent in element.parents):
                markdown_content += f"- {text}\n"
        elif element.name == 'blockquote':
            text = element.get_text().strip()
            if text:
                lines = text.split('\n')
                for line in lines:
                    if line.strip():
                        markdown_content += f"> {line.strip()}\n"
                markdown_content += "\n"
        elif element.name == 'pre':
            text = element.get_text()
            if text:
                markdown_content += f"```\n{text}\n```\n\n"
        elif element.name == 'code':
            text = element.get_text()
            if text:
                markdown_content += f"`{text}`"
        elif element.name == 'br':
            markdown_content += "\n"
        else:
            # For other elements, just get the text
            text = element.get_text().strip()
            if text and not any(child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li', 'blockquote', 'pre'] for child in element.find_all()):
                markdown_content += text
    
    # Clean up extra whitespace
    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
    markdown_content = re.sub(r'[ \t]+', ' ', markdown_content)
    
    return markdown_content.strip()

def main():
    # Get all HTML files
    html_files = glob.glob('*.html')
    
    for filepath in html_files:
        print(f"Converting {filepath}...")
        markdown_content = clean_html_to_markdown(filepath)
        
        # Create markdown filename
        md_filename = filepath.replace('.html', '.md')
        
        # Write markdown content
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Created {md_filename}")

if __name__ == "__main__":
    main()



