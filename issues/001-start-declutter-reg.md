# Start `worksafe/declutter.reg`

**Labels:** windows, worksafe, deliverable
**Implements:** `DESTIJL_STYLE.md` §0 (purpose), §3 (tolerated residue), §7 Windows 11 (24H2)

## Why

§0: the skin is the smaller half of saving a user from Windows; removing
what the platform put in their way is the larger half, and a surface that
ships one without the other is unfinished. This file is the larger half.

## Scope

One `.reg` file, HKCU only, importable without elevation, idempotent.
Removal only — colors, DWM accent and wallpaper belong to the skin
(`worksafe/theme.reg`, separate issue), not here. Ship with
`declutter_undo.reg` that restores every key to the 24H2 default.

Every key gets a comment naming the Settings toggle it mirrors, so a
reviewer can verify it by flipping the toggle in the UI.

### Start

| Settings toggle | Key | Value |
|---|---|---|
| Show recommendations for tips, shortcuts, new apps | `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced` `Start_IrisRecommendations` | 0 |
| Show account-related notifications occasionally in Start (24H2) | same key, `Start_AccountNotifications` | 0 |
| Show recently added apps | same key, `Start_TrackProgs` | 0 |
| Show recently opened items in Start, Jump Lists, Explorer | same key, `Start_TrackDocs` | 0 |
| Show search highlights | `HKCU\Software\Microsoft\Windows\CurrentVersion\SearchSettings` `IsDynamicSearchBoxEnabled` | 0 |
| Web results in Start search | `HKCU\Software\Policies\Microsoft\Windows\Explorer` `DisableSearchBoxSuggestions` | 1 — policy path under HKCU; verify it is honored without GPO and not locked on the work machine |

### Taskbar

| Settings toggle | Key | Value |
|---|---|---|
| Taskbar alignment: left | `...\Explorer\Advanced` `TaskbarAl` | 0 |
| Widgets | `...\Explorer\Advanced` `TaskbarDa` | 0 |
| Task view | `...\Explorer\Advanced` `ShowTaskViewButton` | 0 |
| Search: icon only | `HKCU\Software\Microsoft\Windows\CurrentVersion\Search` `SearchboxTaskbarMode` | 1 |
| Copilot | 24H2 pins it as an app — unpin; `ShowCopilotButton` is 23H2 only, include for mixed fleets |

### Suggestions, tips, ads

All under `HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager`
unless noted.

| Settings toggle | Value name | Value |
|---|---|---|
| Get tips and suggestions when using Windows | `SubscribedContent-338389Enabled` | 0 |
| Show the Windows welcome experience | `SubscribedContent-310093Enabled` | 0 |
| Show suggested content in the Settings app | `SubscribedContent-338393Enabled`, `-353694Enabled`, `-353696Enabled` | 0 |
| Lock screen: get fun facts, tips, tricks | `SubscribedContent-338387Enabled`, `RotatingLockScreenOverlayEnabled` | 0 |
| Start app suggestions | `SubscribedContent-338388Enabled`, `SystemPaneSuggestionsEnabled`, `SoftLandingEnabled` | 0 |
| Auto-install suggested apps | `SilentInstalledAppsEnabled` | 0 |
| Suggest ways to finish setting up my device | `HKCU\Software\Microsoft\Windows\CurrentVersion\UserProfileEngagement` `ScoobeSystemSettingEnabled` | 0 |
| Advertising ID | `HKCU\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo` `Enabled` | 0 |
| Tailored experiences | `HKCU\Software\Microsoft\Windows\CurrentVersion\Privacy` `TailoredExperiencesWithDiagnosticDataEnabled` | 0 |

### Explorer

| Settings toggle | Key | Value |
|---|---|---|
| Show sync provider notifications (OneDrive ads) | `...\Explorer\Advanced` `ShowSyncProviderNotifications` | 0 |
| File name extensions | `...\Explorer\Advanced` `HideFileExt` | 0 |
| Compact view | `...\Explorer\Advanced` `UseCompactMode` | 1 |
| Open Explorer to This PC | `...\Explorer\Advanced` `LaunchTo` | 1 |
| Quick access: recent / frequent | `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer` `ShowRecent`, `ShowFrequent` | 0 |
| Home: show files from Office.com (24H2 "Recommended") | `...\Explorer` `ShowCloudFilesInQuickAccess` | 0 — verify key on 24H2 |

### Motion and blur (§0 names both)

| Settings toggle | Key | Value |
|---|---|---|
| Transparency effects | `HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize` `EnableTransparency` | 0 |
| Animation effects | `HKCU\Control Panel\Desktop\WindowMetrics` `MinAnimate` 0; `...\Explorer\Advanced` `TaskbarAnimations` 0; `UserPreferencesMask` bits — settle in implementation, Settings toggle is the fallback |
| Always show scrollbars | `HKCU\Control Panel\Accessibility` `DynamicScrollbars` | 0 |

## Acceptance

- [ ] Imports on a clean 24H2 user profile with no elevation prompt; second import is a no-op.
- [ ] Each key's Settings toggle reads in the expected state after import and after a logoff/logon — log any key 24H2 rewrites at logon (WindowMetrics precedent).
- [ ] `declutter_undo.reg` restores every toggle; verified the same way.
- [ ] Keys marked *verify* confirmed or dropped, with the outcome noted in the file comment.
- [ ] Runs on the locked-down work machine without tripping policy; anything blocked there moves to `elevated/` with a note, per §3.
- [ ] `README` in `worksafe/` lists each toggle in plain language for the user, not the key.

## Out of scope

Colors, DWM accent, cursors, wallpaper, Terminal (skin). OneDrive, Teams,
Edge first-run (app-level; separate issues if wanted). Anything HKLM.
