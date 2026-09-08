# Wallpaper: reserve icon columns; per-monitor install

**Labels:** windows, worksafe, wallpaper, deferred
**Implements:** `DESTIJL_STYLE.md` §0 (purpose), §5 (default desktop), §7 Windows

## Observed (2026-09-08 screenshot, two 1920×1080 monitors, 100% + 125%)

- One `.theme` → one `Wallpaper=` → same file on every monitor. The s125 file
  on the 100% monitor leaves 13 px of extra DARK above the taskbar (harmless);
  the reverse would put art under the bar.
- Desktop icons sit on a 75 × scale px grid. Five columns need 375 px at 100%;
  the left pillar is 357–364. Column five's labels cross onto the canvas, and
  free-placed icons land on the white field where Windows' white label text is
  unreadable.

## Do

1. ~~`--icon-columns N`~~ Superseded: the composition moved to the top-right
   corner with a DARK left wall (771 px at 1080p/100%, ten icon columns) and
   a bottom band of two taskbar heights. See §5 and `build/wallpaper.py`.
2. `worksafe/install.ps1` (issue 004): enumerate monitors via
   `IDesktopWallpaper` (`{C2CF3110-460E-4fc1-B9D0-8A1C0C9CC4BD}`, per-user,
   no elevation), read each monitor's resolution and DPI, build or select the
   matching variant, and call `SetWallpaper(monitorId, path)` per monitor.
   Falls back to the `.theme`'s single file if COM is blocked.
3. Verify: no art under any taskbar; no icon label over the canvas at the
   user's icon count; re-measure field medians after any resize.

## Out of scope

Icon spacing (`IconSpacing`, rewritten at logon in 24H2), icon count, auto-hide
taskbar.
