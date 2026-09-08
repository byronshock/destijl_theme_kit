"""DeStijl line test (DESTIJL_STYLE.md §1).

on_line(hex_or_rgb) -> bool : within TOLERANCE (sRGB code values) of one of the
four segments BLACK->END.  Semantic values (§1b) are allow-listed by the caller.
Usage: python3 build/lines.py '#9C9EA0' '#FF0000' ...   or   import and call.
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

if __name__ == '__main__':
    bad = 0
    for h in sys.argv[1:]:
        n, t, d = nearest(h); H = h.upper()
        ok = d <= TOL or H in EXEMPT or H in LEGEND
        bad += not ok
        tag = '  (exempt)' if H in EXEMPT else '  (legend: only on a §1b field)' if H in LEGEND else ''
        print(f"{h:8} {'ok    ' if ok else 'OFF   '} nearest {n:6} t={t:.3f} d={d:.2f}{tag}")
    sys.exit(1 if bad else 0)
