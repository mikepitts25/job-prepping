(function () {
  var nav = document.getElementById('navtoggle');
  var side = document.getElementById('sidebar');
  if (nav && side) nav.addEventListener('click', function () { side.classList.toggle('open'); });

  var t = document.getElementById('themetoggle');
  var root = document.documentElement;
  try {
    var saved = localStorage.getItem('prep-theme');
    if (saved) root.setAttribute('data-theme', saved);
  } catch (e) {}
  if (t) t.addEventListener('click', function () {
    var cur = root.getAttribute('data-theme');
    if (!cur) {
      cur = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    var next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('prep-theme', next); } catch (e) {}
  });

  document.querySelectorAll('main table').forEach(function (tbl) {
    if (tbl.parentElement.classList.contains('tablewrap')) return;
    var w = document.createElement('div');
    w.className = 'tablewrap';
    tbl.parentNode.insertBefore(w, tbl);
    w.appendChild(tbl);
  });
})();
