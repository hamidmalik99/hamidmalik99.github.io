(function () {
  // ---- Cookie consent for Google Analytics ----
  // The tag in <head> only loads gtag.js once the visitor has accepted (see hbLoadGA).
  // The choice is kept in localStorage under 'hb_consent' ('granted' or 'denied').
  var KEY = 'hb_consent';

  function getChoice() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function setChoice(v) {
    try { localStorage.setItem(KEY, v); } catch (e) {}
  }

  // Remove Google Analytics cookies (_ga, _ga_XXXX) on this domain and its parent.
  function clearGACookies() {
    var host = location.hostname.replace(/^www\./, '');
    document.cookie.split(';').forEach(function (c) {
      var name = c.split('=')[0].trim();
      if (name === '_ga' || name.indexOf('_ga_') === 0 || name === '_gid') {
        [host, '.' + host, ''].forEach(function (d) {
          document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + (d ? '; domain=' + d : '');
        });
      }
    });
  }

  var banner;
  function hide() { if (banner) banner.hidden = true; }

  function show() {
    if (!banner) {
      banner = document.createElement('div');
      banner.className = 'cookie-banner';
      banner.setAttribute('role', 'region');
      banner.setAttribute('aria-label', 'Cookie consent');
      banner.innerHTML =
        '<p><strong>Cookies</strong><br>I use Google Analytics cookies to see which pages are useful and improve the site. ' +
        'They’re only set if you accept, and you can change your mind any time from “Cookie settings” in the footer.</p>' +
        '<div class="cookie-actions">' +
        '<button type="button" class="btn btn-gold" data-consent="granted">Accept</button>' +
        '<button type="button" class="btn btn-ghost" data-consent="denied">Reject</button>' +
        '</div>';
      banner.addEventListener('click', function (e) {
        var v = e.target.getAttribute && e.target.getAttribute('data-consent');
        if (!v) return;
        setChoice(v);
        if (v === 'granted') {
          if (window.hbLoadGA) window.hbLoadGA();
        } else {
          if (window.gtag) window.gtag('consent', 'update', { analytics_storage: 'denied' });
          clearGACookies();
        }
        hide();
      });
      document.body.appendChild(banner);
    }
    banner.hidden = false;
  }

  function init() {
    var c = getChoice();
    if (c !== 'granted' && c !== 'denied') show();
    document.addEventListener('click', function (e) {
      var t = e.target.closest && e.target.closest('[data-cookie-settings]');
      if (t) { e.preventDefault(); show(); }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
