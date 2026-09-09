"""Compose the DeStijl desktop (DESTIJL_STYLE.md §5) for a given screen.

The screen is itself a composition. The painting is the large field, flush
to the right edge, never cropped, never stretched. A DARK wall on the left
carries the desktop icons (Windows) or the dock (COSMIC). A DARK band along
the edge that carries the platform's bar is --bottom or --top bar-heights
tall (default: bottom, 2), the bar in its outer part with an equal strip of
wall showing inside it. Asymmetric on purpose: the canvas's own logic — big
field to one side, small fields along two edges — repeated one level up.

Windows 11: the taskbar is 48 logical px at the bottom.
COSMIC:     the panel is 32 logical px at the top (size XS); the dock is on
            the left wall. Pass --top 2 --bottom 0 --bar 32 --tag cosmic.

Usage:
  python3 build/wallpaper.py 1920x1080 100
  python3 build/wallpaper.py 3840x2160 150 --out worksafe/ --bottom 2
  python3 build/wallpaper.py 3840x2160 150 --top 2 --bottom 0 --bar 32 --tag cosmic
Writes  mondrian_1922[_<tag>]_<W>x<H>_s<scale>.png  (sRGB-tagged PNG) and a
JSON sidecar with the layout numbers; rule_px (physical) and rule_pt
(logical) are the §3 rule at this painting's scale — the COSMIC gap reads
rule_pt.
"""
import argparse, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
SRC = os.path.join(ROOT, 'wallpaper', 'mondrian_1922_wallpaper.png')
PAL = json.load(open(os.path.join(ROOT, 'palette.json')))
TASKBAR_LOGICAL = 48          # Windows 11, bottom, fixed
PAINTING = (5286, 4526)       # wallpaper/mondrian_1922_wallpaper.png, px


def hex_rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def layout(W, H, scale_pct, bottom=2.0, top=0.0, bar_logical=TASKBAR_LOGICAL, painting=PAINTING):
    """The numbers only (no Pillow): where the art goes and what the rule is on this screen."""
    sw, sh = painting
    bar = round(bar_logical * scale_pct / 100)         # the platform's bar, physical px
    band_b = round(bar * bottom)                       # DARK band below the art; bar in its lower part
    band_t = round(bar * top)                          # DARK band above the art; bar in its upper part
    s = min(W / sw, (H - band_t - band_b) / sh)        # proportional fit into the field between the bands
    w, h = round(sw * s), round(sh * s)
    x0, y0 = W - w, band_t                             # flush right, under the top band; the left wall takes the residual
    rule = round(PAL['geometry']['rule_fraction'] * w)   # §3: the rule at this painting's scale
    return dict(art=(w, h), at=(x0, y0), bar=bar, band_top=band_t, band_bottom=band_b,
                wall_left=x0, wall_below_top_bar=band_t - bar if band_t else 0,
                wall_above_bottom_bar=H - y0 - h - bar if band_b else 0,
                rule_px=rule, rule_pt=round(rule * 100 / scale_pct))


def compose(W, H, scale_pct, **kw):
    from PIL import Image
    src = Image.open(SRC).convert('RGB')
    info = layout(W, H, scale_pct, painting=src.size, **kw)
    art = src.resize(info['art'], Image.LANCZOS)
    canvas = Image.new('RGB', (W, H), hex_rgb(PAL['grays']['DARK']))
    canvas.paste(art, info['at'])
    return canvas, info


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('size', help='WxH, e.g. 1920x1080')
    ap.add_argument('scale', type=int, help='display scale percent: 100, 125, 150, 200')
    ap.add_argument('--out', default=os.path.join(ROOT, 'worksafe'))
    ap.add_argument('--bottom', type=float, default=2.0, help='bottom band in bar heights (0 for none)')
    ap.add_argument('--top', type=float, default=0.0, help='top band in bar heights (0 for none)')
    ap.add_argument('--bar', type=int, default=TASKBAR_LOGICAL, help='bar height, logical px (Windows taskbar 48, COSMIC panel XS 32)')
    ap.add_argument('--tag', default='', help='name tag, e.g. cosmic')
    ap.add_argument('--layout-only', action='store_true', help='print the layout JSON and write nothing (no Pillow needed)')
    a = ap.parse_args()
    W, H = map(int, a.size.lower().split('x'))
    kw = dict(bottom=max(0.0, a.bottom), top=max(0.0, a.top), bar_logical=a.bar)
    if a.layout_only:
        print(json.dumps(dict(size=[W, H], scale=a.scale, **layout(W, H, a.scale, **kw)))); raise SystemExit
    from PIL import ImageCms
    im, info = compose(W, H, a.scale, **kw)
    srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
    tag = f'_{a.tag}' if a.tag else ''
    out = os.path.join(a.out, f'mondrian_1922{tag}_{W}x{H}_s{a.scale}.png')
    im.save(out, icc_profile=srgb, optimize=True)
    json.dump(dict(size=[W, H], scale=a.scale, **{k: v for k, v in info.items()}),
              open(out[:-4] + '.json', 'w'), indent=1)
    print(f'{out}: art {info["art"][0]}x{info["art"][1]} at {info["at"]}; left wall {info["wall_left"]}px; '
          f'top band {info["band_top"]}px, bottom band {info["band_bottom"]}px (bar {info["bar"]}); '
          f'rule {info["rule_px"]}px = {info["rule_pt"]}pt')
