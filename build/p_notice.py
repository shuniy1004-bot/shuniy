from shell import page, SHARED_TAIL

CSS = """
    .nt-item{
      border:1px solid var(--line);background:var(--glass);
      backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
      cursor:pointer;transition:background 160ms ease;
    }
    body:not(.dark) .nt-item{box-shadow:0 10px 34px rgba(31,82,133,.06)}
    .nt-item + .nt-item{margin-top:12px}
    .nt-item:hover{background:var(--glass-deep)}
    .nt-head{display:grid;grid-template-columns:auto 1fr auto auto;gap:14px;align-items:baseline;padding:20px 24px}
    .nt-pin{padding:3px 9px;border:1px solid var(--point);background:var(--point);color:#fff;font-size:calc(12px * var(--fs-label));font-weight:900;letter-spacing:.1em}
    .nt-title{font-size:calc(17px * var(--fs-body));font-weight:700;line-height:1.5;min-width:0}
    .nt-date{font-family:var(--font-serif);font-style:italic;font-size:calc(14px * var(--fs-label));color:var(--tx-dim);white-space:nowrap}
    .nt-caret{color:var(--accent-txt);font-size:12px;transition:transform 200ms ease}
    .nt-item.open .nt-caret{transform:rotate(90deg)}
    .nt-body{display:none;padding:0 24px 24px;color:var(--tx-soft);font-size:calc(15px * var(--fs-body));line-height:1.85;white-space:pre-wrap}
    .nt-item.open .nt-body{display:block}
    .nt-item.pinned{border-color:var(--point)}
    @media (max-width:959px){
      .nt-head{grid-template-columns:1fr auto;gap:8px;padding:16px 18px}
      .nt-pin{grid-column:1/-1;justify-self:start}
      .nt-caret{display:none}
      .nt-body{padding:0 18px 18px}
    }
"""

BODY = """    <div class="chapter-head rv">
      <div class="chapter-ghost" aria-hidden="true">Notice</div>
      <p class="kicker" data-t="nt-kicker">LOG 02 · BROADCAST</p>
      <h1><em data-t="nt-eyebrow">from the observatory</em>공지</h1>
      <p class="desc" data-t="nt-desc">슈니가 전하는 소식입니다.</p>
    </div>

    <div class="sn-toolbar rv">
      <span class="sn-count" id="count">총 0개의 공지</span>
    </div>

    <div id="notice-list" class="rv"></div>
"""

SCRIPT = SHARED_TAIL + """
    (function () {
      function render(rows) {
        var all = rows.filter(function (n) { return n.pinned; })
                 .concat(rows.filter(function (n) { return !n.pinned; }));
        var el = document.getElementById('notice-list');
        document.getElementById('count').textContent = '총 ' + all.length + '개의 공지';
        if (!all.length) { el.innerHTML = '<div class="sn-card sn-empty">등록된 공지가 없습니다</div>'; return; }
        el.innerHTML = all.map(function (n) {
          var d = new Date(n.created_at);
          var ds = isNaN(d) ? '' : d.getFullYear() + '.' + String(d.getMonth() + 1).padStart(2, '0') + '.' + String(d.getDate()).padStart(2, '0');
          var imgs = (n.images && n.images.length) ? n.images : (n.image_url ? [n.image_url] : []);
          return '<article class="nt-item' + (n.pinned ? ' pinned' : '') + '">' +
            '<div class="nt-head">' +
              (n.pinned ? '<span class="nt-pin">고정</span>' : '<span></span>') +
              '<span class="nt-title">' + esc(n.title) + '</span>' +
              '<span class="nt-date">' + ds + '</span>' +
              '<span class="nt-caret" aria-hidden="true">▸</span>' +
            '</div>' +
            '<div class="nt-body">' +
              imgs.map(function (u) {
                return '<img src="' + esc(u) + '" class="post-img" referrerpolicy="no-referrer" loading="lazy" alt="">';
              }).join('') +
              esc(n.content) +
            '</div></article>';
        }).join('');
        el.querySelectorAll('.nt-item').forEach(function (it) {
          it.addEventListener('click', function () {
            it.classList.toggle('open');
            enableIframeAutoHeight();
          });
        });
      }
      async function init() {
        await snCommon();
        try { render(await fetchAll('notice', { order: 'created_at', asc: false })); }
        catch (e) { render([]); }
        finally { SN.dataReady(); SN.reveal(); enableIframeAutoHeight(); }
      }
      render([]);
      init();
    })();
"""


def build():
    return page(slug="notice", title="공지", desc="공지", root="../", body=BODY,
                css=CSS, script=SCRIPT, footer_mark="STAR ATLAS · LOG 02")
