(function () {
  // ---- Mobile nav ----
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
    });
  }

  // ---- Live website screenshots (WordPress.com mShots) ----
  // Screenshots are captured on first request and cached by the service.
  // If the service is still generating, it returns a small placeholder; we retry a few times.
  var SHOT_W = 1200, SHOT_H = 750;
  function shotUrl(site, bust) {
    return 'https://s0.wp.com/mshots/v1/' + encodeURIComponent(site) + '?w=' + SHOT_W + '&h=' + SHOT_H + (bust ? '&r=' + bust : '');
  }
  window.loadShot = function (img) {
    var site = img.getAttribute('data-site');
    if (!site) return;
    var tries = 0;
    img.addEventListener('load', function () {
      if (img.naturalWidth && img.naturalWidth < SHOT_W && tries < 4) {
        tries++;
        setTimeout(function () { img.src = shotUrl(site, Date.now()); }, 3500 * tries);
      } else {
        img.classList.add('ready');
        var fb = img.parentNode.querySelector('.thumb-fallback');
        if (fb) fb.remove();
      }
    });
    img.addEventListener('error', function () { img.remove(); });
    img.src = shotUrl(site);
  };
  function initShots(root) {
    var imgs = (root || document).querySelectorAll('img[data-site]:not([src])');
    if (!('IntersectionObserver' in window)) { imgs.forEach(window.loadShot); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { io.unobserve(en.target); window.loadShot(en.target); }
      });
    }, { rootMargin: '300px' });
    imgs.forEach(function (i) { io.observe(i); });
  }
  window.initShots = initShots;
  initShots();

  // ---- Project count ----
  if (window.PROJECTS) {
    document.querySelectorAll('[data-project-count]').forEach(function (el) {
      el.textContent = window.PROJECTS.length;
    });
  }

  // ---- Testimonials ----
  // Only quotes a client has approved are shown. Set approved: true once they confirm the wording.
  var TESTIMONIALS = [
    {
      approved: false,
      quote: 'Hamid turned our mockups into a clean, working site and stayed on top of every small edit until it was right. We came back to him for our second website.',
      name: 'Andrew Ludlam',
      role: 'Founder, Longfield Business Group · UK',
      initials: 'AL'
    },
    {
      approved: false,
      quote: 'From the logo to the website, Hamid understood what international travellers need to see. Clear, patient, and easy to work with over WhatsApp.',
      name: "Sylla N'Faly",
      role: 'Founder, Guinea Travel and Services · Conakry',
      initials: 'SN'
    }
  ];
  var tWrap = document.getElementById('testimonials');
  var tList = document.getElementById('quote-list');
  if (tWrap && tList) {
    var live = TESTIMONIALS.filter(function (t) { return t.approved; });
    if (live.length) {
      live.forEach(function (t) {
        var fig = document.createElement('figure');
        fig.className = 'quote';
        var bq = document.createElement('blockquote');
        bq.textContent = '“' + t.quote + '”';
        var cap = document.createElement('figcaption');
        var av = document.createElement('span');
        av.className = 'avatar'; av.setAttribute('aria-hidden', 'true'); av.textContent = t.initials;
        var who = document.createElement('span');
        var b = document.createElement('strong'); b.textContent = t.name;
        var s = document.createElement('small'); s.textContent = t.role;
        who.appendChild(b); who.appendChild(s);
        cap.appendChild(av); cap.appendChild(who);
        fig.appendChild(bq); fig.appendChild(cap);
        tList.appendChild(fig);
      });
      tWrap.hidden = false;
    }
  }

  // ---- Contact form (Formspree) ----
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var status = document.getElementById('form-status');
      btn.disabled = true; btn.textContent = 'Sending…';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (res) {
          if (res.ok) {
            form.reset();
            status.textContent = 'Thanks — your message is in. I’ll reply within 24 hours (usually sooner).';
          } else {
            status.textContent = 'That didn’t send. Please try again, or message me on WhatsApp.';
          }
        })
        .catch(function () { status.textContent = 'Network error. Please try again, or message me on WhatsApp.'; })
        .then(function () { btn.disabled = false; btn.textContent = 'Send enquiry'; });
    });
  }

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
