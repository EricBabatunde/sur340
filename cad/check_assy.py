import sys, itertools
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad/assy")
import cadquery as cq
import build_assembly as BA
subs = [BA.sa1()[0], BA.sa2()[0], BA.sa3()[0], BA.sa4(), BA.sa5(), BA.sa6(), BA.sa7()[0]]
items = []
for s in subs:
    for ch in s.a.children:
        items.append((ch.name, ch.obj.moved(ch.loc)))
bb = cq.Compound.makeCompound([s for _, s in items]).BoundingBox()
print(f"robot envelope X {bb.xmin:.1f}..{bb.xmax:.1f} ({bb.xlen:.1f})  Y {bb.ymin:.1f}..{bb.ymax:.1f} ({bb.ylen:.1f})  Z {bb.zmin:.1f}..{bb.zmax:.1f} ({bb.zlen:.1f})")
boxes = [(n, s, s.BoundingBox()) for n, s in items]
hits = []
for (n1, s1, b1), (n2, s2, b2) in itertools.combinations(boxes, 2):
    if b1.xmax < b2.xmin or b2.xmax < b1.xmin or b1.ymax < b2.ymin or b2.ymax < b1.ymin or b1.zmax < b2.zmin or b2.zmax < b1.zmin:
        continue
    try:
        v = s1.intersect(s2).Volume()
    except Exception:
        v = -1
    if v > 0.5:
        hits.append((v, n1, n2))
for v, a, b in sorted(hits, reverse=True):
    print(f"{v:9.1f} mm3  {a}  x  {b}")
print(len(hits), "interferences > 0.5 mm3")
