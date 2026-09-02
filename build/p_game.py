from shell import page, SHARED_TAIL

EXTRA_HEAD = ""

CSS = """
    .seg{display:flex;border:1px solid var(--line);margin:0 0 22px}
    .seg-btn{
      flex:1;padding:13px 10px;border:0;border-right:1px solid var(--line-soft);
      background:transparent;color:var(--tx-dim);cursor:pointer;
      font-family:var(--font-body);font-size:calc(13.5px * var(--fs-label));font-weight:800;letter-spacing:.1em;
      transition:background 160ms ease,color 160ms ease;
    }
    .seg-btn:last-child{border-right:0}
    .seg-btn:hover{background:rgba(126,180,232,.12);color:var(--tx)}
    .seg-btn.active{background:var(--point);color:#fff}

    .game-bar{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:0 0 18px}
    .game-note{color:var(--tx-dim);font-size:calc(13.5px * var(--fs-label));line-height:1.6}

    /* ladder */
    .ld-stage{display:grid;gap:8px;justify-items:center}
    .ld-row{display:grid;gap:6px;width:100%}
    .ld-cell{min-width:0}
    .ld-name,.ld-prize{
      width:100%;box-sizing:border-box;padding:9px 6px;text-align:center;
      border:1px solid var(--line);background:rgba(255,255,255,.6);color:var(--tx);
      font-family:var(--font-body);font-size:calc(14px * var(--fs-body));font-weight:700;
      white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
    }
    body.dark .ld-name,body.dark .ld-prize{background:rgba(191,213,235,.07)}
    .ld-name.locked,.ld-prize.locked{display:block;border-width:2px;cursor:pointer}
    .ld-name.locked:hover{background:rgba(126,180,232,.18)}
    .ld-canvas-wrap{position:relative;width:100%;display:flex;justify-content:center}
    #ld-canvas{display:block;max-width:100%}
    .ld-runner{
      position:absolute;width:25px;height:25px;border-radius:50%;
      display:grid;place-items:center;color:#fff;
      font-size:12.5px;font-weight:900;transform:translate(-50%,-50%);pointer-events:none;
    }
    .res-list{display:grid;gap:0;margin-top:18px}
    .res-row{display:grid;grid-template-columns:1fr auto 1fr;gap:12px;align-items:baseline;padding:10px 2px;border-bottom:1px solid var(--line-soft)}
    .res-row:last-child{border-bottom:0}
    .res-row .rn{font-size:calc(15px * var(--fs-body));font-weight:800;text-align:right}
    .res-row .ra{color:var(--tx-dim)}
    .res-row .rp{font-size:calc(15px * var(--fs-body));font-weight:700}

    /* marble race */
    .rl-wrap{display:grid;grid-template-columns:auto 1fr;gap:22px;align-items:start}
    .rl-stage{position:relative;border:1px solid var(--line);background:rgba(126,180,232,.07)}
    #rl-canvas{display:block;max-width:100%;height:auto}
    #rl-mini{position:absolute;right:8px;top:8px;border:1px solid var(--line-soft);background:var(--glass-deep)}
    .rl-win{
      position:absolute;inset:0;display:none;place-items:center;
      background:rgba(6,12,26,.62);backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);
    }
    .rl-win.show{display:grid}
    .rl-win .in{display:grid;justify-items:center;gap:8px;color:#fff;text-align:center;padding:20px}
    .rl-win small{font-size:calc(13px * var(--fs-label));font-weight:900;letter-spacing:.3em;opacity:.8}
    .rl-win b{font-family:var(--font-serif);font-size:calc(40px * var(--fs-display));font-weight:400;line-height:1.15}
    .rl-win em{font-style:italic;font-family:var(--font-serif);font-size:calc(16px * var(--fs-body));opacity:.85}
    .rl-side{display:grid;gap:14px;min-width:0}
    .rl-opt{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
    .rl-opt .k{min-width:44px;color:var(--tx-dim);font-size:calc(13px * var(--fs-label));font-weight:800;letter-spacing:.16em}
    .rl-seg{display:flex;border:1px solid var(--line)}
    .rl-seg button{
      padding:8px 12px;border:0;border-right:1px solid var(--line-soft);
      background:transparent;color:var(--tx-dim);cursor:pointer;
      font-family:var(--font-body);font-size:calc(13px * var(--fs-label));font-weight:800;
    }
    .rl-seg button:last-child{border-right:0}
    .rl-seg button.on{background:var(--point);color:#fff}
    .rl-check{display:inline-flex;align-items:center;gap:7px;color:var(--tx-soft);font-size:calc(14px * var(--fs-body))}
    .rl-rank{margin-top:4px}
    .rl-rank .lbl{margin:0 0 8px;color:var(--tx-dim);font-family:var(--font-serif);font-style:italic;font-size:calc(13.5px * var(--fs-label));letter-spacing:.12em}
    .rl-rank ol{margin:0;padding:0;list-style:none;display:grid;gap:0;max-height:280px;overflow:auto}
    .rl-rank li{display:flex;align-items:center;gap:9px;padding:8px 2px;border-bottom:1px solid var(--line-soft);font-size:calc(14px * var(--fs-body));counter-increment:rk}
    .rl-rank li::before{content:counter(rk);min-width:18px;font-family:var(--font-serif);font-style:italic;color:var(--tx-dim)}
    .rl-rank ol{counter-reset:rk}
    .rl-rank li.win{color:var(--accent-txt);font-weight:800}
    .rl-rank li.none{color:var(--tx-dim);font-style:italic;font-family:var(--font-serif)}
    .rl-rank li.none::before{content:""}
    .dotc{width:9px;height:9px;border-radius:50%;flex:none}

    /* spin wheel */
    .wh-wrap{display:grid;grid-template-columns:auto 1fr;gap:22px;align-items:start}
    .wh-stage{position:relative;display:grid;justify-items:center;gap:14px}
    #wh-canvas{display:block;max-width:100%;height:auto}
    .wh-ptr{
      position:absolute;left:50%;top:-2px;transform:translateX(-50%);
      width:0;height:0;border-left:11px solid transparent;border-right:11px solid transparent;
      border-top:20px solid var(--point);z-index:2;
    }
    .wh-out{
      display:grid;justify-items:center;gap:5px;padding:18px 22px;min-width:min(100%,260px);
      border:1px solid var(--line);background:rgba(126,180,232,.08);
    }
    .wh-out small{color:var(--tx-dim);font-size:calc(13px * var(--fs-label));font-weight:900;letter-spacing:.3em}
    .wh-out b{font-family:var(--font-serif);font-size:calc(32px * var(--fs-display));font-weight:400;line-height:1.15;text-align:center}
    .wh-out.hit{animation:whhit 620ms cubic-bezier(.2,.75,.25,1)}
    @keyframes whhit{0%{transform:scale(.94)}55%{transform:scale(1.03)}100%{transform:scale(1)}}
    .wh-side{display:grid;gap:14px;min-width:0}
    .wh-hist{display:grid;gap:0;max-height:220px;overflow:auto}
    .wh-hist div{display:grid;grid-template-columns:auto 1fr;gap:10px;padding:8px 2px;border-bottom:1px solid var(--line-soft);font-size:calc(14px * var(--fs-body))}
    .wh-hist div:last-child{border-bottom:0}
    .wh-hist i{font-style:italic;font-family:var(--font-serif);color:var(--tx-dim)}

    @media (max-width:959px){
      .rl-wrap,.wh-wrap{grid-template-columns:1fr}
      #rl-canvas,#wh-canvas{width:100%}
      .rl-win b{font-size:calc(28px * var(--fs-display))}
    }
"""

BODY = """    <div class="chapter-head rv">
      <div class="chapter-ghost" aria-hidden="true">Game</div>
      <p class="kicker" data-t="gm-kicker">LOG 08 · DRAW LOTS</p>
      <h1><em data-t="gm-eyebrow">let the stars decide</em>미니게임</h1>
      <p class="desc" data-t="gm-desc">방송에서 뽑기할 때 쓰는 사다리타기 · 구슬 레이스 · 룰렛입니다.</p>
    </div>

    <div class="seg rv" id="mode-seg">
      <button class="seg-btn active" type="button" data-mode="ladder" data-t="gm-m1">사다리타기</button>
      <button class="seg-btn" type="button" data-mode="marble" data-t="gm-m2">구슬 레이스</button>
      <button class="seg-btn" type="button" data-mode="wheel" data-t="gm-m3">룰렛</button>
    </div>

    <section class="sn-card rv" id="panel-ladder">
      <p class="sn-kicker" data-t="gm-ladder">LADDER · 사다리타기</p>
      <div class="game-bar">
        <label class="input-label" for="ld-count" style="margin:0">인원</label>
        <select class="input" id="ld-count" style="width:96px"></select>
        <button class="sn-btn-solid" type="button" id="ld-make">사다리 만들기</button>
        <button class="sn-btn-line" type="button" id="ld-all">전부 공개</button>
        <button class="sn-btn-line" type="button" id="ld-reset">다시 입력</button>
      </div>
      <p class="game-note" id="ld-msg">이름과 결과를 적고 사다리를 만드세요</p>
      <div class="ld-stage">
        <div class="ld-row" id="ld-names"></div>
        <div class="ld-canvas-wrap">
          <canvas id="ld-canvas"></canvas>
          <div id="ld-runner" class="ld-runner" hidden></div>
        </div>
        <div class="ld-row" id="ld-prizes"></div>
      </div>
      <div id="ld-log"></div>
    </section>

    <section class="sn-card rv" id="panel-marble" style="display:none">
      <p class="sn-kicker" data-t="gm-marble">MARBLE RACE · 구슬 레이스</p>
      <div class="rl-wrap">
        <div class="rl-stage">
          <canvas id="rl-canvas" width="560" height="740"></canvas>
          <canvas id="rl-mini" width="120" height="200"></canvas>
          <div class="rl-win" id="rl-win"><div class="in"><small>WINNER</small><b id="rl-win-name">—</b><em id="rl-win-sub"></em></div></div>
        </div>
        <div class="rl-side">
          <div class="form-field">
            <label class="input-label" for="rl-names">참가자 (쉼표 또는 줄바꿈)</label>
            <textarea class="input" id="rl-names" rows="7" spellcheck="false">별,달,행성,혜성</textarea>
            <p class="hint"><b>이름*3</b> 은 구슬 3개, <b>이름/2</b> 는 스킬을 자주 쓰는 구슬. 최대 120개</p>
          </div>
          <div class="rl-opt">
            <span class="k">맵</span>
            <select class="input" id="rl-map" style="flex:1"></select>
          </div>
          <div class="rl-opt">
            <span class="k">당첨</span>
            <div class="rl-seg" id="rl-wintype">
              <button type="button" class="on" data-w="first">1등</button>
              <button type="button" data-w="last">꼴등</button>
            </div>
            <input class="input" id="rl-rank-in" type="number" min="1" value="1" style="width:78px">
            <span class="game-note">등</span>
          </div>
          <div class="rl-opt">
            <span class="k">속도</span>
            <div class="rl-seg" id="rl-speed">
              <button type="button" data-s="1">1배</button>
              <button type="button" class="on" data-s="2">2배</button>
              <button type="button" data-s="4">4배</button>
              <button type="button" data-s="8">8배</button>
            </div>
          </div>
          <div class="rl-opt">
            <span class="k">스킬</span>
            <label class="rl-check"><input type="checkbox" id="rl-skill" checked> 구슬이 가끔 주변을 밀칩니다</label>
          </div>
          <div class="game-bar" style="margin:4px 0 0">
            <button class="sn-btn-line" type="button" id="rl-shuffle">섞기</button>
            <button class="sn-btn-solid" type="button" id="rl-start">시작</button>
          </div>
          <p class="game-note" id="rl-msg"></p>
          <div class="rl-rank">
            <p class="lbl">RANKING · 순위</p>
            <ol id="rl-list"><li class="none">아직 도착한 구슬이 없습니다</li></ol>
          </div>
        </div>
      </div>
      <p class="game-note" style="margin-top:16px">코스는 <a class="sn-link" href="https://github.com/lazygyu/roulette" target="_blank" rel="noreferrer">lazygyu 의 Marble Roulette</a> 에서 가져왔습니다 · MIT License, Copyright (c) 2023 LazyGyu</p>
    </section>

    <section class="sn-card rv" id="panel-wheel" style="display:none">
      <p class="sn-kicker" data-t="gm-wheel">SPIN WHEEL · 룰렛</p>
      <div class="wh-wrap">
        <div class="wh-stage">
          <div style="position:relative">
            <div class="wh-ptr" aria-hidden="true"></div>
            <canvas id="wh-canvas" width="420" height="420"></canvas>
          </div>
          <div class="wh-out" id="wh-out">
            <small>RESULT</small>
            <b id="wh-name">—</b>
          </div>
        </div>
        <div class="wh-side">
          <div class="form-field">
            <label class="input-label" for="wh-names">항목 (쉼표 또는 줄바꿈)</label>
            <textarea class="input" id="wh-names" rows="8" spellcheck="false">당첨,꽝,한 번 더,꽝</textarea>
            <p class="hint"><b>이름*3</b> 은 그 칸이 3배 넓어집니다. 최대 60개</p>
          </div>
          <div class="rl-opt">
            <span class="k">제외</span>
            <label class="rl-check"><input type="checkbox" id="wh-remove"> 뽑힌 항목을 목록에서 뺍니다</label>
          </div>
          <div class="game-bar" style="margin:4px 0 0">
            <button class="sn-btn-solid" type="button" id="wh-spin">돌리기 ✦</button>
            <button class="sn-btn-line" type="button" id="wh-reset">기록 지우기</button>
          </div>
          <p class="game-note" id="wh-msg"></p>
          <div class="rl-rank">
            <p class="lbl">HISTORY · 뽑은 기록</p>
            <div class="wh-hist" id="wh-hist"></div>
          </div>
        </div>
      </div>
    </section>
"""

SCRIPT = SHARED_TAIL + """
    (function () {
      var G = window.SHUNI_GAME, W = window.SHUNI_WHEEL;
      var PC = ['#3370A8','#7FB4E8','#2f8f6e','#9a7a17','#6b57ad','#b8557f','#b06526','#2aa9c9','#5b8de0','#b34141'];

      /* ladder */
      var ldCv = document.getElementById('ld-canvas');
      var ldRunner = document.getElementById('ld-runner');
      var ldN = 4, ldPhase = 'setup', ldL = null, ldBusy = false, ldDone = {};

      function ldGeom() {
        var w = ldCv.width, h = ldCv.height;
        var pad = Math.max(34, w * 0.09);
        var colW = ldN > 1 ? (w - pad * 2) / (ldN - 1) : 0;
        var rows = ldL ? ldL.rows : 10;
        var y0 = 14, y1 = h - 14;
        return { w: w, h: h, pad: pad, colW: colW, y0: y0, y1: y1, rows: rows, rowH: (y1 - y0) / (rows + 1) };
      }
      function ldColX(i) { var g = ldGeom(); return g.pad + g.colW * i; }
      function ldRowY(r) { var g = ldGeom(); return r < 0 ? g.y0 : (r >= g.rows ? g.y1 : g.y0 + g.rowH * (r + 1)); }

      function ldSizeCanvas() {
        var wrap = ldCv.parentElement;
        var avail = Math.max(260, wrap.clientWidth || 640);
        /* spread the columns to fill the card, but cap the pitch so a two person
           ladder does not become two lines a card apart */
        var pitch = Math.max(96, Math.min(170, (avail - 108) / Math.max(1, ldN - 1)));
        var w = Math.min(avail, 54 * 2 + pitch * (ldN - 1));
        /* before a ladder exists there is nothing to be tall for */
        var rows = ldL ? ldL.rows : 0;
        ldCv.width = w;
        ldCv.height = ldL ? Math.max(300, Math.min(430, 110 + rows * 7)) : 260;
        ldCv.style.width = w + 'px';
        ldCv.style.maxWidth = '100%';
        ['ld-names', 'ld-prizes'].forEach(function (id) {
          var el = document.getElementById(id);
          if (el) { el.style.width = w + 'px'; el.style.maxWidth = '100%'; el.style.gridTemplateColumns = 'repeat(' + ldN + ',1fr)'; }
        });
      }
      function ldRenderRows() {
        var top = document.getElementById('ld-names');
        var bot = document.getElementById('ld-prizes');
        var keepN = [], keepP = [], i;
        for (i = 0; i < ldN; i++) {
          var a = document.getElementById('ldn' + i), b = document.getElementById('ldp' + i);
          keepN.push(a ? (a.value !== undefined ? a.value : a.textContent) : '참가자' + (i + 1));
          keepP.push(b ? (b.value !== undefined ? b.value : b.textContent) : (i === 0 ? '당첨' : '꽝'));
        }
        function cell(i, id, val, cls) {
          return ldPhase === 'setup'
            ? '<div class="ld-cell"><input class="' + cls + '" id="' + id + '" value="' + esc(val) + '" maxlength="10"></div>'
            : '<div class="ld-cell"><span class="' + cls + ' locked" id="' + id + '" style="border-color:' + PC[i % PC.length] + '">' + esc(val) + '</span></div>';
        }
        top.innerHTML = keepN.map(function (v, i) { return cell(i, 'ldn' + i, v, 'ld-name'); }).join('');
        bot.innerHTML = keepP.map(function (v, i) { return cell(i, 'ldp' + i, v, 'ld-prize'); }).join('');
        ldSizeCanvas();
      }
      function ldText(id) {
        var el = document.getElementById(id);
        if (!el) return '';
        return (el.value !== undefined ? el.value : el.textContent).trim();
      }
      function ldDrawBase() {
        var ctx = ldCv.getContext('2d');
        var g = ldGeom();
        ctx.clearRect(0, 0, g.w, g.h);
        /* the reference ladder never draws the horizontal bars: only the runner
           reveals where they were */
        ctx.lineCap = 'round';
        ctx.lineWidth = 3;
        ctx.strokeStyle = getComputedStyle(document.body).getPropertyValue('--tx-dim') || 'rgba(40,89,136,.55)';
        for (var i = 0; i < ldN; i++) {
          ctx.beginPath();
          ctx.moveTo(ldColX(i), g.y0);
          ctx.lineTo(ldColX(i), g.y1);
          ctx.stroke();
        }
      }
      function ldPixels(i) {
        var t = G.traceLadder(ldL, i);
        return { end: t.end, pts: t.path.map(function (p) { return { x: ldColX(p.col), y: ldRowY(p.row) }; }) };
      }
      function ldStrokeWhole(i) {
        var ctx = ldCv.getContext('2d');
        var p = ldPixels(i);
        ctx.strokeStyle = PC[i % PC.length];
        ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
        ctx.beginPath();
        ctx.moveTo(p.pts[0].x, p.pts[0].y);
        for (var k = 1; k < p.pts.length; k++) ctx.lineTo(p.pts[k].x, p.pts[k].y);
        ctx.stroke();
        return p.end;
      }
      function ldRun(i) {
        if (ldPhase !== 'play' || ldBusy || ldDone[i] !== undefined) return;
        ldBusy = true;
        var ctx = ldCv.getContext('2d');
        var p = ldPixels(i), pts = p.pts;
        /* cumulative length, so the walk is animated by distance travelled
           instead of a per segment counter */
        var cum = [0], q;
        for (q = 1; q < pts.length; q++) cum.push(cum[q - 1] + Math.hypot(pts[q].x - pts[q - 1].x, pts[q].y - pts[q - 1].y));
        var total = cum[cum.length - 1] || 1;
        var DURATION = Math.min(7000, 2600 + total * 2.2);
        var rect = ldCv.getBoundingClientRect();
        var scale = rect.width / ldCv.width;
        ldRunner.hidden = false;
        ldRunner.style.background = PC[i % PC.length];
        ldRunner.textContent = String(i + 1);
        var start = performance.now();
        function tick(now) {
          var prog = Math.min(1, (now - start) / DURATION);
          var want = total * prog;
          ctx.strokeStyle = PC[i % PC.length];
          ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
          ctx.beginPath();
          ctx.moveTo(pts[0].x, pts[0].y);
          var cx = pts[0].x, cy = pts[0].y;
          for (var q2 = 1; q2 < pts.length; q2++) {
            if (cum[q2] <= want) { ctx.lineTo(pts[q2].x, pts[q2].y); cx = pts[q2].x; cy = pts[q2].y; continue; }
            var segLen = cum[q2] - cum[q2 - 1] || 1;
            var f = (want - cum[q2 - 1]) / segLen;
            cx = pts[q2 - 1].x + (pts[q2].x - pts[q2 - 1].x) * f;
            cy = pts[q2 - 1].y + (pts[q2].y - pts[q2 - 1].y) * f;
            ctx.lineTo(cx, cy);
            break;
          }
          ctx.stroke();
          ldRunner.style.left = (cx * scale) + 'px';
          ldRunner.style.top = (cy * scale) + 'px';
          if (prog < 1) { requestAnimationFrame(tick); return; }
          ldRunner.hidden = true;
          ldDone[i] = p.end;
          ldLog();
          ldBusy = false;
        }
        requestAnimationFrame(tick);
      }
      function ldLog() {
        var box = document.getElementById('ld-log');
        var keys = Object.keys(ldDone);
        if (!keys.length) { box.innerHTML = ''; return; }
        box.innerHTML = '<div class="res-list">' + keys.map(function (k) {
          var i = Number(k);
          return '<div class="res-row"><span class="rn" style="color:' + PC[i % PC.length] + '">' + esc(ldText('ldn' + i)) + '</span>' +
                 '<span class="ra">→</span><span class="rp">' + esc(ldText('ldp' + ldDone[k])) + '</span></div>';
        }).join('') + '</div>';
      }
      function ldMake() {
        if (ldPhase === 'play') return;
        ldPhase = 'play';
        ldL = G.buildLadder(ldN);
        ldDone = {};
        ldSizeCanvas(); ldRenderRows(); ldDrawBase(); ldLog();
        document.getElementById('ld-msg').textContent = '위쪽 이름을 누르면 한 명씩 내려갑니다';
        document.getElementById('ld-count').disabled = true;
        enableIframeAutoHeight();
      }
      function ldResetGame() {
        ldPhase = 'setup'; ldL = null; ldDone = {}; ldBusy = false;
        ldRunner.hidden = true;
        ldSizeCanvas(); ldRenderRows(); ldDrawBase(); ldLog();
        document.getElementById('ld-msg').textContent = '이름과 결과를 적고 사다리를 만드세요';
        document.getElementById('ld-count').disabled = false;
        enableIframeAutoHeight();
      }
      document.getElementById('ld-make').addEventListener('click', ldMake);
      document.getElementById('ld-reset').addEventListener('click', ldResetGame);
      document.getElementById('ld-all').addEventListener('click', function () {
        if (ldPhase !== 'play' || ldBusy) return;
        ldDrawBase();
        for (var i = 0; i < ldN; i++) ldDone[i] = ldStrokeWhole(i);
        ldRunner.hidden = true;
        ldLog();
      });
      document.getElementById('ld-names').addEventListener('click', function (e) {
        var cell = e.target.closest('.ld-cell');
        if (!cell || ldPhase !== 'play') return;
        ldRun([].indexOf.call(cell.parentElement.children, cell));
      });
      (function () {
        var sel = document.getElementById('ld-count');
        for (var i = 2; i <= 10; i++) sel.insertAdjacentHTML('beforeend', '<option value="' + i + '"' + (i === 4 ? ' selected' : '') + '>' + i + '명</option>');
        sel.addEventListener('change', function () { ldN = Number(sel.value); ldResetGame(); });
      })();
      ldRenderRows(); ldDrawBase();

      /* marble race */
      var rlCv = document.getElementById('rl-canvas');
      var rlMini = document.getElementById('rl-mini');
      var RLV = { w: 560, h: 740, unit: 26 };
      var race = null, rlRaf = 0, rlMapIndex = 0, rlWinType = 'first', rlRank = 1, rlSpeed = 2;
      var cam = { x: 13, y: 0, zoom: 1 };

      function rlBaseZoom() { return RLV.w / RLV.unit; }
      function rlNames() { return document.getElementById('rl-names').value; }

      function rlBuild() {
        cancelAnimationFrame(rlRaf);
        race = G.newRace(rlMapIndex, rlNames(), rlRank, document.getElementById('rl-skill').checked);
        cam = { x: 13, y: race.marbles.length ? race.marbles[0].y : 0, zoom: 1 };
        document.getElementById('rl-win').classList.remove('show');
        var ol = document.getElementById('rl-list');
        ol.dataset.n = '-1';
        ol.innerHTML = '<li class="none">아직 도착한 구슬이 없습니다</li>';
        document.getElementById('rl-msg').textContent = race.total
          ? '구슬 ' + race.total + '개 · ' + race.stage.title
          : '참가자를 적어 주세요';
        try { localStorage.setItem('shuni-rl-names', rlNames()); } catch (e) {}
        rlDraw();
        rlRaf = requestAnimationFrame(rlLoop);
      }
      function rlApplyRank() {
        var total = race ? race.total : 1;
        if (rlWinType === 'first') rlRank = 1;
        else if (rlWinType === 'last') rlRank = Math.max(1, total);
        document.getElementById('rl-rank-in').value = rlRank;
        if (race) race.winningRank = Math.max(0, rlRank - 1);
      }
      function rlStart() {
        if (!race || !race.total) { rlBuild(); return; }
        if (race.winner || race.started) rlBuild();
        rlApplyRank();
        G.startRace(race);
        document.getElementById('rl-msg').textContent = '굴러가는 중…';
      }
      var rlLast = 0, rlAcc = 0;
      function rlLoop(now) {
        if (!rlLast) rlLast = now || 0;
        var elapsed = (now || 0) - rlLast;
        rlLast = now || 0;
        /* fixed timestep. the cap is in wall clock milliseconds, so a stalled tab
           skips ahead instead of trying to simulate the whole gap. */
        if (elapsed > 250) elapsed = 250;
        rlAcc += elapsed * rlSpeed;
        if (race) {
          var tick = 1000 / 60, done = 0, cap = 90;
          while (race.started && !race.over && rlAcc >= tick && done++ < cap) {
            G.stepRace(race);
            rlAcc -= tick;
          }
          if (done >= cap) rlAcc = 0;
          if (!race.started) rlAcc = 0;
          rlCamera(); rlDraw(); rlRankList();
          if (race.winner && !race.announced) { race.announced = true; rlAnnounce(); }
        }
        rlRaf = requestAnimationFrame(rlLoop);
      }
      function rlAnnounce() {
        var w = race.winners[race.winningRank] || race.winner;
        document.getElementById('rl-win-name').textContent = w.name;
        document.getElementById('rl-win-sub').textContent = (race.winningRank + 1) + '등';
        document.getElementById('rl-win').classList.add('show');
        document.getElementById('rl-msg').textContent = '끝났습니다. 섞기를 눌러 다시 준비하세요';
      }
      /* follows the deciding marble and closes in near the finish line */
      function rlCamera() {
        var live = race.marbles.filter(function (m) { return !m.done; });
        var targetIndex = race.winningRank - race.winners.length;
        var t = live[targetIndex] || live[0];
        if (t && race.started) {
          var needZoom = race.goalDist < G.RL.zoomThreshold;
          var tz = needZoom ? Math.max(1, (1 - race.goalDist / G.RL.zoomThreshold) * 4) : 1;
          cam.x += (t.x - cam.x) / 10;
          cam.y += (t.y - cam.y) / 10;
          cam.zoom += (tz - cam.zoom) / 10;
        } else if (t) {
          cam.x += (13 - cam.x) / 10;
          cam.y += (t.y - cam.y) / 10;
        }
      }
      function rlRankList() {
        var ol = document.getElementById('rl-list');
        if (ol.dataset.n === String(race.winners.length)) return;
        ol.dataset.n = String(race.winners.length);
        if (!race.winners.length) return;
        ol.innerHTML = race.winners.map(function (m, i) {
          return '<li class="' + (i === race.winningRank ? 'win' : '') + '"><span class="dotc" style="background:hsl(' + m.hue + ' 78% 58%)"></span>' + esc(m.name) + '</li>';
        }).join('');
      }
      function rlDraw() {
        var ctx = rlCv.getContext('2d');
        var S = race.stage;
        var z = rlBaseZoom() * cam.zoom;
        var dark = document.body.classList.contains('dark');
        var stroke = dark ? '#9CC6EE' : '#3370A8';
        var fill = dark ? 'rgba(156,198,238,.24)' : 'rgba(51,112,168,.22)';
        var hot = dark ? '#F0A3C2' : '#b8557f';
        var ink = dark ? '#EAF2FB' : '#14273A';
        var halo = dark ? 'rgba(7,11,24,.9)' : 'rgba(255,255,255,.92)';
        ctx.clearRect(0, 0, RLV.w, RLV.h);
        ctx.save();
        ctx.translate(RLV.w / 2 - cam.x * z, RLV.h / 2 - cam.y * z);
        ctx.scale(z, z);
        var top = cam.y - RLV.h / 2 / z - 2, bottom = cam.y + RLV.h / 2 / z + 2;
        ctx.lineWidth = 2 / z;
        S.entities.forEach(function (e) {
          if (e.dead || e.bottom < top || e.top > bottom) return;
          if (e.shape.type === 'polyline') {
            ctx.strokeStyle = stroke;
            ctx.beginPath();
            e.segs.forEach(function (sg) { ctx.moveTo(sg[0], sg[1]); ctx.lineTo(sg[2], sg[3]); });
            ctx.stroke();
          } else if (e.shape.type === 'circle') {
            ctx.fillStyle = e.life > 0 ? 'rgba(184,85,127,.28)' : fill;
            ctx.strokeStyle = e.life > 0 ? hot : stroke;
            ctx.beginPath(); ctx.arc(e.x, e.y, e.shape.radius, 0, 6.284);
            ctx.fill(); ctx.stroke();
          } else {
            var c = G.boxCorners(e);
            ctx.fillStyle = fill; ctx.strokeStyle = stroke;
            ctx.beginPath(); ctx.moveTo(c[0].x, c[0].y);
            for (var i = 1; i < 4; i++) ctx.lineTo(c[i].x, c[i].y);
            ctx.closePath(); ctx.fill(); ctx.stroke();
          }
        });
        ctx.strokeStyle = stroke; ctx.lineWidth = 4 / z;
        ctx.setLineDash([10 / z, 8 / z]);
        ctx.beginPath(); ctx.moveTo(-40, S.goalY); ctx.lineTo(80, S.goalY); ctx.stroke();
        ctx.setLineDash([]);
        race.marbles.forEach(function (m) {
          if (m.done || m.y < top || m.y > bottom) return;
          var light = 58 + 25 * Math.min(1, m.impact / 500);
          ctx.fillStyle = 'hsl(' + m.hue + ' 78% ' + light + '%)';
          ctx.beginPath(); ctx.arc(m.x, m.y, G.RL.radius, 0, 6.284); ctx.fill();
          if (race.useSkills) {
            ctx.strokeStyle = stroke; ctx.lineWidth = 1 / z;
            ctx.beginPath();
            ctx.arc(m.x, m.y, G.RL.radius + 2 / z, -Math.PI / 2, -Math.PI / 2 + 6.284 * (m.cool / m.coolMax));
            ctx.stroke();
          }
          ctx.save();
          ctx.translate(m.x, m.y + G.RL.radius + 2 / z);
          ctx.scale(1 / z, 1 / z);
          ctx.font = '800 12px "Noto Sans KR", sans-serif';
          ctx.textAlign = 'center';
          ctx.lineWidth = 3; ctx.strokeStyle = halo;
          ctx.strokeText(m.name, 0, 10);
          ctx.fillStyle = ink;
          ctx.fillText(m.name, 0, 10);
          ctx.restore();
        });
        ctx.restore();
        rlDrawMini();
      }
      function rlDrawMini() {
        var ctx = rlMini.getContext('2d');
        var S = race.stage;
        var Wd = rlMini.width, H = rlMini.height;
        var dark = document.body.classList.contains('dark');
        ctx.clearRect(0, 0, Wd, H);
        ctx.fillStyle = dark ? 'rgba(9,14,30,.92)' : 'rgba(255,255,255,.9)';
        ctx.fillRect(0, 0, Wd, H);
        var sy = H / (S.goalY + 8), sx = Wd / RLV.unit;
        ctx.fillStyle = dark ? 'rgba(156,198,238,.3)' : 'rgba(51,112,168,.3)';
        S.entities.forEach(function (e) {
          if (e.dead || e.shape.type === 'polyline') return;
          ctx.fillRect((e.x - 0.4) * sx, e.y * sy - 1, 3, 2);
        });
        ctx.strokeStyle = dark ? '#9CC6EE' : '#3370A8'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(0, S.goalY * sy); ctx.lineTo(Wd, S.goalY * sy); ctx.stroke();
        race.marbles.forEach(function (m) {
          if (m.done) return;
          ctx.fillStyle = 'hsl(' + m.hue + ' 78% 55%)';
          ctx.beginPath(); ctx.arc(m.x * sx, m.y * sy, 2.4, 0, 6.284); ctx.fill();
        });
        ctx.strokeStyle = dark ? 'rgba(191,213,235,.4)' : 'rgba(31,82,133,.4)'; ctx.lineWidth = 1;
        ctx.strokeRect(0.5, cam.y * sy - 14, Wd - 1, 28);
      }
      (function () {
        var sel = document.getElementById('rl-map');
        G.stagesList().forEach(function (st, i) { sel.insertAdjacentHTML('beforeend', '<option value="' + i + '">' + esc(st.title) + '</option>'); });
        sel.addEventListener('change', function () { rlMapIndex = Number(sel.value); rlBuild(); });
        try {
          var saved = localStorage.getItem('shuni-rl-names');
          if (saved) document.getElementById('rl-names').value = saved;
        } catch (e) {}
      })();
      document.getElementById('rl-names').addEventListener('blur', function (e) {
        var v = G.normalizeNames(e.target.value);
        if (v && v !== e.target.value) e.target.value = v;
        rlBuild();
      });
      document.getElementById('rl-skill').addEventListener('change', rlBuild);
      document.getElementById('rl-shuffle').addEventListener('click', rlBuild);
      document.getElementById('rl-start').addEventListener('click', rlStart);
      document.querySelectorAll('#rl-wintype button').forEach(function (b) {
        b.addEventListener('click', function () {
          rlWinType = b.dataset.w;
          document.querySelectorAll('#rl-wintype button').forEach(function (x) { x.classList.toggle('on', x === b); });
          rlApplyRank();
        });
      });
      document.querySelectorAll('#rl-speed button').forEach(function (b) {
        b.addEventListener('click', function () {
          rlSpeed = Number(b.dataset.s);
          document.querySelectorAll('#rl-speed button').forEach(function (x) { x.classList.toggle('on', x === b); });
          try { localStorage.setItem('shuni-rl-speed', String(rlSpeed)); } catch (e) {}
        });
      });
      (function () {
        var v = 2;
        try { v = Number(localStorage.getItem('shuni-rl-speed')) || 2; } catch (e) {}
        var btn = document.querySelector('#rl-speed button[data-s="' + v + '"]');
        if (btn) btn.click();
      })();
      document.getElementById('rl-rank-in').addEventListener('change', function (e) {
        rlWinType = 'custom';
        document.querySelectorAll('#rl-wintype button').forEach(function (x) { x.classList.remove('on'); });
        rlRank = Math.max(1, parseInt(e.target.value, 10) || 1);
        rlApplyRank();
      });
      rlBuild();

      /* spin wheel */
      var whCv = document.getElementById('wh-canvas');
      var whEntries = [], whSegs = [], whTurns = 0, whSpinning = false, whHist = [];

      function whRead() {
        whEntries = W.parseList(document.getElementById('wh-names').value);
        whSegs = W.segments(whEntries);
        document.getElementById('wh-msg').textContent = whEntries.length
          ? '항목 ' + whEntries.length + '개'
          : '항목을 적어 주세요';
        whDraw();
      }
      function whDraw() {
        var ctx = whCv.getContext('2d');
        var S = whCv.width, R = S / 2 - 6, cx = S / 2, cy = S / 2;
        var dark = document.body.classList.contains('dark');
        ctx.clearRect(0, 0, S, S);
        if (!whSegs.length) {
          ctx.strokeStyle = dark ? 'rgba(191,213,235,.34)' : 'rgba(31,82,133,.28)';
          ctx.lineWidth = 1;
          ctx.beginPath(); ctx.arc(cx, cy, R, 0, 6.284); ctx.stroke();
          return;
        }
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(whTurns * 6.283185307);
        whSegs.forEach(function (s, i) {
          var a0 = s.from * 6.283185307 - Math.PI / 2;
          var a1 = s.to * 6.283185307 - Math.PI / 2;
          ctx.fillStyle = PC[i % PC.length];
          ctx.globalAlpha = i % 2 ? 0.82 : 1;
          ctx.beginPath(); ctx.moveTo(0, 0); ctx.arc(0, 0, R, a0, a1); ctx.closePath(); ctx.fill();
          ctx.globalAlpha = 1;
          var mid = (a0 + a1) / 2;
          var span = s.to - s.from;
          if (span > 0.035) {
            ctx.save();
            ctx.rotate(mid);
            ctx.translate(R * 0.62, 0);
            ctx.rotate(Math.PI / 2);
            ctx.textAlign = 'center';
            ctx.font = '800 ' + Math.max(11, Math.min(17, 320 * span)) + 'px "Noto Sans KR", sans-serif';
            ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(6,12,26,.55)';
            var label = s.name.length > 9 ? s.name.slice(0, 8) + '…' : s.name;
            ctx.strokeText(label, 0, 0);
            ctx.fillStyle = '#fff';
            ctx.fillText(label, 0, 0);
            ctx.restore();
          }
        });
        ctx.restore();
        ctx.strokeStyle = dark ? 'rgba(191,213,235,.5)' : 'rgba(31,82,133,.4)';
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(cx, cy, R, 0, 6.284); ctx.stroke();
        ctx.fillStyle = dark ? '#070B18' : '#fff';
        ctx.beginPath(); ctx.arc(cx, cy, 26, 0, 6.284); ctx.fill(); ctx.stroke();
      }
      function whSpin() {
        if (whSpinning) return;
        whRead();
        if (!whEntries.length) { showToast('항목을 적어 주세요'); return; }
        if (whEntries.length === 1) { whFinish(0); return; }
        /* the winner is drawn first, then the wheel is animated onto it */
        var idx = W.pick(whEntries);
        var spins = 5 + Math.floor(Math.random() * 3);
        var from = whTurns % 1;
        var to = W.targetTurns(whSegs, idx, spins);
        whSpinning = true;
        document.getElementById('wh-out').classList.remove('hit');
        document.getElementById('wh-name').textContent = '…';
        var start = performance.now(), DUR = 4200;
        (function tick(now) {
          var p = Math.min(1, ((now || performance.now()) - start) / DUR);
          whTurns = from + (to - from) * W.easeOut(p);
          whDraw();
          if (p < 1) { requestAnimationFrame(tick); return; }
          whSpinning = false;
          whFinish(idx);
        })(start);
      }
      function whFinish(idx) {
        var name = whEntries[idx].name;
        var out = document.getElementById('wh-out');
        document.getElementById('wh-name').textContent = name;
        out.classList.remove('hit'); void out.offsetWidth; out.classList.add('hit');
        whHist.unshift(name);
        whHist = whHist.slice(0, 30);
        renderHist();
        SN.pop(window.innerWidth / 2, window.innerHeight / 2, 10);
        if (document.getElementById('wh-remove').checked) {
          var ta = document.getElementById('wh-names');
          var left = whEntries.filter(function (e, i) { return i !== idx; })
            .map(function (e) { return e.weight > 1 ? e.name + '*' + e.weight : e.name; });
          ta.value = left.join('\\n');
          whRead();
        }
      }
      function renderHist() {
        var el = document.getElementById('wh-hist');
        el.innerHTML = whHist.length
          ? whHist.map(function (n, i) { return '<div><i>' + (i + 1) + '</i><span>' + esc(n) + '</span></div>'; }).join('')
          : '<div><i>—</i><span style="color:var(--tx-dim)">아직 뽑은 기록이 없습니다</span></div>';
      }
      document.getElementById('wh-names').addEventListener('blur', whRead);
      document.getElementById('wh-spin').addEventListener('click', whSpin);
      document.getElementById('wh-reset').addEventListener('click', function () { whHist = []; renderHist(); });
      whRead(); renderHist();

      /* mode switch */
      document.querySelectorAll('#mode-seg .seg-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var mode = btn.dataset.mode;
          document.querySelectorAll('#mode-seg .seg-btn').forEach(function (b) { b.classList.toggle('active', b === btn); });
          document.getElementById('panel-ladder').style.display = mode === 'ladder' ? '' : 'none';
          document.getElementById('panel-marble').style.display = mode === 'marble' ? '' : 'none';
          document.getElementById('panel-wheel').style.display = mode === 'wheel' ? '' : 'none';
          if (mode === 'ladder') { ldSizeCanvas(); ldDrawBase(); if (ldPhase === 'play') { for (var k in ldDone) ldStrokeWhole(Number(k)); } }
          if (mode === 'wheel') whDraw();
          enableIframeAutoHeight();
        });
      });
      document.addEventListener('click', function (e) {
        if (e.target.closest && e.target.closest('.mode-toggle')) { setTimeout(function () { ldDrawBase(); whDraw(); }, 30); }
      });

      (async function () {
        await snCommon();
        SN.dataReady(); SN.reveal(); enableIframeAutoHeight();
      })();
    })();
"""


def build():
    extra = ('  <script src="maps.js?v=20260902a"></script>\n'
             '  <script src="engine.js?v=20260902a"></script>\n'
             '  <script src="wheel.js?v=20260902a"></script>\n')
    return page(slug="game", title="미니게임", desc="미니게임", root="../", body=BODY,
                css=CSS, script=SCRIPT, extra_head=extra, footer_mark="STAR ATLAS · LOG 08")
