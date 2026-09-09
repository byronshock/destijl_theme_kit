# DeStijl — Firefox

The browser is where the user lives part of the time, and Firefox is the one
browser that hands its whole chrome to a per-profile stylesheet, so every
strip gets an exact value. Everything here is per profile, no sudo:
`sh install.sh` with Firefox closed, then start Firefox. Measured on
Firefox 154 (deb) on COSMIC.

| File | What it does |
|---|---|
| `user.js` | prefs, read at every start: enables the stylesheets; Firefox draws its own titlebar so the tab strip can be the blue key titlebar; compact density; no rounded bottom corners; scrollbars always shown; reduced motion; light theme; Nimbus Sans and Hack; and the §0 declutter — sponsored tiles and suggestions, Pocket, trending, promos, "what's new", hover previews, recommendations off. |
| `chrome/userChrome.css` | the chrome. Tab strip blue `#1B3A6D` with WHITE text when the window is key, LIGHT `#9C9EA0` with BLACK text when it is not (§1, the one surface on this desktop that can show it). Toolbars yellow `#DFCC82`: the painting's small field under its blue band, the one place yellow is a surface (the windows are WHITE). Current tab yellow, joined to the field. Address and search fields LIGHT `#9C9EA0`, a well on the field, BLACK text, BLACK 2 px focus outline, yellow selection. Menus and panels WHITE with BLACK text and a yellow hovered row. Sidebar blue with WHITE text. Every radius 0. No hairline separators: a change of tone instead (§3). |
| `chrome/userContent.css` | the in-browser pages that are chrome, not content: new tab, home, blank, private. WHITE ground, BLACK text, blue primary buttons, square. Page content is untouched (§0). |
| `install.sh` | finds the profile this Firefox install opens (`installs.ini`, else the default in `profiles.ini`), backs up any existing `user.js` and `chrome/` files into the profile, copies these three in. Refuses while Firefox runs, since both are read at startup. |
| `install.sh --stylus` | the same, plus Stylus, sideloaded like uBlock. Then, in Firefox, Stylus › Manage › Import and choose `elevated/destijl.stylus.json` (`install.sh --style` prints the path). Stylus reads its own JSON cleanly and balks at `*.user.css` files, so the kit ships both: `elevated/destijl.user.css` is the source, `build/stylus_json.py` generates the JSON from it, and `--style-css` is the fallback that serves the user.css on localhost for Stylus's install page. The sheet is the kit's all-sites restyle of web pages: on Windows an all-sites extension is the elevated tier, here it is a per-profile extension and the tier boundary does not bite. After editing the sheet, bump `@version`, regenerate, import again. |
| `install.sh --ublock` | the same, plus uBlock Origin: downloads the current signed build from addons.mozilla.org into the profile's `extensions/` directory and sets `extensions.autoDisableScopes` to 14 so a profile-directory extension starts enabled instead of asking. §0: advertisements are noise, and the larger half of the kit is removing what was put in the user's way. Off by default; the flag is the user's choice each install. |

## uBlock Origin

`--ublock` fetches `uBlock0@raymondhill.net.xpi` from Mozilla's add-on
site, signed, into the profile's own extensions directory: no elevation,
nothing outside the profile. Firefox normally starts a sideloaded
extension disabled and asks once; the prefs change narrows that to "the
profile directory is trusted" (scope 1 of 15) and leaves the user, system
and application scopes as they were. Remove the `.xpi` and the pref line
to undo. Updates come from Firefox's own add-on updater afterwards.

## Reached, measured

| Element | Value |
|---|---|
| tab strip, key window | `#1B3A6D` |
| tab strip, non-key window | `#9C9EA0`, BLACK text |
| current tab, toolbars, bookmarks bar | `#DFCC82` |
| address bar, at rest and focused | `#9C9EA0` |
| new tab page ground | `#E5E6E8` |
| new tab page primary button | `#1B3A6D` |
| toolbar button hover / active | `#988D5C` / `#514E36`, the yellow line's thirds |

Firefox 154 renamed most of its theme tokens (`--toolbox-background-color`
and its `-inactive` pair, `--toolbar-field-background-color-focus`,
`--urlbar-background-color-focus`, `--tab-background-color-selected`,
`--color-accent-primary`, ...). The stylesheet sets both the new names and
the older `--lwt-*` / `--toolbar-field-*` names, so it holds on older
builds too. When a strip falls back to a Firefox color after an update,
a token was renamed again: `unzip -p /usr/lib/firefox/browser/omni.ja
chrome/browser/skin/classic/browser/urlbar/urlbar.tokens.css` and the
`tabbrowser/*.tokens.css` files next to it list the current names.

## Residue

- **The dock icon while Firefox runs** is Firefox's own orange fox, not the
  pigment version: a running Wayland window can supply its icon directly,
  and COSMIC shows that over the theme. The pinned, not-running icon is the
  theme's.
- **Window corners**: top corners follow Firefox's client-side titlebar;
  they measured square on COSMIC. Bottom corners are squared by pref.
- **Page content** keeps its own colors, by design. `elevated/destijl.user.css`
  is the Stylus sheet for sites, when the user wants that.
- **Native GTK widgets** inside dialogs (file picker) are GTK's.

## Why not Chrome

Chrome's frame takes the theme through whichever UI backend it runs, and
misassigns it (README_COSMIC.md); its own theme format reaches a few colors
and no shapes. Firefox's stylesheet reaches all of it. The kit's Chrome
pieces stay for Windows.
