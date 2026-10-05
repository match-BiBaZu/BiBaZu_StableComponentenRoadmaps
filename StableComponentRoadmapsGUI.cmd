@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Start-StableComponentRoadmapsGUI.ps1"
if errorlevel 1 (
  echo BiBaZu Observed Pose Roadmaps could not start. See error above.
  pause
  exit /b 1
)
