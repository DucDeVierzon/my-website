#!/usr/bin/env python3
"""
Script to check HTML files for encoding issues.
This script verifies that all HTML files:
1. Have proper UTF-8 charset declaration
2. Don't contain problematic control characters
3. Use proper UTF-8 encoding for accented characters
"""

import os
import sys

def check_file(filepath):
    """Check a single HTML file for encoding issues."""
    issues = []
    
    # Read as binary first to check for control characters
    with open(filepath, 'rb') as f:
        binary_content = f.read()
    
    # Check for control characters that shouldn't be in text
    control_chars = []
    for byte in range(0x00, 0x20):
        if byte in binary_content and byte not in [0x09, 0x0A, 0x0D]:  # Tab, LF, CR are OK
            control_chars.append(hex(byte))
    
    if control_chars:
        issues.append(f"Found problematic control characters: {control_chars}")
    
    # Try to read as UTF-8
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError as e:
        issues.append(f"Not valid UTF-8: {e}")
        return issues
    
    # Check for charset declaration
    has_charset = '<meta charset="utf-8">' in content or "<meta charset='utf-8'>" in content
    if not has_charset:
        issues.append("Missing <meta charset=\"utf-8\"> declaration")
    
    return issues

def main():
    """Check all HTML files in the current directory."""
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    if not html_files:
        print("No HTML files found.")
        return 0
    
    print(f"Checking {len(html_files)} HTML files...\n")
    
    all_ok = True
    for filepath in sorted(html_files):
        issues = check_file(filepath)
        if issues:
            print(f"❌ {filepath}:")
            for issue in issues:
                print(f"   - {issue}")
            all_ok = False
        else:
            print(f"✅ {filepath}")
    
    if all_ok:
        print("\n✅ All HTML files passed encoding checks!")
        return 0
    else:
        print("\n❌ Some files have encoding issues.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
