"""Regenerate wallpaper/mondrian_1922_wallpaper.{png,jpg} from the two sources.

  wallpaper/rawpixel_3219952.jpg   pixels (5286x4526, Adobe RGB 1998)
  wallpaper/mondrian_1922_palette.json   MIA field medians = the line endpoints (§1)

Method (wallpaper/mondrian_1922_wallpaper_transform.json): convert Adobe RGB
to sRGB (relative colorimetric), then per pixel add a soft-assigned offset so
each of the five fields' medians lands on its MIA value while brushwork inside
the field is kept. Re-measures the result and prints the residuals.
"""
import io, json, os
import numpy as np
from PIL import Image, ImageCms

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
W = os.path.join(ROOT, 'wallpaper')
T = json.load(open(os.path.join(W, 'mondrian_1922_wallpaper_transform.json')))
src = np.array(T['anchors_src'], float); dst = np.array(T['anchors_dst'], float); sigma = float(T['sigma'])

im = Image.open(os.path.join(W, 'rawpixel_3219952.jpg'))
prof = ImageCms.ImageCmsProfile(io.BytesIO(im.info['icc_profile']))
srgb = ImageCms.createProfile('sRGB')
im = ImageCms.profileToProfile(im, prof, srgb, renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC, outputMode='RGB')
a = np.asarray(im).astype(float); H, Wd, _ = a.shape
p = a.reshape(-1, 3); out = np.empty_like(p); delta = dst - src
for i in range(0, len(p), 2_000_000):
    q = p[i:i + 2_000_000]
    d2 = ((q[:, None, :] - src[None, :, :]) ** 2).sum(-1)
    w = np.exp(-(d2 - d2.min(1, keepdims=True)) / (2 * sigma ** 2)); w /= w.sum(1, keepdims=True)
    out[i:i + 2_000_000] = q + w @ delta
out = np.clip(np.round(out), 0, 255).astype(np.uint8).reshape(H, Wd, 3)
res = Image.fromarray(out); icc = ImageCms.ImageCmsProfile(srgb).tobytes()
res.save(os.path.join(W, 'mondrian_1922_wallpaper.png'), icc_profile=icc)
res.save(os.path.join(W, 'mondrian_1922_wallpaper.jpg'), quality=95, subsampling=0, icc_profile=icc, dpi=(300, 300))

b = out.astype(float); hx = lambda v: '#%02X%02X%02X' % tuple(int(round(c)) for c in v)
for k, r in [('WHITE', (1456, 4988, 403, 4007)), ('BLACK', (1456, 4988, 4097, 4156)), ('BLUE', (1456, 4988, 40, 154)),
             ('RED', (3400, 4950, 4240, 4500)), ('YELLOW', (520, 1208, 3102, 4486))]:
    x0, x1, y0, y1 = r; m = np.median(b[y0:y1, x0:x1].reshape(-1, 3), 0)
    tgt = dst[['WHITE', 'BLACK', 'BLUE', 'RED', 'YELLOW'].index(k)]
    print(f'{k:7} {hx(m)}  target {hx(tgt)}  d={np.linalg.norm(m - tgt):.2f}')
