// Rebar Math engine: bar counts at a spacing, stock bars for a cut length, and bar mass from a label figure. Exact integers (cm and hundredths), results rounded half up.
function _d(t, err, places, lo, hi) { // decimal text with at most `places` decimals -> integer scaled by 10^places
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{1,3})(?:\.([0-9]+))?$/.exec(t);
  if (!m || (m[2] && m[2].length > places)) throw new Error(err);
  var f = (m[2] || "").padEnd(places, "0");
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (f ? parseInt(f, 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _w(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,3}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _RUN = "the run must be from 0.1 to 100 m with at most one decimal place";
var _SP = "the spacing must be a whole number of cm from 5 to 100";
var _PIECE = "the bar length must be from 0.1 to 12 m with at most two decimal places";
var _STOCK = "the stock length must be from 1 to 12 m with at most two decimal places";
var _MASS = "the label mass must be from 0.01 to 10 kg per m with at most two decimal places";
var _LONG = "the bar length cannot be longer than the stock length";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _bars(n) { return n + (n === 1 ? " bar" : " bars"); }
function _run(run, sp) { return { cm: _d(run, _RUN, 1, 1, 1000) * 10, s: _w(sp, _SP, 5, 100) }; }
function _n(p) { return Math.floor(p.cm / p.s) + 1; }

function countTruth(run, spacing) {
  var p = _run(run, spacing), n = _n(p), last = (n - 1) * p.s, gap = p.cm - last;
  var tail = gap === 0 ? "leaving nothing to the end of the run." : "leaving " + gap + " cm to the end of the run.";
  return "A " + _dec(p.cm, 2) + " m run at " + p.s + " cm spacing takes " + (n === 1 ? "1 bar, at 0 cm" : _bars(n) + ", the last at " + last + " cm") + ", " + tail;
}
function stockTruth(run, spacing, pieceM, stockM) {
  var p = _run(run, spacing), n = _n(p), l = _d(pieceM, _PIECE, 2, 10, 1200), k = _d(stockM, _STOCK, 2, 100, 1200);
  if (l > k) throw new Error(_LONG);
  var per = Math.floor(k / l), sb = Math.floor((n + per - 1) / per), off = sb * k - n * l;
  return "The " + _bars(n) + " of " + _dec(l, 2) + " m cut " + per + " to a " + _dec(k, 2) + " m stock bar, so they take " + sb + (sb === 1 ? " stock bar" : " stock bars") + ", with " + (off === 0 ? "no offcut." : _dec(off, 2) + " m of offcut in total.");
}
function massTruth(run, spacing, pieceM, labelMass) {
  var p = _run(run, spacing), n = _n(p), l = _d(pieceM, _PIECE, 2, 10, 1200), m = _d(labelMass, _MASS, 2, 1, 1000);
  var kg = _hu(n * l * m, 100);                                            // hundredths of a kg
  return "The " + _bars(n) + " of " + _dec(l, 2) + " m, at a label mass of " + _dec(m, 2) + " kg per m, " + (n === 1 ? "weighs " : "weigh ") + (kg === 0 ? "under 0.01 kg." : _dec(kg, 2) + " kg.");
}
