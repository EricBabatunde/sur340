"""Extract true-scale geometry from a part sheet of the SUR340 drawing set.

Usage: python extract.py <page(1-based)> [FRONT|LEFT|TOP ...]

The part sheets are A4 at the scale in the title block ("Scale 1:2 A4").
Visible edges: black stroked polylines (~0.99 pt). Hidden edges: grey (~0.62 pt).
Dimension lines/arrows are filled shapes and are ignored.

Output per view, in mm, origin = lower-left of the view's bounding box, x right, y up:
  O  full circle   centre, diameter
  A  arc           centre, radius, start/end angle (deg, CCW from +x)
  L  straight segment (collinear runs merged)
S = visible, H = hidden.
"""
import sys, math, re
import pymupdf as fitz

PDF = "/home/eric/Documents/projects/sur340/SUR340_Complete_2D_Drawing_Set.pdf"
PT = 72 / 25.4


def sheet_scale(pg):
    t = pg.get_text()
    m = re.search(r"Scale (\d+):(\d+)", t)
    a, b = int(m.group(1)), int(m.group(2))
    return PT * a / b, f"{a}:{b}"


def polylines(d):
    """Split a drawing path into connected point chains."""
    chains, cur = [], []
    for it in d["items"]:
        if it[0] == "l":
            p, q = it[1], it[2]
        elif it[0] == "c":
            p, q = it[1], it[4]
        elif it[0] == "re":
            r = it[1]
            chains.append([fitz.Point(r.x0, r.y0), fitz.Point(r.x1, r.y0), fitz.Point(r.x1, r.y1), fitz.Point(r.x0, r.y1), fitz.Point(r.x0, r.y0)])
            continue
        else:
            continue
        if cur and abs(cur[-1].x - p.x) < 1e-3 and abs(cur[-1].y - p.y) < 1e-3:
            cur.append(q)
        else:
            if cur:
                chains.append(cur)
            cur = [p, q]
    if cur:
        chains.append(cur)
    return chains


def fit_circle(pts):
    # algebraic least squares
    n = len(pts)
    sx = sum(p[0] for p in pts) / n
    sy = sum(p[1] for p in pts) / n
    u = [p[0] - sx for p in pts]
    v = [p[1] - sy for p in pts]
    suu = sum(a * a for a in u); svv = sum(b * b for b in v); suv = sum(a * b for a, b in zip(u, v))
    suuu = sum(a ** 3 for a in u); svvv = sum(b ** 3 for b in v)
    suvv = sum(a * b * b for a, b in zip(u, v)); svuu = sum(b * a * a for a, b in zip(u, v))
    det = suu * svv - suv * suv
    if abs(det) < 1e-12:
        return None
    uc = (0.5 * (suuu + suvv) * svv - 0.5 * (svvv + svuu) * suv) / det
    vc = (0.5 * (svvv + svuu) * suu - 0.5 * (suuu + suvv) * suv) / det
    cx, cy = uc + sx, vc + sy
    r = sum(math.hypot(p[0] - cx, p[1] - cy) for p in pts) / n
    err = max(abs(math.hypot(p[0] - cx, p[1] - cy) - r) for p in pts)
    return cx, cy, r, err


def classify(chain):
    """Return list of primitives for a point chain (already in mm coords)."""
    pts = chain
    if len(pts) >= 5:
        f = fit_circle(pts)
        if f and f[3] < max(0.03 * f[2], 0.12) and f[2] < 500:
            cx, cy, r, _ = f
            closed = math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) < 0.05
            # turning check: points must be on one arc (not straight)
            if closed:
                return [("O", cx, cy, 2 * r)]
            a0 = math.degrees(math.atan2(pts[0][1] - cy, pts[0][0] - cx))
            a1 = math.degrees(math.atan2(pts[-1][1] - cy, pts[-1][0] - cx))
            am = math.degrees(math.atan2(pts[len(pts) // 2][1] - cy, pts[len(pts) // 2][0] - cx))
            # orient CCW
            def ccw_between(s, m, e):
                return (m - s) % 360 < (e - s) % 360
            if not ccw_between(a0, am, a1):
                a0, a1 = a1, a0
            return [("A", cx, cy, r, a0 % 360, a1 % 360)]
    # straight segments: merge collinear
    out = []
    i = 0
    while i < len(pts) - 1:
        j = i + 1
        while j + 1 < len(pts):
            (x0, y0), (x1, y1), (x2, y2) = pts[i], pts[j], pts[j + 1]
            cr = abs((x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0))
            if cr < 1e-3 * max(1, math.hypot(x2 - x0, y2 - y0)):
                j += 1
            else:
                break
        out.append(("L", pts[i][0], pts[i][1], pts[j][0], pts[j][1]))
        i = j
    # if many short segments, try arc fit on the whole chain
    return out


def hidden_prims(d, r, R, k):
    """Hidden lines are drawn as grey filled dash strips (~0.5 pt wide)."""
    X = lambda x: (x - R.x0) / k
    Y = lambda y: (R.y1 - y) / k
    if r.width < 1.0:
        x = (r.x0 + r.x1) / 2
        return [("L", X(x), Y(r.y1), X(x), Y(r.y0))]
    if r.height < 1.0:
        y = (r.y0 + r.y1) / 2
        return [("L", X(r.x0), Y(y), X(r.x1), Y(y))]
    pts = []
    for it in d["items"]:
        if it[0] == "l":
            pts += [it[1], it[2]]
        elif it[0] == "c":
            pts += [it[1], it[4]]
        elif it[0] == "re":
            pts += [it[1].tl, it[1].br]
    pts = [(X(p.x), Y(p.y)) for p in pts]
    if len(pts) >= 8:
        f = fit_circle(pts)
        if f and f[3] < 0.35 + 0.02 * f[2]:
            cx, cy, rr, _ = f
            angs = sorted(math.degrees(math.atan2(y - cy, x - cx)) % 360 for x, y in pts)
            gaps = [(angs[(i + 1) % len(angs)] - angs[i]) % 360 for i in range(len(angs))]
            g = max(gaps)
            if g < 60:
                return [("O", cx, cy, 2 * rr)]
            i = gaps.index(g)
            return [("A", cx, cy, rr, angs[(i + 1) % len(angs)], angs[i])]
    # diagonal straight hidden line: endpoints = farthest pair
    best = max(((a, b) for a in pts for b in pts), key=lambda ab: (ab[0][0] - ab[1][0]) ** 2 + (ab[0][1] - ab[1][1]) ** 2)
    return [("L", best[0][0], best[0][1], best[1][0], best[1][1])]


def cluster(rects, gap):
    n = len(rects)
    parent = list(range(n))

    def f(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    g = [fitz.Rect(r.x0 - gap, r.y0 - gap, r.x1 + gap, r.y1 + gap) for r in rects]
    for a in range(n):
        for b in range(a + 1, n):
            if g[a].intersects(g[b]):
                parent[f(a)] = f(b)
    out = {}
    for i in range(n):
        out.setdefault(f(i), []).append(i)
    return list(out.values())


def views(page_no):
    doc = fitz.open(PDF)
    pg = doc[page_no - 1]
    k, sc = sheet_scale(pg)
    labels = []
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["text"].strip() in ("FRONT", "LEFT", "TOP (plan)", "TOP"):
                    labels.append((s["text"].strip().split()[0], fitz.Rect(s["bbox"])))
    tb = None
    strokes, hfills = [], []
    for d in pg.get_drawings():
        if d["type"] == "f" and d.get("fill") and 0.2 < d["fill"][0] < 0.5 and abs(d["fill"][0] - d["fill"][2]) < 0.01:
            r = fitz.Rect(d["rect"])
            if r.x0 < 520 and r.y0 < 420:
                hfills.append((d, r, "HF"))
            continue
        if d["type"] != "s":
            continue
        r = fitz.Rect(d["rect"])
        r = fitz.Rect(r.x0 - 0.01, r.y0 - 0.01, r.x1 + 0.01, r.y1 + 0.01)
        if r.width > 400 or r.x0 > 520 or r.y0 > 420:
            continue  # frame, title block, notes
        grey = d.get("color") and d["color"][0] > 0.05
        strokes.append((d, r, "H" if grey else "S"))
    groups = cluster([s[1] for s in strokes], gap=2.0)
    res, boxes, rest = {}, {}, []
    for g in groups:
        R = fitz.Rect()
        for i in g:
            R |= strokes[i][1]
        best, bd = None, 1e9
        for name, lr in labels:
            if lr.y0 >= R.y1 - 1 and lr.x0 >= R.x0 - 25 and lr.x0 <= R.x1:
                dd = lr.y0 - R.y1
                if dd < bd:
                    best, bd = name, dd
        if best is None or bd > 25:
            rest.append((g, R))
            continue
        res.setdefault(best, []).extend(strokes[i] for i in g)
        boxes[best] = boxes.get(best, fitz.Rect()) | R
    # interior features (holes etc.) not touching the outline
    for g, R in rest:
        for name, B in boxes.items():
            if B.contains(fitz.Point((R.x0 + R.x1) / 2, (R.y0 + R.y1) / 2)):
                res[name].extend(strokes[i] for i in g)
                break
    for d, r, h in hfills:
        c = fitz.Point((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
        for name, B in boxes.items():
            if fitz.Rect(B.x0 - 1, B.y0 - 1, B.x1 + 1, B.y1 + 1).contains(c):
                res[name].append((d, r, h))
                break
    return k, sc, res


def main(page_no, want=None):
    k, sc, res = views(page_no)
    print(f"page {page_no}  scale {sc}  ({k:.4f} pt/mm)")
    for name in ("FRONT", "LEFT", "TOP"):
        if name not in res or (want and name not in want):
            continue
        items = res[name]
        R = fitz.Rect()
        for _, r, h in items:
            if h != "HF":
                R |= r
        print(f"\n=== {name}  {R.width / k:.2f} x {R.height / k:.2f} mm")
        prims = set()
        for d, r, h in items:
            if h == "HF":
                for p in hidden_prims(d, r, R, k):
                    prims.add((p[0], "H") + tuple(round(v, 2) for v in p[1:]))
                continue
            for ch in polylines(d):
                pts = [((p.x - R.x0) / k, (R.y1 - p.y) / k) for p in ch]
                for p in classify(pts):
                    prims.add((p[0], h) + tuple(round(v, 2) for v in p[1:]))
        for p in sorted(prims, key=lambda p: ("OAL".index(p[0]), p[1], p[2:])):
            t, h = p[0], p[1]
            v = p[2:]
            if t == "O":
                print(f"  O {h} c=({v[0]:7.2f},{v[1]:7.2f}) d={v[2]:6.2f}")
            elif t == "A":
                print(f"  A {h} c=({v[0]:7.2f},{v[1]:7.2f}) r={v[2]:6.2f} {v[3]:6.1f}->{v[4]:6.1f}")
            else:
                ln = math.hypot(v[2] - v[0], v[3] - v[1])
                if ln >= 0.05:
                    print(f"  L {h} ({v[0]:7.2f},{v[1]:7.2f})-({v[2]:7.2f},{v[3]:7.2f}) {ln:6.2f}")


if __name__ == "__main__":
    main(int(sys.argv[1]), set(sys.argv[2:]) or None)
