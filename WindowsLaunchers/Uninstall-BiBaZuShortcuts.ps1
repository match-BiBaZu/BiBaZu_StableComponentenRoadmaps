[CmdletBinding()]
param([switch]$DesktopOnly, [switch]$StartMenuOnly)
$ErrorActionPreference = 'Stop'
if ($DesktopOnly -and $StartMenuOnly) { throw 'Choose DesktopOnly OR StartMenuOnly.' }
$locations = @()
if (-not $StartMenuOnly) { $locations += [Environment]::GetFolderPath('Desktop') }
if (-not $DesktopOnly) { $locations += Join-Path ([Environment]::GetFolderPath('Programs')) 'BiBaZu' }
foreach ($location in $locations) {
    $shortcut = Join-Path $location 'BiBaZu Observed Pose Roadmaps.lnk'
    if (Test-Path -LiteralPath $shortcut -PathType Leaf) {
        Remove-Item -LiteralPath $shortcut
        Write-Host "Removed shortcut: $shortcut (rerun installer to restore)"
    }
}
