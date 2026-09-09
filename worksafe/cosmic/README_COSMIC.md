# DeStijl — COSMIC (Pop!_OS)

Mondrian's pigments on COSMIC. Everything here is per-user: `sh install.sh`, no sudo.
Implements `DESTIJL_STYLE.md` §7 COSMIC; measured on COSMIC (Pop!_OS 24.04), 3840×2160 @ 150%.

| File | Apply | What it does |
|---|---|---|
| `destijl.ron` | `cosmic-settings appearance import destijl.ron` (install.sh does it, after setting the gaps) or Settings › Desktop › Appearance › Import | ThemeBuilder v2, Light palette. WHITE `#E5E6E8` window backgrounds (the panel and header bars take the same value), blue `#1B3A6D` nav sidebars, BLACK text, yellow `#DFCC82` accent (selection), FHWA semantic colors, every corner radius 0, no frosting, no window hint, tiling gaps = the rule. Every accent-picker swatch is a point on a DeStijl line. |
| `destijl-term.ron` | install.sh adds it to COSMIC Terminal's light schemes and selects it (or Terminal › View › Color schemes › Import) | BLACK on WHITE; Mondrian's red, yellow and blue lines in their ANSI slots (normal = dark third, bright = endpoint), SUCCESS green, gray-line magenta and cyan, Mondrian red cursor. |
| `cosmic-config/com.system76.CosmicTk/v1/` | copied by install.sh | Nimbus Sans UI, Hack mono, Compact header and density. The icon theme key is not shipped (§4, issue 006). |
| `install.sh` | `sh install.sh` (or `sh install.sh --mondrian`) | reads the output's size and scale from `cosmic-randr`, composes the Mondrian wallpaper into `~/Pictures/destijl` (or copies a pre-generated one from `../`), sets the background to BLACK so the gaps are rules — or to the Mondrian with `--mondrian` —, copies the toolkit config, sets light mode, writes the rule into the theme's gaps and imports it, and installs the terminal scheme. Backs up the previous background config to `~/Pictures/destijl/`. |

Fonts are not bundled: `fonts-urw-base35` (Nimbus Sans) and `fonts-hack` are
packages, and install.sh says so if either is missing.

## The screen as composition (§5, §3)

On a tiled workspace the screen is windows and rules, and the rule is
BLACK: the default install sets the output's background to BLACK
`#0A0F10` (a `Color(Single(...))` source for `cosmic-bg`) so every gap
is a rule and nothing else. The Mondrian is composed alongside for a
second output, or for a machine that floats its windows
(`install.sh --mondrian`). §7 describes the two-output arrangement; on
one output, this is the choice, and it was made for the rule.

The BLACK is a measured value, not a crop. The painting has no black
field: its black is the rules, about 130 px wide, and the largest 16:9
patch that is 95% black is a 253 x 142 px T-junction that would be
blown up fifteen times. Chosen 2026-09-08 from a proof sheet against
four crops.

When the Mondrian is the background, the panel is at the top, so the DARK band goes there: two panel heights
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
| window backgrounds, panel, header bars | `#E5E6E8` WHITE | on |
| rows and cards, derived from WHITE | `#CCCDCF` | on |
| background (default install): every gap | `#0A0F10` BLACK | on |
| band, desktop wall (`--mondrian`) | `#535758` DARK | on |
| nav sidebar | `#1B3A6D` blue | on |
| nav sidebar, selected row text; links; selection outline | `#DFCC82` yellow | on |
| toggle, off | `#787A7C` gray ½ | on |
| accent swatches | nine points on the lines | on |

## Residue (§3), measured

| Where | Value | Off the nearest line by | Why the kit can't reach it |
|---|---|---|---|
| nav sidebar, selected and hovered row | `#2E4670` | 22.7 (blue) | libcosmic overlays the container to derive the state; on a blue container the result is a tint. This is the one §1c exception on COSMIC. |
| header bars, panel | `#E5E6E8` WHITE | on the line, but the wrong role | This libcosmic paints the header bar and the panel with the window background, not the primary container, so a header bar cannot be blue, every window reads as non-key, and the panel cannot be LIGHT. §7's "headerbars blue" is unreachable; the blue field is the nav sidebar instead. |
| toggles, nav indicators, check marks | yellow | on the line, but the wrong role | COSMIC has one accent, and selection is what it paints most. §1 gives the platform accent to blue; here it follows selection. On the blue sidebar blue text would vanish. |
| focus rings | yellow | — | drawn with the accent; §1 says BLACK. |
| accent as text (links, selected nav row) | derived from the accent | — | libcosmic lightens a dark accent for text: Mondrian red as accent gave exact `#D64D24` outlines and toggles but `#FFBFAD` links and nav text, 46 off the lines. Yellow is light enough to pass through unchanged, which is one more reason it is the accent. Tried and reverted 2026-09-08. |
| menu text, or any text in a hue | BLACK | — | there is no text-color slot. The "interface text tint" tints a near-black toward a hue and cannot set one: Mondrian red as the tint produced `#1C0300` labels and `#360900` panel text, 24 and 27 off the red line. Tried and reverted 2026-09-08. |
| Electron and GTK windows | their own chrome | — | client-side decorations; the theme does not reach them. |
| Chrome with the Qt UI backend | accent `#DFCC82` on the focused title bar | on the line, wrong role | Qt takes the COSMIC theme colors better than the GTK backend but misassigns them: the accent lands on the key title bar, where §1 puts blue. Observed 2026-09-08. |

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
