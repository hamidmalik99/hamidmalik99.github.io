(function () {
  var cards = Array.prototype.slice.call(document.querySelectorAll('#grid .card'));
  var tabs = Array.prototype.slice.call(document.querySelectorAll('#tabs .tab'));
  var input = document.getElementById('search');
  var results = document.getElementById('results');
  var empty = document.getElementById('empty');
  var active = 'All', query = '';

  function apply() {
    var shown = 0;
    cards.forEach(function (c) {
      var ok = (active === 'All' || c.getAttribute('data-group') === active) &&
               (!query || c.getAttribute('data-search').indexOf(query) > -1);
      c.hidden = !ok;
      if (ok) shown++;
    });
    results.textContent = shown + (shown === 1 ? ' project' : ' projects') + (active !== 'All' ? ' in ' + active : '');
    empty.hidden = shown !== 0;
    if (window.initShots) window.initShots(document.getElementById('grid'));
  }

  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      active = t.getAttribute('data-group');
      tabs.forEach(function (x) { x.setAttribute('aria-pressed', x === t ? 'true' : 'false'); });
      apply();
    });
  });
  if (input) input.addEventListener('input', function () { query = input.value.trim().toLowerCase(); apply(); });
})();
