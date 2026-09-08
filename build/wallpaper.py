"""Compose the DeStijl desktop (DESTIJL_STYLE.md §5) for a given screen.

The screen is itself a composition. The painting is the large field, flush
to the top-right corner, never cropped, never stretched. A DARK wall on the
left carries the desktop icons; a DARK band along the bottom, --bottom
taskbar-heights tall (default 2), carries the Windows 11 taskbar (48 logical
px, scaled) with an equal strip of wall showing above it. Asymmetric on
purpose: the canvas's own logic — big field upper right, small fields along
the left and bottom edges — repeated one level up.

Usage:
  python3 build/wallpaper.py 1920x1080 100
  python3 build/wallpaper.py 3840x2160 150 --out worksafe/ --bottom 2
Writes  mondrian_1922_<W>x<H>_s<scale>.png  (sRGB-tagged PNG).
"""
import argparse, json, os
from PIL import Image, ImageCms

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
SRC = os.path.join(ROOT, 'wallpaper', 'mondrian_1922_wallpaper.png')
PAL = json.load(open(os.path.join(ROOT, 'palette.json')))
TASKBAR_LOGICAL = 48          # Windows 11, bottom, fixed


def hex_rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def compose(W, H, scale_pct, bottom=2.0, taskbar_logical=TASKBAR_LOGICAL):
    dark = hex_rgb(PAL['grays']['DARK'])
    taskbar = round(taskbar_logical * scale_pct / 100)
    band = round(taskbar * bottom)                     # DARK band; taskbar occupies its lower part
    src = Image.open(SRC).convert('RGB'); sw, sh = src.size
    s = min(W / sw, (H - band) / sh)                   # proportional fit into the field above the band
    w, h = round(sw * s), round(sh * s)
    art = src.resize((w, h), Image.LANCZOS)
    canvas = Image.new('RGB', (W, H), dark)
    x0, y0 = W - w, 0                                  # flush top-right; the left wall takes the residual
    canvas.paste(art, (x0, y0))
    rule = round(PAL['geometry']['rule_fraction'] * w)   # §3: the rule at this painting's scale
    return canvas, dict(art=(w, h), at=(x0, y0), taskbar=taskbar, band=band,
                        wall_left=x0, wall_above_taskbar=H - h - taskbar, rule_px=rule)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('size', help='WxH, e.g. 1920x1080')
    ap.add_argument('scale', type=int, help='display scale percent: 100, 125, 150, 200')
    ap.add_argument('--out', default=os.path.join(ROOT, 'worksafe'))
    ap.add_argument('--bottom', type=float, default=2.0, help='bottom band in taskbar heights (>= 1)')
    a = ap.parse_args()
    W, H = map(int, a.size.lower().split('x'))
    im, info = compose(W, H, a.scale, bottom=max(1.0, a.bottom))
    srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
    out = os.path.join(a.out, f'mondrian_1922_{W}x{H}_s{a.scale}.png')
    im.save(out, icc_profile=srgb, optimize=True)
    json.dump(dict(size=[W, H], scale=a.scale, **{k: v for k, v in info.items()}),
              open(out[:-4] + '.json', 'w'), indent=1)          # sidecar: the COSMIC gap reads rule_px
    print(f'{out}: art {info["art"][0]}x{info["art"][1]} at {info["at"]}; '
          f'left wall {info["wall_left"]}px; bottom band {info["band"]}px '
          f'(taskbar {info["taskbar"]}, wall above it {info["wall_above_taskbar"]}); rule {info["rule_px"]}px')
