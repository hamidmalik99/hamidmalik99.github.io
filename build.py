#!/usr/bin/env python3
"""Regenerate the portfolio from projects.json.

Usage:  python3 build.py

Adds every project in projects.json to work.html as plain HTML (so search engines
can read it), updates the project counts on both pages, and refreshes sitemap.xml.
Each project: {"n": name, "u": url, "c": category, "g": filter group, "r": region}
"""
import json, re, html, datetime
from urllib.parse import urlparse
from collections import Counter

SITE = 'https://hamidbuilds.dev'
ORDER = ['Trades & Construction', 'Legal & Professional', 'Property & Travel', 'Healthcare',
         'E-commerce', 'Industrial & Energy', 'Tech & Telecom', 'Media & Marketing', 'Nonprofit & Education']

P = json.load(open('projects.json', encoding='utf-8'))
e = html.escape


def host(u):
    return urlparse(u).hostname.replace('www.', '')


def initials(n):
    words = re.sub(r'[^A-Za-z0-9 ]', '', n).split()
    return ''.join(w[0] for w in words[:2]).upper()


def slot(s, name, content):
    return re.sub(r'(<!-- %s:START -->).*?(<!-- %s:END -->)' % (name, name),
                  lambda m: m.group(1) + content + m.group(2), s, flags=re.S)


cards = []
for p in P:
    h = host(p['u'])
    cards.append(
        '\n<a class="card" href="%s" target="_blank" rel="noopener" data-group="%s" data-search="%s">'
        '<div class="thumb"><div class="thumb-fallback" aria-hidden="true"><b>%s</b>%s</div>'
        '<img data-site="%s" alt="Screenshot of the %s website" width="1200" height="750"></div>'
        '<div class="card-body"><span class="card-meta">%s · %s</span><h3>%s</h3>'
        '<div class="card-foot"><span>%s</span><span>Visit site ↗</span></div></div></a>' % (
            e(p['u']), e(p['g']), e((p['n'] + ' ' + p['c'] + ' ' + p['g'] + ' ' + p['r'] + ' ' + h).lower()),
            e(initials(p['n'])), e(h), e(p['u']), e(p['n']), e(p['r']), e(p['c']), e(p['n']), e(h)))

groups = Counter(p['g'] for p in P)
tabs = ['<button class="tab" type="button" data-group="All" aria-pressed="true">All<small>%d</small></button>' % len(P)]
for g in ORDER:
    if groups[g]:
        tabs.append('<button class="tab" type="button" data-group="%s" aria-pressed="false">%s<small>%d</small></button>' % (e(g), e(g), groups[g]))

regions = Counter(p['r'] for p in P)
reg = ''.join('<span><b>%d</b> %s</span>' % (n, e(r)) for r, n in regions.most_common())

ld = {
    '@context': 'https://schema.org', '@type': 'CollectionPage',
    'name': 'Portfolio — Hamid Ali Asad', 'url': SITE + '/work.html',
    'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(P), 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': p['n'], 'url': p['u']} for i, p in enumerate(P)]}
}
ldtxt = '\n<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n'

w = open('work.html', encoding='utf-8').read()
w = slot(w, 'PROJECTS', ''.join(cards) + '\n')
w = slot(w, 'TABS', ''.join(tabs))
w = slot(w, 'REGIONS', reg)
w = slot(w, 'RESULTS', '%d projects' % len(P))
w = slot(w, 'LDJSON', ldtxt)
w = re.sub(r'(data-project-count>)[^<]*(<)', r'\g<1>%d\2' % len(P), w)
open('work.html', 'w', encoding='utf-8').write(w)

i = open('index.html', encoding='utf-8').read()
i = re.sub(r'(data-project-count>)[^<]*(<)', r'\g<1>%d\2' % len(P), i)
open('index.html', 'w', encoding='utf-8').write(i)

today = datetime.date.today().isoformat()
urls = [('/', '1.0'), ('/work.html', '0.8'), ('/industries/', '0.8')] + [('/industries/%s/' % q['slug'], '0.8') for q in json.load(open('industries.json', encoding='utf-8'))] + [('/blog/', '0.7')] + [('/blog/%s.html' % q['slug'], '0.6') for q in json.load(open('posts.json', encoding='utf-8'))]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += ''.join('  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n' % (SITE, u, today, pr) for u, pr in urls)
sm += '</urlset>\n'
open('sitemap.xml', 'w').write(sm)
print('Built %d projects' % len(P))
