from shell import page, SHARED_TAIL

CSS = """
    .dy-item{
      border:1px solid var(--line);background:var(--glass);
      backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
    }
    body:not(.dark) .dy-item{box-shadow:0 10px 34px rgba(31,82,133,.06)}
    .dy-item + .dy-item{margin-top:12px}
    .dy-head{display:grid;grid-template-columns:1fr auto auto;gap:14px;align-items:baseline;padding:20px 24px;cursor:pointer}
    .dy-head:hover{background:rgba(126,180,232,.08)}
    .dy-title{font-size:calc(17px * var(--fs-body));font-weight:700;line-height:1.5;min-width:0}
    .dy-mood{padding:3px 9px;border:1px solid var(--line);color:var(--accent-txt);font-size:calc(13px * var(--fs-label));font-weight:800;letter-spacing:.08em;white-space:nowrap}
    .dy-date{font-family:var(--font-serif);font-style:italic;font-size:calc(14px * var(--fs-label));color:var(--tx-dim);white-space:nowrap}
    .dy-body{display:none;padding:0 24px 22px;color:var(--tx-soft);font-size:calc(15px * var(--fs-body));line-height:1.85;white-space:pre-wrap}
    .dy-item.open .dy-body{display:block}

    .cmt-wrap{margin-top:22px;padding-top:18px;border-top:1px solid var(--line-soft)}
    .cmt-lab{margin:0 0 12px;color:var(--tx-dim);font-family:var(--font-serif);font-style:italic;font-size:calc(13.5px * var(--fs-label));letter-spacing:.12em}
    .cmt-item{display:grid;grid-template-columns:auto 1fr;gap:12px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--line-soft)}
    .cmt-item:last-child{border-bottom:0}
    .cmt-item .cn{color:var(--accent-txt);font-size:calc(13.5px * var(--fs-label));font-weight:800;white-space:nowrap}
    .cmt-item .cm{font-size:calc(14.5px * var(--fs-body));line-height:1.6;white-space:pre-wrap}
    .cmt-empty{padding:16px 0;color:var(--tx-dim);font-family:var(--font-serif);font-style:italic;font-size:calc(14px * var(--fs-body))}
    .cmt-form{display:grid;grid-template-columns:140px 1fr auto;gap:8px;margin-top:14px}
    @media (max-width:959px){
      .dy-head{grid-template-columns:1fr auto;gap:8px;padding:16px 18px}
      .dy-mood{grid-column:1}
      .dy-body{padding:0 18px 18px}
      .cmt-form{grid-template-columns:1fr}
    }
"""

BODY = """    <div class="chapter-head rv">
      <div class="chapter-ghost" aria-hidden="true">Diary</div>
      <p class="kicker" data-t="dy-kicker">LOG 07 · JOURNAL</p>
      <h1><em data-t="dy-eyebrow">notes from the night</em>일기</h1>
      <p class="desc" data-t="dy-desc">슈니가 남긴 기록입니다. 한마디 남길 수 있습니다.</p>
    </div>

    <div id="diary-list" class="rv"></div>
    <div class="sn-pager" id="pagination"></div>
"""

SCRIPT = SHARED_TAIL + """
    (function () {
      var PAGE_SIZE = 15;
      var allData = [], currentPage = 1;

      function renderPage(page) {
        currentPage = page;
        var items = allData.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);
        var el = document.getElementById('diary-list');
        if (!allData.length) {
          el.innerHTML = '<div class="sn-card sn-empty">등록된 일기가 없습니다</div>';
          document.getElementById('pagination').innerHTML = '';
          return;
        }
        el.innerHTML = items.map(function (d) {
          var imgs = (d.images && d.images.length) ? d.images : (d.image_url ? [d.image_url] : []);
          return '<article class="dy-item" data-id="' + d.id + '">' +
            '<div class="dy-head">' +
              '<span class="dy-title">' + esc(d.title) + '</span>' +
              (d.mood ? '<span class="dy-mood">' + esc(d.mood) + '</span>' : '<span></span>') +
              '<span class="dy-date">' + esc(d.diary_date || '') + '</span>' +
            '</div>' +
            '<div class="dy-body">' +
              imgs.map(function (u) { return '<img src="' + esc(u) + '" class="post-img" referrerpolicy="no-referrer" loading="lazy" alt="">'; }).join('') +
              esc(d.content) +
              '<div class="cmt-wrap">' +
                '<p class="cmt-lab" data-t="dy-cmt">COMMENTS · 한마디</p>' +
                '<div class="cmt-list" id="cmt-list-' + d.id + '"></div>' +
                '<div class="cmt-form">' +
                  '<input class="input cmt-nick" id="cmt-nick-' + d.id + '" placeholder="닉네임 (비우면 익명)" maxlength="20">' +
                  '<input class="input cmt-msg" id="cmt-msg-' + d.id + '" placeholder="한마디 남기기" maxlength="200">' +
                  '<button class="sn-btn-solid" type="button" data-send="' + d.id + '">등록</button>' +
                '</div>' +
              '</div>' +
            '</div></article>';
        }).join('');

        el.querySelectorAll('.dy-head').forEach(function (h) {
          h.addEventListener('click', function () {
            var item = h.closest('.dy-item');
            var wasOpen = item.classList.contains('open');
            item.classList.toggle('open');
            if (!wasOpen) { loadComments(item.dataset.id); enableIframeAutoHeight(); }
          });
        });
        el.querySelectorAll('.cmt-wrap').forEach(function (w) {
          w.addEventListener('click', function (e) { e.stopPropagation(); });
        });
        el.querySelectorAll('[data-send]').forEach(function (b) {
          b.addEventListener('click', function () { addComment(b.dataset.send); });
        });
        el.querySelectorAll('.cmt-msg').forEach(function (i) {
          i.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') addComment(i.id.replace('cmt-msg-', ''));
          });
        });

        var totalPages = Math.ceil(allData.length / PAGE_SIZE);
        var pg = document.getElementById('pagination');
        pg.innerHTML = '';
        if (totalPages > 1) for (var i = 1; i <= totalPages; i++) {
          var b = document.createElement('button');
          b.className = i === page ? 'active' : '';
          b.textContent = i;
          b.dataset.pg = i;
          b.onclick = function () { renderPage(+this.dataset.pg); enableIframeAutoHeight(); window.scrollTo(0, 0); };
          pg.appendChild(b);
        }
      }

      async function loadComments(diaryId) {
        var list = document.getElementById('cmt-list-' + diaryId);
        if (!list) return;
        var all = [];
        try { all = await fetchAll('comments', { order: 'created_at', asc: true }); } catch (e) { all = []; }
        var mine = all.filter(function (c) { return String(c.diary_id) === String(diaryId); });
        list.innerHTML = mine.length
          ? mine.map(function (c) {
              return '<div class="cmt-item"><span class="cn">' + esc(c.nickname || '익명') + '</span>' +
                     '<span class="cm">' + esc(c.message) + '</span></div>';
            }).join('')
          : '<div class="cmt-empty">아직 한마디가 없습니다</div>';
        enableIframeAutoHeight();
      }

      async function addComment(diaryId) {
        var msgEl = document.getElementById('cmt-msg-' + diaryId);
        var msg = (msgEl.value || '').trim();
        if (!msg) { showToast('내용을 입력해 주세요'); return; }
        var nick = (document.getElementById('cmt-nick-' + diaryId).value || '').trim() || '익명';
        var ok = false;
        try { ok = await insertRow('comments', { diary_id: diaryId, nickname: nick, message: msg }); } catch (e) { ok = false; }
        if (ok) { msgEl.value = ''; loadComments(diaryId); showToast('등록했습니다'); }
        else showToast('등록에 실패했습니다');
      }

      async function init() {
        renderPage(1);
        await snCommon();
        try { allData = await fetchAll('diary', { order: 'diary_date', asc: false }); }
        catch (e) { allData = []; }
        renderPage(1);
        SN.dataReady(); SN.reveal(); enableIframeAutoHeight();
      }
      init();
    })();
"""


def build():
    return page(slug="diary", title="일기", desc="일기", root="../", body=BODY,
                css=CSS, script=SCRIPT, footer_mark="STAR ATLAS · LOG 07")
