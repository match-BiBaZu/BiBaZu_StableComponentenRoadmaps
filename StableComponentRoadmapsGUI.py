"""Double-click launcher; independent of the caller's working directory."""
import ctypes
from pathlib import Path
import sys
import traceback

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
try:
    from bibazu_stable_roadmaps.gui import main
    raise SystemExit(main())
except Exception:
    error = traceback.format_exc()
    if sys.platform == "win32":
        ctypes.windll.user32.MessageBoxW(None, error, "BiBaZu Observed Pose Roadmaps could not start", 0x10)
    else:
        raise
