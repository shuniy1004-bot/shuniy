"""Page shell for the SHUNI site.

Every page gets the identical head / header / footer / overlay layers from here,
so the top bar cannot drift between pages (that is what makes it jump on
navigation). Only the chapter body, the page CSS and the page script differ.
"""

NAV = [
    ("",   "홈",       ""),
    ("01", "프로필",   "profile"),
    ("02", "공지",     "notice"),
    ("03", "일정",     "schedule"),
    ("04", "노래책",   "song"),
    ("05", "옷장",     "dress"),
    ("06", "업보",     "work"),
    ("07", "일기",     "diary"),
    ("08", "미니게임", "game"),
]

SOOP_ID = "k4187421"
FAVICON = f"https://profile.img.sooplive.co.kr/LOGO/{SOOP_ID[:2]}/{SOOP_ID}/{SOOP_ID}.jpg"
STATION = f"https://www.sooplive.com/station/{SOOP_ID}"
VER = "20260902a"


def nav_html(active, root):
    """The home link carries no number: 01-08 belong to the eight categories."""
    out = []
    for num, label, slug in NAV:
        on = ' class="on"' if slug == active else ""
        href = (root or "./") if not slug else f"{root}{slug}/"
        inner = (f'<span>{num}</span>' if num else '') + label
        out.append(f'      <a href="{href}"{on}>{inner}</a>')
    return "\n".join(out)


def page(*, slug, title, desc, root, body, css="", script="", extra_head="", footer_mark,
         cover=False):
    """root is '' for the site root page and '../' for a folder page.
    cover=True swaps the scrolling chapter for the one screen cover layout."""
    main_cls = "sn-cover" if cover else "chapter"
    body_cls = "sn-sub sn-home" if cover else "sn-sub"
    foot = (f'    <footer class="cover-foot rv">\n'
            f'      <span>\u00a9 <b id="copyright-year">2026</b> SHUNI OFFICIAL</span>\n'
            f'      <b id="dday-strip">BIRTHDAY</b>\n'
            f'      <span data-t="foot-mark">{footer_mark}</span>\n'
            f'    </footer>') if cover else (
            f'    <footer class="sn-footer rv">\n'
            f'      <span>\u00a9 <b id="copyright-year">2026</b> SHUNI OFFICIAL</span>\n'
            f'      <b data-t="foot-mark">{footer_mark}</b>\n'
            f'      <span data-hook="fan_name">\uc288\ubabd</span>\n'
            f'    </footer>')
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <!-- Fixed width so phones render the desktop layout. No scale limits: setting
       minimum-scale locks zoom and the in-app browser snaps back. -->
  <meta name="viewport" content="width=1180, user-scalable=yes">
  <meta name="color-scheme" content="light dark">
  <meta name="description" content="SHUNI OFFICIAL — {desc}">
  <meta property="og:title" content="{title} | SHUNI OFFICIAL">
  <meta property="og:description" content="SHUNI OFFICIAL — {desc}">
  <meta property="og:type" content="website">
  <title>{title} | SHUNI OFFICIAL</title>
  <link rel="icon" type="image/jpeg" href="{FAVICON}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}css/cosmos.css?v={VER}">
  <script src="{root}pcview.js?v={VER}"></script>
{extra_head}  <style>
    /* Same gate on the page itself, so a cached stylesheet cannot let the
       hard-coded defaults flash before the DB values arrive. */
    body:not(.dataready) .chapter,
    body:not(.dataready) .sn-cover{{opacity:0}}
    [hidden]{{display:none !important}}
{css}  </style>
</head>
<body class="{body_cls}">
<script>
  try {{ if (localStorage.getItem('theme') === 'dark') document.body.classList.add('dark'); }} catch (e) {{}}
  try {{ if (window.self !== window.top) document.body.classList.add('embed'); }}
  catch (e) {{ document.body.classList.add('embed'); }}
  /* Defined before the images parse: a hot-linked avatar can fail while the page
     is still parsing, and the onerror attribute fires right then. */
  function snAvatarFallback(img) {{
    img.style.display = 'none';
    var ini = document.getElementById(img.dataset.ini || 'avatar-ini');
    if (ini) ini.hidden = false;
  }}
</script>

  <header class="site-header">
    <a href="{root or './'}" class="monogram" aria-label="SHUNI 홈">Shuni</a>
    <nav id="main-navigation" class="main-navigation" aria-label="메인 메뉴">
{nav_html(slug, root)}
    </nav>
    <div class="header-side">
      <a class="open-full" href="?pc=1" target="_blank" rel="noreferrer">PC 화면 ↗</a>
      <a class="live-link" id="live-link" href="{STATION}" target="_blank" rel="noreferrer"><i aria-hidden="true"></i>ON AIR</a>
      <button class="ask-btn" type="button" data-letter aria-label="슈니에게 한마디 보내기"><span>SIGNAL</span> ✦</button>
      <button class="mode-toggle" type="button" aria-label="밤하늘로">☾</button>
    </div>
    <button class="menu-toggle" type="button" aria-controls="main-navigation" aria-expanded="false" aria-label="메뉴 열기"><span></span><span></span></button>
  </header>

  <main class="{main_cls}">
{body}
{foot}
  </main>

  <div id="snStars" aria-hidden="true"></div>
  <div id="snMongs"></div>
  <div id="snFx" aria-hidden="true"></div>
  <div id="snMask"></div>
  <div id="snLetter" role="dialog" aria-modal="true" aria-label="슈니에게 신호 보내기">
    <p class="lk" data-t="modal-k">SEND A SIGNAL · 익명</p>
    <h3 data-t="modal-h">슈니에게 한마디</h3>
    <textarea id="snTa" placeholder="남긴 내용은 관리자만 확인합니다"></textarea>
    <div class="acts">
      <button id="snClose" type="button">CLOSE</button>
      <button id="snSend" class="sn-btn-solid" type="button">보내기 ✦</button>
    </div>
    <p class="ok-msg" data-t="modal-ok">신호가 도착했습니다</p>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js"></script>
  <script src="{root}supabase.js?v={VER}"></script>
  <script src="{root}js/cosmos.js?v={VER}"></script>
  <script>
{script}  </script>
</body>
</html>
"""


SHARED_TAIL = """
    /* palette, type scale and fixed screen text come from profile.data on
       every page, so the admin theme and text tabs reach all of them */
    async function snCommon() {
      try {
        var res = await db.from('profile').select('data').eq('id', 1);
        var d = (res && res.data && res.data[0] && res.data[0].data) || {};
        SN.applyTheme(d);
        SN.applyTexts(d);
        SN.watchTexts(d);
        var fn = SN.txt(d.fan_name).trim();
        if (fn) document.querySelectorAll('[data-hook="fan_name"]').forEach(function (el) { el.textContent = fn; });
        var lk = d.links && d.links.soop;
        var lv = document.getElementById('live-link');
        if (lv && SN.txt(lk).trim()) lv.href = SN.txt(lk);
        SN.mongs({
          img: SN.txt(d.mong_img).trim(),
          count: d.mong_count != null ? d.mong_count : 3,
          lines: Array.isArray(d.mong_lines) ? d.mong_lines : null
        });
        return d;
      } catch (e) { SN.mongs({}); return {}; }
    }
"""
