"""Render a part in first-angle FRONT / LEFT / TOP + iso (hidden-line removed),
next to the PDF sheet, to a PNG for visual comparison.

usage: python render.py <part module name e.g. sur001_base_plate> <pdf page>
"""
import sys, importlib, math
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad/parts")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pymupdf
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
import cadquery as cq

PDF = "/home/eric/Documents/projects/sur340/SUR340_Complete_2D_Drawing_Set.pdf"
OUT = "/tmp/claude-1000/-home-eric-Documents-projects-sur340/53825c54-8918-4fde-ae7f-b27e22006541/scratchpad/render"

# view: (direction the viewer looks FROM, x-dir on sheet)
VIEWS = {
    "FRONT": ((0, -1, 0), (1, 0, 0)),
    "LEFT": ((-1, 0, 0), (0, -1, 0)),
    "TOP": ((0, 0, 1), (1, 0, 0)),
    "ISO": ((1, -1, 1), (1, 1, 0)),
}


def edges_of(shape):
    out = []
    if shape is None or shape.IsNull():
        return out
    ex = TopExp_Explorer(shape, TopAbs_EDGE)
    while ex.More():
        e = TopoDS.Edge(ex.Current())
        c = BRepAdaptor_Curve(e)
        d = GCPnts_QuasiUniformDeflection(c, 0.02)
        if d.IsDone():
            out.append([(d.Value(i).X(), d.Value(i).Y()) for i in range(1, d.NbPoints() + 1)])
        ex.Next()
    return out


def hlr(shape, vdir, xdir):
    algo = HLRBRep_Algo()
    algo.Add(shape)
    vx = gp_Dir(*vdir)
    ax = gp_Ax2(gp_Pnt(0, 0, 0), vx, gp_Dir(*xdir))
    algo.Projector(HLRAlgo_Projector(ax))
    algo.Update()
    algo.Hide()
    h = HLRBRep_HLRToShape(algo)
    vis = edges_of(h.VCompound()) + edges_of(h.OutLineVCompound()) + edges_of(h.Rg1LineVCompound())
    hid = edges_of(h.HCompound()) + edges_of(h.OutLineHCompound())
    return vis, hid


def main(mod, page):
    m = importlib.import_module(mod)
    shp = m.build()
    s = shp.val().wrapped if isinstance(shp, cq.Workplane) else shp.wrapped
    import os
    os.makedirs(OUT, exist_ok=True)
    fig = plt.figure(figsize=(22, 11))
    # first-angle layout: FRONT top-left, LEFT right of it, TOP below FRONT
    pos = {"FRONT": [0.02, 0.52, 0.24, 0.44], "LEFT": [0.27, 0.52, 0.24, 0.44],
           "TOP": [0.02, 0.04, 0.24, 0.44], "ISO": [0.27, 0.04, 0.24, 0.44]}
    for name, (vd, xd) in VIEWS.items():
        ax = fig.add_axes(pos[name])
        vis, hid = hlr(s, vd, xd)
        for pl in hid:
            ax.plot(*zip(*pl), color="0.55", lw=0.6, ls=(0, (3, 2)))
        for pl in vis:
            ax.plot(*zip(*pl), color="k", lw=0.8)
        ax.set_aspect("equal"); ax.set_title(name); ax.axis("off")
    pg = pymupdf.open(PDF)[page - 1]
    pix = pg.get_pixmap(dpi=110, clip=pymupdf.Rect(28, 28, 520, 420))
    img = f"{OUT}/_sheet.png"
    pix.save(img)
    ax = fig.add_axes([0.53, 0.04, 0.46, 0.92])
    ax.imshow(plt.imread(img)); ax.axis("off"); ax.set_title(f"PDF page {page}")
    out = f"{OUT}/{mod}.png"
    fig.savefig(out, dpi=70)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
