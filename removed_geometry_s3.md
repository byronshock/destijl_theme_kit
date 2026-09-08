## 3. Geometry (measured)

Constants below are measured from source, not eyeballed. All values
in pt.

### Window
- Titlebar: **23** (includes the 1pt black border line at the top)
- Titlebar buttons (close left, minimize right): **15 × 15**,
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

**Button / raised**:
```
outer:  right + bottom  BLACK
inner:  left  + top     WHITE
inner:  right + bottom  DARK
fill:                   LIGHT
```
Shadow sides are 2pt total (BLACK outside DARK); highlight sides 1pt.

**Sunken field** — text fields, wells:
```
outer:  right + bottom  WHITE
outer:  left  + top     DARK
inner:  right + bottom  LIGHT
inner:  left  + top     BLACK
fill:                   DARK
```

**White bezel** — lists, browser columns, text views:
```
outer:  all four        DARK      (top) / WHITE (right, bottom) / DARK (left)
inner:  top             DARK
inner:  right, bottom   LIGHT
inner:  left            DARK
fill:                   WHITE
```

**Groove** — separators, box frames:
```
outer: left + top  DARK, inner left + top WHITE
outer: right + bottom WHITE, inner right + bottom DARK
```

Pressed button = raised recipe with WHITE and DARK/BLACK edges swapped,
fill LIGHT. Default button carries a Return-key glyph at the right.

### Scroller
- Width: **18**, on the **left** of the scrolled content
- Track: sunken (gray bezel), knob: raised button with a single centered
  dimple, arrows at the **bottom**, both together

### Menus
- Vertical, top-left of screen, tear-off. Item height: **20**.
  Title bar of a menu: BLACK with WHITE text.
- Items: Helvetica 12 on LIGHT. Submenu indicator: right-pointing
  triangle. Keyboard equivalent right-aligned.
- Selected item: BLACK fill, WHITE text. (Tone, not hue.)

### Dock and tiles
- Tile: **64 × 64**, raised-button bevel over a **diagonal gradient LIGHT
  (top-left) → DARK (bottom-right)**.
  This is the second and last exception to §1 (the badge pill is the first):
  a gradient *between two canon grays*, on the tile only.
- Icon art: **48 × 48**, centered, 8pt margin
- Dock: right edge, single column, application tile top
- Minimized windows: 64 × 64 tiles, bottom-left, with the app icon and the
  window title in Helvetica 9 beneath
- Badge (unread count): BLACK rounded pill — the *only* rounding in the
  system, radius = half height — WHITE Helvetica Bold 10, bottom-right
  of the tile. It is the state signal for everything.

### File viewer
- Browser columns, white bezel, column width **~155**, Helvetica 12,
  directory rows end in a right-pointing triangle.

### Desktop
- Default: flat DARK, no image. Image wallpapers allowed; see §5.

