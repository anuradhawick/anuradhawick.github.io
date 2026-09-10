import os
import re
import json
import xml.etree.ElementTree as ET

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML_PATH = os.path.join(WORKSPACE_DIR, 'anuradhawickramarachchi.WordPress.2026-09-10.xml')
BLOG_DIR = os.path.join(WORKSPACE_DIR, 'src', 'content', 'blog')
os.makedirs(BLOG_DIR, exist_ok=True)

tree = ET.parse(XML_PATH)
root = tree.getroot()
channel = root.find('channel')
namespaces = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/'
}

def clean_html_to_markdown(content):
    # If jetpack markdown source exists in comments, extract that directly
    jetpack_match = re.search(r'<!-- wp:jetpack/markdown (\{.*?\}) -->', content)
    if jetpack_match:
        try:
            data = json.loads(jetpack_match.group(1))
            if 'source' in data:
                return data['source']
        except Exception:
            pass

    # Replace local image URLs
    content = re.sub(r'https?://anuradhawick\.com/wp-content/uploads/\d{4}/\d{2}/([^\"\'\s\?\>]+)(\?[^\"\'\s\>]*)?', r'/assets/uploads/\1', content)
    
    # Remove Gutenberg comments
    content = re.sub(r'<!-- /?wp:[^>]*-->', '', content)

    # Convert figures with images and captions
    def replace_figure(m):
        fig_content = m.group(1)
        img_src = ''
        img_alt = ''
        caption = ''
        link = ''
        
        link_m = re.search(r'<a\s+[^>]*href=[\"\'](.*?)[\"\'][^>]*>', fig_content)
        if link_m:
            link = link_m.group(1)

        img_m = re.search(r'<img\s+[^>]*src=[\"\'](.*?)[\"\'](?:[^>]*alt=[\"\'](.*?)[\"\'])?[^>]*>', fig_content)
        if img_m:
            img_src = img_m.group(1)
            img_alt = img_m.group(2) or ''

        cap_m = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', fig_content, re.DOTALL)
        if cap_m:
            caption = re.sub(r'<[^>]+>', '', cap_m.group(1)).strip()

        if link and img_src:
            out = f"[![{img_alt or caption}]({img_src})]({link})"
        elif img_src:
            out = f"![{img_alt or caption}]({img_src})"
        else:
            out = ''
        if caption:
            out += f"\n\n*{caption}*"
        return out

    content = re.sub(r'<figure[^>]*>(.*?)</figure>', replace_figure, content, flags=re.DOTALL)

    # Convert headings
    content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', content)
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', content)
    content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', content)
    content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', content)

    # Convert blockquotes
    content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: '\n'.join(['> ' + line.strip() for line in re.sub(r'<[^>]+>', '', m.group(1)).split('\n') if line.strip()]), content, flags=re.DOTALL)

    # Convert pre / code
    content = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', r'```\n\1\n```', content, flags=re.DOTALL)
    content = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```', content, flags=re.DOTALL)

    # Convert unordered lists
    content = re.sub(r'<ul[^>]*>(.*?)</ul>', lambda m: '\n' + '\n'.join(['- ' + re.sub(r'<[^>]+>', '', li).strip() for li in re.findall(r'<li[^>]*>(.*?)</li>', m.group(1), re.DOTALL)]) + '\n', content, flags=re.DOTALL)

    # Convert links
    content = re.sub(r'<a\s+[^>]*href=[\"\'](.*?)[\"\'][^>]*>(.*?)</a>', r'[\2](\1)', content)

    # Convert paragraphs
    content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)

    # Clean residual tags and HTML entities
    content = re.sub(r'<[^>]+>', '', content)
    content = content.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&#8211;', '-').replace('&#8217;', "'").replace('&#8220;', '"').replace('&#8221;', '"')

    # Trim multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content).strip()
    return content

items = channel.findall('item')
for item in items:
    pt = item.find('wp:post_type', namespaces).text
    if pt != 'post':
        continue

    title = item.find('title').text or 'Untitled'
    slug = item.find('wp:post_name', namespaces).text
    status = item.find('wp:status', namespaces).text
    post_date = item.find('wp:post_date', namespaces).text or '2022-01-01 00:00:00'
    pub_date = post_date.split(' ')[0]
    
    if not slug:
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')

    categories = [c.text for c in item.findall('category') if c.attrib.get('domain') == 'category']
    tags = [c.text for c in item.findall('category') if c.attrib.get('domain') == 'post_tag']
    raw_content = item.find('content:encoded', namespaces).text or ''

    # Find hero image if available
    hero_img = ''
    img_match = re.search(r'https?://anuradhawick\.com/wp-content/uploads/\d{4}/\d{2}/([^\"\'\s\?\>]+)', raw_content)
    if img_match:
        hero_img = f"/assets/uploads/{img_match.group(1)}"

    markdown_body = clean_html_to_markdown(raw_content)

    # Create description excerpt
    desc_match = re.sub(r'\[.*?\]\(.*?\)', '', markdown_body)
    desc_lines = [line.strip() for line in desc_match.split('\n') if line.strip() and not line.strip().startswith('!') and not line.strip().startswith('#')]
    desc = desc_lines[0] if desc_lines else f"{title} - Article by Anuradha Wickramarachchi"
    desc = re.sub(r'\"', '\\\"', desc[:160])

    is_draft = (status != 'publish')

    frontmatter = f"""---
title: "{title.replace('"', '\\"')}"
description: "{desc}"
pubDate: {pub_date}
heroImage: "{hero_img}"
tags: {json.dumps(tags)}
categories: {json.dumps(categories)}
draft: {str(is_draft).lower()}
---

{markdown_body}
"""

    target_file = os.path.join(BLOG_DIR, f"{slug}.md")
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
    print(f"Generated {slug}.md (draft={is_draft})")

print("Content migration script completed.")
