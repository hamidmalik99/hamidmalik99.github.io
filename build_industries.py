#!/usr/bin/env python3
"""Build the industry pages from industries.json.

Usage:  python3 build_industries.py

Writes industries/index.html (the hub) and industries/<slug>/index.html for each
industry. Portfolio examples are looked up by domain in projects.json; blog posts
whose category matches an industry's "blogCategory" are listed on its page.
"""
import json, os, re
from urllib.parse import urlparse
from site_template import head, foot, cta_block, SITE, e

IND = json.load(open('industries.json', encoding='utf-8'))
PROJ = json.load(open('projects.json', encoding='utf-8'))
POSTS = json.load(open('posts.json', encoding='utf-8')) if os.path.exists('posts.json') else []


def host(u):
    return urlparse(u).hostname.replace('www.', '')


BY_HOST = {host(p['u']): p for p in PROJ}


def initials(n):
    return ''.join(w[0] for w in re.sub(r'[^A-Za-z0-9 ]', '', n).split()[:2]).upper()


def project_card(p):
    h = host(p['u'])
    return (f'<a class="card" href="{e(p["u"])}" target="_blank" rel="noopener">'
            f'<div class="thumb"><div class="thumb-fallback" aria-hidden="true"><b>{e(initials(p["n"]))}</b>{e(h)}</div>'
            f'<img data-site="{e(p["u"])}" alt="Screenshot of the {e(p["n"])} website" width="1200" height="750"></div>'
            f'<div class="card-body"><span class="card-meta">{e(p["r"])} · {e(p["c"])}</span><h3>{e(p["n"])}</h3>'
            f'<div class="card-foot"><span>{e(h)}</span><span>Visit site ↗</span></div></div></a>')


def post_card(p):
    return (f'<a class="post-card" href="/blog/{p["slug"]}.html"><div class="post-card-top"><span class="post-cat">{e(p["category"])}</span></div>'
            f'<div class="post-card-body"><span class="card-meta">{e(p["date"])} · {e(p["readTime"])}</span><h3>{e(p["title"])}</h3>'
            f'<p class="card-desc">{e(p["metaDescription"])}</p><span class="post-more">Read article →</span></div></a>')


os.makedirs('industries', exist_ok=True)

for i in IND:
    url = f'{SITE}/industries/{i["slug"]}/'
    projects = []
    for d in i['portfolio']:
        if d in BY_HOST:
            projects.append(BY_HOST[d])
        else:
            print('  note: %s not found in projects.json, skipped' % d)
    posts = [p for p in POSTS if p['category'] == i['blogCategory']]
    ld = [
        {'@context': 'https://schema.org', '@type': 'Service', 'name': i['h1'], 'description': i['metaDescription'],
         'serviceType': 'Website design and SEO', 'url': url,
         'provider': {'@type': 'ProfessionalService', 'name': 'hamidbuilds.dev', 'url': SITE + '/'},
         'audience': {'@type': 'BusinessAudience', 'name': i['navName']}},
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Industries', 'item': SITE + '/industries/'},
            {'@type': 'ListItem', 'position': 3, 'name': i['navName'], 'item': url}]},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': f['question'], 'acceptedAnswer': {'@type': 'Answer', 'text': f['answer']}} for f in i['faq']]},
    ]
    extra = ''.join('<script type="application/ld+json">%s</script>\n' % json.dumps(x, ensure_ascii=False) for x in ld)
    pains = ''.join(f'<div class="pain"><h3>{e(p["title"])}</h3><p>{e(p["text"])}</p></div>' for p in i['problems'])
    incl = ''.join(f'<li>{e(x)}</li>' for x in i['includes'])
    faq = ''.join(f'<details class="faq"><summary>{e(f["question"])}</summary><p>{e(f["answer"])}</p></details>' for f in i['faq'])

    work = ''
    if projects:
        work = f'''
  <section class="section" style="padding-top:24px">
    <div class="wrap">
      <div class="head-row"><div class="section-head"><p class="eyebrow">From the portfolio</p><h2>Sites in this space</h2></div><a class="btn btn-navy" href="/work.html">All projects →</a></div>
      <div class="cards">{"".join(project_card(p) for p in projects)}</div>
    </div>
  </section>'''
    guides = ''
    if posts:
        guides = f'''
  <section class="section section-white">
    <div class="wrap">
      <div class="section-head"><p class="eyebrow">Guides</p><h2>Articles for {e(i["navName"].lower())}</h2></div>
      <div class="post-grid">{"".join(post_card(p) for p in posts[:6])}</div>
    </div>
  </section>'''

    page = head(i['metaTitle'], i['metaDescription'], url, 'website', extra, current='industries')
    page += f'''
<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/industries/">Industries</a><span aria-hidden="true">/</span><span>{e(i["navName"])}</span></nav>
      <p class="eyebrow" style="color:var(--gold-soft)">{e(i["eyebrow"])}</p>
      <h1 style="margin-top:14px">{e(i["h1"])}</h1>
      <p>{e(i["heroSub"])}</p>
      <div class="cta-row" style="margin-top:32px">
        <a class="btn btn-gold btn-lg" href="/#contact">Get a fixed quote →</a>
        <a class="btn btn-ghost btn-lg" href="#how">What's included</a>
      </div>
      <p class="hero-meta" style="margin-top:24px">Working with firms in {e(i["regions"])}</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head"><p class="eyebrow">The problem</p><h2>Where most {e(i["singular"])} websites fall short</h2></div>
      <div class="pains">{pains}</div>
    </div>
  </section>

  <section class="section section-white" id="how">
    <div class="wrap includes">
      <div class="includes-copy">
        <p class="eyebrow">What you get</p>
        <h2>Built around how your clients choose</h2>
        <ul class="ticks">{incl}</ul>
      </div>
      <aside class="includes-side">
        <h3>How it works</h3>
        <ol>
          <li><strong>Fixed quote in 24 hours</strong> from a short call or written brief.</li>
          <li><strong>Built on staging</strong>, so your live site stays untouched.</li>
          <li><strong>Review rounds</strong> turned around overnight.</li>
          <li><strong>Launch and handover</strong>, with an optional care plan.</li>
        </ol>
        <a class="btn btn-gold" href="/#contact">Start with a quote →</a>
      </aside>
    </div>
  </section>
{work}
{guides}
  <section class="section">
    <div class="wrap post-wrap" style="padding:0">
      <div class="faqs" style="margin-top:0"><h2>Questions {e(i["navName"].lower())} ask</h2>{faq}</div>
    </div>
  </section>
{cta_block("Let's talk about your website")}
</main>'''
    page += foot()
    os.makedirs(f'industries/{i["slug"]}', exist_ok=True)
    open(f'industries/{i["slug"]}/index.html', 'w', encoding='utf-8').write(page)

# Hub page
cards = ''.join(f'''<a class="ind-card" href="/industries/{i["slug"]}/"><span class="eyebrow">{e(i["regions"])}</span><h3>{e(i["navName"])}</h3><p>{e(i["cardText"])}</p><span class="post-more">See websites for {e(i["navName"].lower())} →</span></a>''' for i in IND)
ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Industries', 'url': SITE + '/industries/',
      'hasPart': [{'@type': 'WebPage', 'name': i['h1'], 'url': f'{SITE}/industries/{i["slug"]}/'} for i in IND]}
hub = head('Industries I Build Websites For | Hamid Ali Asad',
           'Websites and SEO for engineering firms, fractional CFOs, business brokers, home care agencies and industrial suppliers.',
           SITE + '/industries/', 'website', '<script type="application/ld+json">%s</script>\n' % json.dumps(ld, ensure_ascii=False), current='industries')
hub += f'''
<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow" style="color:var(--gold-soft)">Industries</p>
      <h1 style="margin-top:14px">Websites for firms that <span>sell on trust.</span></h1>
      <p>I work with businesses of every kind, and these are the industries I know best: what their clients look for, what search terms they use, and what their sites need to do.</p>
    </div>
  </section>
  <section class="section" style="padding-top:56px">
    <div class="wrap">
      <div class="ind-grid">{cards}</div>
      <div class="note-box"><p><strong>Don't see your industry?</strong> Most of my 100+ projects are outside these five. Tell me about your business and I'll show you relevant work.</p><a href="/work.html"><strong>Browse all projects →</strong></a></div>
    </div>
  </section>
{cta_block("Not sure where to start?")}
</main>'''
hub += foot()
open('industries/index.html', 'w', encoding='utf-8').write(hub)
print('Built %d industry pages + hub' % len(IND))
