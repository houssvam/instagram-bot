import os
import re

def check_cookie_file(filename):
    if not os.path.exists(filename):
        print(f"❌ File {filename} not found")
        return
    
    print(f"Checking {filename}:")
    print("-" * 50)
    
    with open(filename, 'r', encoding='ascii') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Check if tabs are used
        if '\t' not in line:
            print(f"❌ Line {i+1}: No tabs found - using spaces instead")
        else:
            parts = line.split('\t')
            if len(parts) == 7:
                print(f"✅ Line {i+1}: Correct format with {len(parts)} fields")
                print(f"   Domain: {parts[0]}")
                print(f"   Cookie: {parts[5]} = {parts[6][:20]}...")
            else:
                print(f"❌ Line {i+1}: Wrong number of fields: {len(parts)} (should be 7)")

if __name__ == "__main__":
    check_cookie_file('instagram_cookies.txt')
