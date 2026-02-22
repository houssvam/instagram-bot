import os

def create_cookie_file():
    """Create cookies file with proper tab separation"""
    
    # Your cookie values (from your browser)
    cookies = [
        {
            'domain': '.instagram.com',
            'include_subdomains': 'TRUE',
            'path': '/',
            'secure': 'FALSE',
            'expiry': '1735689600',
            'name': 'sessionid',
            'value': '72087654141%3ADLIQU383DUqwDR%3A14%3AAYgbRVIDemayhFdCtd7PIBfWzk3vOZqm-0BBdB8edA'
        }
    ]
    
    # Create file with proper tab separation
    with open('instagram_cookies.txt', 'w', encoding='ascii') as f:
        f.write('# Netscape HTTP Cookie File\n')
        
        for cookie in cookies:
            # Join with actual tabs
            line = '\t'.join([
                cookie['domain'],
                cookie['include_subdomains'],
                cookie['path'],
                cookie['secure'],
                cookie['expiry'],
                cookie['name'],
                cookie['value']
            ])
            f.write(line + '\n')
    
    print("✅ Cookies file created with tabs!")
    
    # Verify the file
    print("\nVerifying file content:")
    print("-" * 50)
    with open('instagram_cookies.txt', 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[1:], 2):  # Skip header
            if '\t' in line:
                parts = line.split('\t')
                print(f"Line {i}: ✅ Has {len(parts)} tab-separated fields")
                print(f"  Cookie: {parts[5]} = {parts[6][:30]}...")
            else:
                print(f"Line {i}: ❌ No tabs found")

if __name__ == "__main__":
    create_cookie_file()
