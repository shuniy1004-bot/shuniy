/* Spin wheel. The draw is decided by a weighted pick first and the wheel is then
   animated to land on it, so the result never depends on frame timing or on how
   long the pointer happens to be held. Same entry syntax as the marble race:
   `이름*3` counts as three tickets.
   Loaded by game/index.html and by the fairness test, so the shipped code is the
   code that was measured. */
(function (root) {
  'use strict';

  function parseEntry(raw) {
    var s = String(raw || '').trim();
    if (!s) return null;
    var weight = 1;
    var m = s.match(/^(.*?)\s*\*\s*(\d+)$/);
    if (m) { s = m[1].trim(); weight = Math.max(1, Math.min(99, parseInt(m[2], 10) || 1)); }
    if (!s) return null;
    return { name: s, weight: weight };
  }

  function parseList(text) {
    return String(text || '')
      .split(/[\n,]/)
      .map(parseEntry)
      .filter(Boolean)
      .slice(0, 60);
  }

  /* Weighted pick over the entry list. Uses one uniform draw scaled to the total
     weight, so an entry with weight w wins exactly w/total of the time. */
  function pick(entries, rng) {
    if (!entries || !entries.length) return -1;
    var r = (rng || Math.random)();
    if (!(r >= 0 && r < 1)) r = Math.random();
    var total = 0, i;
    for (i = 0; i < entries.length; i++) total += entries[i].weight;
    if (total <= 0) return 0;
    var x = r * total;
    for (i = 0; i < entries.length; i++) {
      x -= entries[i].weight;
      if (x < 0) return i;
    }
    return entries.length - 1;
  }

  /* Segment boundaries in turns (0..1), proportional to weight. */
  function segments(entries) {
    var total = 0, i;
    for (i = 0; i < entries.length; i++) total += entries[i].weight;
    var out = [], acc = 0;
    for (i = 0; i < entries.length; i++) {
      var span = entries[i].weight / total;
      out.push({ index: i, name: entries[i].name, weight: entries[i].weight, from: acc, to: acc + span });
      acc += span;
    }
    if (out.length) out[out.length - 1].to = 1;
    return out;
  }

  /* Final wheel rotation, in turns, that puts segment `idx` under the pointer at
     the top. A random offset inside the segment keeps the landing spot from
     looking mechanical, kept off the edges so the pointer never straddles two. */
  function targetTurns(segs, idx, spins, rng) {
    var s = segs[idx];
    var r = (rng || Math.random)();
    var span = s.to - s.from;
    var at = s.from + span * (0.18 + r * 0.64);
    return spins - at;                 /* wheel turns clockwise; pointer sits at 0 */
  }

  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

  var api = {
    parseEntry: parseEntry, parseList: parseList,
    pick: pick, segments: segments, targetTurns: targetTurns, easeOut: easeOut
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.SHUNI_WHEEL = api;
})(typeof window !== 'undefined' ? window : globalThis);
