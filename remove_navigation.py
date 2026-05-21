#!/usr/bin/env python3
"""
Script to remove bottom navigation from all templates.
This creates a cleaner design without navigation bars.
"""

import os
import re

def remove_bottom_nav_from_file(file_path):
    """Remove bottom navigation from a template file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match bottom navigation sections
        patterns = [
            # Standard bottom nav pattern
            r'<!-- Bottom Navigation -->\s*<div class="bottom-nav">.*?</div>',
            # Alternative pattern
            r'<div class="bottom-nav">.*?</div>',
        ]
        
        original_content = content
        
        for pattern in patterns:
            content = re.sub(pattern, '<!-- Bottom Navigation removed for cleaner design -->', content, flags=re.DOTALL)
        
        # Also remove bottom-nav CSS if it exists
        css_pattern = r'\.bottom-nav\s*\{[^}]*\}[^}]*(?:\}[^}]*)*'
        content = re.sub(css_pattern, '/* Bottom navigation CSS removed */', content, flags=re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"⏭️  No changes: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def clean_all_templates():
    """Remove bottom navigation from all template files"""
    print("🧹 Removing bottom navigation from all templates...")
    
    templates_dir = "templates"
    files_updated = 0
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if remove_bottom_nav_from_file(file_path):
                    files_updated += 1
    
    print(f"\n🎉 Cleanup complete! Updated {files_updated} template files")
    print("📱 Application now has a cleaner design without navigation bars")

if __name__ == '__main__':
    clean_all_templates()
