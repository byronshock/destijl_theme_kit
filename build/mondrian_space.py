"""Mondrian space: project sRGB into the color space Mondrian's five pigments define (DESTIJL_STYLE.md §1, issue 006).

Five anchors — K, W, R, Y, B, measured from the 1922 composition (palette.json) — define the space as their
convex hull in sRGB. Pure sRGB red, yellow and blue map to R, Y, B; black and white map to K and W. Any
other color goes to the nearest point of the hull: colors already inside are kept, colors outside are
clipped to the hull's surface. Greens, cyans, magentas and tints toward white have no place in the
composition and land on the nearest face, keeping their lightness and as much of their chroma as the
pigments allow.

    project(rgb) -> rgb            one color, 0-255 floats or a hex string
    project_image(PIL.Image)       every pixel; alpha untouched
    python3 build/mondrian_space.py in.png out.png [--lines]

Modes (--mode=pigment|hue|hull|lines):
  pigment  nearest of the five pigments, flat: the actual pigments, a poster. Chosen 2026-09-08 (issue 006).
           Grays go to K or W, and a 3x3 majority vote cleans anti-aliased edges (project_image clean=True).
  hue      hue chooses the line, HSV value chooses the point on it (luminance for grays). Shading kept, no banding, no mixes.
  hull     warp to the anchors, clip to the hull. Admits mixes, so tints and mud. The first attempt.
  lines    warp, then nearest of the four §1 lines. Bands across a gradient.
"""
import json, os, sys
import numpy as np

_here = os.path.dirname(os.path.abspath(__file__))
PAL = json.load(open(os.path.join(_here, '..', 'palette.json')))


def _rgb(h):
    if isinstance(h, str):
        h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)
    return np.asarray(h, float)


K = _rgb(PAL['black']); W = _rgb(PAL['lines']['gray']['end'])
R = _rgb(PAL['lines']['red']['end']); Y = _rgb(PAL['lines']['yellow']['end']); B = _rgb(PAL['lines']['blue']['end'])
ANCHORS = {'K': K, 'W': W, 'R': R, 'Y': Y, 'B': B}
SRGB = {'K': _rgb('#000000'), 'W': _rgb('#FFFFFF'), 'R': _rgb('#FF0000'), 'Y': _rgb('#FFFF00'), 'B': _rgb('#0000FF')}

# --- the warp: sRGB anchors -> Mondrian anchors, exact at the anchors, smooth between (match_wallpaper.py's method)
_SRC = np.stack([SRGB[k] for k in 'KWRYB']); _DST = np.stack([ANCHORS[k] for k in 'KWRYB'])
_SIGMA = 60.0     # width of each anchor's pull, sRGB code values: exact at the anchors (e^-9 leakage), smooth between


def warp(p):
    """Move p by the anchor offsets, weighted by proximity. Exact at the five anchors."""
    p = np.atleast_2d(p).astype(float)
    d2 = ((p[:, None, :] - _SRC[None, :, :]) ** 2).sum(-1)                # (n, 5)
    w = np.exp(-d2 / (2 * _SIGMA ** 2)); w /= w.sum(-1, keepdims=True) + 1e-12
    return p + (w[:, :, None] * (_DST - _SRC)[None, :, :]).sum(1)


# --- the hull of the five anchors, as triangles; nearest point on each, take the closest
def _hull_faces(pts):
    n = len(pts); faces = []
    from itertools import combinations
    for i, j, k in combinations(range(n), 3):
        a, b, c = pts[i], pts[j], pts[k]; nrm = np.cross(b - a, c - a)
        if np.linalg.norm(nrm) < 1e-9: continue
        s = np.sign([np.dot(nrm, pts[m] - a) for m in range(n) if m not in (i, j, k)])
        if np.all(s >= 0) or np.all(s <= 0): faces.append((a, b, c))
    return faces


FACES = _hull_faces(np.stack(list(ANCHORS.values())))


def _closest_on_triangle(p, a, b, c):
    """Ericson, Real-Time Collision Detection 5.1.5, vectorised over p (n,3)."""
    ab, ac, ap = b - a, c - a, p - a
    d1, d2 = ap @ ab, ap @ ac
    bp = p - b; d3, d4 = bp @ ab, bp @ ac
    cp = p - c; d5, d6 = cp @ ab, cp @ ac
    out = np.empty_like(p); done = np.zeros(len(p), bool)
    def put(mask, val):
        m = mask & ~done; out[m] = val[m] if val.ndim == 2 else val; done[m] = True
    put((d1 <= 0) & (d2 <= 0), np.broadcast_to(a, p.shape))
    put((d3 >= 0) & (d4 <= d3), np.broadcast_to(b, p.shape))
    vc = d1 * d4 - d3 * d2
    v = np.where(d1 - d3 != 0, d1 / np.where(d1 - d3 != 0, d1 - d3, 1), 0)
    put((vc <= 0) & (d1 >= 0) & (d3 <= 0), a + v[:, None] * ab)
    put((d6 >= 0) & (d5 <= d6), np.broadcast_to(c, p.shape))
    vb = d5 * d2 - d1 * d6
    w = np.where(d2 - d6 != 0, d2 / np.where(d2 - d6 != 0, d2 - d6, 1), 0)
    put((vb <= 0) & (d2 >= 0) & (d6 <= 0), a + w[:, None] * ac)
    va = d3 * d6 - d5 * d4
    den = (d4 - d3) + (d5 - d6); w2 = np.where(den != 0, (d4 - d3) / np.where(den != 0, den, 1), 0)
    put((va <= 0) & (d4 - d3 >= 0) & (d5 - d6 >= 0), b + w2[:, None] * (c - b))
    denom = 1.0 / np.where(va + vb + vc != 0, va + vb + vc, 1)
    v2, w3 = vb * denom, vc * denom
    put(~done, a + ab * v2[:, None] + ac * w3[:, None])
    return out


def clip_hull(p):
    """Nearest point of the Mondrian hull. Inside points are returned unchanged."""
    p = np.atleast_2d(p).astype(float)
    best, bestd = None, None
    for a, b, c in FACES:
        q = _closest_on_triangle(p, a, b, c); d = ((q - p) ** 2).sum(-1)
        if best is None: best, bestd = q, d
        else:
            m = d < bestd; best[m] = q[m]; bestd[m] = d[m]
    # a point is inside iff it is on the inner side of every face: keep it then
    inside = np.ones(len(p), bool)
    centroid = np.stack(list(ANCHORS.values())).mean(0)
    for a, b, c in FACES:
        nrm = np.cross(b - a, c - a); nrm *= np.sign(np.dot(nrm, centroid - a))
        inside &= ((p - a) @ nrm) >= -1e-9
    return np.where(inside[:, None], p, best)


def clip_lines(p):
    """Nearest point on the four lines of §1 — the chrome rule, for when the hull is too generous."""
    p = np.atleast_2d(p).astype(float); best, bestd = None, None
    for end in (W, R, Y, B):
        ab = end - K; t = np.clip(((p - K) @ ab) / (ab @ ab), 0, 1); q = K + t[:, None] * ab
        d = ((q - p) ** 2).sum(-1)
        if best is None: best, bestd = q, d
        else:
            m = d < bestd; best[m] = q[m]; bestd[m] = d[m]
    return best


_LUMA = np.array([0.2126, 0.7152, 0.0722])


PIGMENTS = np.stack([K, W, R, Y, B])          # index order for pigment_index / majority


def pigment_index(p, grays_to_kw=True, chroma_min=28.0):
    """Index into PIGMENTS of the nearest pigment. With grays_to_kw (issue 006, accepted 2026-09-08), a
    low-chroma pixel goes to the nearer of K and W, so gray shading does not turn yellow."""
    p = np.atleast_2d(p).astype(float)
    d = ((p[:, None, :] - PIGMENTS[None, :, :]) ** 2).sum(-1)
    if grays_to_kw:
        gray = (p.max(1) - p.min(1)) < chroma_min
        d[gray, 2:] = np.inf
    return d.argmin(1)


def pigment(p, grays_to_kw=True):
    """Nearest of the five pigments, flat: a poster, no shading."""
    return PIGMENTS[pigment_index(p, grays_to_kw)]


def majority(idx, alpha=None):
    """3x3 majority vote over a 2-D index map (issue 006, accepted 2026-09-08): an anti-aliased edge pixel
    joins the pigment most of its neighbours chose instead of a third one. Ties keep the pixel's own choice;
    transparent neighbours do not vote."""
    H, W_ = idx.shape; n = len(PIGMENTS)
    votes = np.zeros((n, H, W_), int)
    valid = np.ones((H, W_), bool) if alpha is None else alpha > 0
    pad_i = np.pad(idx, 1, mode='edge'); pad_v = np.pad(valid, 1, mode='constant')
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            si = pad_i[1 + dy:1 + dy + H, 1 + dx:1 + dx + W_]; sv = pad_v[1 + dy:1 + dy + H, 1 + dx:1 + dx + W_]
            for k in range(n): votes[k] += (si == k) & sv
    best = votes.argmax(0); own = votes[idx, np.arange(H)[:, None], np.arange(W_)[None, :]]
    return np.where(votes.max(0) > own, best, idx)


def hue_lines(p, chroma_min=28.0):
    """Hue picks the line, value picks the point on it. A gradient stays on one line, so no banding;
    nothing is brighter than the pigment at the end of its line."""
    p = np.atleast_2d(p).astype(float)
    mx, mn = p.max(1), p.min(1); chroma = mx - mn
    r, g, b = p.T
    h = np.zeros(len(p))
    m = chroma > 0
    hr = ((g - b) / np.where(chroma == 0, 1, chroma)) % 6
    hg = (b - r) / np.where(chroma == 0, 1, chroma) + 2
    hb = (r - g) / np.where(chroma == 0, 1, chroma) + 4
    h = np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60          # degrees
    # nearest pigment by hue: red 0/360, yellow 60, blue 240. green (120) -> yellow, cyan (180) -> blue, magenta (300) -> red
    dr = np.minimum(np.abs(h - 0), np.abs(h - 360)); dy = np.abs(h - 60); db = np.abs(h - 240)
    choice = np.argmin(np.stack([dr, dy, db], 1), 1)                   # 0 red, 1 yellow, 2 blue
    ends = np.stack([R, Y, B])[choice]
    achroma = chroma < chroma_min
    ends = np.where(achroma[:, None], W[None, :], ends)                 # low chroma: the gray line
    # position on the line: HSV value for a hue (pure sRGB red is t=1, half-dark red t=0.5, a tint collapses to
    # the pigment, since tints toward white are not admitted), luminance for a gray
    t_hue = mx / 255.0
    t_gray = np.clip((p @ _LUMA - K @ _LUMA) / (W @ _LUMA - K @ _LUMA), 0, 1)
    t = np.where(achroma, t_gray, t_hue)
    return K + t[:, None] * (ends - K)


MODES = {'hull': lambda q: clip_hull(warp(q)), 'lines': lambda q: clip_lines(warp(q)),
         'pigment': pigment, 'hue': hue_lines}


def project(p, lines=False, mode=None):
    q = _rgb(p) if isinstance(p, str) else np.asarray(p, float)
    mode = mode or ('lines' if lines else 'pigment')
    return np.clip(np.rint(MODES[mode](q)), 0, 255)


def project_image(im, lines=False, mode=None, clean=True):
    """Project every pixel; alpha untouched. In pigment mode, clean=True applies the 3x3 majority filter."""
    from PIL import Image
    im = im.convert('RGBA'); a = np.asarray(im); H, W_ = a.shape[:2]; rgb = a[..., :3].reshape(-1, 3)
    mode = mode or ('lines' if lines else 'pigment')
    if mode == 'pigment':
        idx = pigment_index(rgb).reshape(H, W_)
        if clean: idx = majority(idx, a[..., 3])
        out = PIGMENTS[idx].astype(np.uint8)
    else:
        out = project(rgb, mode=mode).astype(np.uint8).reshape(H, W_, 3)
    return Image.fromarray(np.concatenate([out, a[..., 3:]], -1), 'RGBA')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        for h in ('#FF0000', '#FFFF00', '#0000FF', '#000000', '#FFFFFF', '#00FF00', '#00FFFF', '#FF00FF', '#808080', '#FF8000'):
            print(h, ' '.join(f"{k}=#{int(v[0]):02X}{int(v[1]):02X}{int(v[2]):02X}" for k, v in ((k, project(h, mode=k)[0]) for k in MODES)))
        sys.exit()
    from PIL import Image
    mode = next((a.split('=')[1] for a in sys.argv if a.startswith('--mode=')), 'lines' if '--lines' in sys.argv else 'pigment')
    project_image(Image.open(sys.argv[1]), mode=mode).save(sys.argv[2]); print(sys.argv[2], mode)
