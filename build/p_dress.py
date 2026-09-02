from shell import page, SHARED_TAIL

CSS = """
    .seg{display:flex;border:1px solid var(--line);margin:0 0 18px}
    .seg-btn{
      flex:1;padding:13px 10px;border:0;border-right:1px solid var(--line-soft);
      background:transparent;color:var(--tx-dim);cursor:pointer;
      font-family:var(--font-body);font-size:calc(13.5px * var(--fs-label));font-weight:800;letter-spacing:.1em;
      transition:background 160ms ease,color 160ms ease;
    }
    .seg-btn:last-child{border-right:0}
    .seg-btn:hover{background:rgba(126,180,232,.12);color:var(--tx)}
    .seg-btn.active{background:var(--point);color:#fff}

    .poster-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
    .poster{
      position:relative;aspect-ratio:3/4;overflow:hidden;cursor:pointer;
      border:1px solid var(--line);background:rgba(126,180,232,.10);
    }
    .poster img{width:100%;height:100%;object-fit:cover;display:block;transition:transform 420ms cubic-bezier(.2,.75,.25,1)}
    .poster:hover img{transform:scale(1.04)}
    .poster.no-img{display:grid;place-items:center}
    .poster .ph-ph{font-size:34px;opacity:.5}
    .poster::after{
      content:"";position:absolute;inset:0;pointer-events:none;
      background:linear-gradient(0deg,rgba(6,11,24,.82),rgba(6,11,24,.12) 46%,rgba(6,11,24,.42));
    }
    .p-top{position:absolute;z-index:1;left:14px;right:14px;top:12px;display:flex;justify-content:space-between;align-items:center;gap:8px}
    .p-brand{font-family:var(--font-serif);font-style:italic;font-size:calc(14px * var(--fs-label));color:#EAF2FB}
    .p-new{padding:3px 8px;border:1px solid rgba(234,242,251,.7);color:#EAF2FB;font-size:calc(12px * var(--fs-label));font-weight:900;letter-spacing:.16em}
    .p-bottom{position:absolute;z-index:1;left:14px;right:14px;bottom:13px;display:grid;gap:5px}
    .p-cat{color:#BFD5EB;font-size:calc(12px * var(--fs-label));font-weight:900;letter-spacing:.2em}
    .p-name{color:#fff;font-family:var(--font-serif);font-size:calc(20px * var(--fs-title));line-height:1.2;letter-spacing:-.01em}
    .p-meta{color:rgba(234,242,251,.72);font-family:var(--font-serif);font-style:italic;font-size:calc(13.5px * var(--fs-label))}
    .p-desc{
      color:rgba(234,242,251,.82);font-size:calc(13.5px * var(--fs-body));line-height:1.55;
      display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
    }

    .item-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
    .item-card{border:1px solid var(--line);background:var(--glass);cursor:pointer;transition:background 160ms ease}
    .item-card:hover{background:var(--glass-deep)}
    .item-card img{width:100%;aspect-ratio:3/4;object-fit:cover;display:block}
    .item-card.no-img{display:grid;place-items:center;aspect-ratio:3/4}
    .item-card .ph{font-size:32px;opacity:.5}
    .item-cap{padding:14px 15px}
    .item-cap .name{font-size:calc(15px * var(--fs-body));font-weight:700;line-height:1.45}
    .item-cap .desc{margin-top:5px;color:var(--tx-dim);font-size:calc(13.5px * var(--fs-body));line-height:1.55;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}

    @media (max-width:959px){
      .poster-grid,.item-grid{grid-template-columns:repeat(2,1fr);gap:12px}
      .p-name{font-size:calc(16px * var(--fs-title))}
    }
"""

BODY = """    <div class="chapter-head rv">
      <div class="chapter-ghost" aria-hidden="true">Dress</div>
      <p class="kicker" data-t="dr-kicker">LOG 05 · WARDROBE</p>
      <h1><em data-t="dr-eyebrow">what the star wears</em>옷장</h1>
      <p class="desc" data-t="dr-desc">헤어 · 의상 · 렌즈를 모아 두었습니다.</p>
    </div>

    <div class="seg rv" id="mode-seg">
      <button class="seg-btn active" type="button" data-mode="new" data-t="dr-mode-new">✦ 새 옷</button>
      <button class="seg-btn" type="button" data-mode="old" data-t="dr-mode-old">◇ 기존 옷</button>
    </div>

    <div class="sn-tabs rv" id="cat-tabs"></div>

    <div id="dress-body" class="rv"></div>

    <div class="lb" id="lightbox">
      <figure>
        <img id="lb-img" src="" alt="" referrerpolicy="no-referrer">
        <figcaption class="cap"><b id="lb-name"></b><span id="lb-desc"></span></figcaption>
      </figure>
    </div>
"""

SCRIPT = SHARED_TAIL + """
    (function () {
      /* keep CATS in sync with admin: select#dr-cat options + DRESS_CATS */
      var CATS = [{ key: 'hair', label: '헤어' }, { key: 'outfit', label: '의상' }, { key: 'lens', label: '렌즈' }];
      var LABELS = {};
      CATS.forEach(function (c) { LABELS[c.key] = c.label; });
      var PER_PAGE = 9;
      var allItems = [], curCat = CATS[0].key, curMode = 'new', curPage = 1, brand = '슈니';

      function isNew(it) {
        return (it.badges || []).some(function (b) {
          var label = (b && (b.label != null ? b.label : b)) || '';
          return String(label).trim().toUpperCase() === 'NEW';
        });
      }
      function viewItems() {
        if (curMode === 'new') {
          return allItems.filter(function (i) { return i.category === curCat && isNew(i); })
            .slice().sort(function (a, b) { return new Date(b.created_at || 0) - new Date(a.created_at || 0); });
        }
        return allItems.filter(function (i) { return i.category === curCat && !isNew(i); });
      }
      function buildTabs() {
        var wrap = document.getElementById('cat-tabs');
        wrap.innerHTML = CATS.map(function (c) {
          var cnt = allItems.filter(function (i) {
            return i.category === c.key && (curMode === 'new' ? isNew(i) : !isNew(i));
          }).length;
          return '<button class="sn-tab' + (c.key === curCat ? ' active' : '') + '" type="button" data-k="' + c.key + '">' +
                 esc(c.label) + ' <span class="cnt">' + cnt + '</span></button>';
        }).join('');
        wrap.querySelectorAll('.sn-tab').forEach(function (b) {
          b.addEventListener('click', function () { curCat = b.dataset.k; curPage = 1; buildTabs(); render(); });
        });
      }
      function posterHTML(items) {
        return '<div class="poster-grid">' + items.map(function (it, idx) {
          var img = it.image_url
            ? '<img src="' + esc(it.image_url) + '" referrerpolicy="no-referrer" alt="' + esc(it.name) + '" loading="lazy">'
            : '<span class="ph-ph">✦</span>';
          var cat = (it.category && LABELS[it.category]) ? '<span class="p-cat">' + esc(LABELS[it.category]) + '</span>' : '';
          var date = it.created_at ? '<div class="p-meta">' + fmtDate(it.created_at) + '</div>' : '';
          return '<div class="poster' + (it.image_url ? '' : ' no-img') + '" data-idx="' + idx + '">' + img +
            '<div class="p-top"><span class="p-brand">' + esc(brand) + '</span><span class="p-new">✦ NEW</span></div>' +
            '<div class="p-bottom">' + cat + '<div class="p-name">' + esc(it.name) + '</div>' + date +
            (it.description ? '<div class="p-desc">' + esc(it.description) + '</div>' : '') +
            '</div></div>';
        }).join('') + '</div>';
      }
      function gridHTML(items) {
        return '<div class="item-grid">' + items.map(function (it, idx) {
          var hasImg = !!it.image_url;
          var inner = hasImg
            ? '<img src="' + esc(it.image_url) + '" referrerpolicy="no-referrer" alt="' + esc(it.name) + '" loading="lazy">'
            : '<span class="ph">✦</span>';
          return '<div class="item-card' + (hasImg ? '' : ' no-img') + '" data-idx="' + idx + '">' + inner +
            '<div class="item-cap"><div class="name">' + esc(it.name) + '</div>' +
            (it.description ? '<div class="desc">' + esc(it.description) + '</div>' : '') +
            '</div></div>';
        }).join('') + '</div>';
      }
      function render() {
        var body = document.getElementById('dress-body');
        var items = viewItems();
        if (!items.length) {
          body.innerHTML = '<div class="sn-card sn-empty">' +
            (curMode === 'new'
              ? esc(LABELS[curCat] || '') + ' 새 옷이 없습니다'
              : esc(LABELS[curCat] || '') + ' 항목이 없습니다') + '</div>';
          enableIframeAutoHeight();
          return;
        }
        var totalPages = Math.max(1, Math.ceil(items.length / PER_PAGE));
        if (curPage > totalPages) curPage = 1;
        var pageItems = items.slice((curPage - 1) * PER_PAGE, curPage * PER_PAGE);
        var main = (curMode === 'new') ? posterHTML(pageItems) : gridHTML(pageItems);
        var pager = '';
        if (totalPages > 1) {
          pager = '<div class="sn-pager">';
          for (var i = 1; i <= totalPages; i++) pager += '<button type="button" class="' + (i === curPage ? 'active' : '') + '" data-pg="' + i + '">' + i + '</button>';
          pager += '</div>';
        }
        body.innerHTML = main + pager;
        body.querySelectorAll('[data-idx]').forEach(function (el) {
          el.addEventListener('click', function () {
            var it = pageItems[+el.dataset.idx];
            if (it && it.image_url) openLb(it);
          });
        });
        body.querySelectorAll('[data-pg]').forEach(function (btn) {
          btn.addEventListener('click', function () { curPage = +btn.dataset.pg; render(); window.scrollTo(0, 0); });
        });
        enableIframeAutoHeight();
      }
      function openLb(item) {
        document.getElementById('lb-img').src = item.image_url;
        document.getElementById('lb-name').textContent = item.name || '';
        var d = document.getElementById('lb-desc');
        d.textContent = item.description || '';
        d.style.display = item.description ? 'block' : 'none';
        document.getElementById('lightbox').classList.add('open');
      }

      document.querySelectorAll('#mode-seg .seg-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          curMode = btn.dataset.mode; curPage = 1;
          document.querySelectorAll('#mode-seg .seg-btn').forEach(function (b) {
            b.classList.toggle('active', b.dataset.mode === curMode);
          });
          buildTabs(); render();
        });
      });

      async function init() {
        buildTabs(); render();
        var d = await snCommon();
        var nm = SN.txt(d && d.name).trim();
        if (nm) brand = nm;
        try {
          var res = await db.from('dress_items').select('*').order('sort_order').order('created_at');
          allItems = (res && res.data) || [];
        } catch (e) { allItems = []; }
        buildTabs(); render();
        SN.dataReady(); SN.reveal(); enableIframeAutoHeight();
      }
      init();
    })();
"""


def build():
    return page(slug="dress", title="옷장", desc="옷장", root="../", body=BODY,
                css=CSS, script=SCRIPT, footer_mark="STAR ATLAS · LOG 05")
