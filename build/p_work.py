from shell import page, SHARED_TAIL

CSS = """
    .vw-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
    .viewer-card{
      display:grid;justify-items:center;gap:8px;padding:24px 14px 20px;
      border:1px solid var(--line);background:var(--glass);cursor:pointer;
      backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
      transition:background 160ms ease;
    }
    .viewer-card:hover{background:var(--glass-deep)}
    .viewer-av,.viewer-av-fb{width:62px;height:62px;border-radius:50%;border:1px solid var(--line);display:block}
    .viewer-av{object-fit:cover}
    .viewer-av-fb{display:grid;place-items:center;background:var(--main);color:#14273A;font-family:var(--font-serif);font-style:italic;font-size:26px}
    .viewer-nick{font-size:calc(15px * var(--fs-body));font-weight:700;text-align:center;line-height:1.4}
    .viewer-id{color:var(--tx-dim);font-size:calc(13.5px * var(--fs-label))}
    .viewer-total{
      margin-top:2px;padding:3px 11px;border:1px solid var(--line);
      color:var(--accent-txt);font-size:calc(13px * var(--fs-label));font-weight:900;letter-spacing:.1em;
    }

    .modal-top{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:center;margin:0 0 18px;padding-right:34px}
    .modal-av,.modal-av-fb{width:54px;height:54px;border-radius:50%;border:1px solid var(--line);display:block}
    .modal-av{object-fit:cover}
    .modal-av-fb{display:grid;place-items:center;background:var(--main);color:#14273A;font-family:var(--font-serif);font-style:italic;font-size:23px}
    .modal-nick{font-family:var(--font-serif);font-size:calc(22px * var(--fs-title));line-height:1.2}
    .modal-id{margin-top:3px;color:var(--tx-dim);font-size:calc(13.5px * var(--fs-label))}
    .upbo-row{display:grid;grid-template-columns:1fr auto auto;gap:10px;align-items:baseline;padding:11px 0;border-bottom:1px solid var(--line-soft)}
    .upbo-row:last-child{border-bottom:0}
    .upbo-row .nm{font-size:calc(15px * var(--fs-body));font-weight:700}
    .upbo-row .ev{padding:2px 8px;border:1px solid var(--line);color:var(--accent-txt);font-size:calc(12px * var(--fs-label));font-weight:900;letter-spacing:.1em}
    .upbo-row .ct{font-family:var(--font-serif);font-style:italic;font-size:calc(16px * var(--fs-body));color:var(--accent-txt)}
    .modal-empty{padding:34px 0;text-align:center;color:var(--tx-dim);font-family:var(--font-serif);font-style:italic;font-size:calc(15px * var(--fs-body))}

    @media (max-width:959px){ .vw-grid{grid-template-columns:repeat(2,1fr)} }
"""

BODY = """    <div class="chapter-head rv">
      <div class="chapter-ghost" aria-hidden="true">Debt</div>
      <p class="kicker" data-t="wk-kicker">LOG 06 · LEDGER</p>
      <h1><em data-t="wk-eyebrow">what the star owes</em>업보</h1>
      <p class="desc" data-t="wk-desc">시청자별 업보 기록입니다. 카드를 누르면 종류별로 볼 수 있습니다.</p>
    </div>

    <div class="sn-toolbar rv">
      <input class="input grow" id="search" type="search" placeholder="닉네임 또는 아이디 검색" autocomplete="off">
      <span class="sn-count" id="update-date"></span>
    </div>

    <div class="vw-grid rv" id="grid"></div>

    <div class="ov" id="ov">
      <div class="ov-back"></div>
      <div class="ov-box">
        <button class="ov-x" type="button" id="ovClose" aria-label="닫기">✕</button>
        <div class="modal-top" id="modal-top"></div>
        <div id="modal-body"></div>
      </div>
    </div>
"""

SCRIPT = SHARED_TAIL + """
    (function () {
      var viewers = [], types = [], counts = [];

      function viewerTotal(vid) {
        return counts.filter(function (c) { return c.viewer_id === vid && c.count > 0; })
                     .reduce(function (s, c) { return s + c.count; }, 0);
      }
      function avEl(v, cls) {
        var av = soopAvatar(v.soop_id);
        var ini = esc((v.nickname || '?').charAt(0));
        if (!av) return '<div class="' + cls + '-fb">' + ini + '</div>';
        return '<img class="' + cls + '" src="' + esc(av) + '" alt="" referrerpolicy="no-referrer" ' +
               'data-ini="' + ini + '" data-fb="' + cls + '-fb" onerror="wkAvatarFallback(this)">';
      }
      window.wkAvatarFallback = function (img) {
        var d = document.createElement('div');
        d.className = img.dataset.fb;
        d.textContent = img.dataset.ini;
        img.replaceWith(d);
      };
      function render(list) {
        var grid = document.getElementById('grid');
        if (!list.length) { grid.innerHTML = '<div class="sn-card sn-empty">등록된 시청자가 없습니다</div>'; enableIframeAutoHeight(); return; }
        grid.innerHTML = list.map(function (v) {
          return '<div class="viewer-card" data-v="' + v.id + '">' + avEl(v, 'viewer-av') +
            '<div class="viewer-nick">' + esc(v.nickname) + '</div>' +
            (v.soop_id ? '<div class="viewer-id">(' + esc(v.soop_id) + ')</div>' : '<div class="viewer-id">&nbsp;</div>') +
            '<span class="viewer-total">업보 ' + viewerTotal(v.id) + '</span></div>';
        }).join('');
        grid.querySelectorAll('[data-v]').forEach(function (c) {
          c.addEventListener('click', function () { openModal(+c.dataset.v); });
        });
        enableIframeAutoHeight();
      }
      function openModal(vid) {
        var v = viewers.filter(function (x) { return x.id === vid; })[0];
        if (!v) return;
        document.getElementById('modal-top').innerHTML = avEl(v, 'modal-av') +
          '<div><div class="modal-nick">' + esc(v.nickname) + '</div>' +
          (v.soop_id ? '<div class="modal-id">(' + esc(v.soop_id) + ')</div>' : '') + '</div>';
        var my = {};
        counts.filter(function (c) { return c.viewer_id === vid; }).forEach(function (c) { my[c.type_id] = c.count; });
        var rows = types.filter(function (t) { return (my[t.id] || 0) > 0; }).map(function (t) {
          return '<div class="upbo-row"><span class="nm">' + esc(t.name) + '</span>' +
            (t.category === '이벤트' ? '<span class="ev">이벤트</span>' : '<span></span>') +
            '<span class="ct">×' + my[t.id] + '</span></div>';
        }).join('');
        document.getElementById('modal-body').innerHTML = rows || '<div class="modal-empty">기록된 업보가 없습니다</div>';
        placeOverlay(document.getElementById('ov'));
      }
      document.getElementById('ovClose').addEventListener('click', function () { hideOverlay(document.getElementById('ov')); });
      document.getElementById('search').addEventListener('input', function (e) {
        var q = e.target.value.trim().toLowerCase();
        render(viewers.filter(function (v) {
          return (v.nickname || '').toLowerCase().indexOf(q) !== -1 || (v.soop_id || '').toLowerCase().indexOf(q) !== -1;
        }));
      });

      async function init() {
        render([]);
        await snCommon();
        try {
          var r = await Promise.all([
            fetchAll('viewers', { order: 'sort_order', asc: true }),
            fetchAll('upbo_types', { order: 'sort_order', asc: true }),
            fetchAll('upbo_counts', { order: 'id', asc: true })
          ]);
          viewers = r[0]; types = r[1]; counts = r[2];
        } catch (e) { viewers = []; types = []; counts = []; }
        var latest = counts.reduce(function (m, c) { return c.updated_at && c.updated_at > m ? c.updated_at : m; }, '');
        document.getElementById('update-date').textContent = latest ? '갱신일 ' + latest.slice(0, 10) : '';
        render(viewers);
        SN.dataReady(); SN.reveal(); enableIframeAutoHeight();
      }
      init();
    })();
"""


def build():
    return page(slug="work", title="업보", desc="업보", root="../", body=BODY,
                css=CSS, script=SCRIPT, footer_mark="STAR ATLAS · LOG 06")
