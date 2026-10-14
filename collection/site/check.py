#!/usr/bin/env python3
"""Smoke-check generated HTML, local paths, metadata and the sitemap."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set(); self.canonical=[]; self.description=[]; self.h1=0; self.title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='title':self.title=True
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href',''))
        if tag=='meta' and a.get('name')=='description':self.description.append(a.get('content',''))
        for name in ['href','src','poster','data-preview','data-poster','data-link']:
            if a.get(name): self.links.append(a[name])

pages={}
for file in OUT.rglob('*.html'):
    verification = ROOT / 'site/public' / file.name
    if file.parent == OUT and file.name.startswith('google') and verification.is_file():
        assert file.read_bytes() == verification.read_bytes(), 'Verification file was changed'
        continue
    page=Page();page.feed(file.read_text());pages[file.resolve()]=page
errors=[]
for file,page in pages.items():
    if page.h1!=1 or not page.title or len(page.canonical)!=1 or not page.description:
        errors.append(f'Missing/duplicate page metadata: {file}')
    for href in page.links:
        url=urlsplit(href)
        if url.scheme or url.netloc:continue
        target=(file.parent/unquote(url.path)).resolve() if url.path else file
        if target.is_dir():target=target/'index.html'
        if not target.is_file():errors.append(f'{file.relative_to(OUT)}: missing {href}')
        elif url.fragment and target in pages and url.fragment not in pages[target].ids:
            errors.append(f'{file.relative_to(OUT)}: missing anchor {href}')
canonicals=[p.canonical[0] for f,p in pages.items() if f.name!='404.html']
if len(canonicals)!=len(set(canonicals)):errors.append('Duplicate canonicals')
xml=ET.parse(OUT/'sitemap.xml')
locations=[e.text for e in xml.findall('.//{*}loc')]
if set(locations)!=set(canonicals):errors.append('Sitemap does not match indexable pages')
for case in json.loads((ROOT/'data/videos.json').read_text()):
    if not (ROOT/'prompts'/(case['id']+'.md')).is_file():errors.append('Missing repository prompt '+case['id'])
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} HTML pages, {len(locations)} sitemap entries, metadata, local assets, links and anchors.')
