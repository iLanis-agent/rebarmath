#!/usr/bin/env python3
# Rebar Math oracle - mirrors engine.js with Fractions: bars are placed one at a time along the run, stock bars are filled one piece at a time, mass is the exact product of the entered numbers, rounding is Decimal half-up.
import json, re, random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

RUN = "the run must be from 0.1 to 100 m with at most one decimal place"
SP = "the spacing must be a whole number of cm from 5 to 100"
PIECE = "the bar length must be from 0.1 to 12 m with at most two decimal places"
STOCK = "the stock length must be from 1 to 12 m with at most two decimal places"
MASS = "the label mass must be from 0.01 to 10 kg per m with at most two decimal places"
LONG = "the bar length cannot be longer than the stock length"
def dec(t, err, places, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,3}(\.[0-9]+)?", t): raise ValueError(err)
    if "." in t and len(t.split(".")[1]) > places: raise ValueError(err)
    if not F(lo) <= F(t) <= F(hi): raise ValueError(err)
    return F(t)
def whole(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,3}", t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def txt(fr, places):
    v = int((Decimal(fr.numerator) / Decimal(fr.denominator) * (10 ** places)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    ip, fp = divmod(v, 10 ** places); fs = str(fp).zfill(places).rstrip("0")
    return f"{ip}.{fs}" if fs else str(ip)
def bars(n): return f"{n} bar" + ("" if n == 1 else "s")
def run_in(run, sp):
    r = dec(run, RUN, 1, "0.1", "100"); s = whole(sp, SP, 5, 100)
    cm = r * 100; n = 0; pos = F(0)
    while pos <= cm: n += 1; pos += s
    return r, cm, s, n, pos - s

def count(run, sp):
    r, cm, s, n, last = run_in(run, sp); gap = cm - last
    tail = "leaving nothing to the end of the run." if gap == 0 else f"leaving {txt(gap,0)} cm to the end of the run."
    mid = "1 bar, at 0 cm" if n == 1 else f"{bars(n)}, the last at {txt(last,0)} cm"
    return f"A {txt(r,1)} m run at {s} cm spacing takes {mid}, {tail}"
def stock(run, sp, piece, stk):
    r, cm, s, n, last = run_in(run, sp)
    l = dec(piece, PIECE, 2, "0.1", "12") * 100; k = dec(stk, STOCK, 2, "1", "12") * 100
    if l > k: raise ValueError(LONG)
    used = 0; per = 0; sb = 0; off = F(0)
    left = n; per = 0
    while per * l + l <= k: per += 1
    while left > 0:                      # take a fresh stock bar, cut pieces from it one at a time
        sb += 1; room = k
        while left > 0 and room >= l: room -= l; left -= 1
        off += room
    return f"The {bars(n)} of {txt(l/100,2)} m cut {per} to a {txt(k/100,2)} m stock bar, so it takes {sb} stock bar{'' if sb == 1 else 's'}, with " + ("no offcut." if off == 0 else f"{txt(off/100,2)} m of offcut in total.")
def mass(run, sp, piece, lm):
    r, cm, s, n, last = run_in(run, sp)
    l = dec(piece, PIECE, 2, "0.1", "12"); m = dec(lm, MASS, 2, "0.01", "10")
    t = txt(n * l * m, 2)
    return f"The {bars(n)} of {txt(l,2)} m, at a label mass of {txt(m,2)} kg per m, {'weighs' if n == 1 else 'weigh'} " + ("under 0.01 kg." if t == "0" else t + " kg.")

FNS = {"countTruth": count, "stockTruth": stock, "massTruth": mass}
def cases():
    c = []
    runs = ["0.1", "0.5", "4", "7.3", "25", "99.9", "100"]; sps = ["5", "7", "20", "33", "100"]
    for a in runs:
        for s in sps: c.append(("countTruth", [a, s]))
    for a in ["0.1", "4", "7.3", "100"]:
        for s in ["5", "20", "100"]:
            for p, k in [("0.1", "1"), ("3.5", "12"), ("6", "12"), ("12", "12"), ("1.25", "9"), ("4", "6"), ("0.33", "12")]:
                c.append(("stockTruth", [a, s, p, k]))
    for a in ["0.1", "4", "100"]:
        for s in ["5", "20", "100"]:
            for p in ["0.1", "3.5", "12"]:
                for m in ["0.01", "0.62", "2.47", "10"]:
                    c.append(("massTruth", [a, s, p, m]))
    for t in [(" 4 ", " 20 ", " 3.5 ", " 12 "), ("4.0", "20", "3.50", "12.00")]:
        c += [("countTruth", list(t[:2])), ("stockTruth", list(t)), ("massTruth", [t[0], t[1], t[2], " 0.62 "])]
    bad = ["", "x", "0", "0.0", "0.001", "1.255", "-1", ".5", "5.", "1e2", "1000", "99999"]
    for v in bad:
        c += [("countTruth", [v, "20"]), ("countTruth", ["4", v]), ("stockTruth", ["4", "20", v, "12"]), ("stockTruth", ["4", "20", "3.5", v]), ("massTruth", ["4", "20", "3.5", v]), ("massTruth", ["4", "20", v, "0.62"])]
    for t in [("100.1", "20"), ("4", "4"), ("4", "101"), ("4", "20.5")]: c.append(("countTruth", list(t)))
    for t in [("4", "20", "12.01", "12"), ("4", "20", "7", "6.99"), ("4", "20", "3.5", "0.99"), ("4", "20", "3.5", "12.01")]: c.append(("stockTruth", list(t)))
    for t in [("4", "20", "3.5", "10.01"), ("4", "20", "3.5", "0.009"), ("4", "20", "12.01", "1")]: c.append(("massTruth", list(t)))
    r = random.Random(711)
    for _ in range(10):
        a = f"{r.randint(0, 99)}.{r.randint(0, 9)}"; a = "0.1" if a == "0.0" else a
        s = str(r.randint(5, 100)); p = f"{r.randint(0, 11)}.{r.randint(0, 99):02d}"; p = "0.1" if p in ("0.00", "0.0") else p
        k = str(r.randint(12, 12)) if float(p) > 11 else f"{r.randint(int(float(p))+1, 12)}.{r.randint(0,99):02d}"
        m = f"{r.randint(0, 9)}.{r.randint(0, 99):02d}"; m = "0.01" if m == "0.00" else m
        c += [("countTruth", [a, s]), ("stockTruth", [a, s, p, k]), ("massTruth", [a, s, p, m])]
    return c
out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(o, separators=(",", ":"), ensure_ascii=False) for o in out) + "\n]\n")
print(len(out), "cases written")
