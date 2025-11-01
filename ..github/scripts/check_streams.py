import requests
import re

with open('sivarenu.m3u', 'r') as f:
    content = f.read()

urls = re.findall(r'^http.*$', content, re.MULTILINE)
print(f"Found {len(urls)} URLs to check...")

working_urls = []
for url in urls:
    try:
        response = requests.head(url, timeout=10)
        if response.status_code == 200:
            working_urls.append(url)
            print(f"✅ {url}")
        else:
            print(f"❌ {url} - Status: {response.status_code}")
    except:
        print(f"❌ {url} - Failed to connect")

print(f"\nWorking: {len(working_urls)}/{len(urls)}")