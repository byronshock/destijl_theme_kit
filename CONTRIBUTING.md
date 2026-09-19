# Contributing to DeStijl

`DESTIJL_STYLE.md` is the authority. This file is the procedure: what a
change carries before it lands. §8.13 makes both binding. Every rule
below cites the section it comes from; where this file and the authority
disagree, the authority is right and this file is the defect.

The kit is one composition rendered on several platforms. A change is
judged by whether the screen is still that composition, and the judgment
is a measurement (§8.8), not an opinion.

## 1. The tier boundary (§7, §3)

Two tiers. `worksafe/` is what a user can do to their own account;
`elevated/` is everything that needs more — admin, or a reach across
every site.

| Tier | Reach | Ships in |
|---|---|---|
| worksafe | per-user, no elevation: `HKCU`, `$HOME`, a browser profile. No sudo, no admin shell, nothing outside the user's own account. | `worksafe/` |
| elevated | admin, or all-sites: `HKLM` (`FontSubstitutes`), shell32 icons, an extension that restyles every site. | `elevated/` |

- Nothing in `worksafe/` asks for a password. An installer there is
  `sh install.sh` or a double-clicked `.reg`, and it backs up what it
  replaces — the Firefox installer copies the existing `user.js` and
  `chrome/` aside, the COSMIC one saves the previous background config.
  Per-user means reversible.
- **A residue that elevation could remove is not unavoidable** (§3).
  Before a defect is written into a surface's residue table, ask it:
  would elevation remove this? If yes, it is not residue. It is removed
  in `elevated/` and tolerated in `worksafe/`, and the worksafe entry
  says which. Residue is only what neither tier reaches.
- Reach decides the tier where the platform is generous about privilege.
  Firefox hands an all-sites sheet to a per-profile extension, so
  `elevated/destijl.user.css` needs no elevation on that surface; it
  stays in `elevated/` because its reach is every site. On Windows the
  same reach is an installed extension and the boundary bites.
- A surface entry (§7) is unfinished until it states all three: what is
  reached, what is tolerated as residue, what elevation adds.
- The kit's larger half is removal (§0). A surface that sets colors and
  leaves the recommendations, nags, motion and blur in place is not done.

## 2. Chrome: every authored value on a line (§1)

Every color the kit authors lies within 1.0 sRGB code values of one of
the four segments. The test is not advisory:

```
python3 build/lines.py '#9C9EA0' '#1B3A6D' '#DFCC82'
```

It prints each value with its nearest line and distance, and exits
nonzero if any is off. The three §1b semantic values are allow-listed as
exempt; `#FFFFFF` and `#000000` pass only as legend, and only on a
semantic field — anywhere else they are off the lines and a defect.
`build/lines.py` needs numpy and nothing else.

Values are not always written as hex. Extract them first:

| File | Form | Extraction |
|---|---|---|
| `*.ron` | `"#RRGGBBAA"` | truncate the alpha to 7 characters |
| `*.css`, `*.json` | `#RRGGBB` | as written |
| `destijl.theme` | `R G B` decimal | the gray and hue names in the section comment |
| `theme.reg` | ABGR / ARGB dwords | the hex named in the comment above each key |

```
grep -ohE '#[0-9A-Fa-f]{6,8}' worksafe/cosmic/destijl.ron | cut -c1-7 | sort -u | xargs python3 build/lines.py
```

A file that carries colors says so at its top, the way `destijl.ron`
does, and names the grays and hues it uses.

Checked 2026-09-19 over everything `worksafe/` and `elevated/` install,
and over `palette.json`: two values are off the lines, and neither is
painted — `#2E4670`, the §1c overlay admitted below, and `#FBE89D`, the
yellow-field derivation retired 2026-09-09. Both appear only as records:
a comment, a residue table, a note. A third off-line value is a defect
until §1c admits it.

## 3. Content: away from the points (§0a)

Content may take any color; *which* colors it takes is decided against
the chrome, by distance.

```
python3 build/lines.py --apart '#FCFBFD' '#E2E2EF' '#B6B6D8' '#8683BD' '#61409B' '#3F007D'
```

- The bar is **35**, the palette's own nearest-neighbour separation over
  its sixteen points. Content that clears it is as distinct from the
  chrome as the chrome's values are from each other. Under about 20 it
  has joined the furniture.
- The test applies the one exemption itself: a step whose chroma is
  under **27** — the chroma of yellow ⅓, the faintest hue the kit names
  — is a tint of the ground, carries no hue to confuse with a chrome
  hue, and is not measured.
- A ramp is chosen by the measurement, and the measurement is recorded
  next to the choice, so the next person regenerating the figure knows
  the hue was picked against the chrome and not because it looked nice.
- Chrome-aware applications are preferred. A library that reads
  `palette.json` in order to *avoid* it is doing the right thing; one
  that reads it in order to match it is painting information into the
  furniture.

## 4. Measure, don't eyeball (§8.8)

A new value lands with its measurement beside it: the number, what
produced it, the date, and the machine where the machine matters
(COSMIC / Pop!_OS 24.04, 3840×2160 @ 150%). Nothing arrives as "looks
right".

- Contrast ratios are stated with their pair — WHITE on the blue
  titlebar is 9.0:1 — never alone.
- Distances are stated with the line or point they are from: 22.7 off
  the blue line; 45.3 from LIGHT.
- Measurements go in the surface README's *reached* and *residue*
  tables; anything the whole kit depends on goes in `palette.json`;
  values the authority names go in `DESTIJL_STYLE.md`.
- Failed trials are kept, dated, with what they produced: the yellow
  window field (tried 2026-09-08, retired 2026-09-09), Mondrian red as
  the COSMIC accent (`#FFBFAD` links, 46 off), red as the interface text
  tint (`#1C0300` labels). The record is why no one tries them twice.
- A value with no measurement beside it is a guess, and the next person
  cannot tell it from a measured one.

## 5. Overlay exceptions (§1c)

An off-line value is admitted only in the case §1c describes: a toolkit
derives a surface from the theme's inputs and no input prevents it.
Three things first, in order.

1. **Change the input.** The exception is the last move, not the first.
   A WHITE window field derives `#CCCDCF`, on the gray line; the yellow
   field it replaced derived `#FBE89D`, 47.9 off, and the field changed
   rather than the derivation being admitted. Yellow is the COSMIC
   accent because it is light enough to pass the accent-text derivation
   unchanged.
2. **Measure it on the platform.** A prediction is not a measurement:
   the 10% pure-white overlay predicted for the sidebar row was wrong,
   and the screenshot gave `#2E4670`, 22.7 off the blue line.
3. **Record it twice.** In `palette.json`, with the date, the machine
   and the distance; and in the surface README's residue table, with why
   the kit cannot reach it. `build/lines.py` does not allow-list
   exceptions — only §1b — so the value reads as off the line wherever
   it is written down. That is intended.

An exception's scope is the surface it was measured on. Nothing else may
use it, and it lands as close to the lines as the container allows
(§8.3).

## 6. QA every build visually (§8.9)

Every build is looked at on the target before delivery, as a screen and
not as a file. The theme a toolkit builds is not the theme that was
imported: COSMIC derives surfaces no file records, so those values exist
only on the screen. On COSMIC the pass is non-interactive:

```
cosmic-settings appearance export ~/destijl-before.ron
sh worksafe/cosmic/install.sh
cosmic-screenshot --interactive=false --modal=false --notify=false -s ~/Pictures/destijl
```

Sample the regions out of the PNG and run the samples back through
`build/lines.py`. The line test needs only numpy; sampling needs Pillow,
and `icon_theme.py` needs cairosvg as well. Where the system python
lacks them, a venv does, and `install.sh` takes
`DESTIJL_PYTHON=/path/to/venv/bin/python`.

What the pass is looking for: one rule, the same width everywhere on the
screen, carrying no state (§3); key and non-key windows told apart by
the titlebar and not by the rule (§1); no curve the kit drew; no hue in
chrome outside the three, in roughly the painting's proportions; the
semantic three present only where the meaning is (§1b).

## 7. Generated files

The repo ships sources and what cannot be regenerated. What a machine
can make, the machine makes on the machine that needs it:

- composed wallpapers — `build/wallpaper.py` writes
  `worksafe/mondrian_1922_<W>x<H>_s<scale>.png` and its JSON sidecar;
  both are gitignored, and the size and scale are the user's, not the
  repo's.
- the application icon theme — `build/icon_theme.py` builds
  `~/.local/share/icons/destijl` at install time from the icons that
  machine actually has (§4b). It is the user's brands in the user's
  paint and never enters the repo.
- `__pycache__`, always.

One generated file is committed, for a reason: `elevated/destijl.stylus.json`.
Stylus imports its own JSON and balks at `*.user.css`, so the import file
has to ship. `elevated/destijl.user.css` is the source. After editing the
sheet: bump `@version`, add the change to the header's changelog with what
it fixed, run `python3 build/stylus_json.py`, and commit both files
together.

The pipeline generates its own demo assets (§8.12): a sample in the repo
is reproducible by a command named in the README, not drawn by hand.

## 8. License

Two licenses, split by what the file is; a file's license follows the
directory it lands in.

| Covers | License | Text |
|---|---|---|
| `build/`, `elevated/`, `worksafe/` | GNU GPL v3.0 or later | `LICENSE` |
| `DESTIJL_STYLE.md`, `palette.json`, `wallpaper/`, `issues/`, `cosmic_screenshot.png`, `README.md`, this file | CC BY-SA 4.0 | `LICENSE-CC-BY-SA` |

Contributing is agreeing to those terms for what you contribute. Both
are copyleft: a derivative is shared under the same license. Color
values are not copyrightable; what is licensed is the documents, images
and code that express them.

A new image carries its provenance in the README the way the two source
photographs do — where it came from, its object or item number, and the
rights statement that permits the use (Minneapolis Institute of Art
object 1595, CC PDM; rawpixel 3219952, CC0 1.0). An image whose rights
cannot be stated that plainly does not ship.

## 9. The form of a change

- Issues are files: `issues/NNN-slug.md`, titled, with `**Labels:**` and
  `**Implements:** DESTIJL_STYLE.md §…` beneath, then what was observed,
  dated, with the numbers.
- A change that alters a rule edits `DESTIJL_STYLE.md` in the same
  commit as the thing that proves it. The authority is not brought up to
  date afterwards from memory.
- A commit subject names the surface or the section it touches.
- Deliverables are PDFs with fonts embedded (§8.10). Speaker notes are
  extracted from the built pptx, never retyped (§8.11).

Before it lands: the line test passes over every value the change
authors; content values clear 35 (§0a); every new number has its
measurement, date and machine beside it; any §1c exception is recorded
in `palette.json` and in the surface README; the build has been seen on
the target; nothing generated has been committed except the Stylus JSON
with its `@version` bumped; the tier the change ships in matches the
privilege and the reach it needs.
