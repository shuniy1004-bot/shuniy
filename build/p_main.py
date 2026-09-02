from shell import page, SHARED_TAIL

CSS = """
    .mn-hero{
      position:relative;display:grid;grid-template-columns:1.05fr .95fr;gap:0;
      border:1px solid var(--line);margin:0 0 22px;overflow:hidden;
    }
    .mn-shot{position:relative;min-height:420px}
    .mn-shot img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 28%}
    .mn-shot .wash{position:absolute;inset:0;background:linear-gradient(90deg,transparent 42%,rgba(233,242,251,.94))}
    body.dark .mn-shot .wash{background:linear-gradient(90deg,transparent 42%,rgba(7,11,24,.95))}
    .mn-shot .frame{
      position:absolute;left:16px;top:14px;padding:4px 9px;
      background:rgba(255,255,255,.82);color:var(--accent-txt);
      backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);
      font-size:calc(12px * var(--fs-label));font-weight:800;letter-spacing:.24em;
    }
    body.dark .mn-shot .frame{background:rgba(6,11,24,.6)}

    .mn-plate{
      position:relative;display:grid;align-content:center;gap:0;
      padding:44px 40px;background:var(--glass);
      backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
    }
    .mn-plate .ghost{
      position:absolute;right:-1vw;top:-.2em;z-index:0;
      color:transparent;-webkit-text-stroke:1px rgba(31,82,133,.14);
      font-family:var(--font-serif);font-style:italic;
      font-size:calc(190px * var(--fs-display));letter-spacing:-.06em;
      user-select:none;pointer-events:none;white-space:nowrap;
    }
    body.dark .mn-plate .ghost{-webkit-text-stroke-color:rgba(191,213,235,.15)}
    .mn-plate > *{position:relative;z-index:1}
    .mn-kick{
      display:flex;align-items:center;gap:12px;margin:0 0 14px;
      color:var(--accent-txt);font-family:var(--font-serif);
      font-size:calc(13.5px * var(--fs-label));font-style:italic;letter-spacing:.14em;
    }
    .mn-kick::after{content:"";flex:1;height:1px;background:var(--line)}
    .mn-name{
      margin:0;font-family:var(--font-serif);font-weight:400;
      font-size:calc(84px * var(--fs-display));line-height:.86;letter-spacing:-.05em;
    }
    .mn-name em{display:block;font-size:.26em;letter-spacing:.02em;margin-bottom:.5em;font-style:italic}
    .mn-en{margin:14px 0 0;color:var(--tx-dim);font-size:calc(13px * var(--fs-label));font-weight:800;letter-spacing:.34em}
    .mn-tag{margin:18px 0 0;color:var(--tx-soft);font-size:calc(16px * var(--fs-body));line-height:1.75}
    .mn-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
    .mn-acts{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}

    .mn-grid{display:grid;grid-template-columns:minmax(280px,360px) 1fr;gap:22px;align-items:start}
    .mn-col{display:grid;gap:22px}

    .mn-ava{display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:center;padding-bottom:20px;border-bottom:1px solid var(--line-soft);margin-bottom:16px}
    .mn-ava .ring{position:relative;width:78px;height:78px;border-radius:50%;border:1px solid var(--line);padding:5px;cursor:pointer;transition:transform 160ms ease}
    .mn-ava .ring:hover{transform:scale(1.05)}
    .mn-ava .ring.sn-bump{animation:mbump 520ms cubic-bezier(.2,.75,.25,1)}
    @keyframes mbump{30%{transform:scale(1.14)}60%{transform:scale(.95)}}
    .mn-ava img{width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;background:var(--main)}
    .mn-ava .ini{position:absolute;inset:5px;display:grid;place-items:center;border-radius:50%;background:var(--main);color:#14273A;font-family:var(--font-serif);font-style:italic;font-size:30px}
    .mn-ava .who b{display:block;font-family:var(--font-serif);font-weight:400;font-size:calc(24px * var(--fs-title));letter-spacing:-.02em;line-height:1.1}
    .mn-ava .who span{display:block;margin-top:5px;color:var(--tx-dim);font-size:calc(12px * var(--fs-label));font-weight:800;letter-spacing:.3em}

    .week-strip{display:grid;grid-template-columns:repeat(7,1fr);border:1px solid var(--line-soft)}
    .week-cell{display:grid;gap:6px;justify-items:center;padding:14px 2px 12px;border-right:1px solid var(--line-soft);min-width:0}
    .week-cell:last-child{border-right:0}
    .week-cell .d{font-family:var(--font-serif);font-style:italic;font-size:calc(13.5px * var(--fs-label));color:var(--tx-dim)}
    .week-cell .t{font-size:calc(13.5px * var(--fs-body));font-weight:800;white-space:nowrap}
    .week-cell.off .t{color:var(--tx-dim);font-weight:500}
    .week-cell.today{background:rgba(126,180,232,.14)}
    .week-cell.today .d{color:var(--accent-txt)}

    .link-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
    .link-cell{display:grid;gap:5px;padding:16px;border:1px solid var(--line);transition:background 160ms ease}
    .link-cell:hover{background:rgba(126,180,232,.14)}
    .link-cell b{font-size:calc(13.5px * var(--fs-label));font-weight:900;letter-spacing:.14em}
    .link-cell span{color:var(--tx-dim);font-size:calc(13.5px * var(--fs-label));letter-spacing:.04em}

    .mn-notice{display:grid}
    .mn-nrow{display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:baseline;padding:13px 2px;border-bottom:1px solid var(--line-soft)}
    .mn-nrow:last-child{border-bottom:0}
    .mn-nrow .pin{padding:2px 8px;border:1px solid var(--line);color:var(--accent-txt);font-size:calc(12px * var(--fs-label));font-weight:900;letter-spacing:.1em}
    .mn-nrow .tt{font-size:calc(15px * var(--fs-body));font-weight:700;line-height:1.5;min-width:0}
    .mn-nrow .dt{font-family:var(--font-serif);font-style:italic;font-size:calc(13.5px * var(--fs-label));color:var(--tx-dim);white-space:nowrap}

    .mn-map{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
    .mn-mcell{background:transparent;font-family:inherit;text-align:left}
    .mn-mcell{
      display:grid;gap:6px;padding:18px 16px;border:1px solid var(--line);
      transition:background 160ms ease;
    }
    .mn-mcell:hover{background:rgba(126,180,232,.14)}
    .mn-mcell i{font-style:normal;font-family:var(--font-serif);font-size:calc(13.5px * var(--fs-label));color:var(--tx-dim)}
    .mn-mcell b{font-size:calc(15px * var(--fs-body));font-weight:800;letter-spacing:.02em}

    @media (max-width:959px){
      .mn-hero{grid-template-columns:1fr}
      .mn-shot{min-height:300px}
      .mn-shot .wash{background:linear-gradient(0deg,rgba(233,242,251,.94),transparent 55%)}
      body.dark .mn-shot .wash{background:linear-gradient(0deg,rgba(7,11,24,.95),transparent 55%)}
      .mn-plate{padding:30px 22px}
      .mn-plate .ghost{display:none}
      .mn-name{font-size:calc(58px * var(--fs-display))}
      .mn-grid{grid-template-columns:1fr}
      .link-grid,.mn-map{grid-template-columns:repeat(2,1fr)}
    }
"""

BODY = """    <section class="mn-hero rv">
      <div class="mn-shot">
        <img id="mn-art" src="assets/shuni-crosswalk.webp" alt="슈니" referrerpolicy="no-referrer">
        <div class="wash" aria-hidden="true"></div>
        <span class="frame" data-t="mn-frame">STATION k4187421</span>
      </div>
      <div class="mn-plate">
        <div class="ghost" aria-hidden="true">Shuni</div>
        <p class="mn-kick" data-t="mn-kicker">SHUNI OFFICIAL · 관측 기록</p>
        <h1 class="mn-name"><em data-t="mn-eyebrow">the little star</em><span data-hook="name">슈니</span></h1>
        <p class="mn-en" data-hook="name_en">SHUNI</p>
        <p class="mn-tag" data-hook="tagline">너희는 내 우주야</p>
        <div class="mn-chips" id="mn-keywords"></div>
        <div class="mn-acts">
          <a class="sn-btn-solid" id="mn-live" href="https://www.sooplive.com/station/k4187421" target="_blank" rel="noreferrer" data-t="mn-live">방송국 가기 ↗</a>
          <a class="sn-btn" href="profile/" data-t="mn-more">프로필 자세히 <span aria-hidden="true">✦</span></a>
        </div>
      </div>
    </section>

    <div class="mn-grid">
      <div class="mn-col">
        <section class="sn-card rv">
          <p class="sn-kicker" data-t="mn-file">OBSERVER FILE · 기본 기록</p>
          <div class="mn-ava">
            <div class="ring" id="avatarWrap" role="button" tabindex="0" aria-label="프로필 사진">
              <img id="avatar" class="avatar" alt="슈니 프로필 사진"
                   src="https://profile.img.sooplive.co.kr/LOGO/k4/k4187421/k4187421.jpg"
                   referrerpolicy="no-referrer" onerror="snAvatarFallback(this)">
              <span class="ini" id="avatar-ini" hidden>S</span>
            </div>
            <div class="who">
              <b data-hook="name2">슈니</b>
              <span data-hook="name_en2">SHUNI</span>
            </div>
          </div>
          <div class="sn-rows">
            <div class="sn-row"><b>BIRTHDAY</b><span><span data-hook="birthday-txt">10월 4일</span> · <b class="dd" id="mn-dday">D-?</b></span></div>
            <div class="sn-row"><b>DEBUT</b><span><span data-hook="debut">2025.08.12</span> · <b class="dd" id="mn-dplus">D+?</b></span></div>
            <div class="sn-row"><b>AGENCY</b><span data-hook="agency">개인세</span></div>
            <div class="sn-row"><b>FANDOM</b><span data-hook="fan_name">슈몽</span></div>
            <div class="sn-row" id="mn-row-mbti" hidden><b>MBTI</b><span data-hook="mbti"></span></div>
            <div class="sn-row"><b>SHOWTIME</b><span data-hook="schedule">매일 저녁 7시</span></div>
          </div>
        </section>

        <section class="sn-card rv">
          <p class="sn-kicker" data-t="mn-about">SIGNAL · 소개</p>
          <p style="margin:0;color:var(--tx-soft);font-size:calc(15.5px * var(--fs-body));line-height:1.85" data-hook="intro">
            별과 달, 밤하늘을 모티브로 하는 개인세 버추얼 슈니입니다.
            매일 저녁 7시에 켜서 게임하고 소통하고 노래해요.
          </p>
        </section>
      </div>

      <div class="mn-col">
        <section class="sn-card rv">
          <p class="sn-kicker" data-t="mn-week">WEEKLY ORBIT · 이번 주 방송</p>
          <div class="week-strip" id="week"></div>
        </section>

        <section class="sn-card rv">
          <p class="sn-kicker" data-t="mn-notice">LATEST LOG · 최근 공지</p>
          <div class="mn-notice" id="mn-notice"></div>
          <div style="margin-top:16px"><a class="sn-btn" href="notice/" data-t="mn-notice-all">공지 전체 보기 <span aria-hidden="true">✦</span></a></div>
        </section>

        <section class="sn-card rv">
          <p class="sn-kicker" data-t="mn-links">CONSTELLATION MAP · 슈니를 만나는 곳</p>
          <div class="link-grid" id="links"></div>
        </section>
      </div>
    </div>

    <section class="sn-card rv" style="margin-top:22px">
      <p class="sn-kicker" data-t="mn-pages">STAR ATLAS · 페이지</p>
      <div class="mn-map">
        <a class="mn-mcell" href="profile/"><i>01</i><b>프로필</b></a>
        <a class="mn-mcell" href="notice/"><i>02</i><b>공지</b></a>
        <a class="mn-mcell" href="schedule/"><i>03</i><b>일정</b></a>
        <a class="mn-mcell" href="song/"><i>04</i><b>노래책</b></a>
        <a class="mn-mcell" href="dress/"><i>05</i><b>옷장</b></a>
        <a class="mn-mcell" href="work/"><i>06</i><b>업보</b></a>
        <a class="mn-mcell" href="diary/"><i>07</i><b>일기</b></a>
        <a class="mn-mcell" href="game/"><i>08</i><b>미니게임</b></a>
      </div>
    </section>
"""

SCRIPT = SHARED_TAIL + """
    (function () {
      var esc = SN.esc, txt = SN.txt;
      var D = {
        name:'슈니', name_en:'SHUNI', soop_id:'k4187421',
        tagline:'너희는 내 우주야', main_art:'assets/shuni-crosswalk.webp',
        intro:'별과 달, 밤하늘을 모티브로 하는 개인세 버추얼 슈니입니다.\\n매일 저녁 7시에 켜서 게임하고 소통하고 노래해요.',
        birthday:'10-04', debut:'2025.08.12', agency:'개인세', fan_name:'슈몽',
        schedule:'매일 저녁 7시',
        keywords:['소통','게임','노래','배틀그라운드','별자리'],
        week:['19:00','19:00','19:00','19:00','19:00','19:00','19:00'],
        links:{ soop:'https://www.sooplive.com/station/k4187421',
                youtube:'https://www.youtube.com/@shuni_0812',
                x:'https://x.com/shuni_1', cafe:'' }
      };
      function arr(v, fb){
        if (Array.isArray(v)) return v;
        if (typeof v === 'string' && v.trim()) return v.split(/\\n|,/).map(function (s) { return s.trim(); }).filter(Boolean);
        return fb;
      }
      function hook(k, v){
        document.querySelectorAll('[data-hook="' + k + '"]').forEach(function (el) {
          if (v != null && txt(v).trim() !== '') el.innerHTML = esc(v).replace(/\\n/g, '<br>');
        });
      }
      function renderWeek(week){
        var el = document.getElementById('week'); if (!el) return;
        var DW = ['월','화','수','목','금','토','일'];
        var todayIdx = (new Date().getDay() + 6) % 7;   /* JS 0=Sun -> our 0=Mon */
        el.innerHTML = DW.map(function (d, i) {
          var t = txt(week && week[i] != null ? week[i] : '').trim();
          var off = !t || t === '휴방' || t === '-';
          return '<div class="week-cell' + (off ? ' off' : '') + (i === todayIdx ? ' today' : '') + '">' +
                 '<span class="d">' + d + '</span><span class="t">' + (off ? '휴방' : esc(t)) + '</span></div>';
        }).join('');
      }
      function renderLinks(L){
        var el = document.getElementById('links'); if (!el) return;
        L = L || {};
        var defs = [['SOOP','방송국',L.soop],['YOUTUBE','유튜브',L.youtube],['X','SNS',L.x],['CAFE','팬카페',L.cafe]];
        el.innerHTML = defs.filter(function (d) { return txt(d[2]).trim() !== ''; }).map(function (d) {
          return '<a class="link-cell" href="' + esc(d[2]) + '" target="_blank" rel="noreferrer"><b>' + d[0] + ' ↗</b><span>' + d[1] + '</span></a>';
        }).join('');
        var lv = document.getElementById('mn-live');
        if (lv && txt(L.soop).trim()) lv.href = txt(L.soop);
      }
      function apply(d){
        d = d || {};
        var g = function (k) {
          var v = d[k];
          return (v === undefined || v === null || txt(v).trim() === '') ? D[k] : v;
        };
        hook('name', g('name')); hook('name2', g('name'));
        var en = txt(g('name_en')).split('').join(' ').replace(/\\s{2,}/g, '  ');
        hook('name_en', en); hook('name_en2', en);
        hook('tagline', g('tagline')); hook('intro', g('intro'));
        hook('debut', g('debut')); hook('agency', g('agency'));
        hook('fan_name', g('fan_name')); hook('schedule', g('schedule'));

        var bd = txt(g('birthday')), bp = bd.split('-');
        if (bp.length === 2) hook('birthday-txt', (+bp[0]) + '월 ' + (+bp[1]) + '일');
        var n = SN.dday(bd), dd = document.getElementById('mn-dday');
        if (dd) dd.textContent = n == null ? '' : (n === 0 ? 'TODAY ✦' : 'D-' + n);
        var dp = SN.dplus(txt(g('debut'))), de = document.getElementById('mn-dplus');
        if (de) de.textContent = dp == null ? '' : 'D+' + dp;

        var mb = txt(d.mbti).trim(), row = document.getElementById('mn-row-mbti');
        if (row && mb) { row.hidden = false; hook('mbti', mb); }

        var art = txt(d.main_art).trim(), ae = document.getElementById('mn-art');
        if (ae && art) ae.src = art;
        var av = document.getElementById('avatar');
        var direct = txt(d.avatar).trim();
        if (av) av.src = direct || SN.soopAvatar(txt(g('soop_id'))) || av.src;
        var ini = document.getElementById('avatar-ini');
        if (ini) ini.textContent = (txt(g('name_en')).charAt(0) || 'S').toUpperCase();

        var kw = document.getElementById('mn-keywords');
        if (kw) kw.innerHTML = arr(d.keywords, D.keywords).map(function (k) {
          return '<span class="sn-chip">#' + esc(String(k).replace(/^#/, '')) + '</span>';
        }).join('');
        renderWeek(Array.isArray(d.week) && d.week.length === 7 ? d.week : D.week);
        renderLinks(d.links && typeof d.links === 'object' ? d.links : D.links);
      }

      function renderNotice(rows){
        var el = document.getElementById('mn-notice'); if (!el) return;
        rows = rows || [];
        var all = rows.filter(function (n) { return n.pinned; })
                 .concat(rows.filter(function (n) { return !n.pinned; })).slice(0, 4);
        if (!all.length) { el.innerHTML = '<div class="sn-empty">등록된 공지가 없습니다</div>'; return; }
        el.innerHTML = all.map(function (n) {
          var d = new Date(n.created_at);
          var ds = isNaN(d) ? '' : d.getFullYear() + '.' + String(d.getMonth() + 1).padStart(2, '0') + '.' + String(d.getDate()).padStart(2, '0');
          return '<a class="mn-nrow" href="notice/">' +
                 (n.pinned ? '<span class="pin">고정</span>' : '<span></span>') +
                 '<span class="tt">' + esc(n.title) + '</span>' +
                 '<span class="dt">' + ds + '</span></a>';
        }).join('');
      }

      async function load(){
        var d = await snCommon();
        apply(d);
        try { renderNotice(await fetchAll('notice', { order: 'created_at', asc: false })); }
        catch (e) { renderNotice([]); }
        finally { SN.dataReady(); SN.reveal(); }
      }
      apply({});
      renderNotice([]);
      load();

      var wrap = document.getElementById('avatarWrap');
      if (wrap) {
        var tap = function () {
          SN.bump(wrap);
          var r = wrap.getBoundingClientRect();
          SN.pop(r.left + r.width / 2, r.top + r.height / 2, 6);
        };
        wrap.addEventListener('click', tap);
        wrap.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tap(); } });
      }
    })();
"""


def build():
    return page(slug="", title="홈", desc="메인", root="", body=BODY,
                css=CSS, script=SCRIPT, footer_mark="STAR ATLAS · HOME")
