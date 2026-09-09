# DeStijl — COSMIC (Pop!_OS)

Mondrian's pigments on COSMIC. Everything here is per-user: `sh install.sh`, no sudo.
Implements `DESTIJL_STYLE.md` §7 COSMIC; measured on COSMIC (Pop!_OS 24.04), 3840×2160 @ 150%.

| File | Apply | What it does |
|---|---|---|
| `destijl.ron` | `cosmic-settings appearance import destijl.ron` (install.sh does it, after setting the gaps) or Settings › Desktop › Appearance › Import | ThemeBuilder v2, Light palette. LIGHT `#9C9EA0` window surfaces and panel, blue `#1B3A6D` nav sidebars, WHITE `#E5E6E8` content wells, BLACK text, yellow `#DFCC82` accent (selection), FHWA semantic colors, every corner radius 0, no frosting, no window hint, tiling gaps = the rule. Every accent-picker swatch is a point on a DeStijl line. |
| `destijl-term.ron` | install.sh adds it to COSMIC Terminal's light schemes and selects it (or Terminal › View › Color schemes › Import) | BLACK on WHITE; Mondrian's red, yellow and blue lines in their ANSI slots (normal = dark third, bright = endpoint), SUCCESS green, gray-line magenta and cyan, Mondrian red cursor. |
| `cosmic-config/com.system76.CosmicTk/v1/` | copied by install.sh | Nimbus Sans UI, Hack mono, Compact header and density. The icon theme key is not shipped (§4, issue 006). |
| `install.sh` | `sh install.sh` | reads the output's size and scale from `cosmic-randr`, composes the wallpaper (or copies a pre-generated one from `../`), points `cosmic-bg` at it, copies the toolkit config, sets light mode, writes the rule into the theme's gaps and imports it, and installs the terminal scheme. Backs up the previous background config to `~/Pictures/destijl/`. |

Fonts are not bundled: `fonts-urw-base35` (Nimbus Sans) and `fonts-hack` are
packages, and install.sh says so if either is missing.

## The screen as composition (§5, §3)

The panel is at the top, so the DARK band goes there: two panel heights
(size XS = 32 pt) tall, panel in its upper half, an equal strip of wall
below it. The painting sits flush right under the band, never cropped or
stretched, and the DARK wall on the left carries the dock and the desktop
icons. On 4K @ 150% the painting is 2411 px wide, the left wall 1429 px.

The rule (§3) is 2.46% of the painting's displayed width: 59 px = 39 pt on
this output, and install.sh writes `gaps: (39, 39)` — outer and inner
alike, a rule where a field meets the wall and one rule between two fields.
`active_hint` is 0: COSMIC draws its hint on the focused window only, and a
rule that appears with focus is carrying state (§3).

## What COSMIC reaches, measured

| Surface | Value | Line test |
|---|---|---|
| panel, window surfaces | `#9C9EA0` LIGHT | on |
| band, desktop wall | `#535758` DARK | on |
| nav sidebar | `#1B3A6D` blue | on |
| nav sidebar, selected row text; links; selection outline | `#DFCC82` yellow | on |
| content wells | `#E5E6E8` WHITE | on |
| toggle, off | `#787A7C` gray ½ | on |
| accent swatches | nine points on the lines | on |

## Residue (§3), measured

| Where | Value | Off the nearest line by | Why the kit can't reach it |
|---|---|---|---|
| nav sidebar, selected and hovered row | `#2E4670` | 22.7 (blue) | libcosmic overlays the container to derive the state; on a blue container the result is a tint. This is the one §1c exception on COSMIC. |
| header bars | `#9C9EA0` LIGHT | on the line, but the wrong role | This libcosmic paints the header bar with the window background, not the primary container, so a header bar cannot be blue and every window reads as non-key. §7's "headerbars blue" is unreachable; the blue field is the nav sidebar instead. |
| toggles, nav indicators, check marks | yellow | on the line, but the wrong role | COSMIC has one accent, and selection is what it paints most. §1 gives the platform accent to blue; here it follows selection. On the blue sidebar blue text would vanish. |
| focus rings | yellow | — | drawn with the accent; §1 says BLACK. |
| gaps on a tiled workspace | painting shows through | — | one output, one wallpaper. §7 wants a BLACK tiled workspace with the Mondrian on a floating one; COSMIC sets wallpaper per output, not per workspace. On a second output, set its wallpaper to BLACK and the gaps become rules. |
| Electron and GTK windows | their own chrome | — | client-side decorations; the theme does not reach them. |

Earlier prediction of a 10% pure-white overlay (`#324E7C`) was wrong by
measurement; the overlay libcosmic applies is smaller. `palette.json`
records the measured value.

## Light mode, always

Mondrian is light mode: the system's polarity is BLACK on WHITE (§7).
install.sh sets `is_dark` false and `auto_switch` false, and the kit ships
no dark builder. Any dark builder a machine already has is not the kit's;
to clear one so dark mode falls back to COSMIC's own default:

```
cd ~/.config/cosmic && tar czf ~/Pictures/destijl/backup/cosmic-dark-builders.tgz \
  com.system76.CosmicTheme.Dark com.system76.CosmicTheme.Dark.Builder && \
  rm -rf com.system76.CosmicTheme.Dark com.system76.CosmicTheme.Dark.Builder
```
