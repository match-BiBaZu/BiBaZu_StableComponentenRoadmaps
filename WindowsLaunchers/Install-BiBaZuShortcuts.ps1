[CmdletBinding()]
param(
    [switch]$DesktopOnly,
    [switch]$StartMenuOnly,
    [string]$DestinationDirectory,
    [switch]$CheckOnly
)
$ErrorActionPreference = 'Stop'
if ($DesktopOnly -and $StartMenuOnly) { throw 'Choose DesktopOnly OR StartMenuOnly.' }
$launcherDirectory = Split-Path -Parent $PSCommandPath
$repository = Split-Path -Parent $launcherDirectory
$launcher = Join-Path $repository 'StableComponentRoadmapsGUI.cmd'
$python = Join-Path $repository '.venv\Scripts\pythonw.exe'
$consolePython = Join-Path $repository '.venv\Scripts\python.exe'
$icon = Join-Path $launcherDirectory 'icons\stable-roadmaps.ico'
$commandHost = Join-Path $env:WINDIR 'System32\cmd.exe'
$arguments = '/d /c ""' + $launcher + '""'
foreach ($file in @($launcher, $commandHost, $python, $consolePython, $icon)) {
    if (-not (Test-Path -LiteralPath $file -PathType Leaf)) {
        throw "Missing: $file. Run 'uv sync' in $repository first."
    }
}
Push-Location $repository
try {
    & $consolePython -c "import PyQt6, bibazu_stable_roadmaps.gui"
    if ($LASTEXITCODE -ne 0) { throw "Application dependencies missing. Run 'uv sync' in $repository." }
} finally { Pop-Location }
if ($CheckOnly) { Write-Host 'Launcher prerequisites OK.'; return }
$destinations = @()
if ($DestinationDirectory) { $destinations += $DestinationDirectory }
else {
    if (-not $StartMenuOnly) { $destinations += [Environment]::GetFolderPath('Desktop') }
    if (-not $DesktopOnly) { $destinations += Join-Path ([Environment]::GetFolderPath('Programs')) 'BiBaZu' }
}
$shell = New-Object -ComObject WScript.Shell
foreach ($destination in $destinations) {
    New-Item -ItemType Directory -Path $destination -Force | Out-Null
    $path = Join-Path $destination 'BiBaZu Observed Pose Roadmaps.lnk'
    $shortcut = $shell.CreateShortcut($path)
    $shortcut.TargetPath = $commandHost
    $shortcut.Arguments = $arguments
    $shortcut.WorkingDirectory = $repository
    $shortcut.IconLocation = "$icon,0"
    $shortcut.Description = 'BiBaZu Observed Pose Roadmaps'
    $shortcut.WindowStyle = 1
    $shortcut.Save()
    $saved = $shell.CreateShortcut($path)
    if ($saved.TargetPath -ne $commandHost -or $saved.Arguments -ne $arguments -or
        $saved.IconLocation -ne "$icon,0" -or $saved.WorkingDirectory -ne $repository) {
        throw "Shortcut verification failed: $path"
    }
    Write-Host "Created: $path"
}
