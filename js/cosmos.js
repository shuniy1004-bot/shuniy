/* cosmos.js — SHUNI OFFICIAL common behaviour
   Day/night (localStorage 'theme') · star field · drifting fan characters ·
   click sparkle · D-Day · signal modal (inquiries.message) · page cover ·
   reveal · FOUC gate · palette + type scale from profile.data
   Load order: supabase.js -> cosmos.js -> page loader */

(function () {
  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };
  var SN = window.SN = {};
  var noMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var EMBED = (function () { try { return window.self !== window.top; } catch (e) { return true; } })();
  SN.embed = EMBED;

  /* ---- day / night ---- */
  function syncMode() {
    var d = document.body.classList.contains('dark');
    $$('.mode-toggle').forEach(function (b) {
      b.textContent = d ? '☀' : '☾';
      b.setAttribute('aria-label', d ? '낮 하늘로' : '밤하늘로');
      b.title = d ? 'DAY SKY' : 'NIGHT SKY';
    });
  }
  syncMode();
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.mode-toggle');
    if (!b) return;
    document.body.classList.toggle('dark');
    try { localStorage.setItem('theme', document.body.classList.contains('dark') ? 'dark' : 'light'); } catch (err) {}
    syncMode();
  });

  /* ---- mobile menu ---- */
  var toggle = $('.menu-toggle'), nav = $('.main-navigation');
  if (toggle && nav) {
    var closeMenu = function () {
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    };
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });
    nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeMenu); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
  }

  /* ---- value guards — never render [object Object] ---- */
  SN.txt = function (v) {
    if (v == null) return '';
    if (typeof v === 'string' || typeof v === 'number') return String(v);
    if (Array.isArray(v)) return v.map(SN.txt).join(', ');
    if (typeof v === 'object') return Object.keys(v).map(function (k) { return SN.txt(v[k]); }).join(' ');
    return String(v);
  };
  SN.esc = function (s) {
    return SN.txt(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  };
  SN.linkify = function (s) {
    return SN.esc(s)
      .replace(/(https?:\/\/[^\s<>"']+)/g, '<a class="sn-link" href="$1" target="_blank" rel="noreferrer">$1</a>')
      .replace(/\n/g, '<br>');
  };

  /* ---- dates ---- */
  SN.dday = function (md) {                       /* 'MM-DD' -> days until the next birthday */
    var p = String(md || '').split('-'); if (p.length < 2) return null;
    var n = new Date(), today = new Date(n.getFullYear(), n.getMonth(), n.getDate());
    var t = new Date(n.getFullYear(), +p[0] - 1, +p[1]);
    if (isNaN(t)) return null;
    if (t < today) t = new Date(n.getFullYear() + 1, +p[0] - 1, +p[1]);
    return Math.round((t - today) / 864e5);
  };
  SN.dplus = function (iso) {                     /* 'YYYY-MM-DD' or 'YYYY.MM.DD' -> days since debut */
    var p = String(iso || '').split(/[-.]/); if (p.length < 3) return null;
    var s = new Date(+p[0], +p[1] - 1, +p[2]); if (isNaN(s)) return null;
    var n = new Date(), today = new Date(n.getFullYear(), n.getMonth(), n.getDate());
    return Math.floor((today - s) / 864e5);
  };
  SN.soopAvatar = function (id) {
    id = String(id || '').trim();
    if (!id) return '';
    return 'https://profile.img.sooplive.co.kr/LOGO/' + id.slice(0, 2) + '/' + id + '/' + id + '.jpg';
  };

  /* ---- star field ---- */
  var stars = $('#snStars');
  if (stars && !noMotion) {
    var GLYPH = ['✦', '✧', '·', '✦', '★', '·'];
    for (var i = 0; i < 26; i++) {
      var el = document.createElement('i');
      el.textContent = GLYPH[i % GLYPH.length];
      /* starting past 92% pushes the glyph off-screen and creates a sideways scrollbar */
      el.style.left = (Math.random() * 92) + '%';
      el.style.fontSize = (7 + Math.random() * 8) + 'px';
      if (i % 4 === 0) {
        el.className = 'fall';
        el.style.top = '0';
        el.style.animationDuration = (13 + Math.random() * 12) + 's';
      } else {
        el.style.top = (Math.random() * 94) + '%';
        el.style.animationDuration = (2.4 + Math.random() * 3.6) + 's';
      }
      el.style.animationDelay = (-Math.random() * 18) + 's';
      stars.appendChild(el);
    }
  }

  /* ---- drifting fan characters ----
     Image comes from profile.data.mong_img; without it a star sprite is used,
     so the layer works before the artwork exists. */
  var STAR_SPRITE = 'data:image/svg+xml;base64,' + btoa(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">' +
    '<defs><radialGradient id="g" cx="50%" cy="42%"><stop offset="0" stop-color="#ffffff"/>' +
    '<stop offset="1" stop-color="#BFD5EB"/></radialGradient></defs>' +
    '<path fill="url(#g)" stroke="#7FB4E8" stroke-width="2" stroke-linejoin="round" ' +
    'd="M32 6 39 24 58 26 44 39 48 58 32 48 16 58 20 39 6 26 25 24Z"/>' +
    '<circle cx="26" cy="31" r="2.6" fill="#2b4763"/><circle cx="38" cy="31" r="2.6" fill="#2b4763"/>' +
    '<path d="M28 37q4 3.4 8 0" fill="none" stroke="#2b4763" stroke-width="2" stroke-linecap="round"/></svg>');

  var MONG_LINES = ['반짝', '슈니 보러 왔어?', '오늘도 별 하나', '히히', '나 여기 있다', '별 이어줘'];
  var mongLayer = $('#snMongs');

  SN.mongs = function (opts) {
    if (!mongLayer || noMotion) return;
    opts = opts || {};
    var img = SN.txt(opts.img).trim() || STAR_SPRITE;
    var lines = (opts.lines && opts.lines.length) ? opts.lines : MONG_LINES;
    var n = Math.max(0, Math.min(6, parseInt(opts.count, 10) || 3));
    mongLayer.innerHTML = '';
    for (var i = 0; i < n; i++) {
      var m = document.createElement('div');
      m.className = 'sn-mong';
      m.setAttribute('role', 'button');
      m.setAttribute('tabindex', '0');
      m.setAttribute('aria-label', '팬 캐릭터');
      m.style.backgroundImage = 'url("' + img + '")';
      m.style.setProperty('--mw', (46 + Math.random() * 26).toFixed(0) + 'px');
      m.style.setProperty('--my', (-14 - Math.random() * 34).toFixed(0) + 'px');
      m.style.top = (12 + Math.random() * 64) + '%';
      m.style.animationDuration = (34 + Math.random() * 26).toFixed(1) + 's';
      m.style.animationDelay = (-Math.random() * 40).toFixed(1) + 's';
      mongLayer.appendChild(m);
    }
    var say = function (el) {
      el.classList.remove('bump'); void el.offsetWidth; el.classList.add('bump');
      var r = el.getBoundingClientRect();
      var b = document.createElement('div');
      b.className = 'sn-bubble';
      b.textContent = lines[(Math.random() * lines.length) | 0];
      b.style.left = (r.left + r.width / 2) + 'px';
      b.style.top = (r.top - 6 + (EMBED ? window.scrollY : 0)) + 'px';
      mongLayer.appendChild(b);
      setTimeout(function () { b.remove(); }, 1750);
      SN.pop(r.left + r.width / 2, r.top + r.height / 2, 4);
    };
    mongLayer.addEventListener('click', function (e) {
      var t = e.target.closest && e.target.closest('.sn-mong');
      if (t) say(t);
    });
    mongLayer.addEventListener('keydown', function (e) {
      var t = e.target.closest && e.target.closest('.sn-mong');
      if (t && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); say(t); }
    });
  };

  /* ---- click sparkle ---- */
  SN.pop = function (x, y, n) {
    var fx = $('#snFx'); if (!fx || noMotion) return;
    var oy = EMBED ? window.scrollY : 0;
    for (var i = 0; i < (n || 1); i++) {
      var p = document.createElement('span');
      p.className = 'sn-pop';
      p.textContent = i % 2 ? '✧' : '✦';
      p.style.left = (x + (Math.random() * 26 - 13)) + 'px';
      p.style.top = (y + oy + (Math.random() * 10 - 5)) + 'px';
      fx.appendChild(p);
      (function (q) { setTimeout(function () { q.remove(); }, 900); })(p);
    }
  };
  document.addEventListener('click', function (e) {
    if (e.target.closest('button, a, textarea, input, select, #snLetter, .sn-mong')) return;
    SN.pop(e.clientX, e.clientY, 1);
  });
  SN.bump = function (el) { el.classList.remove('sn-bump'); void el.offsetWidth; el.classList.add('sn-bump'); };

  /* ---- signal (inquiry) modal ---- */
  var lastY = 0;
  document.addEventListener('click', function (e) { if (e.pageY) lastY = e.pageY; }, true);
  var mask = $('#snMask'), M = $('#snLetter');

  /* Inside an iframe the modal must sit near the click: fixed would centre it in
     the full iframe box, which the SOOP app makes thousands of px tall. */
  function place() {
    if (!EMBED || !M || !mask) return;
    var dh = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
    mask.style.height = dh + 'px';
    var ih = M.offsetHeight || 320;
    var y = Math.round(Math.max(16, Math.min(lastY - ih / 2, dh - ih - 16)));
    M.style.top = y + 'px';
  }
  function openLetter() {
    if (!M) return;
    mask.classList.add('on'); M.classList.add('on'); M.classList.remove('ok');
    place();
    var t = $('#snTa'); if (t) { t.value = ''; setTimeout(function () { t.focus(); }, 120); }
  }
  function closeLetter() { if (!M) return; mask.classList.remove('on'); M.classList.remove('on'); }
  SN.openLetter = openLetter;
  if (M) {
    $$('[data-letter]').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); openLetter(); }); });
    mask.addEventListener('click', closeLetter);
    var cb = $('#snClose'); if (cb) cb.addEventListener('click', closeLetter);
    var sb = $('#snSend');
    if (sb) sb.addEventListener('click', function () {
      var t = $('#snTa'), v = (t && t.value || '').trim();
      if (!v) { alert('내용을 입력해 주세요'); return; }
      if (typeof insertRow !== 'function' || (typeof SB_READY !== 'undefined' && !SB_READY)) {
        alert('서버 연결 전입니다 — 키 설정 후 전송할 수 있습니다'); return;
      }
      sb.disabled = true;
      insertRow('inquiries', { message: v }).then(function (ok) {
        sb.disabled = false;
        if (ok) { M.classList.add('ok'); setTimeout(closeLetter, 1500); }
        else alert('전송에 실패했습니다. 잠시 후 다시 시도해 주세요');
      });
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeLetter(); });
  }

  /* ---- page transition cover ---- */
  var cover = document.createElement('div');
  cover.id = 'snCover';
  cover.innerHTML = '<div class="in"><div class="mono">Shu <b>✦</b> ni</div><i></i><div class="cap">OBSERVING</div></div>';
  document.body.appendChild(cover);
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href]');
    if (!a || noMotion) return;
    var href = a.getAttribute('href');
    if (!href || a.target === '_blank' || href.charAt(0) === '#') return;
    if (/^(https?:|mailto:|tel:|blob:|data:|javascript:)/i.test(href)) return;
    if (a.hasAttribute('download') || a.hasAttribute('data-letter')) return;
    e.preventDefault();
    cover.classList.add('on');
    setTimeout(function () { location.href = href; }, 260);
  });

  /* ---- scroll reveal + gauges ---- */
  function fill(scope) {
    Array.prototype.forEach.call(scope.querySelectorAll('.fl[data-w]'), function (f) {
      if (!f.dataset.done) { f.dataset.done = 1; setTimeout(function () { f.style.width = f.dataset.w + '%'; }, 120); }
    });
  }
  SN.reveal = function () {
    var rvs = $$('.rv');
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add('in'); fill(en.target); io.unobserve(en.target); }
        });
      }, { threshold: .12 });
      rvs.forEach(function (el) { if (!el.classList.contains('in')) io.observe(el); });
    } else rvs.forEach(function (el) { el.classList.add('in'); fill(el); });
  };
  SN.reveal();

  /* ---- FOUC gate ----
     ready     = animations may start
     dataready = DB values applied; the opacity gate uses this one so the
                 hard-coded defaults never flash before the real values land */
  SN.dataReady = function () { document.body.classList.add('dataready'); SN.ready(); };
  SN.ready = function () {
    if (document.body.classList.contains('ready')) return;
    document.body.classList.add('ready');
    $$('.rv').forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight * .92) { el.classList.add('in'); fill(el); }
    });
  };
  if (document.readyState === 'complete') SN.ready();
  else window.addEventListener('load', SN.ready);
  setTimeout(function () { SN.dataReady(); }, 1600);   /* offline / no response fallback */

  /* ---- palette + type scale from the admin theme tab ---- */
  var THEME_MAP = {
    'theme-main': '--main', 'theme-point': '--point', 'theme-accent': '--accent-txt',
    'theme-deep': '--deep', 'theme-bg': '--bg', 'theme-ink': '--ink',
    'theme-cover-a': '--cover-a', 'theme-cover-b': '--cover-b'
  };
  var TYPE_MAP = {
    'type-display': '--fs-display', 'type-title': '--fs-title',
    'type-body': '--fs-body', 'type-label': '--fs-label'
  };
  SN.applyTheme = function (d) {
    if (!d) return;
    Object.keys(THEME_MAP).forEach(function (k) {
      var v = d[k];
      if (typeof v === 'string' && /^#[0-9a-fA-F]{6}$/.test(v.trim()))
        document.documentElement.style.setProperty(THEME_MAP[k], v.trim());
    });
    Object.keys(TYPE_MAP).forEach(function (k) {
      var v = parseFloat(d[k]);
      if (!isNaN(v) && v >= .6 && v <= 1.8)
        document.documentElement.style.setProperty(TYPE_MAP[k], String(v));
    });
  };

  /* ---- fixed screen text, editable from the admin text tab ---- */
  SN.applyTexts = function (T, root) {
    if (!T) return;
    (root || document).querySelectorAll('[data-t]').forEach(function (el) {
      var v = SN.txt(T['txt-' + el.getAttribute('data-t')] || '');
      if (v) el.textContent = v;
    });
  };
  SN.watchTexts = function (T) {
    if (!T || !window.MutationObserver) return;
    new MutationObserver(function (muts) {
      muts.forEach(function (r) {
        Array.prototype.forEach.call(r.addedNodes, function (n) {
          if (n.nodeType === 1) SN.applyTexts(T, n);
        });
      });
    }).observe(document.body, { childList: true, subtree: true });
  };

  var y = $('#copyright-year'); if (y) y.textContent = String(new Date().getFullYear());

  /* ---- globals the category pages call by bare name ---- */
  window.esc = SN.esc;
  window.fmtDate = function (s) {
    try {
      var d = new Date(s); if (isNaN(d)) return '';
      return String(d.getFullYear()).slice(2) + '.' +
             String(d.getMonth() + 1).padStart(2, '0') + '.' +
             String(d.getDate()).padStart(2, '0');
    } catch (e) { return ''; }
  };
  window.soopAvatar = function (id) {
    if (!id) return null;
    id = String(id).trim().toLowerCase();
    if (id.length < 2) return null;
    return 'https://profile.img.sooplive.co.kr/LOGO/' + id.slice(0, 2) + '/' + id + '/' + id + '.jpg';
  };

  /* Detail overlays sit at the click, not at the viewport centre: inside an
     iframe a fixed centre lands in the middle of the whole embed box. */
  window.placeOverlay = function (ov) {
    if (!ov) return;
    var y = lastY || (window.scrollY + 160);
    ov.style.top = Math.max(10, y - 80) + 'px';
    ov.style.height = 'auto';
    ov.style.minHeight = '0';
    ov.classList.add('show');
    document.body.classList.add('ov-open');
  };
  window.hideOverlay = function (ov) {
    if (!ov) return;
    ov.classList.remove('show');
    document.body.classList.remove('ov-open');
  };

  /* Kept as a call site only. Posting a height makes the SOOP post viewer
     resize the frame, report again, and reload in a loop. */
  window.enableIframeAutoHeight = function () {};

  window.showToast = function (msg) {
    var t = document.getElementById('snToast');
    if (!t) {
      t = document.createElement('div'); t.id = 'snToast'; t.className = 'toast';
      document.body.appendChild(t);
    }
    t.textContent = msg;
    if (EMBED) t.style.top = Math.max(10, (lastY || window.scrollY) - 40) + 'px';
    t.classList.add('show');
    clearTimeout(t._h);
    t._h = setTimeout(function () { t.classList.remove('show'); }, 2200);
  };

  /* every overlay closes on ESC and on a backdrop click */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    $$('.ov.show, .lb.open').forEach(function (o) { o.classList.remove('show', 'open'); });
    document.body.classList.remove('ov-open');
  });
  document.addEventListener('click', function (e) {
    var o = e.target.closest && e.target.closest('.ov.show, .lb.open');
    if (o && (e.target === o || e.target.classList.contains('ov-back'))) {
      o.classList.remove('show', 'open');
      document.body.classList.remove('ov-open');
    }
  });

  /* ---- inquiry helpers under the names the wiring doc uses ---- */
  window.openAsk = openLetter;
  window.closeAsk = closeLetter;
})();
