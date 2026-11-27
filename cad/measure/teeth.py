"""Print polar coordinates of tooth outline points in TOP view, one pitch near angle a0."""
import sys, math
import extract as e, pymupdf as fz
page, cx, cy, z, view = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), (sys.argv[5] if len(sys.argv)>5 else "TOP")
k, sc, res = e.views(page)
items = res[view]
R = fz.Rect()
for _, r, h in items:
    if h != "HF": R |= r
pts=set()
for d, r, h in items:
    if h!="S": continue
    for ch in e.polylines(d):
        for p in ch:
            x=(p.x-R.x0)/k-cx; y=(R.y1-p.y)/k-cy
            rr=math.hypot(x,y); a=math.degrees(math.atan2(y,x))
            pts.add((round(a,2), round(rr,3)))
pitch=360/z
RMAX=float(sys.argv[6]) if len(sys.argv)>6 else 1e9
sel=sorted(p for p in pts if -pitch*0.75<=p[0]<=pitch*0.75 and 0.6*min(RMAX,max(q[1] for q in pts))<p[1]<=RMAX)
print("rmax",max(q[1] for q in pts),"pitch",pitch)
for a,r in sel: print(f"{a:8.2f} {r:8.3f}")
