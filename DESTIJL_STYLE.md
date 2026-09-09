# De Stijl design system

Four grays and Piet Mondrian's palette, rendered on modern displays with
anti-aliased type, resolution-independent geometry, and 8-bit tonal
icons. Every color the kit authors lies on
one of four lines from Mondrian's black to his white, red, blue and
yellow (§1). This file is the authority for De Stijl.

## 0. The strong statement

**The point is to save users from Windows**, and from any platform
that behaves like it. The skin is the smaller half of that. The larger
half is removing what the platform put in the user's way —
recommendations, nags, motion, blur — and both are in scope. A surface
that ships the first without the second is unfinished.

**Chrome is Mondrian's pigments — the black, white, gray, red, blue
and yellow of this one composition (§1) — and nothing else. No accent
color from outside it, no highlight tint, no "just this once."**
Titlebars, buttons, scrollers, menus, focus rings, selection: those six
and nothing else, and hue in chrome is composition, never state (§8.4).

Three further things may have color:

1. *Content* — a photo in a window, a syntax-colored buffer, a chart.
   The frame around it never takes a hue.
2. *Semantic state* — exactly three: **success green, warning yellow,
   destructive red** (§1b), in US highway sign colors. A green check, a
   yellow triangle, a red destructive button. Not decoration, not
   accent, not selection.
3. *Identity* — an application's own icon (§4b). Branding is
   information; the eye finds a brand faster than it reads a label.
   The chrome around it stays gray.

This is the one rule that makes the system what it is. Everything else
is measurement.

## 1. Palette

### The four lines

Every color the kit specifies or generates lies on one of four line
segments through the sRGB cube, all radiating from one black. The
endpoints are Mondrian's own, measured from *Composition with Blue,
Red, Yellow, and Black* (1922) — the default desktop (§5) — as the
per-channel median of each field's interior in the Minneapolis
Institute of Art reproduction (`wallpaper/mondrian_1922_palette.json`
records the method). Shades toward black are admitted; tints toward
white are not, and nothing is brighter than the painting.

| Line   | 0 (BLACK) | 1/3       | 2/3       | 1         |
|--------|-----------|-----------|-----------|-----------|
| gray   | `#0A0F10` | `#535758` | `#9C9EA0` | `#E5E6E8` |
| red    | `#0A0F10` | `#4E2417` | `#92381D` | `#D64D24` |
| blue   | `#0A0F10` | `#101D2F` | `#152C4E` | `#1B3A6D` |
| yellow | `#0A0F10` | `#514E36` | `#988D5C` | `#DFCC82` |

Named points sit at thirds along every line, interpolated in sRGB code
values. Nothing off these segments is a DeStijl color: no green, no
cyan or magenta, no tint of any hue toward white, no gray outside
`#0A0F10`–`#E5E6E8`. The test is distance to the nearest segment,
tolerance 1.0 in sRGB code values (integer rounding of an on-line
point never exceeds 0.87). It lives in `build/lines.py` and runs over
every palette value, with the three §1b values allow-listed:

```
on_line(p) = min over segments (BLACK→END) of
             | p − (BLACK + t·(END − BLACK)) |  ≤ 1.0,
             t = clamp(((p − BLACK)·(END − BLACK)) / |END − BLACK|², 0, 1)
```

### The four grays

Four values on the gray line at NeXT's steps, the NeXTSTEP AppKit gray
constants NSBlack 0, NSDarkGray .333, NSLightGray .667, NSWhite 1.000:
the steps are NeXT's, the endpoints are Mondrian's.

| Role  | Hex       | Step  | Use |
|-------|-----------|-------|-----|
| WHITE | `#E5E6E8` | 1.000 | window backgrounds, text fields, lists, bevel highlights, titlebar text on key windows; the COSMIC accent (§7) |
| LIGHT | `#9C9EA0` | .667  | panels, buttons, non-key titlebars |
| DARK  | `#535758` | .333  | desktop, bevel shadows, dock tiles, disabled text |
| BLACK | `#0A0F10` | 0.000 | rules (§3), text, badges |

### Hue in chrome (composition, §8.1)

Mondrian's three hues appear in chrome as composition, in roughly the
painting's proportions (yellow 8.6%, blue 4.5%, red 2.4%), and never as
state (§8.4):

| Hue    | Hex       | Chrome |
|--------|-----------|--------|
| blue   | `#1B3A6D` | key titlebars and window borders — the painting's blue band is a titlebar; toggles, nav indicators and whatever else the platform paints with its one accent; hyperlinks; browser frame |
| yellow | `#DFCC82` | selection — selected rows and selected text, BLACK on it (12.0:1); appears only when the user acts. On COSMIC, the window field and title bars (§7) |
| red    | `#D64D24` | the text cursor indicator; the terminal cursor; the COSMIC panel — a 32 pt band on a 1440 pt screen is 2.2% of it, the painting's own red share |

WHITE on the blue titlebar is 9.0:1. Focus rings stay BLACK.

### 1b. Semantic state colors

The only hue permitted in chrome. US highway sign colors: the FHWA's
MUTCD color designations (Pantone 342 / 116 / 187), in the sRGB
conversion used for road-sign renderings on Wikimedia Commons. Exempt
from the four lines (§1): these are signals, chosen to be read at a
glance, not composition colors. The mapping is the road's own — green
guides, yellow warns, red prohibits. Legend on a sign is pure white or
pure black, never a tint, and the same holds here: text and glyphs on a
semantic field are `#FFFFFF` or `#000000`, not the kit's WHITE and
BLACK. Those two values are admitted for that use only; anywhere else
they are off the lines and a defect.

| Role        | Hex       | FHWA color           | Legend    | Where |
|-------------|-----------|----------------------|-----------|-------|
| SUCCESS     | `#006B54` | Green (Pantone 342)  | `#FFFFFF` | confirmations, ok emblems, "done" |
| WARNING     | `#FCD116` | Yellow (Pantone 116) | `#000000` | caution panels, warning triangle |
| DESTRUCTIVE | `#AF1E2D` | Red (Pantone 187)    | `#FFFFFF` | delete/discard buttons, error panels |

Measured: white on green 6.5:1, white on red 6.9:1, black on yellow
14.3:1.

They appear only when the *meaning* is present. A red button that isn't
destructive is a defect. Accent and selection are composition hues
(§1); focus remains BLACK.

### 1c. Exception: toolkit derivations (COSMIC only)

COSMIC derives some surfaces from the theme's inputs, and no theme value
can prevent it. Two of those derivations land off the lines and are
admitted, in COSMIC chrome only, as exceptions to §1; `palette.json`
records both and `worksafe/cosmic/README_COSMIC.md` has the measurements.

- The selected and hovered row of the blue `#1B3A6D` nav sidebar:
  `#2E4670`, 22.7 off the blue line. The overlay is not Mondrian's.
- The row, card and well surface lightened from the yellow `#DFCC82`
  window field: `#FBE89D`, 47.9 off the yellow line. A tint toward
  white, which §1 otherwise forbids.

The inputs themselves stay canon, and the accent is WHITE so that text
painted with it passes the derivation unchanged. Nothing else may use
these two values.

## 2. Typography

Two fonts. Both anti-aliased, hinted, rendered clean at any DPI. The
bitmap era is over.

- **UI: Helvetica**, 12pt system size. The kit ships
  **Nimbus Sans** (URW, free, metric-compatible) and names it in every
  artifact; Helvetica proper is not redistributable.
  Bold for titlebar text and default buttons only.
- **Mono: Hack**, all weights. Advance width 0.602 em; all cursor and
  column math depends on it. Terminal, code, fixed-width tables, the
  `destijl` session chip in decks.

Sizes are in points. 1pt = 1px @1x, 2px @2x, 3px @3x. Never fractional.

## 3. Geometry

All values in pt (§2). Measured from source, not eyeballed.

### Rules

**One rule: Mondrian's, at the scale the painting is shown; BLACK; the
same everywhere on a screen.** His rules on this canvas average 130 px
of 5286 — 2.46% of the width — so the rule on a screen is 2.46% of the
width the painting is displayed at (§5): 28 px on a 1080p desktop,
58 px on a 4K one. The rule scales with the painting, not with the
display or the window. Where no painting is shown — a deck, a
stylesheet — the reference is the 1080p desktop: 28 pt.

- A rule is drawn *outside* the field it bounds. A window is its field
  plus a 28 pt band around it. Where two fields meet, one rule between
  them; where a field meets the wall, a rule.
- There is no thinner rule. A separator that wants to be lighter than
  28 pt is not a rule; it is a change of field tone (WHITE against
  LIGHT) and draws no line.
- The rule carries no state. Key and non-key windows have the same
  rule; the titlebar tells them apart (§1). This was the trade: rules
  are visual, not semantic.
- Where the platform will not draw it — Windows' DWM frame is 1 px —
  the rule is residue (below), and the kit does not fake it with
  shadows or a second color.

### Tolerated residue

The kit authors none of the following. Where proprietary software
imposes one the kit cannot reach, it is tolerated, not adopted: left
at the platform default, never extended, never echoed in anything the
kit does draw. A residue that elevation could remove is not
unavoidable; it is removed in `elevated/` and tolerated in `worksafe/`.
Each surface entry (§7) lists its residue.

- **Curves.** Deprecated. No corner radius, no arc, no ellipse, no dot
  that is not a square. Residue: control radii, tab shapes. Window
  corners are not residue: `DwmSetWindowAttribute` takes a corner
  preference per window from any process, so `worksafe/` removes them
  (`square_corners.ps1`).
- **Off-canon grays.** Chrome is four values (§1). A locked surface the
  platform paints in its own gray is residue if the value is neutral
  (r = g = b, or within 1.0 of the gray line), a defect if it is tinted.
- **Platform font.** UI is Helvetica (§2). A locked surface set in the
  platform's face is residue; the kit never sets a third face anywhere
  to match it.

*Remainder unwritten.*

## 4. Icons

### 4a. System icons

- 48pt base. Shipped @1x / @2x / @3x (48/96/144 px).
- **Grayscale, 8-bit, smooth-shaded**, photorealistic: soft top-left
  light, real form, no outlines, no flat "material" fills. Dither is
  an optional pipeline flag (`--dither 2bit`) for texture, not canon.
- State: disabled = DARK-tinted; document state = dogear. The three semantic colors (§1b) appear only on status
  icons that mean success, warning or destructive.
- A plain unlettered isometric cube is the generic glyph.
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
  not repaint it gray, does not snap it to the four lines (§1), and
  does not redraw it. The brand is the application's; the line rule
  governs what the kit authors.
- Chrome around the brand; the brand never bleeds into the chrome.
- Disabled tint and semantic emblems on an application icon follow
  §1b and §4a unchanged.
- Advertising is noise: promotional variants, seasonal recolors,
  attention-seeking animation. An icon that changes to get noticed has
  stopped being a brand and is replaced by the generic cube.

Rule of thumb: if removing the color would make the icon harder to
*find*, the color is information. If removing it would make the icon
harder to *ignore*, it was noise.

## 5. Wallpapers and the image pipeline

- Default desktop: Mondrian, *Composition with Blue, Red, Yellow, and
  Black* (1922), Minneapolis Institute of Art, public domain. The screen
  is itself a composition: the painting is the large field, flush to
  the top-right corner, never cropped or stretched; a DARK wall on the
  left carries the desktop icons; a DARK band along the bottom, two
  taskbar heights tall, carries the taskbar with an equal strip of wall
  above it. Asymmetric on purpose — the canvas's own logic, big field
  upper right and small fields along the left and bottom, repeated one
  level up.
- House wallpapers are **grayscale**: luminance-mapped, gamma-preserved,
  full 8-bit. Color photographs are content and are *permitted* as
  wallpapers, but nothing the kit generates is in color.
- Pipeline: proportional fit, edge-aligned integer grid where a grid is
  used (no stretch, residual as center crop, matting is a separate
  step). Upscaling of legacy assets is
  nearest-neighbor only.
- ASCII/glyph art in DeStijl is Hack, BLACK on WHITE (terminal polarity),
  single class.

## 6. Decks

Built with the pptxgenjs toolchain:

- Background WHITE. Body text BLACK Helvetica. Code Hack.
- Frame: a 28 pt BLACK rule around the slide content area (§3).
- Session chip top-left: `destijl` in Hack 11 DARK. Slide chip top-right
  `[ 03 / 07 ]` Hack 11 DARK. Slide title: Helvetica Bold, BLACK.
- Cursor: BLACK block rect named `cursor_blink`; blink via `inject_blink.py`.
- Emphasis: bold. Semantic colors only when a
  slide is literally reporting a success, warning or destructive act.

## 7. Surfaces

One entry per platform: what the kit reaches, what it tolerates as
residue (§3), and what elevation adds. Everything under *reached* is
per-user and ships in `worksafe/`.

### Windows 11 (24H2)

Primary surface: the standard theme engine in light mode, not a
contrast theme. Forced colors strip affordances users need — background
images, icon and control shading, color-coded content — and read as an
accessibility mode. Light mode because the system's polarity is BLACK
on WHITE.

Reached:

- Transparency effects off (mica and acrylic gone system-wide);
  animation effects off; scrollbars always shown.
- Accent Mondrian blue on title bars and borders (§1); the same accent
  colors toggles, nav indicators and Quick Settings tiles. Inactive
  titlebar LIGHT via `AccentColorInactive` under
  `HKCU\Software\Microsoft\Windows\DWM`.
- Selection yellow, hyperlinks blue: `Hilight` / `HotTrackingColor` in
  the `.theme` colors table (legacy Win32 honours them).
- Text cursor indicator red: Accessibility → Text cursor → indicator on,
  custom color.
- Edge frame blue: edge://settings/appearance, custom theme color —
  a Preferences entry, not a registry key, so a README step.
- Taskbar aligned left; widgets, Copilot and task view off; Start
  recommendations and search highlights off.
- Wallpaper (§5), cursors, sounds, desktop icons, folder icons via
  `desktop.ini`. Cursors are the one Windows element the kit draws with
  no residue at all.
- Window corners square: `square_corners.ps1` sets
  `DWMWA_WINDOW_CORNER_PREFERENCE` on every window as it appears; a
  Startup-folder shortcut runs it hidden at logon.
- Windows Terminal entire: palette, Hack, padding.
- Explorer: compact view, extensions shown, sync-provider notifications
  off.
- `worksafe/declutter.reg` (HKCU): tips and suggestions, welcome
  experience, Settings suggestions, lock-screen facts, notification
  defaults. The most useful file in the build.

Residue:

- Control corner radii; Terminal and Chrome tab shapes.
- The rule (§3): DWM draws a 1 px frame and nothing per-user thickens
  it.
- Segoe UI Variable in system chrome.
- Surface grays (`#F3F3F3`, `#FFFFFF` fields, `#202020` in dark
  panels): neutral, but brighter than WHITE and off the four values.

Elevated adds: HKLM `FontSubstitutes` (Nimbus in chrome), shell32
icons, all-sites extensions.

### COSMIC (Pop!_OS)

The surface where the kit is nearest to exact: the theme takes radius 0,
the four grays at their values, and the gaps. With tiling, the screen is
the composition. Build: `worksafe/cosmic/`, measured values in its README.

Reached:

- Light mode, always, auto-switch off; no dark builder exists. Mondrian
  is light mode: the system's polarity is BLACK on WHITE.
- Window fields and title bars yellow, text BLACK, nav sidebars blue,
  the panel red on its own key. Yellow as the large field inverts the
  painting's proportions on purpose; the author's call, 2026-09-08.
- Accent WHITE: selection, links, outlines, toggles, selected nav text.
  9:1 on the blue sidebar; on the yellow field legible by chroma, not
  lightness (about 1.3:1), which is enough for an outline or a label and
  is never asked to carry body text. — the painting's blue band is the field on the left
  of a window. Every corner radius 0; no frosting.
- Semantic colors (§1b) in the theme's success, warning and destructive
  slots.
- Tiling gaps are the rule (§3): 2.46% of the painting's displayed width
  on that output; `install.sh` computes it from the wallpaper layout and
  writes it into the theme (39 pt on 4K @ 150%, 28 pt on 1080p). COSMIC
  adds its outer gap to the inner one at a screen edge, so the outer gap
  is 0 and the inner gap is the rule: one rule everywhere.
- `active_hint` 0. COSMIC draws its hint on the focused window only,
  which would make the rule carry state.
- Background BLACK on a tiled output, so every gap is a rule and nothing
  else: COSMIC sets wallpaper per output, not per workspace, and on one
  output the rule wins. The Mondrian (§5) is composed alongside for a
  second output or a floating desktop: the panel is at the top, so the
  DARK band goes there, two panel heights tall; the painting flush right
  under it; the DARK wall on the left carries the dock and the desktop
  icons.
- Nimbus Sans UI, Hack mono, compact header and density. Terminal BLACK
  on WHITE with the pigments in their ANSI slots: red, yellow and blue
  lines, SUCCESS green, gray-line magenta and cyan, red cursor.

Residue:

- Header bars: this libcosmic paints them with the window background,
  so they are yellow with the field. A header bar cannot be blue and
  every window reads as non-key.
- Toggles, nav indicators, check marks and focus rings follow the one
  accent and are WHITE, where §1 has blue for the platform accent and
  BLACK for focus.
- The two §1c derivations: the sidebar overlay and the row surface.
- Client-side decorations (Electron, GTK) keep their own chrome.

## 8. Principles

1. Chrome is the pigment colors Mondrian actually used in this very
   composition (§1, §5). Chrome may be black, white, gray, red, blue,
   or yellow.
2. Any other value is a defect, platform residue (§3) excepted.
3. Overlay values (§1c) are exceptions, measured and recorded, and land
   as close to the lines as the container allows.
4. State is carried by tone and geometry, or by the three semantic hues
   (§1b) when the meaning is present. Mondrian's red, blue and yellow in
   chrome are composition, never state.
5. One rule: Mondrian's, at the scale the painting is shown; BLACK,
   outside the field, the same everywhere on a screen. It carries no
   state.
6. Resolution-independent points, integer-scaled.
7. Modern rendering: AA text, 8-bit icons, real shadows.
8. Measure, don't eyeball.
9. QA every build visually before delivery.
10. Deliverables are PDFs with fonts embedded.
11. Speaker notes are extracted from the built pptx, never retyped.
12. The pipeline generates its own demo assets.
13. The worksafe / elevated tier boundary and every rule in
    `CONTRIBUTING.md` are binding.
