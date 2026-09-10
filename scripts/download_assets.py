import os
import re
import urllib.request
import xml.etree.ElementTree as ET

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML_PATH = os.path.join(WORKSPACE_DIR, 'anuradhawickramarachchi.WordPress.2026-09-10.xml')
ASSETS_DIR = os.path.join(WORKSPACE_DIR, 'public', 'assets', 'uploads')
WP_CONTENT_DIR = os.path.join(WORKSPACE_DIR, 'public', 'wp-content', 'uploads')

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(WP_CONTENT_DIR, exist_ok=True)

tree = ET.parse(XML_PATH)
root = tree.getroot()
namespaces = {'wp': 'http://wordpress.org/export/1.2/'}

urls = []
for item in root.findall('.//item'):
    if item.find('wp:post_type', namespaces).text == 'attachment':
        u = item.find('wp:attachment_url', namespaces).text
        if u:
            urls.append(u)

# Also check for any URLs in post content that might have query strings or variations
content_namespaces = {'wp': 'http://wordpress.org/export/1.2/', 'content': 'http://purl.org/rss/1.0/modules/content/'}
for item in root.findall('.//item'):
    content = item.find('content:encoded', content_namespaces).text or ''
    matches = re.findall(r'https?://anuradhawick\.com/wp-content/uploads/[^\s\"\'\<\>]+', content)
    for m in matches:
        clean_m = m.split('?')[0]
        if clean_m not in urls:
            urls.append(clean_m)

print(f"Total unique assets to download: {len(urls)}")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for url in urls:
    clean_url = url.split('?')[0]
    # url pattern: https://anuradhawick.com/wp-content/uploads/YYYY/MM/filename
    rel_path = clean_url.replace('https://anuradhawick.com/wp-content/uploads/', '')
    filename = os.path.basename(clean_url)
    
    # Save to public/assets/uploads/filename
    target_asset = os.path.join(ASSETS_DIR, filename)
    
    # Also save to public/wp-content/uploads/YYYY/MM/filename for full backward compatibility
    target_wp = os.path.join(WP_CONTENT_DIR, rel_path)
    os.makedirs(os.path.dirname(target_wp), exist_ok=True)

    if os.path.exists(target_asset) and os.path.getsize(target_asset) > 0:
        print(f"Already exists: {filename}")
        if not os.path.exists(target_wp):
            import shutil
            shutil.copy2(target_asset, target_wp)
        continue

    print(f"Downloading {clean_url} ...")
    req = urllib.request.Request(clean_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(target_asset, 'wb') as f:
                f.write(data)
            with open(target_wp, 'wb') as f:
                f.write(data)
            print(f"Downloaded: {filename} ({len(data)} bytes)")
    except Exception as e:
        print(f"Error downloading {clean_url}: {e}")

print("Asset sync complete.")
