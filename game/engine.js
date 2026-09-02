/* Minigame core. Loaded by game/index.html and required by the physics test,
   so the shipped code is the code that was measured.
   Ladder follows the reference build: rungs are never drawn, the runner walks and
   strokes its own path, results stay visible from the start. */
(function (root) {
  'use strict';

  function rand(a, b) { return a + Math.random() * (b - a); }

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  /* ---------------- ladder ----------------
     rung[g][r] = true means a bar joins column g and g+1 on row r.
     Neighbouring gaps never carry a bar on the same row, and every gap gets at
     least one bar so no column is stuck going straight down. */
  /* rows: the reference build uses 9~11, which is tuned for about four people.
     Measured with more players that leaves the walker near its own column
     (8 people: 0.4% ~ 30.2%). The rung rules are untouched; only the ladder is
     made longer, and since the bars are never drawn the screen looks the same.
     2*n*n rows passes the chi square test for 4 to 10 people. */
  function buildLadder(n) {
    var rows = Math.max(10, n * n * 2);
    var gaps = n - 1;
    var rung = [];
    var g, r;
    for (g = 0; g < gaps; g++) { rung[g] = []; for (r = 0; r < rows; r++) rung[g][r] = false; }

    for (r = 0; r < rows; r++) {
      for (g = 0; g < gaps; g++) {
        if (g > 0 && rung[g - 1][r]) continue;
        if (Math.random() < 0.45) rung[g][r] = true;
      }
    }

    for (g = 0; g < gaps; g++) {
      var any = false;
      for (r = 0; r < rows; r++) if (rung[g][r]) { any = true; break; }
      if (any) continue;
      for (var tries = 0; tries < 40; tries++) {
        var rr = Math.floor(Math.random() * rows);
        if ((g > 0 && rung[g - 1][rr]) || (g < gaps - 1 && rung[g + 1][rr])) continue;
        rung[g][rr] = true;
        break;
      }
    }
    return { n: n, rows: rows, rung: rung };
  }

  /* walk down column `start`, returning every corner in row/col space */
  function traceLadder(L, start) {
    var col = start;
    var path = [{ row: -1, col: col }];
    for (var r = 0; r < L.rows; r++) {
      if (col < L.n - 1 && L.rung[col][r]) { path.push({ row: r, col: col }); col += 1; }
      else if (col > 0 && L.rung[col - 1][r]) { path.push({ row: r, col: col }); col -= 1; }
      else continue;
      path.push({ row: r, col: col });
    }
    path.push({ row: L.rows, col: col });
    return { end: col, path: path };
  }

  function closest(px, py, s) {
    var dx = s.x2 - s.x1, dy = s.y2 - s.y1;
    var L = dx * dx + dy * dy;
    var t = L ? ((px - s.x1) * dx + (py - s.y1) * dy) / L : 0;
    t = t < 0 ? 0 : t > 1 ? 1 : t;
    return { x: s.x1 + dx * t, y: s.y1 + dy * t, t: t };
  }

  function closest(px, py, s) {
    var dx = s.x2 - s.x1, dy = s.y2 - s.y1;
    var L = dx * dx + dy * dy;
    var t = L ? ((px - s.x1) * dx + (py - s.y1) * dy) / L : 0;
    t = t < 0 ? 0 : t > 1 ? 1 : t;
    return { x: s.x1 + dx * t, y: s.y1 + dy * t, t: t };
  }

  /* ---------------- marble roulette ----------------
     Ported from lazygyu/roulette (MIT). Same courses, same rules: named marbles
     drop through the stage and the order they cross goalY is the result.
     Box2D is replaced with circle/segment collision in the same world units,
     so the map data can be used as it is. Box shapes carry half extents. */
  var RL = {
    gravity: 10,
    radius: 0.25,
    step: 1 / 60,      /* seconds per physics tick */
    sub: 4,            /* substeps per tick */
    damping: 0.999,
    maxV: 26,
    zoomThreshold: 5,  /* world units from zoomY where the camera closes in */
    stuckMs: 5000
  };

  function stagesList() {
    var m = (typeof module !== 'undefined' && module.exports) ? require('./maps.js') : root.SHUNI_MAPS;
    return m || [];
  }

  /* name*3 makes three marbles, name/2 doubles the skill rate, exactly like the
     original input syntax */
  function parseName(str) {
    var weightRe = /(\/\d+)/, countRe = /(\*\d+)/;
    var nameMatch = /^\s*([^\/*]+)?/.exec(str);
    var name = (nameMatch && nameMatch[1] ? nameMatch[1] : '').trim();
    var weight = weightRe.test(str) ? parseInt(weightRe.exec(str)[1].replace('/', ''), 10) : 1;
    var count = countRe.test(str) ? parseInt(countRe.exec(str)[1].replace('*', ''), 10) : 1;
    return { name: name, weight: weight || 1, count: Math.max(1, Math.min(99, count || 1)) };
  }

  function splitNames(text) {
    return String(text || '').split(/[,\r\n]/g).map(function (v) { return v.trim(); }).filter(Boolean);
  }

  /* collapses duplicates into name*n, the same tidy up the original does on blur */
  function normalizeNames(text) {
    var keys = [], counts = {};
    splitNames(text).forEach(function (raw) {
      var p = parseName(raw);
      if (!p.name) return;
      var key = p.weight > 1 ? p.name + '/' + p.weight : p.name;
      if (counts[key] === undefined) { keys.push(key); counts[key] = 0; }
      counts[key] += p.count;
    });
    return keys.map(function (k) { return counts[k] > 1 ? k + '*' + counts[k] : k; }).join(',');
  }

  /* ---- colliders ---- */
  function boxCorners(e) {
    var w = e.shape.width, h = e.shape.height;      /* half extents */
    var a = (e.shape.rotation || 0) + e.angle;
    var ca = Math.cos(a), sa = Math.sin(a);
    var pts = [[-w, -h], [w, -h], [w, h], [-w, h]];
    return pts.map(function (p) {
      return { x: e.x + p[0] * ca - p[1] * sa, y: e.y + p[0] * sa + p[1] * ca };
    });
  }

  function buildStage(index) {
    var list = stagesList();
    var def = list[Math.max(0, Math.min(list.length - 1, index | 0))];
    var ents = (def.entities || []).map(function (raw) {
      var e = {
        x: raw.position.x, y: raw.position.y,
        angle: 0,
        av: raw.props.angularVelocity || 0,
        rest: raw.props.restitution || 0,
        kinematic: raw.type === 'kinematic',
        shape: raw.shape,
        /* life > 0 means the piece pops on first contact, which is what opens
           the way through BubblePop and Yoru ni Kakeru */
        life: raw.props.life === undefined ? -1 : raw.props.life,
        dead: false,
        segs: null, reach: 0
      };
      if (raw.shape.type === 'polyline') {
        e.segs = [];
        for (var i = 0; i < raw.shape.points.length - 1; i++) {
          var p1 = raw.shape.points[i], p2 = raw.shape.points[i + 1];
          e.segs.push([e.x + p1[0], e.y + p1[1], e.x + p2[0], e.y + p2[1]]);
        }
        var lo = Infinity, hi = -Infinity;
        e.segs.forEach(function (s) { lo = Math.min(lo, s[1], s[3]); hi = Math.max(hi, s[1], s[3]); });
        e.top = lo; e.bottom = hi;
      } else if (raw.shape.type === 'box') {
        e.reach = Math.hypot(raw.shape.width, raw.shape.height);
        e.top = e.y - e.reach; e.bottom = e.y + e.reach;
      } else {
        e.reach = raw.shape.radius;
        e.top = e.y - e.reach; e.bottom = e.y + e.reach;
      }
      return e;
    });
    return {
      title: def.title, goalY: def.goalY, zoomY: def.zoomY,
      entities: ents,
      /* rough course bounds, used by the minimap */
      bounds: (function () {
        var minX = Infinity, maxX = -Infinity, maxY = def.goalY;
        ents.forEach(function (e) {
          var r = e.reach || 1;
          minX = Math.min(minX, e.x - r); maxX = Math.max(maxX, e.x + r);
        });
        if (!isFinite(minX)) { minX = 0; maxX = 26; }
        return { minX: minX, maxX: maxX, maxY: maxY };
      })()
    };
  }

  /* ---- race state ---- */
  function newRace(stageIndex, namesText, winningRank, useSkills) {
    var stage = buildStage(stageIndex);
    var entries = [];
    splitNames(namesText).forEach(function (raw) {
      var p = parseName(raw);
      if (!p.name) return;
      for (var i = 0; i < p.count; i++) entries.push({ name: p.name, weight: p.weight });
    });
    entries = entries.slice(0, 120);
    /* the starting slot is not neutral on every course: measured on Pot of greed
       one slot won 101 of 240 and another 2. names are dealt to slots at random
       so slot bias cannot attach to a person. */
    entries = shuffle(entries);

    var max = entries.length;
    var maxLine = Math.ceil(max / 10);
    var marbles = entries.map(function (en, order) {
      var line = Math.floor(order / 10);
      var lineDelta = -Math.max(0, Math.ceil(maxLine - 5));
      var coolMax = 1000 + (1 - en.weight) * 4000;
      return {
        id: order, name: en.name, weight: en.weight,
        hue: (360 / max) * order,
        x: 10.25 + (order % 10) * 0.6,
        y: maxLine - line + lineDelta,
        vx: 0, vy: 0,
        /* Box2D gave each marble density 1 + random; keep the mass spread */
        mass: 1 + Math.random(),
        done: false, rank: 0,
        impact: 0, skill: 0,
        coolMax: coolMax, cool: coolMax * Math.random(), skillRate: 0.2 * en.weight,
        stuck: 0, lx: 0, ly: 0
      };
    });
    return {
      stage: stage, marbles: marbles, winners: [],
      winningRank: Math.max(0, (winningRank || 1) - 1),
      useSkills: useSkills !== false,
      total: marbles.length,
      started: false, running: false, over: false, winner: null,
      t: 0, goalDist: Infinity, timeScale: 1
    };
  }

  function segHit(m, x1, y1, x2, y2, rest, sv) {
    var c = closest(m.x, m.y, { x1: x1, y1: y1, x2: x2, y2: y2 });
    var dx = m.x - c.x, dy = m.y - c.y;
    var d = Math.sqrt(dx * dx + dy * dy);
    if (d >= RL.radius || d < 1e-9) return false;
    var nx = dx / d, ny = dy / d;
    m.x = c.x + nx * RL.radius;
    m.y = c.y + ny * RL.radius;
    var rvx = m.vx - (sv ? sv.x : 0), rvy = m.vy - (sv ? sv.y : 0);
    var dot = rvx * nx + rvy * ny;
    if (dot < 0) {
      rvx -= (1 + rest) * dot * nx;
      rvy -= (1 + rest) * dot * ny;
      m.vx = rvx * 0.995 + (sv ? sv.x : 0);
      m.vy = rvy * 0.995 + (sv ? sv.y : 0);
    }
    return true;
  }

  function surfaceVel(e, px, py) {
    if (!e.av) return null;
    return { x: -e.av * (py - e.y), y: e.av * (px - e.x) };
  }

  function collideEntity(m, e) {
    var touched = false;
    if (e.shape.type === 'polyline') {
      for (var i = 0; i < e.segs.length; i++) {
        var s = e.segs[i];
        if (segHit(m, s[0], s[1], s[2], s[3], e.rest, null)) touched = true;
      }
      return touched;
    }
    if (e.shape.type === 'circle') {
      var dx = m.x - e.x, dy = m.y - e.y, d = Math.sqrt(dx * dx + dy * dy);
      var min = RL.radius + e.shape.radius;
      if (d < min && d > 1e-9) {
        touched = true;
        var nx = dx / d, ny = dy / d;
        m.x = e.x + nx * min; m.y = e.y + ny * min;
        var sv = surfaceVel(e, m.x, m.y);
        var rvx = m.vx - (sv ? sv.x : 0), rvy = m.vy - (sv ? sv.y : 0);
        var dot = rvx * nx + rvy * ny;
        if (dot < 0) {
          rvx -= (1 + e.rest) * dot * nx;
          rvy -= (1 + e.rest) * dot * ny;
          m.vx = rvx * 0.995 + (sv ? sv.x : 0);
          m.vy = rvy * 0.995 + (sv ? sv.y : 0);
        }
      }
      return touched;
    }
    var c = boxCorners(e);
    for (var k = 0; k < 4; k++) {
      var a = c[k], b = c[(k + 1) % 4];
      var cp = closest(m.x, m.y, { x1: a.x, y1: a.y, x2: b.x, y2: b.y });
      if (segHit(m, a.x, a.y, b.x, b.y, e.rest, surfaceVel(e, cp.x, cp.y))) touched = true;
    }
    return touched;
  }

  function stepRace(race) {
    if (race.over) return race;
    var S = race.stage;
    var dt = RL.step * race.timeScale;
    race.t += RL.step * 1000 * race.timeScale;

    for (var e = 0; e < S.entities.length; e++) {
      var en = S.entities[e];
      if (en.dead) continue;
      if (en.av) {
        en.angle += en.av * dt;
        if (en.shape.type !== 'polyline') {
          en.top = en.y - en.reach; en.bottom = en.y + en.reach;
        }
      }
    }

    var sdt = dt / RL.sub;
    /* the marble order is shuffled every tick: resolving them in array order
       hands the first entry a measurable advantage */
    var order = [];
    for (var i = 0; i < race.marbles.length; i++) order.push(i);
    for (var q = order.length - 1; q > 0; q--) {
      var j = Math.floor(Math.random() * (q + 1));
      var tt = order[q]; order[q] = order[j]; order[j] = tt;
    }

    for (var oi = 0; oi < order.length; oi++) {
      var m = race.marbles[order[oi]];
      if (m.done || !race.started) continue;

      for (var s = 0; s < RL.sub; s++) {
        m.vy += RL.gravity * sdt;
        m.vx *= RL.damping; m.vy *= RL.damping;
        var sp = Math.hypot(m.vx, m.vy);
        if (sp > RL.maxV) { m.vx = m.vx / sp * RL.maxV; m.vy = m.vy / sp * RL.maxV; }
        m.x += m.vx * sdt;
        m.y += m.vy * sdt;

        for (var k2 = 0; k2 < S.entities.length; k2++) {
          var ent = S.entities[k2];
          if (ent.dead) continue;
          if (m.y + 1 < ent.top || m.y - 1 > ent.bottom) continue;
          if (collideEntity(m, ent) && ent.life > 0) ent.dead = true;
        }
      }

      /* marble to marble */
      for (var o2 = 0; o2 < race.marbles.length; o2++) {
        var n = race.marbles[o2];
        if (n === m || n.done) continue;
        var ddx = m.x - n.x, ddy = m.y - n.y;
        var dd = Math.sqrt(ddx * ddx + ddy * ddy);
        var mind = RL.radius * 2;
        if (dd < mind && dd > 1e-9) {
          var ux = ddx / dd, uy = ddy / dd, push = (mind - dd) / 2;
          m.x += ux * push; m.y += uy * push;
          n.x -= ux * push; n.y -= uy * push;
          var rel = (m.vx - n.vx) * ux + (m.vy - n.vy) * uy;
          if (rel < 0) {
            var tot = m.mass + n.mass;
            var imp = rel * (n.mass / tot);
            var imp2 = rel * (m.mass / tot);
            m.vx -= imp * ux; m.vy -= imp * uy;
            n.vx += imp2 * ux; n.vy += imp2 * uy;
          }
        }
      }

      /* stuck for five seconds gets the same random shake as the original */
      if (Math.hypot(m.x - m.lx, m.y - m.ly) < 0.004) {
        m.stuck += RL.step * 1000;
        if (m.stuck > RL.stuckMs) {
          m.vx += rand(-5, 5); m.vy += rand(-5, 5);
          m.stuck = 0;
        }
      } else m.stuck = 0;
      m.lx = m.x; m.ly = m.y;

      /* skills */
      m.skill = 0;
      if (m.impact > 0) m.impact = Math.max(0, m.impact - RL.step * 1000);
      if (race.useSkills) {
        m.cool -= RL.step * 1000;
        if (m.cool <= 0) {
          m.skill = Math.random() < m.skillRate * 0.02 ? 1 : 0;
          m.cool = m.coolMax;
        }
      }
      if (m.skill === 1) {
        m.impact = 500;
        for (var z = 0; z < race.marbles.length; z++) {
          var other = race.marbles[z];
          if (other === m || other.done) continue;
          var vx = other.x - m.x, vy = other.y - m.y;
          var distSq = vx * vx + vy * vy;
          if (distSq < 100 && distSq > 1e-9) {
            var len = Math.sqrt(distSq);
            var power = 1 - len / 10;
            other.vx += (vx / len) * power * power * 5;
            other.vy += (vy / len) * power * power * 5;
          }
        }
      }

      if (m.y > S.goalY) {
        m.done = true;
        race.winners.push(m);
        m.rank = race.winners.length;
        if (race.running && race.winners.length === race.winningRank + 1) {
          race.winner = m; race.running = false;
        }
      }
    }

    race.marbles.sort(function (a, b) { return b.y - a.y; });

    var live = race.marbles.filter(function (x) { return !x.done; });
    var targetIndex = race.winningRank - race.winners.length;
    var target = live[targetIndex] || live[0];
    race.goalDist = target ? Math.abs(S.zoomY - target.y) : Infinity;
    /* the original slows time down as the deciding marble nears the line */
    race.timeScale = (race.winners.length < race.winningRank + 1 && race.goalDist < RL.zoomThreshold && live.length > 1)
      ? Math.max(0.2, race.goalDist / RL.zoomThreshold) : 1;

    if (!live.length) { race.over = true; race.running = false; }
    return race;
  }

  function startRace(race) { race.started = true; race.running = true; }

  var api = {
    rand: rand, shuffle: shuffle,
    buildLadder: buildLadder, traceLadder: traceLadder,
    RL: RL, stagesList: stagesList, buildStage: buildStage, boxCorners: boxCorners,
    parseName: parseName, splitNames: splitNames, normalizeNames: normalizeNames,
    newRace: newRace, stepRace: stepRace, startRace: startRace
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.SHUNI_GAME = api;
})(typeof window !== 'undefined' ? window : globalThis);
