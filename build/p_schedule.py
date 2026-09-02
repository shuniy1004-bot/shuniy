from shell import page, SHARED_TAIL

# Cell padding is 5px and the borders are 1px, so a band must pull back by
# exactly 6px on the right and 5px on the left or a seam shows between cells.
CSS = """
    .cal-top{display:flex;align-items:center;justify-content:space-between;gap:14px;margin:0 0 18px}
    .cal-top h2{margin:0;font-family:var(--font-serif);font-weight:400;font-size:calc(30px * var(--fs-title));letter-spacing:-.02em}
    .cal-nav{display:flex;gap:8px}
    .cal-nav button{
      width:36px;height:36px;border:1px solid var(--line);background:transparent;
      color:var(--tx);cursor:pointer;font-size:13px;line-height:1;transition:background 160ms ease;
    }
    .cal-nav button:hover{background:rgba(126,180,232,.16)}

    .cal-grid{display:grid;grid-template-columns:repeat(7,1fr);border-left:1px solid var(--line-soft);border-bottom:1px solid var(--line-soft)}
    .cal-dow{
      padding:10px 4px;border-top:1px solid var(--line-soft);border-right:1px solid var(--line-soft);
      text-align:center;color:var(--tx-dim);
      font-family:var(--font-serif);font-style:italic;font-size:calc(13.5px * var(--fs-label));
    }
    .cal-dow:first-child,.cal-dow:last-child{color:var(--accent-txt)}
    .cal-cell{
      position:relative;min-height:80px;padding:5px 5px 6px;
      border-top:1px solid var(--line-soft);border-right:1px solid var(--line-soft);
      overflow:hidden;
    }
    .cal-cell.hasband{overflow:visible}
    .cal-cell.other{opacity:.34}
    .cal-cell.has{cursor:pointer}
    .cal-cell.has:hover{background:rgba(126,180,232,.10)}
    .cal-cell.today{background:rgba(126,180,232,.16)}
    .cal-cell.hl{box-shadow:inset 0 0 0 1px var(--point)}
    .cal-date{display:block;margin:0 0 5px;font-family:var(--font-serif);font-style:italic;font-size:calc(14px * var(--fs-label));color:var(--tx-dim)}
    .cal-cell.today .cal-date{color:var(--accent-txt);font-weight:600}
    .ev{
      margin:0 0 3px;padding:2px 5px;border-left:2px solid var(--ec);background:var(--eb);
      color:var(--ec);font-size:calc(12.5px * var(--fs-label));font-weight:800;
      white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
    }
    /* Band spans cells. Negative margin must equal cell padding + border. */
    .band{
      position:relative;z-index:1;height:20px;margin:3px -6px 0 -5px;
      background:var(--eb);border-top:1px solid var(--ec);border-bottom:1px solid var(--ec);
      color:var(--ec);font-size:calc(12.5px * var(--fs-label));font-weight:800;line-height:18px;
    }
    .band span{display:block;padding:0 6px;white-space:nowrap;overflow:hidden}
    .band.b-start{margin-left:0;border-left:1px solid var(--ec)}
    .band.b-end{margin-right:0;border-right:1px solid var(--ec)}
    .cal-cell:nth-child(7n) .band{margin-right:0}
    .cal-cell:nth-child(7n+1) .band{margin-left:0}

    .up-item{
      display:grid;grid-template-columns:auto 1fr auto auto;gap:14px;align-items:baseline;
      padding:13px 2px;border-bottom:1px solid var(--line-soft);cursor:pointer;
    }
    .up-item:last-child{border-bottom:0}
    .up-item:hover{background:rgba(126,180,232,.08)}
    .up-d1{font-family:var(--font-serif);font-style:italic;font-size:calc(14px * var(--fs-label));color:var(--tx-dim);white-space:nowrap}
    .up-title{font-size:calc(15px * var(--fs-body));font-weight:700;line-height:1.5;min-width:0}
    .up-time{font-size:calc(13.5px * var(--fs-label));color:var(--tx-dim);white-space:nowrap}
    .up-badge{padding:3px 9px;border:1px solid var(--ec);color:var(--ec);background:var(--eb);font-size:calc(12px * var(--fs-label));font-weight:900;letter-spacing:.1em;white-space:nowrap}

    .m-date{margin:0 0 16px;font-family:var(--font-serif);font-style:italic;font-size:calc(21px * var(--fs-title))}
    .m-badge{display:inline-block;margin:0 0 10px;padding:3px 10px;border:1px solid var(--ec);color:var(--ec);background:var(--eb);font-size:calc(12px * var(--fs-label));font-weight:900;letter-spacing:.1em}
    .m-part{display:grid;grid-template-columns:74px 1fr;gap:12px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--line-soft)}
    .m-part .pt{font-family:var(--font-serif);font-style:italic;font-size:calc(14px * var(--fs-label));color:var(--tx-dim)}
    .m-part .pn{font-size:calc(15px * var(--fs-body));font-weight:700;line-height:1.5}
    .m-desc{margin-top:14px;color:var(--tx-soft);font-size:calc(14.5px * var(--fs-body));line-height:1.8;white-space:pre-wrap}

    @media (max-width:959px){
      .cal-cell{min-height:66px;padding:4px 4px 5px}
      .band{margin:3px -5px 0 -4px}
      .ev,.band{font-size:calc(12px * var(--fs-label))}
      .up-item{grid-template-columns:auto 1fr;gap:8px}
      .up-time,.up-badge{grid-column:2}
    }
"""

BODY = """    <div class="chapter-head rv">
      <div class="chapter-ghost" aria-hidden="true">Orbit</div>
      <p class="kicker" data-t="sc-kicker">LOG 03 · ORBIT</p>
      <h1><em data-t="sc-eyebrow">when the star is up</em>일정</h1>
      <p class="desc" data-t="sc-desc">방송 예정과 휴방을 달력으로 정리했습니다.</p>
    </div>

    <section class="sn-card rv">
      <div class="cal-top">
        <h2 id="calTitle">—</h2>
        <div class="cal-nav">
          <button type="button" id="calPrev" aria-label="이전 달">◂</button>
          <button type="button" id="calNext" aria-label="다음 달">▸</button>
        </div>
      </div>
      <div class="cal-grid" id="calGrid"></div>
    </section>

    <section class="sn-card rv" style="margin-top:22px">
      <p class="sn-kicker" data-t="sc-up">UPCOMING · 다가오는 일정</p>
      <div id="upcoming"></div>
    </section>

    <div class="ov" id="ov">
      <div class="ov-back"></div>
      <div class="ov-box">
        <button class="ov-x" type="button" id="ovClose" aria-label="닫기">✕</button>
        <div id="modal-body"></div>
      </div>
    </div>
"""

SCRIPT = SHARED_TAIL + """
    (function () {
      var DAYS = ['일','월','화','수','목','금','토'];   /* calendar header uses getDay(); admin days is 0=Mon, do not mix */
      var currentYear, currentMonth, allSchedule = [];

      function kind(t) { return t === '휴방' ? 'off' : 'on'; }
      function colorClass(s) { return 'c-' + (s.color || (kind(s.type) === 'off' ? 'pink' : 'green')); }

      function renderCalendar() {
        document.getElementById('calTitle').textContent = currentYear + '년 ' + (currentMonth + 1) + '월';
        var grid = document.getElementById('calGrid');
        var first = new Date(currentYear, currentMonth, 1);
        var last = new Date(currentYear, currentMonth + 1, 0);
        var startDay = first.getDay();
        var today = new Date();
        var html = DAYS.map(function (d) { return '<div class="cal-dow">' + d + '</div>'; }).join('');
        var prevLast = new Date(currentYear, currentMonth, 0).getDate();
        for (var i = startDay - 1; i >= 0; i--) html += '<div class="cal-cell other"><span class="cal-date">' + (prevLast - i) + '</span></div>';
        for (var d = 1; d <= last.getDate(); d++) {
          var dateStr = currentYear + '-' + String(currentMonth + 1).padStart(2, '0') + '-' + String(d).padStart(2, '0');
          var isToday = today.getFullYear() === currentYear && today.getMonth() === currentMonth && today.getDate() === d;
          var events = allSchedule.filter(function (s) { return s.date <= dateStr && dateStr <= (s.end_date || s.date); });
          var hl = events.some(function (e) { return e.highlight; });
          var bandUsed = false;                       /* one band per cell */
          var evHtml = events.map(function (e) {
            var ranged = e.end_date && e.end_date !== e.date;
            if (ranged) {
              if (bandUsed) return '';
              bandUsed = true;
              var caps = (dateStr === e.date ? ' b-start' : '') + (dateStr === e.end_date ? ' b-end' : '');
              var btxt = (e.time ? e.time + ' ' : '') + (e.title || (kind(e.type) === 'off' ? '휴방' : '방송'));
              return '<div class="band' + caps + ' ' + colorClass(e) + '">' + (dateStr === e.date ? '<span>' + esc(btxt) + '</span>' : '') + '</div>';
            }
            var label = (e.time ? e.time + ' ' : '') + (e.title || (kind(e.type) === 'off' ? '휴방' : '방송'));
            return '<div class="ev ' + colorClass(e) + '" title="' + esc(label) + '">' + esc(label) + '</div>';
          }).join('');
          var cls = 'cal-cell' + (isToday ? ' today' : '') + (events.length ? ' has' : '') + (hl ? ' hl' : '') + (bandUsed ? ' hasband' : '');
          var click = events.length ? ' data-day="' + dateStr + '"' : '';
          html += '<div class="' + cls + '"' + click + '><span class="cal-date">' + d + '</span>' + evHtml + '</div>';
        }
        var totalCells = startDay + last.getDate();
        var rem = totalCells % 7 === 0 ? 0 : 7 - (totalCells % 7);
        for (var k = 1; k <= rem; k++) html += '<div class="cal-cell other"><span class="cal-date">' + k + '</span></div>';
        grid.innerHTML = html;
        grid.querySelectorAll('[data-day]').forEach(function (c) {
          c.addEventListener('click', function () { openModal(c.dataset.day); });
        });
      }

      function renderUpcoming() {
        var now = new Date();
        var today = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0');
        var upcoming = allSchedule.filter(function (s) { return (s.end_date || s.date) >= today; }).slice(0, 12);
        var el = document.getElementById('upcoming');
        if (!upcoming.length) { el.innerHTML = '<div class="sn-empty">다가오는 일정이 없습니다</div>'; return; }
        el.innerHTML = upcoming.map(function (s) {
          var dd = new Date(s.date + 'T00:00:00');
          var k = kind(s.type);
          var label = k === 'off' ? '휴방' : '방송';
          var times = [s.time, s.time2].filter(Boolean).join(' · ');
          return '<div class="up-item ' + colorClass(s) + '" data-day="' + esc(s.date) + '">' +
            '<span class="up-d1">' + String(dd.getMonth() + 1).padStart(2, '0') + '-' + String(dd.getDate()).padStart(2, '0') + ' (' + DAYS[dd.getDay()] + ')</span>' +
            '<span class="up-title">' + esc(s.title || label) + '</span>' +
            (times ? '<span class="up-time">' + esc(times) + '</span>' : '<span></span>') +
            '<span class="up-badge">' + label + '</span></div>';
        }).join('');
        el.querySelectorAll('[data-day]').forEach(function (r) {
          r.addEventListener('click', function () { openModal(r.dataset.day); });
        });
      }

      function openModal(dateStr) {
        var events = allSchedule.filter(function (s) { return s.date === dateStr; });
        if (!events.length) events = allSchedule.filter(function (s) { return s.date <= dateStr && dateStr <= (s.end_date || s.date); });
        if (!events.length) return;
        var dd = new Date(dateStr + 'T00:00:00');
        var html = '<div class="m-date">' + dateStr + ' (' + DAYS[dd.getDay()] + ')</div>';
        events.forEach(function (s) {
          var k = kind(s.type);
          html += '<div class="m-badge ' + colorClass(s) + '">' + (k === 'off' ? '휴방' : '방송') + '</div>';
          html += '<div class="m-part"><div class="pt">' + (s.time ? esc(s.time) : '1부') + '</div><div class="pn">' + esc(s.title || (k === 'off' ? '휴방' : '방송')) + '</div></div>';
          if (s.title2 || s.time2) html += '<div class="m-part"><div class="pt">' + (s.time2 ? esc(s.time2) : '2부') + '</div><div class="pn">' + esc(s.title2 || '방송') + '</div></div>';
          if (s.description) html += '<div class="m-desc">' + esc(s.description) + '</div>';
        });
        document.getElementById('modal-body').innerHTML = html;
        placeOverlay(document.getElementById('ov'));
      }

      document.getElementById('ovClose').addEventListener('click', function () { hideOverlay(document.getElementById('ov')); });
      document.getElementById('calPrev').addEventListener('click', function () { changeMonth(-1); });
      document.getElementById('calNext').addEventListener('click', function () { changeMonth(1); });
      function changeMonth(d) {
        currentMonth += d;
        if (currentMonth > 11) { currentMonth = 0; currentYear++; }
        if (currentMonth < 0) { currentMonth = 11; currentYear--; }
        renderCalendar(); enableIframeAutoHeight();
      }

      async function init() {
        var now = new Date();
        currentYear = now.getFullYear(); currentMonth = now.getMonth();
        renderCalendar(); renderUpcoming();
        await snCommon();
        try { allSchedule = await fetchAll('schedule', { order: 'date', asc: true }); }
        catch (e) { allSchedule = []; }
        renderCalendar(); renderUpcoming();
        SN.dataReady(); SN.reveal(); enableIframeAutoHeight();
      }
      init();
    })();
"""


def build():
    return page(slug="schedule", title="일정", desc="일정", root="../", body=BODY,
                css=CSS, script=SCRIPT, footer_mark="STAR ATLAS · LOG 03")
