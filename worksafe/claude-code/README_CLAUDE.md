# DeStijl — Claude

Three surfaces, one reached.

| Surface | Status |
|---|---|
| **Claude Code** (the CLI, and the Code tab of the desktop app) | reached: `destijl.json`, a custom theme on the `light-ansi` base with every token set to a hex value on the lines, so it does not depend on the terminal's ANSI palette. Install: copy to `~/.claude/themes/destijl.json`, then `/theme` → destijl. |
| **claude.ai in Firefox** | reached by the all-sites sheet, `elevated/destijl.user.css`, through Stylus. |
| **The desktop app's own shell** (title bar, tabs, sidebar) | not reachable. Checked 2026-09-10 on Linux: Settings › Appearance offers Light, Dark and High contrast and nothing else; the app loads no extensions or stylesheets. The four `customCSS` strings in its bundle belong to a sign-in library's widget options, not to the app. Editing the bundle to inject CSS is unsupported and broken by every update: not built. Set Appearance to Light, whose light grays clash least with the WHITE field. |

## The theme

| Token | Value | Why |
|---|---|---|
| text / inverseText | BLACK `#0A0F10` / WHITE `#E5E6E8` | §1 |
| claude, remember, planMode, fastMode, merged, briefLabelClaude | blue `#1B3A6D`, shimmer blue ⅔ `#152C4E` | the platform accent (§1) |
| inactive, subtle, suggestion, bashBorder, ide, briefLabelYou | DARK `#535758` | disabled text (§1) |
| permission, warning | yellow ⅓ `#514E36`, shimmer yellow ⅔ `#988D5C` | the readable yellows on WHITE; the endpoint is 1.3:1 |
| success / error | `#006B54` / `#AF1E2D` | §1b FHWA, exempt |
| autoAccept | red `#D64D24` | the cursor's red: something is running unattended |
| promptBorder | BLACK | the rule |
| selectionBg, diffAddedWord | yellow `#DFCC82` | selection (§1) |
| diffRemovedWord | red `#D64D24` | a word's emphasis, BLACK on it 3.5:1 — a label, not body text |
| diffAdded / diffRemoved rows | WHITE / LIGHT | tone, not hue: the words carry the meaning |
| user, bash and memory message backgrounds | LIGHT `#9C9EA0`, hover gray ⅘ `#B9BBBD` | wells on a WHITE ground |
| subagent and rainbow slots | points on the four lines, no green but SUCCESS | the picker offers eight hues; the kit has three |

Fifteen values, all on the lines or §1b-exempt (`build/lines.py`).
