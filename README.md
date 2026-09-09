# DeStijl theme kit

Mondrian's 1922 pigments as a cross-platform design system. The authority
is `DESTIJL_STYLE.md`; every color the kit authors is validated against
the four lines in `palette.json` by `build/lines.py`.

```
DESTIJL_STYLE.md          authority file
palette.json              lines, grays, semantic (FHWA), chrome hues, rule geometry
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

## License

Two licenses, split by what the file is:

- **Code** (`build/`, `elevated/`, `worksafe/`): GNU General Public License
  v3.0 or later. See `LICENSE`.
- **Design and assets** (`DESTIJL_STYLE.md`, `palette.json`, `samples/`,
  `wallpaper/`, `issues/`, this README): Creative Commons
  Attribution-ShareAlike 4.0 International. See `LICENSE-CC-BY-SA`.

Both are copyleft: derivatives must be shared under the same terms. Color
values themselves are not copyrightable; the license covers the documents,
images, and code that express them.

Provenance of the source images:

- Mondrian, *Composition with Blue, Red, Yellow, and Black* (1922) is in
  the public domain.
- `wallpaper/mia_4001106_800.jpg`: Minneapolis Institute of Art, object
  1595, rendition `mia_4001106.jpg`. Rights type Public Domain (CC PDM);
  Mia permits copying, modifying, and distributing, including commercially,
  without permission. Used here for its color measurements.
- `wallpaper/rawpixel_3219952.jpg`: rawpixel image 3219952, released under
  CC0 1.0 (<https://creativecommons.org/publicdomain/zero/1.0/>). Supplies
  the pixels for the matched master.

The matched master derived from them (`wallpaper/mondrian_1922_wallpaper.*`)
is offered under CC BY-SA 4.0 like the rest of the design assets.
