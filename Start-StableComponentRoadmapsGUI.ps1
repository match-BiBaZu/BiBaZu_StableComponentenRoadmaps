$ErrorActionPreference = 'Stop'
$roadmapRepo = Split-Path -Parent $PSCommandPath
$roadmapPython = Join-Path $roadmapRepo '.venv\Scripts\pythonw.exe'
if (-not (Test-Path -LiteralPath $roadmapPython -PathType Leaf)) {
    throw "Missing local Python environment. Run 'uv sync' in $roadmapRepo first."
}
Start-Process -FilePath $roadmapPython -ArgumentList ('"' + (Join-Path $roadmapRepo 'StableComponentRoadmapsGUI.py') + '"') -WorkingDirectory $roadmapRepo -WindowStyle Hidden
