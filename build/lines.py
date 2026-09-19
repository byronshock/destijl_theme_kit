"""DeStijl line test (§1) and apartness test (§0a).  DESTIJL_STYLE.md is the authority.

on_line(hex_or_rgb) -> bool : within TOLERANCE (sRGB code values) of one of the
four segments BLACK->END.  Semantic values (§1b) are allow-listed by the caller.
apart(hex_or_rgb)   -> float: distance to the nearest of the sixteen palette POINTS
(§0a).  Chrome must lie on the lines; content must stay away from the points.

Usage: python3 build/lines.py '#9C9EA0' '#FF0000' ...          chrome: is it on a line?
       python3 build/lines.py --apart '#54278F' '#08519C' ...  content: is it far enough?
   or  import and call.
"""
import json, os, sys
import numpy as np

_here = os.path.dirname(os.path.abspath(__file__))
PAL = json.load(open(os.path.join(_here, '..', 'palette.json')))

def rgb(h):
    if isinstance(h, str):
        h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], float)
    return np.array(h, float)

BLACK = rgb(PAL['black'])
SEGMENTS = {n: (BLACK, rgb(v['end'])) for n, v in PAL['lines'].items()}
TOL = float(PAL.get('tolerance', 1.0))
EXEMPT = {v['hex'].upper() for v in PAL['semantic'].values() if v.get('exempt')}
LEGEND = {v['legend'].upper() for v in PAL['semantic'].values() if v.get('legend')}   # only ON a semantic field

def nearest(p):
    """(line name, t, distance) for the nearest segment."""
    p = rgb(p); best = None
    for n, (a, b) in SEGMENTS.items():
        ab = b - a
        t = float(np.clip(np.dot(p - a, ab) / np.dot(ab, ab), 0, 1))
        d = float(np.linalg.norm(p - (a + t * ab)))
        if best is None or d < best[2]: best = (n, t, d)
    return best

def on_line(p, tol=TOL):
    return nearest(p)[2] <= tol

def point(line, t):
    """Hex of the point at fraction t along a line."""
    a, b = SEGMENTS[line]; v = np.round(a + t * (b - a)).astype(int)
    return '#%02X%02X%02X' % tuple(v)


# --- §0a: the chrome's own points, and how far content must stay from them -------------------
STEPS = tuple(PAL.get('steps', (0.0, 1 / 3, 2 / 3, 1.0)))
POINTS = {}                                   # hex -> what it is; BLACK is shared by all four lines
for _n in SEGMENTS:
    for _t in STEPS:
        POINTS.setdefault(point(_n, _t), []).append('%s %.2f' % (_n, _t))
for _k, _v in PAL['semantic'].items():
    POINTS.setdefault(_v['hex'].upper(), []).append(_k.lower())
_PV = np.stack([rgb(h) for h in POINTS])
_PN = list(POINTS)

# The bar: the palette's own nearest-neighbour separation. Content at least this far from every
# point is as distinct from the chrome as the chrome's values are from each other.
_D = np.linalg.norm(_PV[:, None, :] - _PV[None, :, :], axis=-1); np.fill_diagonal(_D, np.inf)
APART = float(np.ceil(_D.min()))              # 35

# Hue-bearing: the chroma of the faintest hue the kit itself names (yellow 1/3). Below it a color is
# a tint of the ground, carries no hue to confuse with a chrome hue, and is not measured (§0a).
_HUE = [rgb(h) for h, w in POINTS.items() if not any(x.startswith('gray') for x in w)]
CHROMA_MIN = float(min(v.max() - v.min() for v in _HUE))          # 27


def chroma(p):
    v = rgb(p); return float(v.max() - v.min())


def hue_bearing(p):
    return chroma(p) >= CHROMA_MIN


def nearest_point(p):
    """(hex, what it is, distance) for the nearest palette point."""
    d = np.linalg.norm(_PV - rgb(p), axis=-1); i = int(d.argmin())
    return _PN[i], '/'.join(POINTS[_PN[i]]), float(d[i])


def apart(p):
    """Distance from the nearest palette point (§0a). Content wants >= APART."""
    return nearest_point(p)[2]

if __name__ == '__main__':
    if '--apart' in sys.argv:                 # §0a: content, measured against the chrome's points
        args = [a for a in sys.argv[1:] if a != '--apart']
        worst = None; bad = 0
        for h in args:
            hexv, what, d = nearest_point(h)
            if not hue_bearing(h):            # a tint of the ground, not information: exempt
                print(f"{h:8} ground  {d:5.1f} from {hexv} ({what}), chroma {chroma(h):.0f} < {CHROMA_MIN:.0f}")
                continue
            ok = d >= APART
            bad += not ok
            worst = d if worst is None else min(worst, d)
            print(f"{h:8} {'ok    ' if ok else 'NEAR  '} {d:5.1f} from {hexv} ({what})")
        if worst is not None and len(args) > 1:
            print(f"{'set':8} {'ok    ' if worst >= APART else 'NEAR  '} {worst:5.1f} at its nearest approach"
                  f"  (§0a wants >= {APART:.0f} for every hue-bearing step)")
        sys.exit(1 if bad else 0)
    bad = 0
    for h in sys.argv[1:]:
        n, t, d = nearest(h); H = h.upper()
        ok = d <= TOL or H in EXEMPT or H in LEGEND
        bad += not ok
        tag = '  (exempt)' if H in EXEMPT else '  (legend: only on a §1b field)' if H in LEGEND else ''
        print(f"{h:8} {'ok    ' if ok else 'OFF   '} nearest {n:6} t={t:.3f} d={d:.2f}{tag}")
    sys.exit(1 if bad else 0)
