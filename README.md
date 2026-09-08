# DeStijl theme kit

Mondrian's 1922 pigments as a cross-platform design system. The authority
is `DESTIJL_STYLE.md`; every color the kit authors is validated against
the four lines in `palette.json` by `build/lines.py`.

```
DESTIJL_STYLE.md          authority file
palette.json              lines, grays, semantic (FHWA), chrome hues, rule geometry
NEXTY_STYLE.orig.md       the nexty file this was forked from, untouched, for diffing
build/lines.py            line test:  python3 build/lines.py '#9C9EA0' '#FF0000'
build/match_wallpaper.py  regenerates the matched full-res master from the two sources
build/wallpaper.py        desktop compositor:  python3 build/wallpaper.py 1920x1080 100
wallpaper/                MIA source, measurements, transform, full-res matched PNG
worksafe/                 per-user, no elevation: destijl.theme, theme.reg,
                          square_corners.ps1; composed wallpapers are generated
                          here on demand (see below) and are not committed
elevated/                 all-sites: destijl.user.css (Stylus)
samples/                  frame-size sample cards (28 px chosen)
issues/                   001 declutter.reg, 005 per-monitor install
```

Windows install: see the comments at the top of `worksafe/destijl.theme`.

## Wallpapers: generate on demand

The repo ships the source painting (`wallpaper/mondrian_1922_wallpaper.png`)
but not the composed desktop wallpapers. Make the one for your screen size
and Windows display scale with `build/wallpaper.py` (needs Pillow):

```
python3 build/wallpaper.py 1920x1080 100
python3 build/wallpaper.py 3840x2160 150
```

Each run writes `worksafe/mondrian_1922_<W>x<H>_s<scale>.png` plus a JSON
sidecar with the layout numbers. Both are ignored by git. Copy the PNG to
the path named by `Wallpaper=` in `worksafe/destijl.theme`.
