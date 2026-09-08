<#
.SYNOPSIS
  DeStijl — square window corners on Windows 11 (DESTIJL_STYLE.md §3, curves).

.DESCRIPTION
  Sets DWMWA_WINDOW_CORNER_PREFERENCE = DWMWCP_DONOTROUND on every visible
  top-level window, now and as new windows appear. Per-user, no elevation,
  nothing installed: a hidden process that polls. Optionally recolors the
  1 px DWM border (the 28 pt rule itself is residue on Windows; this is the
  one line DWM will draw).

  Apps that set their own corner preference (Chrome, Edge) may re-round on
  maximize/restore; every window is re-asserted every 60 s.

.PARAMETER Once       Apply to the windows open now and exit.
.PARAMETER Border     accent (default, untouched) | black (#0A0F10) | none
.PARAMETER Install    Put a shortcut in the Startup folder that runs this hidden at logon.
.PARAMETER Uninstall  Remove that shortcut.
.PARAMETER PollMs     Poll interval for new windows. Default 750.

.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File square_corners.ps1 -Once
  powershell -NoProfile -ExecutionPolicy Bypass -File square_corners.ps1 -Install
#>
param(
  [switch]$Once,
  [ValidateSet('accent','black','none')][string]$Border = 'accent',
  [switch]$Install,
  [switch]$Uninstall,
  [int]$PollMs = 750
)

$self = $MyInvocation.MyCommand.Path
$startup = Join-Path ([Environment]::GetFolderPath('Startup')) 'DeStijl square corners.lnk'

if ($Uninstall) { if (Test-Path $startup) { Remove-Item $startup }; "removed $startup"; return }
if ($Install) {
  $ws = New-Object -ComObject WScript.Shell
  $lnk = $ws.CreateShortcut($startup)
  $lnk.TargetPath = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
  $lnk.Arguments  = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$self`" -Border $Border"
  $lnk.WorkingDirectory = Split-Path $self
  $lnk.Description = 'DeStijl: square window corners (DESTIJL_STYLE.md §3)'
  $lnk.Save()
  "installed $startup"; return
}

Add-Type -TypeDefinition @"
using System; using System.Runtime.InteropServices; using System.Collections.Generic;
public static class DS {
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr l);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("dwmapi.dll")]  public static extern int  DwmSetWindowAttribute(IntPtr h, int attr, ref int val, int size);
  public static List<IntPtr> Visible() {
    var L = new List<IntPtr>();
    EnumWindows((h, l) => { if (IsWindowVisible(h)) L.Add(h); return true; }, IntPtr.Zero);
    return L;
  }
}
"@

$DWMWA_WINDOW_CORNER_PREFERENCE = 33
$DWMWA_BORDER_COLOR             = 34
$DWMWCP_DONOTROUND              = 1
$COLORREF_BLACK                 = 0x00100F0A     # #0A0F10 as 0x00BBGGRR
$DWMWA_COLOR_NONE               = [int]-2        # 0xFFFFFFFE

function Set-Square([IntPtr]$h) {
  [int]$v = $DWMWCP_DONOTROUND
  $rc = [DS]::DwmSetWindowAttribute($h, $DWMWA_WINDOW_CORNER_PREFERENCE, [ref]$v, 4)
  if ($Border -ne 'accent') {
    [int]$c = if ($Border -eq 'black') { $COLORREF_BLACK } else { $DWMWA_COLOR_NONE }
    [void][DS]::DwmSetWindowAttribute($h, $DWMWA_BORDER_COLOR, [ref]$c, 4)
  }
  return $rc
}

$seen = New-Object 'System.Collections.Generic.HashSet[IntPtr]'
$lastFull = Get-Date
while ($true) {
  $all  = [DS]::Visible()
  $full = ((Get-Date) - $lastFull).TotalSeconds -ge 60
  $ok = 0; $fail = 0
  foreach ($h in $all) {
    if ($full -or -not $seen.Contains($h)) {
      if ((Set-Square $h) -eq 0) { $ok++ } else { $fail++ }
      [void]$seen.Add($h)
    }
  }
  if ($full) { $seen.Clear(); foreach ($h in $all) { [void]$seen.Add($h) }; $lastFull = Get-Date }
  if ($Once) { "squared $ok of $($all.Count) visible windows ($fail refused)"; break }
  Start-Sleep -Milliseconds $PollMs
}
