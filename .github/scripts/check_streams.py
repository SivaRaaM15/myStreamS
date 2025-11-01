#!/usr/bin/env python3
import requests
import re
import time
from urllib.parse import urlparse

def check_streams():
    print("🔍 Starting stream validation...")
    
    try:
        with open('sivarenu.m3u', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ Error: sivarenu.m3u file not found!")
        return
    
    # Extract URLs from the M3U file
    urls = re.findall(r'^https?://[^\s]+$', content, re.MULTILINE)
    
    if not urls:
        print("❌ No URLs found in the playlist!")
        return
    
    print(f"📊 Found {len(urls)} URLs to check...")
    print("-" * 50)
    
    working_urls = []
    failed_urls = []
    
    for i, url in enumerate(urls, 1):
        print(f"Checking {i}/{len(urls)}: {url[:80]}...")
        
        try:
            # Use a shorter timeout and only get headers to save time
            response = requests.head(
                url, 
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                allow_redirects=True
            )
            
            if response.status_code in [200, 301, 302]:
                working_urls.append(url)
                print(f"   ✅ Working (Status: {response.status_code})")
            else:
                failed_urls.append((url, f"Status: {response.status_code}"))
                print(f"   ❌ Failed (Status: {response.status_code})")
                
        except requests.exceptions.Timeout:
            failed_urls.append((url, "Timeout"))
            print(f"   ❌ Timeout")
        except requests.exceptions.ConnectionError:
            failed_urls.append((url, "Connection Error"))
            print(f"   ❌ Connection Error")
        except requests.exceptions.RequestException as e:
            failed_urls.append((url, str(e)))
            print(f"   ❌ Error: {e}")
        
        # Small delay to be respectful to servers
        time.sleep(1)
    
    print("-" * 50)
    print(f"📈 RESULTS:")
    print(f"✅ Working URLs: {len(working_urls)}")
    print(f"❌ Failed URLs: {len(failed_urls)}")
    
    if failed_urls:
        print("\n🔴 Failed URLs:")
        for url, reason in failed_urls:
            print(f"   - {url}")
            print(f"     Reason: {reason}")
    
    # Calculate success rate
    if urls:
        success_rate = (len(working_urls) / len(urls)) * 100
        print(f"📊 Success Rate: {success_rate:.1f}%")
    
    # Exit with error if too many URLs failed
    if len(failed_urls) > len(urls) * 0.5:  # If more than 50% failed
        print("🚨 Too many streams are failing!")
        exit(1)

if __name__ == "__main__":
    check_streams()