# nexty design system

The branch where NeXT never became Aqua. NeXTSTEP 2.x (1991) chrome,
maintained continuously to the present: same four grays, same bevels,
same square corners, same left scrollbar — rendered on modern displays
with anti-aliased type, resolution-independent geometry, and 8-bit
tonal icons. This file is the authority for nexty. Where nexty inherits
from Phosphor it says so explicitly; nothing is inherited by assumption.

Sibling of `PHOSPHOR_STYLE.md`. The two systems do not mix.

## 0. The strong statement

**Chrome is grayscale. No accent color, no highlight tint, no "just
this once."** Titlebars, buttons, scrollers, menus, dock tiles, badges,
focus rings, selection: four grays and nothing else.

Three things may have hue:

1. *Content* — a photo in a window, a syntax-colored buffer, a chart.
   The frame around it never takes a hue.
2. *Semantic state* — exactly three: **success green, warning yellow,
   destructive red** (§1b). A green check, a yellow triangle, a red
   destructive button. Not decoration, not accent, not selection.
3. *Identity* — an application's own icon, on a canon tile (§4b).
   Branding is information; the eye finds a brand faster than it
   reads a label. The tile under it is chrome and stays gray.

This is the one rule that makes the system what it is. Everything else
is measurement.

## 1. Palette

Four values, the NeXT AppKit gray constants, exact:

| Role  | Hex       | NS constant       | Use |
|-------|-----------|-------------------|-----|
| WHITE | `#FFFFFF` | NSWhite (1.000)   | text fields, lists, bevel highlights, titlebar text on key windows |
| LIGHT | `#AAAAAA` | NSLightGray (.667)| window and panel surfaces, buttons, non-key titlebars |
| DARK  | `#555555` | NSDarkGray (.333) | desktop, bevel shadows, dock tiles, disabled text |
| BLACK | `#000000` | NSBlack (0.000)   | key titlebar, text, outlines, badges |

Rendering at 8-bit means intermediate grays *may* appear in content and
in icon shading. They never appear in chrome. A chrome pixel that is not
one of these four values is a bug.

Terminal ANSI ramp (grayscale, 16 slots mapped by luminance):

```
0 #000000   4 #333333   8  #555555   12 #999999
1 #444444   5 #666666   9  #AAAAAA   13 #BBBBBB
2 #555555   6 #777777   10 #AAAAAA   14 #CCCCCC
3 #888888   7 #AAAAAA   11 #DDDDDD   15 #FFFFFF
```
fg `#000000` · bg `#FFFFFF` · cursor `#000000` block · selection `#AAAAAA`

A color-content ANSI ramp is a *fenced option* (`nexty-color`), not
canon. It exists because ANSI color is content, and content may have
color. It is not the default.

### 1b. Semantic state colors

The only hue permitted in chrome. Deep enough to carry WHITE text on
LIGHT surfaces (yellow carries BLACK).

| Role        | Hex       | Text on it | Where |
|-------------|-----------|------------|-------|
| SUCCESS     | `#1E6E34` | WHITE      | confirmations, ok emblems, "done" |
| WARNING     | `#E6B400` | BLACK      | caution panels, warning triangle |
| DESTRUCTIVE | `#A61B1B` | WHITE      | delete/discard buttons, error panels |

They appear only when the *meaning* is present. A red button that isn't
destructive is a defect. Accent, focus and selection remain BLACK.

### 1c. Exception: toolkit state overlays (COSMIC only)

COSMIC derives hover, selected and pressed states as a 10% / 20% pure-white
or pure-black overlay on the container, and no theme value can prevent it.
On a DARK `#555555` container this yields `#666666` (hover, selected) and
`#777777` (pressed). These two values are admitted, in COSMIC chrome only,
as the third and last exception to §1 (after the badge pill and the tile
gradient). The container itself stays canon; the accent becomes WHITE so
selected text remains legible on the overlay. Nothing else may use them.

## 2. Typography

Two fonts. Both anti-aliased, hinted, rendered clean at any DPI. The
bitmap era is over; a maintained NeXTSTEP would have had AA text since
the late 1990s.

- **UI: Helvetica**, 12pt system size (NSFontSize 12). The kit ships
  **Nimbus Sans** (URW, free, metric-compatible) and names it in every
  artifact; Helvetica proper is not redistributable.
  Bold for titlebar text and default buttons only.
- **Mono: Hack**, all weights. Inherited from Phosphor unchanged,
  advance width 0.602 em, so all Phosphor cursor and column math
  carries over. Terminal, code, fixed-width tables, the `nexty` session
  chip in decks.

Sizes are in points. 1pt = 1px @1x, 2px @2x, 3px @3x. Never fractional.

## 3. Geometry (measured)

Constants below are taken from the GNUstep `libs-gui` and WindowMaker
sources, which reimplement NeXTSTEP pixel-for-pixel, and cross-checked
against period screenshots. All values in pt.

### Window
- Titlebar: **23** (includes the 1pt black border line at the top)
- Titlebar buttons (close left, miniaturize right): **15 × 15**,
  padding **4** top / left / right
- Titlebar text: Helvetica Bold 12, centered
- Resize bar (bottom): **9**, center notch **30** wide
- Key window: titlebar BLACK, text WHITE
- Non-key window: titlebar LIGHT, text BLACK
- Corners: **square**. Radius 0. Everywhere. Forever.
- Shadow: soft BLACK drop shadow, offset 0 / +3, blur 12, opacity 0.5.
  The one modern addition. No translucency, no backdrop blur.

### Bevels (the four recipes)

Edges named in screen orientation. Each edge is a 1pt line.

**Button / raised** (`NSDrawButton`):
```
outer:  right + bottom  BLACK
inner:  left  + top     WHITE
inner:  right + bottom  DARK
fill:                   LIGHT
```
Shadow sides are 2pt total (BLACK outside DARK); highlight sides 1pt.

**Sunken field** (`NSDrawGrayBezel`) — text fields, wells:
```
outer:  right + bottom  WHITE
outer:  left  + top     DARK
inner:  right + bottom  LIGHT
inner:  left  + top     BLACK
fill:                   DARK
```

**White bezel** (`NSDrawWhiteBezel`) — lists, browser columns, text views:
```
outer:  all four        DARK      (top) / WHITE (right, bottom) / DARK (left)
inner:  top             DARK
inner:  right, bottom   LIGHT
inner:  left            DARK
fill:                   WHITE
```

**Groove** (`NSDrawGroove`) — separators, box frames:
```
outer: left + top  DARK, inner left + top WHITE
outer: right + bottom WHITE, inner right + bottom DARK
```

Pressed button = raised recipe with WHITE and DARK/BLACK edges swapped,
fill LIGHT. Default button carries a Return-key glyph at the right.

### Scroller
- Width: **18**, on the **left** of the scrolled content
- Track: sunken (gray bezel), knob: raised button with a single centered
  dimple, arrows at the **bottom** (NeXT convention), both together

### Menus
- Vertical, top-left of screen, tear-off. Item height: **20**.
  Title bar of a menu: BLACK with WHITE text.
- Items: Helvetica 12 on LIGHT. Submenu indicator: right-pointing
  triangle. Keyboard equivalent right-aligned.
- Selected item: BLACK fill, WHITE text. (Tone, not hue.)

### Dock and tiles
- Tile: **64 × 64**, raised-button bevel over a **diagonal gradient LIGHT
  (top-left) → DARK (bottom-right)**. Measured from WindowMaker's
  `IconBack = (dgradient, a6a6b6, 515561)`, desaturated to canon endpoints.
  This is the second and last exception to §1 (the badge pill is the first):
  a gradient *between two canon grays*, on the tile only.
- Icon art: **48 × 48**, centered, 8pt margin
- Dock: right edge, single column, application tile top
- Miniwindows: 64 × 64 tiles, bottom-left, with the app icon and the
  window title in Helvetica 9 beneath
- Badge (unread count): BLACK rounded pill — the *only* rounding in the
  system, radius = half height — WHITE Helvetica Bold 10, bottom-right
  of the tile. This is how Mail.app did it in 1991 and it is the state
  signal for everything.

### File viewer
- Browser columns, white bezel, column width **~155**, Helvetica 12,
  directory rows end in a right-pointing triangle.

### Desktop
- Default: flat DARK, no image. Image wallpapers allowed; see §5.
- Reference screen: 1120 × 832 @ 92 dpi (MegaPixel). Modern targets are
  arbitrary; the reference matters only as the origin of the pt scale.

## 4. Icons

### 4a. System icons

- 48pt base in a 64pt tile. Shipped @1x / @2x / @3x (48/96/144 px).
- **Grayscale, 8-bit, smooth-shaded** in the Ohlfs photorealistic
  house style: soft top-left light, real form, no outlines, no flat
  "material" fills. Dither is an optional pipeline flag
  (`--dither 2bit`) for period texture, not canon.
- State: disabled = DARK-tinted; unread/count = the badge; document
  state = dogear. The three semantic colors (§1b) appear only on status
  icons that mean success, warning or destructive.
- The NeXT cube logo is protected and does not appear. A plain
  unlettered isometric cube is an acceptable generic glyph.
- Scope: folders, devices, mimetypes, status, and first-party desktop
  apps (Files, Terminal, Settings). Furniture, not brands.

### 4b. Application icons

Icons carry information, and in the 21st century they are permitted to
carry it in color. An application icon is a *brand*, and a brand is
information: the eye finds Claude's starburst or Chrome's disc in a
dock faster than it reads a label, and far faster than it can tell one
gray monitor from another. Color that identifies is information.
Color that sells is noise.

- An application keeps its own icon art, hue included. The kit does
  not repaint it gray and does not redraw it.
- The **tile** is chrome and stays canon: 64pt, square, raised-button
  bevel over the LIGHT → DARK diagonal gradient (§3). The app's art
  sits on it at 48pt, centered, 8pt margin, with the standard
  hard-offset shadow. Chrome around the brand; the brand never bleeds
  into the chrome.
- Badge, disabled tint, and semantic emblems on an application icon
  follow §1b and §4a unchanged.
- Advertising is noise: promotional variants, seasonal recolors,
  attention-seeking animation. An icon that changes to get noticed has
  stopped being a brand and is replaced by the generic cube.

Rule of thumb: if removing the color would make the icon harder to
*find*, the color is information. If removing it would make the icon
harder to *ignore*, it was noise.

## 5. Wallpapers and the image pipeline

- House wallpapers are **grayscale**: luminance-mapped, gamma-preserved,
  full 8-bit. Color photographs are content and are *permitted* as
  wallpapers, but nothing the kit generates is in color.
- Pipeline: proportional fit, edge-aligned integer grid where a grid is
  used (inherited from Phosphor: no stretch, residual as center crop,
  matting is a separate step). Upscaling of period assets is
  nearest-neighbor only.
- ASCII/glyph art in nexty is Hack, BLACK on WHITE (terminal polarity),
  single class. Two-class art is a Phosphor thing.

## 6. Decks

Same pptxgenjs toolchain, different chrome:

- Background WHITE. Body text BLACK Helvetica. Code Hack.
- Frame: a single raised-button bevel around the slide content area
  (not corner brackets — those are Phosphor).
- Session chip top-left: `nexty` in Hack 11 DARK. Slide chip top-right
  `[ 03 / 07 ]` Hack 11 DARK. Titlebar band across the top: BLACK,
  WHITE Helvetica Bold, slide title centered — the slide *is* a key
  window.
- Cursor: BLACK block rect named `cursor_blink`, same injector.
- Emphasis: bold, or a sunken LIGHT well. Semantic colors only when a
  slide is literally reporting a success, warning or destructive act.

## 7. What nexty inherits from Phosphor (explicit list)

1. Hack, 0.602 em advance, and all cursor/column math built on it.
2. Edge-aligned zero-stretch grid geometry for any raster pipeline.
3. The worksafe / elevated tier boundary and every rule in
   `CONTRIBUTING.md`.
4. Principle: measure, don't eyeball.
5. Principle: QA every build visually before delivery.
6. Principle: deliverables are PDFs with fonts embedded.
7. Principle: speaker notes extracted from the built pptx, never retyped.
8. Dogfooding: the pipeline generates its own demo assets.

Everything not on this list is not inherited.

## 8. Principles

1. Chrome is grayscale. Content, semantic state, and application
   identity may have color. (§0, §4b.)
2. Four grays in chrome, exact. Any other value is a defect.
3. Square corners. The badge pill is the sole exception.
   Four flat grays in chrome. The tile gradient and the COSMIC overlay
   values of §1c are the only exceptions.
4. Tone and geometry carry state; hue only for success / warning /
   destructive, and only when the meaning is present.
5. Resolution-independent points, integer-scaled. No fractional bevels.
6. Modern rendering, period structure: AA text, 8-bit icons, real
   shadows — on 1991 layout and 1991 bevels.
7. Measure, don't eyeball.
