#!/bin/sh
# DeStijl for Firefox — per-profile, no sudo. (worksafe tier)
# Copies user.js and chrome/ into the default profile. Firefox must be closed: both are read at startup.
set -e
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
echo "destijl: Firefox profile $PROFILE — user.js, chrome/userChrome.css, chrome/userContent.css in place."
[ -d "$BK" ] && echo "         previous files backed up to $BK"
echo "         start Firefox."
