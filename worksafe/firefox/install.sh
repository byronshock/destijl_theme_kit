#!/bin/sh
# DeStijl for Firefox — per-profile, no sudo. (worksafe tier)
# Copies user.js and chrome/ into the default profile. Firefox must be closed: both are read at startup.
# Usage: sh install.sh [--ublock]
#   --ublock  also installs uBlock Origin (§0: advertisements are noise) from addons.mozilla.org into the
#             profile's extensions directory, and lets Firefox enable profile-directory extensions without
#             asking. Needs curl or wget. Leave the flag off and the browser is as Mozilla ships it.
set -e
UBLOCK=no; [ "$1" = "--ublock" ] && UBLOCK=yes
UBLOCK_ID="uBlock0@raymondhill.net"
UBLOCK_URL="https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi"
HERE=$(cd "$(dirname "$0")" && pwd)
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
if [ "$UBLOCK" = yes ]; then
  mkdir -p "$PROFILE/extensions"; XPI="$PROFILE/extensions/$UBLOCK_ID.xpi"
  if command -v curl >/dev/null 2>&1; then curl -fsSL -o "$XPI" "$UBLOCK_URL"
  elif command -v wget >/dev/null 2>&1; then wget -q -O "$XPI" "$UBLOCK_URL"
  else echo "destijl: --ublock needs curl or wget"; exit 1; fi
  # Firefox starts a sideloaded extension disabled and asks; scope 1 is the profile directory, the user's own.
  # 15 - 1 = 14: every other scope still starts disabled.
  printf '\n// --ublock: enable extensions the user put in this profile (uBlock Origin) without asking\nuser_pref("extensions.autoDisableScopes", 14);\n' >> "$PROFILE/user.js"
  echo "destijl: uBlock Origin $(du -h "$XPI" | cut -f1) at $XPI (signed by Mozilla; from $UBLOCK_URL)"
fi
echo "destijl: Firefox profile $PROFILE — user.js, chrome/userChrome.css, chrome/userContent.css in place."
[ -d "$BK" ] && echo "         previous files backed up to $BK"
echo "         start Firefox."
