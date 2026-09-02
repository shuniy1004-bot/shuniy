/* pcview.js — desktop layout inside the SOOP in-app browser (?pc=1)
   The app webview cannot render nested iframes and resets its own zoom, so
   neither a wrapper nor a wide viewport works there. Instead:
     1. drop every mobile media rule from our own stylesheets
     2. lay the document out at DESIGN px
     3. shrink it with a CSS transform, which no webview zoom reset can undo
   Load order: right after the stylesheets, before the page scripts. */

(function () {
  var DESIGN = 1180;
  if (location.search.indexOf('pc=1') === -1) return;

  document.documentElement.setAttribute('data-pc', '1');

  var mv = document.querySelector('meta[name="viewport"]');
  if (mv) mv.setAttribute('content', 'width=device-width, initial-scale=1');

  function stripMobileRules(sheet) {
    var rules;
    try { rules = sheet.cssRules; } catch (e) { return; }   /* cross-origin sheet */
    if (!rules) return;
    for (var i = rules.length - 1; i >= 0; i--) {
      var r = rules[i];
      if (r.type === 4) {
        var t = r.conditionText || (r.media && r.media.mediaText) || '';
        var m = /max-width:\s*(\d+)px/.exec(t);
        if (m && parseInt(m[1], 10) <= DESIGN) {
          try { sheet.deleteRule(i); } catch (e) {}
        }
      }
    }
  }

  /* vw/vh do not follow the transform, so restate the few rules that use them. */
  function injectOverrides() {
    if (document.getElementById('pcview-css') || !document.head) return;
    var css =
      'body.pcview .chapter { width:1180px; max-width:1180px; margin:0 auto; padding:158px 46px 90px; }' +
      'body.pcview .site-header { position:absolute; height:104px; }' +
      'body.pcview #snStars, body.pcview #snMongs, body.pcview #snFx { position:absolute; }' +
      'body.pcview .chapter-head h1 { font-size:calc(96px * var(--fs-display)); }' +
      'body.pcview .chapter-ghost { font-size:calc(210px * var(--fs-display)); display:block; }' +
      'body.pcview .pf-hero { height:400px; }';
    var st = document.createElement('style');
    st.id = 'pcview-css';
    st.textContent = css;
    document.head.appendChild(st);
  }

  /* Capture the width before the body is widened: once the document overflows,
     mobile browsers grow the layout viewport, and reading innerWidth again would
     feed that growth back into the scale (1089 instead of 375 = almost no shrink). */
  var BASE = (function () {
    var sw = (window.screen && window.screen.width) || 0;
    var iw = window.innerWidth || document.documentElement.clientWidth || 0;
    if (sw && iw) return Math.min(sw, iw);
    return sw || iw || DESIGN;
  })();

  function scale() { return BASE / DESIGN; }

  /* transform, not zoom: some in-app webviews ignore `zoom` entirely */
  function place() {
    if (!document.body) return;
    var s = scale();
    document.documentElement.style.overflowX = 'hidden';
    document.documentElement.style.width = BASE + 'px';
    document.body.style.width = DESIGN + 'px';
    document.body.style.transformOrigin = '0 0';
    document.body.style.transform = 'scale(' + s + ')';
    sizeDocument();
  }

  /* the transform is visual only, so the document keeps its unscaled height */
  function sizeDocument() {
    if (!document.body) return;
    var s = scale();
    var anchor = document.querySelector('.sn-footer') || document.querySelector('.chapter');
    var h = anchor ? Math.ceil(anchor.getBoundingClientRect().bottom / s + window.scrollY / s) : document.body.scrollHeight;
    document.documentElement.style.height = Math.ceil(h * s) + 'px';
  }

  function apply() {
    injectOverrides();
    for (var i = 0; i < document.styleSheets.length; i++) stripMobileRules(document.styleSheets[i]);
    if (document.body) document.body.classList.add('pcview');
    place();
  }

  apply();
  document.addEventListener('DOMContentLoaded', apply);
  window.addEventListener('load', function () {
    apply();
    [300, 900, 2000].forEach(function (t) { setTimeout(sizeDocument, t); });
    if (window.ResizeObserver && document.body) new ResizeObserver(sizeDocument).observe(document.body);
  });
  window.addEventListener('resize', function () {
    var sw = (window.screen && window.screen.width) || 0;
    if (sw) BASE = sw;                                     /* orientation change only */
    place();
  });
})();
