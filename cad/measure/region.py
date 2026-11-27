"""Dump visible straight lines (len >= minlen) in a sheet region, in mm at a given scale,
relative to a reference point. usage: region.py page x0 y0 x1 y1 scale refx refy [minlen]"""
import sys, math
import pymupdf as fz
import extract as e
pg_no, x0, y0, x1, y1, sc, rx, ry = int(sys.argv[1]), *map(float, sys.argv[2:9])
minlen = float(sys.argv[9]) if len(sys.argv) > 9 else 3
pg = fz.open(e.PDF)[pg_no - 1]
k = e.PT / sc
R = fz.Rect(x0, y0, x1, y1)
seen = set()
for d in pg.get_drawings():
    if d["type"] != "s" or not R.contains(fz.Rect(d["rect"])):
        continue
    for ch in e.polylines(d):
        pts = [((p.x - rx) / k, (ry - p.y) / k) for p in ch]
        for pr in e.classify(pts):
            if pr[0] == "L":
                ln = math.hypot(pr[3] - pr[1], pr[4] - pr[2])
                if ln >= minlen:
                    key = tuple(round(v, 1) for v in pr[1:])
                    if key not in seen:
                        seen.add(key); print(f"L ({pr[1]:7.1f},{pr[2]:7.1f})-({pr[3]:7.1f},{pr[4]:7.1f}) {ln:6.1f}")
            elif pr[0] == "O" and pr[3] > 2:
                key = ("O",) + tuple(round(v, 1) for v in pr[1:])
                if key not in seen:
                    seen.add(key); print(f"O c=({pr[1]:7.1f},{pr[2]:7.1f}) d={pr[3]:6.1f}")
