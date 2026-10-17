#!/usr/bin/env python3
"""Build the blog from posts.json.

Usage:  pip install markdown   (once)
        python3 build_blog.py

Writes blog/index.html and one page per post at blog/<slug>.html, plain HTML so
search engines can read every word. Each post in posts.json needs: slug, title,
metaTitle, metaDescription, category, date ("February 2026"), readTime, featured,
geoDirectAnswer, keyTakeaways[], contentMarkdown, faq[{question, answer}], ctaText, tags[].
"""
import json, html, re, datetime, os
import markdown

SITE = 'https://hamidbuilds.dev'
EMAIL = 'info@hamidbuilds.dev'
WA = 'https://wa.me/923077138743'
e = html.escape
POSTS = json.load(open('posts.json', encoding='utf-8'))
os.makedirs('blog', exist_ok=True)

MONTHS = {m: i for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                       'August', 'September', 'October', 'November', 'December'], 1)}


def iso(d):
    m, y = d.split()
    return '%s-%02d-01' % (y, MONTHS[m])


POSTS.sort(key=lambda p: iso(p['date']), reverse=True)

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' "
           "fill='%23E2B04A'/%3E%3Ctext x='32' y='43' text-anchor='middle' font-family='Arial' font-weight='800' font-size='30' "
           "fill='%230B1628'%3Ehb%3C/text%3E%3C/svg%3E")

WA_ICON = ('<svg aria-hidden="true" width="30" height="30" viewBox="0 0 24 24" fill="#fff"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm4.5 12.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.6.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3a.5.5 0 0 0 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.7-1.2 2.2 2.2 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3z"/></svg>')


def head(title, desc, url, og_type='website', extra=''):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Hamid Ali Asad">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="hamidbuilds.dev">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/assets/og-image.png">
<meta name="theme-color" content="#0B1628">
<link rel="icon" href="{FAVICON}">
<link rel="alternate" type="application/rss+xml" title="hamidbuilds.dev blog" href="{SITE}/blog/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="hamidbuilds.dev home">
      <span class="brand-mark" aria-hidden="true">hb</span>
      <span class="brand-name">hamidbuilds<span>.dev</span></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
      <svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <a href="/#agencies">For agencies</a>
      <a href="/#businesses">For businesses</a>
      <a href="/work.html">Work</a>
      <a href="/blog/" aria-current="page">Blog</a>
      <a href="/#about">About</a>
      <a class="btn btn-gold" href="/#contact">Get a quote</a>
    </nav>
  </div>
</header>
'''


def foot():
    return f'''
<footer class="site-footer">
  <div class="wrap">
    <span>© <span id="year">2026</span> Hamid Ali Asad · hamidbuilds.dev · Lahore, Pakistan</span>
    <nav aria-label="Footer"><a href="/">Home</a><a href="/work.html">Work</a><a href="/blog/">Blog</a><a href="mailto:{EMAIL}">{EMAIL}</a></nav>
  </div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{WA_ICON}</a>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''


def cta_block(text):
    return f'''
<section class="contact" style="background:transparent;padding:0 0 96px">
  <div class="wrap">
    <div class="contact-card" style="align-items:center">
      <div class="contact-copy">
        <h2>{e(text)}</h2>
        <p>Agencies: send me a test project. Business owners: tell me what you need and get a fixed quote within 24 hours.</p>
      </div>
      <div class="cta-row">
        <a class="btn btn-gold btn-lg" href="/#contact">Start a project →</a>
        <a class="btn btn-ghost btn-lg" href="{WA}" target="_blank" rel="noopener">WhatsApp me</a>
      </div>
    </div>
  </div>
</section>'''


def post_card(p, big=False):
    cls = 'post-card post-card-big' if big else 'post-card'
    return (f'<a class="{cls}" href="/blog/{p["slug"]}.html" data-cat="{e(p["category"])}">'
            f'<div class="post-card-top"><span class="post-cat">{e(p["category"])}</span></div>'
            f'<div class="post-card-body"><span class="card-meta">{e(p["date"])} · {e(p["readTime"])}</span>'
            f'<h3>{e(p["title"])}</h3><p class="card-desc">{e(p["metaDescription"])}</p>'
            f'<span class="post-more">Read article →</span></div></a>')


def render_md(md):
    out = markdown.markdown(md, extensions=['tables', 'fenced_code', 'sane_lists'])
    # Article title is the page H1, so shift the markdown headings down one step
    out = re.sub(r'<(/?)h4>', r'<\1h3>', re.sub(r'<(/?)h3>', r'<\1h2>', out))
    out = out.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')
    return out


# ---------- Post pages ----------
for idx, p in enumerate(POSTS):
    url = f'{SITE}/blog/{p["slug"]}.html'
    ld = [
        {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'], 'description': p['metaDescription'],
         'datePublished': iso(p['date']), 'dateModified': iso(p['date']), 'mainEntityOfPage': url,
         'image': SITE + '/assets/og-image.png', 'keywords': ', '.join(p['tags']), 'articleSection': p['category'],
         'author': {'@type': 'Person', 'name': 'Hamid Ali Asad', 'url': SITE + '/#about'},
         'publisher': {'@type': 'Organization', 'name': 'hamidbuilds.dev', 'url': SITE}},
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': SITE + '/blog/'},
            {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': url}]},
    ]
    if p['faq']:
        ld.append({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': f['question'], 'acceptedAnswer': {'@type': 'Answer', 'text': f['answer']}} for f in p['faq']]})
    extra = ''.join('<script type="application/ld+json">%s</script>\n' % json.dumps(x, ensure_ascii=False) for x in ld)

    takeaways = ''.join(f'<li>{e(k)}</li>' for k in p['keyTakeaways'])
    faq = ''.join(f'<details class="faq"><summary>{e(f["question"])}</summary><p>{e(f["answer"])}</p></details>' for f in p['faq'])
    tags = ''.join(f'<span class="chip">{e(t)}</span>' for t in p['tags'])
    related = [q for q in POSTS if q['slug'] != p['slug']][:3]

    page = head(p['metaTitle'], p['metaDescription'], url, 'article', extra)
    page += f'''
<main id="main">
  <article>
    <header class="page-hero post-hero">
      <div class="wrap post-wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/blog/">Blog</a><span aria-hidden="true">/</span><span>{e(p["category"])}</span></nav>
        <p class="post-cat post-cat-dark">{e(p["category"])}</p>
        <h1>{e(p["title"])}</h1>
        <div class="byline">
          <img src="/assets/hamid-480.webp" alt="" width="44" height="44">
          <span><strong>Hamid Ali Asad</strong><small><time datetime="{iso(p["date"])}">{e(p["date"])}</time> · {e(p["readTime"])}</small></span>
        </div>
      </div>
    </header>
    <div class="wrap post-wrap post-body">
      <aside class="answer-box" aria-label="Short answer">
        <p class="eyebrow">The short answer</p>
        <p>{e(p["geoDirectAnswer"])}</p>
      </aside>
      <section class="takeaways" aria-label="Key takeaways">
        <h2>Key takeaways</h2>
        <ul class="ticks">{takeaways}</ul>
      </section>
      <div class="prose">
{render_md(p["contentMarkdown"])}
      </div>
      {"<section class='faqs'><h2>Frequently asked questions</h2>" + faq + "</section>" if faq else ""}
      <div class="chips post-tags">{tags}</div>
      <div class="author-box">
        <img src="/assets/hamid-480.webp" alt="Hamid Ali Asad" width="72" height="72" loading="lazy">
        <div><strong>Written by Hamid Ali Asad</strong><p>WordPress developer and SEO specialist with 5+ years of experience, building sites for agencies and small businesses across Australia, the UK and the US.</p><a href="/#about">More about Hamid →</a></div>
      </div>
    </div>
  </article>
  <section class="section" style="padding-top:24px">
    <div class="wrap">
      <div class="head-row"><div class="section-head"><p class="eyebrow">Keep reading</p><h2>More from the blog</h2></div><a class="btn btn-navy" href="/blog/">All articles →</a></div>
      <div class="post-grid">{"".join(post_card(q) for q in related)}</div>
    </div>
  </section>
{cta_block(p["ctaText"])}
</main>'''
    page += foot()
    open(f'blog/{p["slug"]}.html', 'w', encoding='utf-8').write(page)

# ---------- Blog index ----------
featured = next((p for p in POSTS if p.get('featured')), POSTS[0])
rest = [p for p in POSTS if p is not featured]
cats = []
for p in POSTS:
    if p['category'] not in cats:
        cats.append(p['category'])
tabs = '<button class="tab" type="button" data-cat="All" aria-pressed="true">All<small>%d</small></button>' % len(POSTS)
tabs += ''.join('<button class="tab" type="button" data-cat="%s" aria-pressed="false">%s<small>%d</small></button>' % (
    e(c), e(c), sum(1 for p in POSTS if p['category'] == c)) for c in cats)
ld = {'@context': 'https://schema.org', '@type': 'Blog', 'name': 'hamidbuilds.dev blog', 'url': SITE + '/blog/',
      'author': {'@type': 'Person', 'name': 'Hamid Ali Asad'},
      'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': f'{SITE}/blog/{p["slug"]}.html',
                    'datePublished': iso(p['date'])} for p in POSTS]}
idx = head('Blog — WordPress, SEO & Automation Guides | Hamid Ali Asad',
           'Practical guides on WordPress performance, WooCommerce, SEO for AI search, and lead automation from Hamid Ali Asad.',
           SITE + '/blog/', 'website', '<script type="application/ld+json">%s</script>\n' % json.dumps(ld, ensure_ascii=False))
idx += f'''
<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow" style="color:var(--gold-soft)">Blog</p>
      <h1 style="margin-top:14px">Guides for faster sites and <span>more enquiries.</span></h1>
      <p>WordPress performance, WooCommerce, SEO for AI search and lead automation, written for agencies and business owners.</p>
    </div>
  </section>
  <section class="section" style="padding-top:56px">
    <div class="wrap">
      {post_card(featured, big=True)}
      <div class="tabs blog-tabs" id="blog-tabs" role="group" aria-label="Filter by topic">{tabs}</div>
      <div class="post-grid" id="post-grid">{"".join(post_card(p) for p in POSTS)}</div>
    </div>
  </section>
{cta_block("Need help with your website?")}
</main>
<script>
(function(){{
  var tabs=[].slice.call(document.querySelectorAll('#blog-tabs .tab'));
  var cards=[].slice.call(document.querySelectorAll('#post-grid .post-card'));
  tabs.forEach(function(t){{t.addEventListener('click',function(){{
    var c=t.getAttribute('data-cat');
    tabs.forEach(function(x){{x.setAttribute('aria-pressed',x===t?'true':'false');}});
    cards.forEach(function(k){{k.hidden=!(c==='All'||k.getAttribute('data-cat')===c);}});
  }});}});
}})();
</script>'''
idx += foot()
open('blog/index.html', 'w', encoding='utf-8').write(idx)

# ---------- RSS feed ----------
items = ''.join(f'''<item><title>{e(p["title"])}</title><link>{SITE}/blog/{p["slug"]}.html</link><guid>{SITE}/blog/{p["slug"]}.html</guid><pubDate>{datetime.datetime.fromisoformat(iso(p["date"])).strftime("%a, %d %b %Y 00:00:00 +0000")}</pubDate><description>{e(p["metaDescription"])}</description></item>''' for p in POSTS)
open('blog/feed.xml', 'w', encoding='utf-8').write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>hamidbuilds.dev blog</title><link>{SITE}/blog/</link><description>WordPress, SEO and automation guides by Hamid Ali Asad</description>{items}</channel></rss>\n')

# ---------- Old URL redirect ----------
open('blog.html', 'w').write(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Blog moved — hamidbuilds.dev</title>
<link rel="canonical" href="{SITE}/blog/"><meta name="robots" content="noindex, follow">
<script>var h=location.hash.slice(1);location.replace(h?'/blog/'+h+'.html':'/blog/');</script>
<meta http-equiv="refresh" content="0; url=/blog/"></head>
<body><p>The blog has moved to <a href="/blog/">hamidbuilds.dev/blog/</a>.</p></body></html>
''')
print('Built blog: %d posts' % len(POSTS))
