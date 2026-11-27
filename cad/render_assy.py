"""Render the robot assembly (FRONT = side view from -Y, TOP = plan) next to GA sheet 001."""
import sys, os
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad/assy")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pymupdf, cadquery as cq
import build_assembly as BA
from render import hlr, PDF, OUT

subs = [BA.sa1()[0], BA.sa2()[0], BA.sa3()[0], BA.sa4(), BA.sa5(), BA.sa6(), BA.sa7()[0]]
shapes = []
for s in subs:
    for ch in s.a.children:
        shapes.append(ch.obj.moved(ch.loc) if hasattr(ch.obj, "moved") else ch.obj)
comp = cq.Compound.makeCompound(shapes).wrapped
fig = plt.figure(figsize=(26, 12))
for i, (name, vd, xd) in enumerate([("SIDE (from -Y)", (0, -1, 0), (1, 0, 0)), ("PLAN", (0, 0, 1), (1, 0, 0))]):
    ax = fig.add_axes([0.01 + i * 0.25, 0.05, 0.24, 0.9])
    vis, hid = hlr(comp, vd, xd)
    for pl in vis:
        ax.plot(*zip(*pl), color="k", lw=0.4)
    ax.set_aspect("equal"); ax.set_title(name); ax.axis("off")
pg = pymupdf.open(PDF)[1]
pg.get_pixmap(dpi=90, clip=pymupdf.Rect(40, 40, 1000, 640)).save(f"{OUT}/_ga.png")
ax = fig.add_axes([0.51, 0.05, 0.48, 0.9]); ax.imshow(plt.imread(f"{OUT}/_ga.png")); ax.axis("off")
fig.savefig(f"{OUT}/assembly_vs_ga.png", dpi=60)
print(f"{OUT}/assembly_vs_ga.png")
