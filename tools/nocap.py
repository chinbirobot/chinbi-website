"""Run a record_*_mujoco.py script at 1280x720 with the debug captions turned off (website clips).
Usage: MUJOCO_GL=egl python nocap.py record_roll_mujoco <script args...>"""
import importlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import record_falls_mujoco as RF
RF.W, RF.H = 1280, 720
RF.caption = lambda img, lines, *a, **k: img
mod = importlib.import_module(sys.argv[1])
mod.W, mod.H = 1280, 720
for name in ("caption", "label_caption"):
    if hasattr(mod, name):
        setattr(mod, name, lambda img, lines, *a, **k: img)
sys.argv = [sys.argv[1] + ".py"] + sys.argv[2:]
mod.main()
