import os
import sys
import json
from pathlib import Path

def create_cookie_instructions():
    """Create instructions for getting cookies"""
    instructions = """
=== HOW TO GET INSTAGRAM COOKIES ===

Option 1: Use browser extension (easiest)
1. Install "Get cookies.txt" extension for Chrome/Firefox
2. Log into Instagram in your browser
3. Click the extension and save cookies to "instagram_cookies.txt"
4. Place the file in the bot folder

Option 2: Manual cookie export
1. Open Chrome/Firefox Dev Tools (F12)
2. Go to Application/Storage tab
3. Find Cookies for instagram.com
4. Export as JSON and save as "instagram_cookies.json"

Option 3: Use a test account without 2FA
1. Create a new Instagram account
2. Disable 2FA
3. Use those credentials in .env file
"""

    print(instructions)
    
    # Create template cookies file
    template = """# Netscape HTTP Cookie File
# This is a generated file! Do not edit.
.instagram.com    TRUE    /    FALSE    1735689600    sessionid    72087654141%3ADLIQU383DUqwDR%3A14%3AAYgbRVIDemayhFdCtd7PIBfWzk3vOZqm-0BBdB8edA
.instagram.com    TRUE    /    FALSE    1735689600    ds_user_id    72087654141
.instagram.com    TRUE    /    FALSE    1735689600    csrftoken    5JrQAb5ernVv1MlWmtmAvQgfj7KsT3cB
"""
    
    with open('cookies_template.txt', 'w') as f:
        f.write(template)
    
    print("\n✅ Created cookies_template.txt")
    print("📁 Place your actual cookies in 'instagram_cookies.txt")

if __name__ == "__main__":
    create_cookie_instructions()
