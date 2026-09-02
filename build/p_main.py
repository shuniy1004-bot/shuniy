from shell import page, SHARED_TAIL

CSS = """
    /* One screen cover. Photo and content are separate layers: the photo fills
       the box, the copy sits on top in percentages of that same box, so nothing
       depends on vh (the SOOP app hands an iframe a very tall viewport). */
    /* The shared sub page ground points at ../assets, which does not exist
       from the site root, and the cover fills the screen anyway. */
    body.sn-home{overflow-x:hidden;background-image:none}
    body.sn-home.dark{background-image:none}
    .sn-cover{position:relative;width:100%;overflow:hidden;isolation:isolate;background:var(--cover-b)}
    body:not(.embed) .sn-cover{height:100svh;min-height:640px}
    body.embed .sn-cover{aspect-ratio:16/9;min-height:600px}

    .cv-photo{
      position:absolute;z-index:0;inset:0;width:100%;height:100%;
      object-fit:cover;object-position:58% 26%;
      filter:saturate(.94) contrast(1.03);transform:scale(1.015);
    }
    .cv-wash{
      position:absolute;z-index:1;inset:0;
      background:
        linear-gradient(270deg,rgba(233,242,251,.86) 0%,rgba(233,242,251,.46) 2.4%,rgba(233,242,251,.16) 6%,transparent 11%),
        linear-gradient(0deg,rgba(233,242,251,.92) 0%,rgba(233,242,251,.42) 12%,transparent 34%),
        linear-gradient(94deg,rgba(233,242,251,.97) 0%,rgba(233,242,251,.86) 22%,
                              rgba(233,242,251,.22) 52%,rgba(233,242,251,.14) 100%);
    }
    body.dark .cv-wash{
      background:
        linear-gradient(270deg,rgba(4,7,18,.84) 0%,rgba(4,7,18,.44) 2.4%,rgba(4,7,18,.16) 6%,transparent 11%),
        linear-gradient(0deg,rgba(4,7,18,.90) 0%,rgba(4,7,18,.44) 12%,transparent 34%),
        linear-gradient(94deg,rgba(6,10,24,.95) 0%,rgba(8,13,30,.82) 22%,
                              rgba(8,13,30,.18) 52%,rgba(4,7,18,.24) 100%);
    }
    /* The fan characters drift between the photo and the copy. The loader moves
       both layers inside the cover, otherwise they paint over the whole section:
       an outside element's z-index cannot lose to a box inside another context. */
    body.sn-home #snMongs,body.sn-home #snStars{position:absolute;z-index:2}
    .cv-in{position:absolute;z-index:3;inset:0;pointer-events:none}
    .cv-in a,.cv-in button{pointer-events:auto}

    .cv-copy{position:absolute;top:23%;left:6.3%;width:min(44%,720px)}
    .cv-vol{
      display:flex;align-items:center;gap:13px;margin:0 0 18px;
      color:var(--tx-soft);font-family:var(--font-serif);font-style:italic;font-weight:600;
      font-size:calc(13.5px * var(--fs-label));letter-spacing:.12em;white-space:nowrap;
    }
    .cv-vol span{width:44px;height:1px;background:var(--line)}
    .cv-copy h1{
      margin:0;font-family:var(--font-serif);font-weight:400;
      font-size:clamp(64px,7vw,136px);line-height:.8;letter-spacing:-.06em;
      text-shadow:0 6px 30px rgba(7,11,24,.14);
    }
    body.dark .cv-copy h1{text-shadow:0 6px 30px rgba(0,0,0,.5)}
    .cv-copy h1 em{display:block;margin:0 0 .3em .06em;font-size:.28em;font-style:italic;letter-spacing:-.02em}
    .cv-sub{margin:30px 0 0;font-size:clamp(16px,1.25vw,24px);font-weight:700;line-height:1.6}
    .cv-acts{display:flex;flex-wrap:wrap;align-items:center;gap:34px;margin-top:26px}
    .cv-meet{
      display:inline-flex;align-items:center;gap:34px;padding:13px 0;
      border-bottom:1px solid var(--line);
      font-size:calc(13px * var(--fs-label));font-weight:900;letter-spacing:.16em;
      transition:gap 180ms ease,opacity 180ms ease;
    }
    .cv-meet:hover,.cv-meet:focus-visible{gap:44px;opacity:.82}
    .cv-meet i{font-style:normal;font-weight:900}
    .cv-signal{
      display:inline-flex;align-items:center;gap:9px;padding:13px 0;
      border:0;background:none;color:var(--tx);cursor:pointer;
      font-size:calc(13px * var(--fs-label));font-weight:900;letter-spacing:.16em;
      transition:opacity 160ms ease;
    }
    .cv-signal:hover{opacity:.82}
    .cv-signal b{color:var(--accent-txt);font-weight:700}

    .cv-quote{
      position:absolute;right:5.5%;bottom:14%;width:min(24%,392px);
      padding:24px 26px;border:1px solid var(--line);background:var(--glass-deep);
      backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
    }
    .cv-quote p{margin:0;font-family:var(--font-serif);font-size:clamp(16px,1.15vw,22px);font-weight:700;line-height:1.55}
    .cv-quote .cap{display:block;margin-top:16px;color:var(--tx-soft);font-size:calc(12px * var(--fs-label));font-weight:800;letter-spacing:.14em}
    .cv-mark{
      position:absolute;top:-30px;right:22px;
      display:grid;place-items:center;overflow:hidden;
      width:clamp(52px,3.6vw,68px);aspect-ratio:1;padding:0;
      border:1px solid var(--line);border-radius:50%;
      background:var(--main);color:var(--ink);cursor:pointer;
      font-family:var(--font-serif);font-size:calc(20px * var(--fs-title));
      transition:transform 160ms ease;
    }
    .cv-mark img{width:100%;height:100%;object-fit:cover;display:block}
    .cv-mark:hover{transform:scale(1.08)}
    .cv-mark.bump{animation:cvbump 500ms cubic-bezier(.2,.75,.25,1)}
    @keyframes cvbump{30%{transform:scale(1.2)}60%{transform:scale(.95)}}

    .cv-side{
      position:absolute;right:1.4%;top:16%;
      color:var(--tx);font-size:calc(12px * var(--fs-label));font-weight:900;letter-spacing:.28em;
      writing-mode:vertical-rl;
    }

    .cover-foot{
      position:absolute;z-index:3;right:3.2%;bottom:3.6%;left:3.2%;
      display:flex;justify-content:space-between;align-items:center;gap:16px;
      color:var(--tx);font-size:calc(12.5px * var(--fs-label));font-weight:700;letter-spacing:.12em;
    }
    .cover-foot b{color:var(--tx);font-size:calc(12px * var(--fs-label));font-weight:900}

    @media (max-width:1200px){.cv-quote{right:3.4%;width:28%}}
    /* Under the SOOP embed width the copy takes the full box and the quote card
       moves below it, because a 28% card next to a 64px headline is unreadable. */
    @media (max-width:959px){
      body.embed .sn-cover,body:not(.embed) .sn-cover{height:auto;aspect-ratio:auto;min-height:0;padding-bottom:26px}
      .cv-photo{position:relative;height:clamp(300px,72vw,520px)}
      .cv-wash{height:clamp(300px,72vw,520px);bottom:auto}
      body.sn-home #snMongs,body.sn-home #snStars{z-index:0}
      /* A static box drops its z-index, so the wash would paint over the copy. */
      .cv-in{position:relative;z-index:3;padding:26px 6vw 0}
      .cv-copy{position:static;width:auto}
      .cv-copy h1{font-size:clamp(56px,15vw,92px)}
      .cv-sub{font-size:17px;margin-top:22px}
      .cv-acts{gap:20px;margin-top:20px}
      .cv-quote{position:static;width:auto;margin-top:40px}
      .cv-mark{top:-28px;right:18px}
      .cv-side{display:none}
      .cover-foot{position:relative;z-index:3;padding:0 6vw;margin-top:24px;flex-wrap:wrap;gap:8px}
    }
"""

BODY = """    <img class="cv-photo" id="hero-bg" src="assets/shuni-crosswalk.webp" alt="슈니 메인 사진" referrerpolicy="no-referrer">
    <div class="cv-wash" aria-hidden="true"></div>

    <div class="cv-in">
      <div class="cv-copy rv">
        <p class="cv-vol"><span data-t="mn-vol">VOL. 01</span> <span aria-hidden="true"></span> <b id="hero-date">OCTOBER 4</b></p>
        <h1><em data-t="mn-eyebrow">the little star</em><span data-hook="name_en">SHUNI</span></h1>
        <p class="cv-sub" data-hook="tagline">밤하늘을 건너온 작은 별,<br>슈니입니다.</p>
        <div class="cv-acts">
          <a class="cv-meet" id="link-youtube" href="https://www.youtube.com/@shuni_0812" target="_blank" rel="noreferrer"><span data-t="mn-meet">MEET SHUNI</span> <i aria-hidden="true">↗</i></a>
          <button class="cv-signal" type="button" data-letter><b>✦</b> <span data-t="mn-signal">SEND A SIGNAL</span></button>
        </div>
      </div>

      <aside class="cv-quote rv">
        <button class="cv-mark" id="star-mark" type="button" aria-label="슈니 프로필 사진">
          <img id="avatar-img" alt="" referrerpolicy="no-referrer" onerror="snAvatarFallback(this)">
          <span id="avatar-ini" hidden>✦</span>
        </button>
        <p data-hook="quote">"너희는 내 우주야"</p>
        <span class="cap" data-t="mn-cap">TALK · GAME · SING</span>
      </aside>

      <div class="cv-side" data-t="mn-side">LITTLE STAR SHUNI</div>
    </div>
"""

SCRIPT = SHARED_TAIL + """
    (function () {
      var MON = ['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY',
                 'AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER'];

      function setHook(k, v) {
        var el = document.querySelector('[data-hook="' + k + '"]');
        if (el && SN.txt(v).trim() !== '') el.innerHTML = SN.esc(v).replace(/\\n/g, '<br>');
      }
      function birthday(md) {
        var p = String(md || '').split('-');
        if (p.length !== 2) return;
        var d = document.getElementById('hero-date');
        if (d) d.textContent = (MON[+p[0] - 1] || '') + ' ' + (+p[1]);
        var n = SN.dday(md), s = document.getElementById('dday-strip');
        if (s && n != null) s.textContent = n === 0 ? 'HAPPY BIRTHDAY ✦ TODAY' : 'BIRTHDAY D-' + n;
      }
      function avatar(d) {
        var img = document.getElementById('avatar-img');
        if (!img) return;
        var direct = SN.txt(d.avatar).trim();
        var src = direct || SN.soopAvatar(SN.txt(d.soop_id).trim() || 'k4187421');
        if (src) img.src = src; else snAvatarFallback(img);
      }

      /* Both effect layers belong inside the cover on this page. */
      function nestLayers() {
        var cv = document.querySelector('.sn-cover'), inn = document.querySelector('.cv-in');
        ['snStars', 'snMongs'].forEach(function (id) {
          var el = document.getElementById(id);
          if (cv && inn && el) cv.insertBefore(el, inn);
        });
      }

      async function load() {
        var d = await snCommon();
        nestLayers();
        try {
          setHook('name_en', d.name_en);
          setHook('tagline', d.tagline);
          setHook('quote', d.quote);
          var art = SN.txt(d.main_art).trim();
          if (art) document.getElementById('hero-bg').src = art;
          var L = d.links || {};
          if (L.youtube) document.getElementById('link-youtube').href = SN.txt(L.youtube);
          avatar(d);
          birthday(SN.txt(d.birthday).trim() || '10-04');
        } catch (e) {
          avatar({});
          birthday('10-04');
        }
        SN.dataReady(); SN.reveal(); enableIframeAutoHeight();
      }
      load();

      var mk = document.getElementById('star-mark');
      if (mk) mk.addEventListener('click', function () {
        mk.classList.remove('bump'); void mk.offsetWidth; mk.classList.add('bump');
        var r = mk.getBoundingClientRect();
        SN.pop(r.left + r.width / 2, r.top + r.height / 2, 5);
      });
    })();
"""


def build():
    return page(slug="", title="SHUNI", desc="슈니 공식 페이지", root="", body=BODY,
                css=CSS, script=SCRIPT, footer_mark="STAR ATLAS · HOME", cover=True)
