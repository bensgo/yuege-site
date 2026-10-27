#!/usr/bin/env python3
"""Offline static-site SEO checks. Run from any directory; no dependencies."""
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://yuege.online'
MANIFEST = json.loads((ROOT / 'GSO_ENGLISH_TOPICS_2026-10-26.json').read_text())

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.links, self.ids, self.canonicals, self.h1, self.titles = path, [], [], [], [], []
        self.meta, self.schemas, self.errors = {}, [], []
        self.active, self.buffer = None, ''
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a' and 'href' in a: self.links.append(a['href'])
        if tag in ('link', 'img', 'script'):
            target = a.get('src') or a.get('href')
            if target: self.links.append(target)
        if tag == 'link' and a.get('rel') == 'canonical': self.canonicals.append(a.get('href'))
        if tag == 'meta': self.meta.setdefault(a.get('name', a.get('property')), []).append(a.get('content'))
        if tag in ('h1','title') or (tag == 'script' and a.get('type') == 'application/ld+json'):
            self.active, self.buffer = tag, ''
        if tag == 'img' and 'alt' not in a: self.errors.append('image lacks alt')
    def handle_data(self, data):
        if self.active: self.buffer += data
    def handle_endtag(self, tag):
        if tag != self.active: return
        if tag == 'h1': self.h1.append(self.buffer.strip())
        if tag == 'title': self.titles.append(self.buffer.strip())
        if tag == 'script':
            try: self.schemas.append(json.loads(self.buffer))
            except ValueError: self.errors.append('invalid JSON-LD')
        self.active, self.buffer = None, ''

def path_for(url):
    part = unquote(urlsplit(url).path)
    p = ROOT / part.lstrip('/')
    if part.endswith('/') or p.is_dir(): p /= 'index.html'
    return p

pages = {p: Page(p) for p in ROOT.rglob('*.html')}
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
xml = ET.parse(ROOT / 'sitemap.xml')
locations = [n.text for n in xml.findall('s:url/s:loc', ns)]
errors = []
for loc, count in Counter(locations).items():
    if count != 1: errors.append(f'duplicate sitemap URL: {loc}')
    if not path_for(loc).is_file(): errors.append(f'sitemap target missing: {loc}')
# Detect duplicate canonical destinations across every HTML page. Alias/redirect routes
# are reported separately; only genuinely indexable documents count as collisions.
canon = {}
for p, page in pages.items():
    if len(page.canonicals) > 1: errors.append(f'multiple canonical tags: {p.relative_to(ROOT)}')
    if page.canonicals and 'noindex' not in ' '.join(page.meta.get('robots', [])) and 'refresh' not in p.read_text().lower():
        canon.setdefault(page.canonicals[0], []).append(p)
for url, members in canon.items():
    if len(members) > 1: errors.append(f'duplicate indexable canonical: {url}')

scoped = [path_for(a['url']) for a in MANIFEST['articles']]
entry = [ROOT / 'private-moments/index.html', ROOT / 'private-moments/guide/index.html']
link_count = 0
for p in scoped + entry:
    page = pages[p]
    errors += [str(p.relative_to(ROOT)) + ': ' + e for e in page.errors]
    source = ORIGIN + '/' + str(p.relative_to(ROOT)).removesuffix('index.html')
    if page.canonicals != [source]: errors.append(f'canonical is not self-referencing: {source}')
    if len(page.h1) != 1 or len(page.titles) != 1: errors.append(f'expected one H1/title: {source}')
    if len(page.meta.get('description', [])) != 1: errors.append(f'expected one description: {source}')
    if 'noindex' in ' '.join(page.meta.get('robots', [])): errors.append(f'noindex: {source}')
    if source not in locations: errors.append(f'not in sitemap: {source}')
    if source.endswith(tuple('/'+a['url'].split('/')[-2]+'/' for a in MANIFEST['articles'])):
        for other in MANIFEST['articles']:
            if other['url'] != source and urlsplit(other['url']).path not in page.links:
                errors.append(f'missing topic link: {source} -> {other["url"]}')
    for href in page.links:
        url = urljoin(source, href); parts = urlsplit(url)
        if parts.scheme not in ('http','https') or parts.netloc != 'yuege.online': continue
        link_count += 1; target = path_for(url)
        if not target.is_file(): errors.append(f'missing local link: {source} -> {href}')
        elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
            errors.append(f'missing anchor: {source} -> {href}')
for a in MANIFEST['articles']:
    page = pages[path_for(a['url'])]
    if page.titles != [a['title']] or page.h1 != [a['title']]: errors.append(f'manifest title/H1 mismatch: {a["url"]}')
    if page.meta.get('description') != [a['meta_description']]: errors.append(f'manifest description mismatch: {a["url"]}')
    if not any('apps.apple.com/us/app/id6812803369' in link for link in page.links): errors.append('missing App Store CTA')
    for key in ['og:title','og:description','og:url','og:image','twitter:card']:
        if len(page.meta.get(key, [])) != 1: errors.append(f'missing/duplicate {key}: {a["url"]}')
    if page.meta.get('og:url') != [a['url']]: errors.append('OG URL mismatch')
    article = [x for x in page.schemas if x.get('@type') == 'Article']
    if len(article) != 1 or article[0].get('headline') != a['title'] or article[0].get('mainEntityOfPage') != a['url']:
        errors.append(f'Article mismatch: {a["url"]}')
    if not any(x.get('@type') == 'BreadcrumbList' for x in page.schemas): errors.append('missing breadcrumb schema')
    for obj in page.schemas:
        if any(k in json.dumps(obj) for k in ['aggregateRating','"Review"','"FAQPage"']): errors.append('unexpected review/rating/FAQ schema')
    text = path_for(a['url']).read_text()
    if 'Frequently asked questions' not in text or '<ol>' not in text: errors.append('missing FAQ/tutorial')
    if 'Written by the Hide Photos developer' not in text: errors.append('missing developer disclosure')
for p in entry:
    for a in MANIFEST['articles']:
        if urlsplit(a['url']).path not in pages[p].links: errors.append(f'entry page lacks topic: {p}')
if len({a['title'] for a in MANIFEST['articles']}) != 6: errors.append('duplicate topic title')
if len({a['meta_description'] for a in MANIFEST['articles']}) != 6: errors.append('duplicate topic description')
# Full-site links are read-only checks, including other products; no files are changed.
site_link_count = 0
for p, page in pages.items():
    source = ORIGIN + '/' + str(p.relative_to(ROOT)).removesuffix('index.html')
    for href in page.links:
        url = urljoin(source, href); parts = urlsplit(url)
        if parts.scheme not in ('http', 'https') or parts.netloc != 'yuege.online': continue
        site_link_count += 1; target = path_for(url)
        if not target.is_file(): errors.append(f'missing site link: {source} -> {href}')
        elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
            errors.append(f'missing site anchor: {source} -> {href}')
print(f'Parsed {len(pages)} HTML documents; {len(locations)} sitemap URLs; {len(scoped)} topic pages + {len(entry)} entry pages; {link_count} changed-page local references and {site_link_count} full-site local references checked.')
print('Canonical collision scan covers all indexable HTML; content checks cover changed English pages; links and anchors cover all HTML pages.')
if errors:
    print('\n'.join('FAIL: '+e for e in errors)); raise SystemExit(1)
print('PASS: titles, H1s, descriptions, canonical uniqueness, sitemap targets, topic mutual links, anchors, assets, Open Graph, JSON-LD, tutorials, FAQs, disclosure and App Store CTAs.')
