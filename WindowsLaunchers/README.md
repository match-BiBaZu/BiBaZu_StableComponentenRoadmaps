# Windows launcher

Run `uv sync` at the repository root, then double-click
`Verknuepfungen-installieren.cmd` to install **BiBaZu Observed Pose Roadmaps**
on the Desktop and in Start Menu > BiBaZu. The shortcut uses the repository's
own Python environment, launcher and icon. Other BiBaZu shortcuts are untouched.

```powershell
.\Install-BiBaZuShortcuts.ps1 -CheckOnly
.\Install-BiBaZuShortcuts.ps1 -DesktopOnly
.\Install-BiBaZuShortcuts.ps1 -StartMenuOnly
.\Install-BiBaZuShortcuts.ps1 -DestinationDirectory C:\Temp\RoadmapShortcuts
.\Uninstall-BiBaZuShortcuts.ps1 -StartMenuOnly
```

Re-run the installer after moving the checkout. The `.cmd` launch file itself
cannot carry a Windows icon; the installed `.lnk` shortcut uses the supplied ICO.
This is a small launcher rather than a bundled EXE. `pythonw.exe` runs the GUI
without keeping a console window open. Startup errors appear in a message box.
