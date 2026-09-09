# Mondrian-space icon tinting

**Labels:** icons, build, cross-platform
**Implements:** `DESTIJL_STYLE.md` §1 (the four lines), §4b (application icons), §8.7 (modern rendering)

## Why

§4b lets an application keep its own icon, hue included, because a brand is
information. But a dock full of brands in their own saturated sRGB reads
as a billboard next to a chrome that is Mondrian's pigments and nothing
else. The reconciliation is to keep the *identity* of each icon and
re-express it in the composition's own colors: Chrome's disc is still
red, yellow, green and blue in shape, but its red is Mondrian's red.

## The projection

Mondrian space is the color space the five pigments define. Its anchors
are the measured endpoints of `palette.json`:

| sRGB | maps to | Mondrian |
|---|---|---|
| `#000000` K | → | BLACK `#0A0F10` |
| `#FFFFFF` W | → | WHITE `#E5E6E8` |
| `#FF0000` R | → | red `#D64D24` |
| `#FFFF00` Y | → | yellow `#DFCC82` |
| `#0000FF` B | → | blue `#1B3A6D` |

These five points define the full space: their convex hull in sRGB. The
projection is two steps, in `build/mondrian_space.py`:

1. **Warp.** Every sRGB color moves by the anchor offsets, weighted by
   its proximity to each anchor (the softmax-of-distance method already
   used by `build/match_wallpaper.py`). Exact at the five anchors: pure
   red becomes Mondrian's red, white becomes WHITE.
2. **Clip.** A color that lands inside the hull is kept. One outside it
   goes to the nearest point of the hull's surface. Green, cyan, magenta
   and every tint toward white have no position in the space and are
   clipped to the nearest one that does.

`--lines` clips to the four *lines* of §1 instead of the hull. The hull is
the icon rule (a brand may mix pigments, as a painting does); the lines
are the chrome rule.

Measured on the primaries (hull / lines):

```
#FF0000 -> #D64D24 / #D64D24      #00FF00 -> #58666D / #5E6263
#FFFF00 -> #DFCC82 / #DFCC82      #00FFFF -> #798AA6 / #939597
#0000FF -> #1B3A6D / #1B3A6D      #FF00FF -> #C69085 / #A2A5A6
#FFFFFF -> #E5E6E8 / #E5E6E8      #FF8000 -> #DA8951 / #B5A66B
```

## First run (2026-09-08, Chrome, Claude, LibreOffice Calc at 128 px)

- **Hull** keeps identity: Chrome's four wedges stay four tones, Claude's
  starburst stays warm. Bright sRGB blue has nowhere bright to go —
  nothing in the space is brighter than the painting — so Chrome's blue
  disc becomes a dark blue-gray. That is the pigments' answer, not a bug.
- **Lines** bands. Nearest-line clipping is discontinuous: a smooth
  coral gradient flips from the gray line to the yellow line partway
  across and the icon splits in two tones. The lines are the chrome rule;
  they are the wrong clip for continuous-tone art. Prefer the hull, or
  clip in a lightness-preserving space (step 3).
- The hull admits tints toward white (a red-white mix is inside it),
  which §1 forbids for chrome. Icons are not chrome; §4b decides.

## Style-guide consequence

§4b currently says an application keeps its icon "hue included" and the
kit "does not snap it to the four lines". Projection into Mondrian space
is a third thing: the brand's hues re-expressed in the composition's
pigments, identity kept. If this ships, §4b needs a sentence saying so.

## Do

1. **Generator.** Resolve each app's real icon through the theme chain the
   way the desktop does (`.desktop` `Icon=` → hicolor / the inherit
   chain), rasterize SVGs at 48pt @1x/@2x/@3x, project every pixel, and
   emit an overlay icon theme (`destijl`, `Inherits=` the platform's own)
   that ships only `apps/`. Alpha untouched; the tile, if any, is chrome
   and comes from §4a.
2. **Judge the two clips on real icons.** Hull keeps more of a brand
   (Chrome's green wedge stays a distinct dull green); lines collapses
   everything foreign to gray. §4b's test decides: if the clipped icon is
   harder to *find*, the clip took information.
3. **Lightness.** Check that the warp preserves luminance ordering inside
   a gradient; if a brand's highlight and shadow swap, project in a
   lightness-preserving space (OKLab) and clip chroma only.
4. **Scope.** Whether COSMIC's first-party icons (Files, Settings, Store,
   Terminal) get projected too. §4a says a desktop's own apps keep their
   icons; §4b says a brand may carry color; the projection satisfies both.
5. **Zed** and any app whose `.desktop` points at an absolute path cannot
   be overridden by a theme. Residue.

## Out of scope

Redrawing icons. The generator projects what exists; it authors nothing.
