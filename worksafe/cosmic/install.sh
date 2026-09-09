#!/bin/sh
# DeStijl for COSMIC (Pop!_OS) — user-level install. No sudo, nothing outside $HOME. (worksafe tier)
# Implements DESTIJL_STYLE.md §7 COSMIC. Re-runnable.
# Usage: sh install.sh [--mondrian]
#   default    the output's background is BLACK, so the tiling gaps are rules (§3, §7). The composed
#              Mondrian is still written to ~/Pictures/destijl for a second output or a floating desktop.
#   --mondrian the composed Mondrian as the background; on a one-output machine the gaps show it.
set -e
BACKGROUND=black; [ "$1" = "--mondrian" ] && BACKGROUND=mondrian
HERE=$(cd "$(dirname "$0")" && pwd)
KIT=$(cd "$HERE/../.." && pwd)
CFG="${XDG_CONFIG_HOME:-$HOME/.config}/cosmic"
PICS="$HOME/Pictures/destijl"
PANEL_PT=32            # COSMIC panel, size XS, logical px (measured on 4K @ 150%: 48 physical)
mkdir -p "$CFG" "$PICS"

# --- 1. fonts (§2). Not bundled: both are packaged. --------------------------------------------
for f in "Nimbus Sans:fonts-urw-base35" "Hack:fonts-hack"; do
  name=${f%%:*}; pkg=${f##*:}
  fc-list 2>/dev/null | grep -qi ":$name:\|: $name:" || \
    echo "destijl: font '$name' not installed — sudo apt install $pkg (or drop the files in ~/.local/share/fonts)"
done

# --- 2. the output: size and scale, from cosmic-randr -------------------------------------------
GEOM=$(cosmic-randr list 2>/dev/null | sed 's/\x1b\[[0-9;]*m//g' | python3 -c '
import re, sys
txt = sys.stdin.read()
blocks = re.split(r"\n(?=\S)", txt)
for b in blocks:
    if "(enabled)" not in b: continue
    scale = re.search(r"Scale:\s*(\d+)%", b); mode = re.search(r"(\d+)x(\d+)\s*@[^\n]*\(current\)", b)
    if scale and mode: print(mode.group(1), mode.group(2), scale.group(1)); break
')
set -- $GEOM
if [ -z "$3" ]; then echo "destijl: could not read the output from cosmic-randr; assuming 1920x1080 @ 100%"; set -- 1920 1080 100; fi
W=$1; H=$2; SCALE=$3
echo "destijl: output ${W}x${H} @ ${SCALE}%"

# --- 3. wallpaper (§5): painting flush right under a DARK band two panel heights tall; DARK wall left ---
LAYOUT="python3 $KIT/build/wallpaper.py ${W}x${H} $SCALE --top 2 --bottom 0 --bar $PANEL_PT --tag cosmic"
RULE_PT=$($LAYOUT --layout-only | python3 -c 'import json,sys; print(json.load(sys.stdin)["rule_pt"])')
PNG="$PICS/mondrian_1922_cosmic_${W}x${H}_s${SCALE}.png"
PRE="$KIT/worksafe/$(basename "$PNG")"       # a copy already generated in the kit (git-ignored)
if python3 -c 'import PIL' 2>/dev/null; then
  $LAYOUT --out "$PICS"
elif [ -f "$PRE" ]; then
  cp "$PRE" "$PICS/"; [ -f "${PRE%.png}.json" ] && cp "${PRE%.png}.json" "$PICS/"
  echo "destijl: Pillow not installed; using the pre-generated $PRE"
else
  echo "destijl: Pillow not installed (python3-pil) — wallpaper not generated; run later, then re-run install.sh:"
  echo "         $LAYOUT --out $PICS"
fi
BG="$CFG/com.system76.CosmicBackground/v1"; mkdir -p "$BG"
[ -f "$BG/all" ] && [ ! -f "$PICS/cosmic-background-all.before-destijl.ron" ] && cp "$BG/all" "$PICS/cosmic-background-all.before-destijl.ron"
if [ "$BACKGROUND" = mondrian ] && [ -f "$PNG" ]; then
  SOURCE="Path(\"$PNG\")"
else
  SOURCE="Color(Single((0.039216, 0.058824, 0.062745)))"    # BLACK #0A0F10: the gaps are rules. RON wants a tuple here, not [ ]
  BACKGROUND=black
fi
cat > "$BG/all" <<RON
(
    output: "all",
    source: $SOURCE,
    filter_by_theme: true,
    rotation_frequency: 300,
    filter_method: Lanczos,
    scaling_mode: Zoom,
    sampling_method: Alphanumeric,
)
RON
printf 'true' > "$BG/same-on-all"

# --- 4. toolkit: Nimbus Sans UI, Hack mono, compact header and density. Icon theme is left alone (§4). ---
mkdir -p "$CFG/com.system76.CosmicTk/v1"
cp "$HERE"/cosmic-config/com.system76.CosmicTk/v1/* "$CFG/com.system76.CosmicTk/v1/"
# --- 4b. panel: Mondrian red, a flat Color, the panel's own key (the theme would give it the window WHITE) ---
mkdir -p "$CFG/com.system76.CosmicPanel.Panel/v1"
[ -f "$CFG/com.system76.CosmicPanel.Panel/v1/background" ] && [ ! -f "$PICS/panel-background.before-destijl.ron" ] && \
  cp "$CFG/com.system76.CosmicPanel.Panel/v1/background" "$PICS/panel-background.before-destijl.ron"
cp "$HERE"/cosmic-config/com.system76.CosmicPanel.Panel/v1/background "$CFG/com.system76.CosmicPanel.Panel/v1/background"

# --- 5. light mode, always (§7): Mondrian's polarity is BLACK on WHITE. No dark builder is shipped. ---
mkdir -p "$CFG/com.system76.CosmicTheme.Mode/v1"
printf 'false' > "$CFG/com.system76.CosmicTheme.Mode/v1/is_dark"
printf 'false' > "$CFG/com.system76.CosmicTheme.Mode/v1/auto_switch"

# --- 6. theme (§1, §1c, §3, §7): gaps are the rule at this output's painting scale ----------------
TMP=$(mktemp --suffix=.ron)
sed "s/^\(\s*gaps:\s*\)([0-9]*, [0-9]*),/\1(0, $RULE_PT),/" "$HERE/destijl.ron" > "$TMP"    # (outer, inner): edge = outer + inner
grep -q "gaps: (0, $RULE_PT)," "$TMP" || { echo "destijl: failed to set gaps"; exit 1; }
if command -v cosmic-settings >/dev/null 2>&1; then
  cosmic-settings appearance import "$TMP"
else
  cp "$TMP" "$PICS/destijl.ron"
  echo "cosmic-settings not on PATH — import $PICS/destijl.ron from Settings > Desktop > Appearance > Import"
fi
rm -f "$TMP"

# --- 7. terminal: add the scheme to COSMIC Terminal's light schemes and select it ---------------------
TERM_CFG="$CFG/com.system76.CosmicTerm/v1"; mkdir -p "$TERM_CFG"
python3 - "$HERE/destijl-term.ron" "$TERM_CFG" <<'PY'
import re, sys, os
src, cfg = sys.argv[1], sys.argv[2]
scheme = re.sub(r'^\s*//.*\n', '', open(src).read(), flags=re.M).strip()
name = re.search(r'name:\s*"([^"]+)"', scheme).group(1)
path = os.path.join(cfg, 'color_schemes_light')
cur = open(path).read() if os.path.exists(path) else '{\n}'
if f'name: "{name}"' not in cur:
    entries = re.findall(r'^\s*(\d+):', cur, flags=re.M)
    nxt = max(map(int, entries)) + 1 if entries else 0
    body = cur.rstrip().rstrip('}').rstrip()
    if body.endswith('{'): new = body + f'\n    {nxt}: {scheme},\n}}'
    else: new = body.rstrip(',') + f',\n    {nxt}: {scheme},\n}}'
    open(path, 'w').write(new)
open(os.path.join(cfg, 'syntax_theme_light'), 'w').write(f'"{name}"')
print(f'destijl: terminal scheme "{name}" installed and selected')
PY

[ -f "$PNG" ] && WP="Mondrian composed at $PNG" || WP="NO Mondrian composed (see above)"
cat <<MSG
destijl: light mode, theme (gaps $RULE_PT pt), toolkit fonts, background $BACKGROUND; $WP.
Log out/in if the panel, wallpaper or terminal doesn't refresh.
MSG
