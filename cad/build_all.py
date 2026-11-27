"""Rebuild everything: 37 part STEPs, sub-assemblies, robot, work cell, verification, log.
usage: ~/miniforge3/envs/sur340-cad/bin/python build_all.py"""
import sys, glob, importlib, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, f"{HERE}/parts")
from lib.common import export_part

PY = sys.executable
mods = sorted(os.path.basename(f)[:-3] for f in glob.glob(f"{HERE}/parts/sur0*.py"))
for m in mods:
    mod = importlib.import_module(m)
    print(export_part(mod.build(), mod.PART_NO, mod.NAME, mod.MAT)[0])
for script in ("verify.py", "assy/build_assembly.py", "make_log.py"):
    r = subprocess.run([PY, f"{HERE}/{script}"], cwd=HERE)
    if r.returncode:
        sys.exit(f"{script} failed")
