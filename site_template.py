"""Shared header, footer and call-to-action for pages built by the build_*.py scripts."""
import html

SITE = 'https://hamidbuilds.dev'
EMAIL = 'info@hamidbuilds.dev'
WA = 'https://wa.me/923077138743'
e = html.escape

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' "
           "fill='%23E2B04A'/%3E%3Ctext x='32' y='43' text-anchor='middle' font-family='Arial' font-weight='800' font-size='30' "
           "fill='%230B1628'%3Ehb%3C/text%3E%3C/svg%3E")

WA_ICON = ('<svg aria-hidden="true" width="30" height="30" viewBox="0 0 24 24" fill="#fff"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm4.5 12.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.6.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3a.5.5 0 0 0 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.7-1.2 2.2 2.2 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3z"/></svg>')

NAV = [('/#agencies', 'For agencies', None), ('/industries/', 'Industries', 'industries'),
       ('/work.html', 'Work', 'work'), ('/blog/', 'Blog', 'blog'), ('/#about', 'About', None)]


def head(title, desc, url, og_type='website', extra='', current=None):
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if k and k == current else '', t) for h, t, k in NAV)
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
      {nav}
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
    <nav aria-label="Footer"><a href="/">Home</a><a href="/industries/">Industries</a><a href="/work.html">Work</a><a href="/blog/">Blog</a><a href="mailto:{EMAIL}">{EMAIL}</a></nav>
  </div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{WA_ICON}</a>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''


def cta_block(text, sub='Agencies: send me a test project. Business owners: tell me what you need and get a fixed quote within 24 hours.'):
    return f'''
<section class="contact" style="background:transparent;padding:0 0 96px">
  <div class="wrap">
    <div class="contact-card" style="align-items:center">
      <div class="contact-copy">
        <h2>{e(text)}</h2>
        <p>{e(sub)}</p>
      </div>
      <div class="cta-row">
        <a class="btn btn-gold btn-lg" href="/#contact">Get a fixed quote →</a>
        <a class="btn btn-ghost btn-lg" href="{WA}" target="_blank" rel="noopener">WhatsApp me</a>
      </div>
    </div>
  </div>
</section>'''
