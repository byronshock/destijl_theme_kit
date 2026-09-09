#!/bin/sh
# DeStijl for Firefox — per-profile, no sudo. (worksafe tier)
# Copies user.js and chrome/ into the default profile. Firefox must be closed: both are read at startup.
# Usage: sh install.sh [--ublock] [--stylus]      (Firefox closed)
#        sh install.sh --style                    (Firefox running, Stylus installed)
#   --ublock  also installs uBlock Origin (§0: advertisements are noise) from addons.mozilla.org into the
#             profile's extensions directory, and lets Firefox enable profile-directory extensions without
#             asking. Needs curl or wget. Leave the flag off and the browser is as Mozilla ships it.
#   --stylus  also installs Stylus the same way, for the kit's all-sites sheet elevated/destijl.user.css.
#   --style   prints where the Stylus import file is: elevated/destijl.stylus.json, generated from the sheet by
#             build/stylus_json.py. Stylus > Manage > Import, pick the file. Stylus reads its own JSON cleanly
#             and balks at *.user.css files. Re-run the generator after editing the sheet, then import again.
#   --style-css  the fallback: serves elevated/destijl.user.css on localhost for a minute and opens it in
#             Firefox, where Stylus may offer its install page.
set -e
UBLOCK=no; STYLUS=no; STYLE=no; STYLECSS=no
for a in "$@"; do case "$a" in --ublock) UBLOCK=yes;; --stylus) STYLUS=yes;; --style) STYLE=yes;; --style-css) STYLECSS=yes;; *) echo "destijl: unknown option $a"; exit 1;; esac; done
UBLOCK_ID="uBlock0@raymondhill.net"
UBLOCK_URL="https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi"
STYLUS_ID="{7a7a4a92-a2a0-41d1-9fd7-1e92480d612d}"
STYLUS_URL="https://addons.mozilla.org/firefox/downloads/latest/styl-us/latest.xpi"
HERE=$(cd "$(dirname "$0")" && pwd)
KIT=$(cd "$HERE/../.." && pwd)

if [ "$STYLE" = yes ]; then
  JSON="$KIT/elevated/destijl.stylus.json"
  [ -f "$JSON" ] || python3 "$KIT/build/stylus_json.py" >/dev/null
  echo "destijl: in Firefox, Stylus > Manage > Import, choose:"
  echo "         $JSON"
  echo "         (regenerate after editing the sheet: python3 $KIT/build/stylus_json.py)"
  exit 0
fi
if [ "$STYLECSS" = yes ]; then
  SHEET="$KIT/elevated/destijl.user.css"; PORT=${DESTIJL_PORT:-8765}
  command -v firefox >/dev/null 2>&1 || { echo "destijl: firefox not on PATH"; exit 1; }
  ( cd "$KIT/elevated" && timeout 60 python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 ) &
  sleep 1
  firefox "http://127.0.0.1:$PORT/destijl.user.css" >/dev/null 2>&1 &
  echo "destijl: serving $SHEET for 60 s; Firefox is opening it. Stylus shows its install page: click Install style."
  exit 0
fi
MOZ="${MOZ_HOME:-$HOME/.mozilla/firefox}"
if pgrep -x firefox >/dev/null 2>&1 || pgrep -x firefox-bin >/dev/null 2>&1; then
  echo "destijl: close Firefox first — user.js and userChrome.css are read at startup"; exit 1
fi
PROFILE=$(python3 - "$MOZ" <<'PY'
import configparser, os, sys
moz = sys.argv[1]
def rel(p, sec): return os.path.join(moz, sec.get('Path', '')) if sec.get('IsRelative', '1') == '1' else sec.get('Path', '')
ini = configparser.RawConfigParser(strict=False); ini.read(os.path.join(moz, 'profiles.ini'))
paths = {}
for s in ini.sections():
    if s.startswith('Profile'): paths[ini[s].get('Path')] = rel(moz, ini[s])
    if s.startswith('Install') and ini[s].get('Default'):          # the profile this Firefox install opens
        print(os.path.join(moz, ini[s]['Default'])); sys.exit()
for s in ini.sections():
    if s.startswith('Profile') and ini[s].get('Default') == '1': print(rel(moz, ini[s])); sys.exit()
PY
)
[ -d "$PROFILE" ] || { echo "destijl: no default Firefox profile under $MOZ"; exit 1; }
STAMP=$(date +%Y%m%d-%H%M%S); BK="$PROFILE/destijl-backup-$STAMP"
for f in user.js chrome/userChrome.css chrome/userContent.css; do
  if [ -f "$PROFILE/$f" ]; then mkdir -p "$BK/chrome"; cp "$PROFILE/$f" "$BK/$f"; fi
done
mkdir -p "$PROFILE/chrome"
cp "$HERE/user.js" "$PROFILE/user.js"
cp "$HERE/chrome/userChrome.css" "$HERE/chrome/userContent.css" "$PROFILE/chrome/"
fetch_xpi() {   # id url name
  mkdir -p "$PROFILE/extensions"; XPI="$PROFILE/extensions/$1.xpi"
  if command -v curl >/dev/null 2>&1; then curl -fsSL -o "$XPI" "$2"
  elif command -v wget >/dev/null 2>&1; then wget -q -O "$XPI" "$2"
  else echo "destijl: sideloading needs curl or wget"; exit 1; fi
  echo "destijl: $3 $(du -h "$XPI" | cut -f1) at $XPI (signed by Mozilla; from $2)"
}
if [ "$UBLOCK" = yes ] || [ "$STYLUS" = yes ]; then
  # Firefox starts a sideloaded extension disabled and asks; scope 1 is the profile directory, the user's own.
  # 15 - 1 = 14: every other scope still starts disabled.
  printf '\n// sideloaded: enable extensions the user put in this profile without asking\nuser_pref("extensions.autoDisableScopes", 14);\n' >> "$PROFILE/user.js"
fi
[ "$UBLOCK" = yes ] && fetch_xpi "$UBLOCK_ID" "$UBLOCK_URL" "uBlock Origin"
[ "$STYLUS" = yes ] && fetch_xpi "$STYLUS_ID" "$STYLUS_URL" "Stylus"
echo "destijl: Firefox profile $PROFILE — user.js, chrome/userChrome.css, chrome/userContent.css in place."
[ -d "$BK" ] && echo "         previous files backed up to $BK"
echo "         start Firefox."
