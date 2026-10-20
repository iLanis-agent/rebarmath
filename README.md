# Rebar Math

Rebar count and stock arithmetic. A 4 m run at 20 cm spacing takes 21 bars, the last at 400 cm, leaving nothing to the end of the run.

## What it computes

- **The count truth** - bars along a run (0.1 to 100 m) at a spacing (whole cm, 5 to 100), one at 0 cm and one every spacing after, and the gap left to the end of the run.
- **The stock truth** - stock bars (1 to 12 m) for that many bars of one cut length (0.1 to 12 m), cut into whole pieces, and the offcut left in total.
- **The mass truth** - the mass of those bars from a label mass you read off the supplier's label (0.01 to 10 kg per m).

## Boundary

Arithmetic only. The spacing, bar lengths and label mass are the owner's own entries. It has not seen any plan or site and does not know the bar size, the cover, the laps, the loads or any rule that applies, and it gives no verdict that a layout is adequate or safe. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on cm and hundredths, half-up rounding).
- `oracle.py` - the Python mirror (Fractions, bars placed and cut one at a time) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/rebarmath/
Repo: https://github.com/iLanis-agent/rebarmath
