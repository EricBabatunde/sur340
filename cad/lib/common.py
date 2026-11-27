"""Shared helpers for the SUR340 CadQuery models.

Modelling rules (for SolidWorks FeatureWorks recognition):
  * one solid per part, built like a feature tree: base extrude/revolve -> boss/cut
    extrudes -> holes (plain / counterbore) -> fillets/chamfers last.
  * planar sketches from lines and arcs.
  * Tapped holes: the drawing set draws them at NOMINAL diameter (sheet 000/001:
    "Threads are cosmetic (modelled at nominal diameter)"), so they are modelled as
    plain holes of nominal diameter. Add cosmetic threads in SolidWorks if wanted.

Part coordinate convention (first-angle sheets):
  FRONT view = X right, Z up (viewed from -Y);  TOP (plan) = X right, Y up (+Y = back);
  LEFT view  = viewed from -X, sheet-x = -Y.
"""
import math, os
import cadquery as cq

ROOT = "/home/eric/Documents/projects/sur340"
OUT_PARTS = f"{ROOT}/out/01_STEP_parts"
OUT_ASSY = f"{ROOT}/out/03_STEP_assemblies"

# material -> RGB (0..1)
MAT = {
    "Al 6061-T6":      (0.78, 0.80, 0.82),
    "Al 7075":         (0.22, 0.24, 0.27),   # hard anodised
    "Brass CuZn39Pb3": (0.85, 0.68, 0.30),
    "Steel":           (0.50, 0.52, 0.55),
    "Steel 42CrMo4":   (0.40, 0.42, 0.45),
    "Steel C45":       (0.55, 0.57, 0.60),
    "Steel S355":      (0.45, 0.47, 0.50),
    "PA6":             (0.95, 0.95, 0.92),
    "black 8.8":       (0.10, 0.10, 0.10),
    "set screw":       (0.20, 0.20, 0.20),
    "bearing":         (0.70, 0.72, 0.75),
    "motor":           (0.15, 0.15, 0.17),
    "motor_flange":    (0.62, 0.64, 0.67),
    "rubber":          (0.12, 0.12, 0.12),
    "servo":           (0.15, 0.30, 0.65),
    "connector":       (0.92, 0.92, 0.90),
    "coupling":        (0.70, 0.72, 0.76),
    "gland":           (0.12, 0.12, 0.14),
}


def color(mat):
    r, g, b = MAT[mat]
    return cq.Color(r, g, b)


def pcd(n, d, start_deg=0.0):
    """Points of n holes on PCD d, starting at start_deg (0 = +X), CCW."""
    return [(d / 2 * math.cos(math.radians(start_deg + i * 360 / n)),
             d / 2 * math.sin(math.radians(start_deg + i * 360 / n))) for i in range(n)]


def single_solid(shape):
    s = shape.val() if isinstance(shape, cq.Workplane) else shape
    s = s.clean()
    sols = s.Solids()
    assert len(sols) == 1, f"expected 1 solid, got {len(sols)}"
    assert sols[0].isValid(), "invalid solid"
    return sols[0]


def export_part(shape, part_no, name, mat):
    """Write one part as a single-body STEP AP214 file (product name + colour),
    so SolidWorks opens it as a part document (not a 1-component assembly)."""
    from OCP.TDocStd import TDocStd_Document
    from OCP.TCollection import TCollection_ExtendedString
    from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorType
    from OCP.TDataStd import TDataStd_Name
    from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
    from OCP.STEPCAFControl import STEPCAFControl_Writer
    from OCP.STEPControl import STEPControl_AsIs
    from OCP.Interface import Interface_Static
    from OCP.IFSelect import IFSelect_RetDone

    os.makedirs(OUT_PARTS, exist_ok=True)
    solid = single_solid(shape)
    label = f"{part_no}_{name}"
    doc = TDocStd_Document(TCollection_ExtendedString("XmlOcaf"))
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    ct = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    lab = st.AddShape(solid.wrapped, False)
    TDataStd_Name.Set_s(lab, TCollection_ExtendedString(label))
    r, g, b = MAT[mat]
    ct.SetColor(lab, Quantity_Color(r, g, b, Quantity_TOC_RGB), XCAFDoc_ColorType.XCAFDoc_ColorSurf)
    Interface_Static.SetCVal_s("write.step.schema", "AP214IS")
    Interface_Static.SetCVal_s("write.step.unit", "MM")
    w = STEPCAFControl_Writer()
    w.SetColorMode(True)
    w.SetNameMode(True)
    w.Transfer(doc, STEPControl_AsIs)
    path = f"{OUT_PARTS}/{label}.step"
    assert w.Write(path) == IFSelect_RetDone
    head = open(path, "r", errors="ignore").read(3000).upper()
    assert "AUTOMOTIVE_DESIGN" in head, "STEP not written as AP214"
    return path, solid


def write_step(assy, path):
    from OCP.Interface import Interface_Static
    Interface_Static.SetCVal_s("write.step.schema", "AP214IS")
    assy.export(path, "STEP", write_pcurves=True)
    # make sure the header says AP214
    head = open(path, "r", errors="ignore").read(3000)
    assert "AUTOMOTIVE_DESIGN" in head.upper(), "STEP not written as AP214"
    return path


# ---------------------------------------------------------------- gears
# Tooth form as drawn on sheets 103/108/109/110 (measured): each flank is a
# 2-segment polyline tip -> pitch circle -> root circle; tip and root are arcs.
# Half tooth widths (mm, chordal): tip 0.27, pitch 0.73, root 1.25 (m 1.5 gears).
# r_tip = m(z+2)/2, r_pitch = m z/2, r_root = r_pitch - 1.25 m.
# First tooth centre at PHASE_FRAC * pitch angle CCW from +X (measured on all
# three m1.5 gears: 0.376).
PHASE_FRAC = 0.376


def gear_profile(wp, z, m, phase_deg=None, hw=(0.27, 0.73, 1.25), r_root=None):
    """Closed gear outline (lines + arcs) on workplane wp, centred at origin."""
    pitch = 2 * math.pi / z
    rt, rp = m * (z + 2) / 2, m * z / 2
    rr = r_root if r_root is not None else rp - 1.25 * m
    ph = math.radians(phase_deg) if phase_deg is not None else PHASE_FRAC * pitch
    at, ap, ar = hw[0] / rt, hw[1] / rp, hw[2] / rr
    P = lambda r, a: (r * math.cos(a), r * math.sin(a))
    w = None
    for i in range(z):
        c = ph + i * pitch
        pts = [P(rr, c - ar), P(rp, c - ap), P(rt, c - at)]
        if w is None:
            w = wp.moveTo(*pts[0])
        else:
            mid = c - pitch / 2
            w = w.threePointArc(P(rr, mid), pts[0])
        w = w.lineTo(*pts[1]).lineTo(*pts[2]).threePointArc(P(rt, c), P(rt, c + at))
        w = w.lineTo(*P(rp, c + ap)).lineTo(*P(rr, c + ar))
    c0 = ph
    w = w.threePointArc(P(rr, c0 + (z - 0.5) * pitch), P(rr, c0 - ar))
    return w.close()


def cyl(d, p0, direction, length):
    """Cylinder (for hole cuts / bosses) of diameter d from point p0 along direction."""
    return cq.Workplane("XY").add(
        cq.Solid.makeCylinder(d / 2, length, cq.Vector(*p0), cq.Vector(*direction)))
