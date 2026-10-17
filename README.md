# hamidbuilds.dev

Static portfolio site for Hamid Ali Asad, served by GitHub Pages (custom domain in `CNAME`).

- `index.html` — homepage (agencies + small businesses)
- `work.html` — full portfolio, filterable and searchable
- `projects.json` — the project list. Add a site as `{"n": name, "u": url, "c": category, "g": filter group, "r": region}`, then run `python3 build.py`
- `build.py` — writes every project into `work.html` as plain HTML (crawlable), updates counts and `sitemap.xml`
- `assets/site.js` — screenshots, contact form, testimonials

Screenshots are captured live by WordPress.com mShots and cached after the first view.
Testimonials in `assets/site.js` stay hidden until a quote is marked `approved: true` — only after the client OKs the wording.
