from shell import page, SHARED_TAIL

CSS = """
    .rnd-box{
      display:grid;justify-items:center;gap:8px;padding:34px 20px;
      border:1px solid var(--line);background:rgba(126,180,232,.08);
    }
    .rnd-box .lab{color:var(--tx-dim);font-size:calc(13px * var(--fs-label));font-weight:800;letter-spacing:.24em}
    .rnd-box .t{font-family:var(--font-serif);font-size:calc(34px * var(--fs-display));line-height:1.15;text-align:center;letter-spacing:-.02em}
    .rnd-box .a{color:var(--tx-soft);font-size:calc(15px * var(--fs-body))}
    .rnd-box.rolling .t{opacity:.55}
    .rnd-box.hit{animation:rndhit 620ms cubic-bezier(.2,.75,.25,1)}
    @keyframes rndhit{0%{transform:scale(.94)}55%{transform:scale(1.03)}100%{transform:scale(1)}}
    .rnd-acts{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}

    .song-head,.song-row{display:grid;grid-template-columns:52px 1fr 1fr 96px 84px;gap:14px;align-items:center}
    .song-head{
      padding:0 4px 10px;border-bottom:1px solid var(--line);
      color:var(--tx-dim);font-family:var(--font-serif);font-style:italic;font-size:calc(13.5px * var(--fs-label));letter-spacing:.1em;
    }
    .song-row{padding:12px 4px;border-bottom:1px solid var(--line-soft)}
    .song-row:last-child{border-bottom:0}
    .song-row:hover{background:rgba(126,180,232,.08)}
    .s-num{font-family:var(--font-serif);font-style:italic;font-size:calc(14px * var(--fs-label));color:var(--tx-dim)}
    .s-title{font-size:calc(15.5px * var(--fs-body));font-weight:700;line-height:1.5;min-width:0}
    .s-artist{color:var(--tx-soft);font-size:calc(14.5px * var(--fs-body));min-width:0}
    .s-genre{color:var(--tx-dim);font-size:calc(13.5px * var(--fs-label));font-weight:800;letter-spacing:.08em}
    .s-diff{display:flex;gap:4px}
    .s-diff .dot{width:7px;height:7px;border:1px solid var(--line)}
    .s-diff .dot.on{background:var(--point);border-color:var(--point)}

    @media (max-width:959px){
      .song-head{display:none}
      .song-row{grid-template-columns:38px 1fr auto;gap:10px;row-gap:4px}
      .s-artist{grid-column:2}
      .s-genre{grid-column:3;grid-row:1}
      .s-diff{grid-column:3;grid-row:2;justify-content:flex-end}
      .rnd-box .t{font-size:calc(26px * var(--fs-display))}
    }
"""

BODY = """    <div class="chapter-head rv">
      <div class="chapter-ghost" aria-hidden="true">Song</div>
      <p class="kicker" data-t="sg-kicker">LOG 04 · FREQUENCY</p>
      <h1><em data-t="sg-eyebrow">what the star sings</em>노래책</h1>
      <p class="desc" data-t="sg-desc">신청할 수 있는 곡 목록입니다.</p>
    </div>

    <section class="sn-card rv">
      <p class="sn-kicker" data-t="sg-pick">RANDOM PICK · 랜덤 선곡</p>
      <div class="rnd-box" id="randBox" hidden>
        <span class="lab" data-t="sg-picked">PICKED</span>
        <span class="t" id="randTitle">—</span>
        <span class="a" id="randArtist"></span>
      </div>
      <div class="rnd-acts">
        <button class="sn-btn-solid" type="button" id="randBtn" data-t="sg-roll">곡 뽑기 ✦</button>
        <button class="sn-btn-line" type="button" id="randAgain" data-t="sg-again">다시 뽑기</button>
        <button class="sn-btn-line" type="button" id="randCopy" data-t="sg-copy">제목 복사</button>
      </div>
    </section>

    <div class="sn-tabs rv" id="genre-tabs" style="margin-top:22px"></div>

    <div class="sn-toolbar rv">
      <input class="input grow" id="search" type="search" placeholder="제목 또는 아티스트 검색" autocomplete="off">
      <span class="sn-count" id="count">총 0곡</span>
    </div>

    <section class="sn-card rv">
      <div class="song-head">
        <span>NO</span><span>TITLE</span><span>ARTIST</span><span>GENRE</span><span>LEVEL</span>
      </div>
      <div id="song-body"></div>
    </section>
    <div class="sn-pager" id="pagination"></div>
"""

SCRIPT = SHARED_TAIL + """
    (function () {
      /* keep GENRES in sync with the admin genre list */
      var GENRES = ['전체','K-POP','J-POP','애니','OST','기타'];
      var PAGE = 30;
      var songs = [], curGenre = '전체', curPage = 1, keyword = '';
      var PICKED = null, rolling = false;

      function renderGenres() {
        document.getElementById('genre-tabs').innerHTML = GENRES.map(function (g) {
          return '<button class="sn-tab' + (g === curGenre ? ' active' : '') + '" type="button" data-g="' + esc(g) + '">' + esc(g) + '</button>';
        }).join('');
        document.querySelectorAll('#genre-tabs .sn-tab').forEach(function (b) {
          b.addEventListener('click', function () {
            curGenre = b.dataset.g; curPage = 1; renderGenres(); render(); enableIframeAutoHeight();
          });
        });
      }
      function filtered() {
        return songs.filter(function (s) {
          var okG = curGenre === '전체' || s.genre === curGenre;
          var q = keyword.toLowerCase();
          return okG && (!q || (s.title || '').toLowerCase().indexOf(q) !== -1 || (s.artist || '').toLowerCase().indexOf(q) !== -1);
        });
      }
      function showPick(s, isFinal) {
        PICKED = s;
        document.getElementById('randTitle').textContent = s.title || '—';
        document.getElementById('randArtist').textContent = s.artist || '아티스트 미상';
        var box = document.getElementById('randBox');
        box.classList.toggle('rolling', !isFinal);
        if (isFinal) { box.classList.remove('hit'); void box.offsetWidth; box.classList.add('hit'); }
      }
      function rollPick() {
        if (rolling) return;
        var arr = filtered();
        if (!arr.length) { showToast('고를 곡이 없습니다'); return; }
        document.getElementById('randBox').hidden = false;
        if (arr.length === 1) { showPick(arr[0], true); return; }
        rolling = true;
        var n = 0, ticks = 14 + Math.floor(Math.random() * 6);
        (function tick() {
          showPick(arr[Math.floor(Math.random() * arr.length)], false);
          n++;
          if (n < ticks) setTimeout(tick, 45 + Math.pow(n / ticks, 3) * 210);
          else { showPick(arr[Math.floor(Math.random() * arr.length)], true); rolling = false; }
        })();
      }
      function render() {
        var list = filtered();
        var totalPages = Math.max(1, Math.ceil(list.length / PAGE));
        if (curPage > totalPages) curPage = 1;
        var pageItems = list.slice((curPage - 1) * PAGE, curPage * PAGE);
        document.getElementById('count').textContent = '총 ' + list.length + '곡 · ' + curPage + '/' + totalPages + ' 페이지';
        var body = document.getElementById('song-body');
        if (!list.length) {
          body.innerHTML = '<div class="sn-empty">등록된 곡이 없습니다</div>';
          document.getElementById('pagination').innerHTML = '';
          return;
        }
        body.innerHTML = pageItems.map(function (s, i) {
          var num = (curPage - 1) * PAGE + i + 1;
          var diff = parseInt(s.difficulty, 10) || 0;
          var dots = '';
          for (var k = 1; k <= 5; k++) dots += '<span class="dot' + (k <= diff ? ' on' : '') + '"></span>';
          return '<div class="song-row" data-song="' + esc(s.title) + '">' +
            '<span class="s-num">' + num + '</span>' +
            '<span class="s-title">' + esc(s.title) + '</span>' +
            '<span class="s-artist">' + (esc(s.artist) || '-') + '</span>' +
            '<span class="s-genre">' + (esc(s.genre) || '기타') + '</span>' +
            '<span class="s-diff">' + dots + '</span></div>';
        }).join('');
        var pg = document.getElementById('pagination');
        pg.innerHTML = '';
        if (totalPages > 1) for (var i = 1; i <= totalPages; i++) {
          var b = document.createElement('button');
          b.className = i === curPage ? 'active' : '';
          b.textContent = i;
          b.dataset.pg = i;
          b.onclick = function () { curPage = +this.dataset.pg; render(); enableIframeAutoHeight(); window.scrollTo(0, 0); };
          pg.appendChild(b);
        }
      }

      document.getElementById('search').addEventListener('input', function (e) {
        keyword = e.target.value.trim(); curPage = 1; render(); enableIframeAutoHeight();
      });
      document.getElementById('randBtn').addEventListener('click', rollPick);
      document.getElementById('randAgain').addEventListener('click', rollPick);
      document.getElementById('randCopy').addEventListener('click', function () {
        if (!PICKED) { showToast('먼저 곡을 뽑아 주세요'); return; }
        var t = PICKED.title + (PICKED.artist ? ' - ' + PICKED.artist : '');
        if (navigator.clipboard) navigator.clipboard.writeText(t).then(function () { showToast('복사했습니다'); });
      });

      async function init() {
        renderGenres(); render();
        await snCommon();
        try { songs = await fetchAll('songs', { order: 'id', asc: true }); }
        catch (e) { songs = []; }
        render();
        SN.dataReady(); SN.reveal(); enableIframeAutoHeight();
      }
      init();
    })();
"""


def build():
    return page(slug="song", title="노래책", desc="노래책", root="../", body=BODY,
                css=CSS, script=SCRIPT, footer_mark="STAR ATLAS · LOG 04")
