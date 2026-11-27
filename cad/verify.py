"""Re-read every part STEP and check: AP214 header, exactly one valid solid, product name,
colour present, and bounding box against the overall size stated on the sheet."""
import glob, os, re, sys
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorType
from OCP.TDF import TDF_LabelSequence
from OCP.TDataStd import TDataStd_Name
from OCP.Quantity import Quantity_Color
from OCP.IFSelect import IFSelect_RetDone
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.TopLoc import TopLoc_Location

OUT = "/home/eric/Documents/projects/sur340/out/01_STEP_parts"

# overall sizes stated on the part sheets (sorted, mm)
STATED = {
    "SUR-001": (220, 220, 12), "SUR-002": (160, 160, 84), "SUR-003": (159, 159, 10),
    "SUR-004": (152, 152, 45), "SUR-005": (153, 126, 113), "SUR-006": (64, 112, 82),
    "SUR-007": (84, 84, 28), "SUR-008": (28.4, 28.4, 20), "SUR-009": (86.9, 86.9, 10),
    "SUR-010": (86.9, 86.9, 10), "SUR-011": (22, 22, 24), "SUR-012": (30, 30, 45),
    "SUR-013": (4, 4, 10), "SUR-014": (28, 28, 3), "SUR-015": (114.7, 27, 252),
    "SUR-016": (30, 48, 30), "SUR-017": (98, 84, 80), "SUR-018": (80, 6, 80),
    "SUR-019": (38, 44, 44), "SUR-020": (50, 8, 8), "SUR-021": (132, 73, 60),
    "SUR-022": (36, 37, 36), "SUR-023": (56, 5, 56), "SUR-024": (58, 46, 80),
    "SUR-025": (8, 8, 80), "SUR-027": (8, 8, 74), "SUR-028": (50, 50, 8),
    "SUR-029": (68, 44, 48), "SUR-030": (59.5, 4, 37.9), "SUR-031": (59.5, 4, 38),
    "SUR-032": (45, 4, 9), "SUR-033": (12, 32, 50), "SUR-034": (38, 8, 43),
    "SUR-035": (28, 8, 22), "SUR-036": (36, 36, 40), "SUR-037": (90, 90, 24),
    "SUR-038": (90, 90, 22),
}


def check(path):
    head = open(path, errors="ignore").read(2000).upper()
    ap214 = "AUTOMOTIVE_DESIGN" in head
    doc = TDocStd_Document(TCollection_ExtendedString("XmlOcaf"))
    r = STEPCAFControl_Reader()
    r.SetColorMode(True); r.SetNameMode(True)
    assert r.ReadFile(path) == IFSelect_RetDone
    r.Transfer(doc)
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    ct = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    labs = TDF_LabelSequence(); st.GetFreeShapes(labs)
    lab = labs.Value(1)
    shape = st.GetShape_s(lab)
    nm = TDataStd_Name()
    name = nm.Get().ToExtString() if lab.FindAttribute(TDataStd_Name.GetID_s(), nm) else "?"
    col = Quantity_Color()
    has_col = ct.GetColor(shape, XCAFDoc_ColorType.XCAFDoc_ColorSurf, col) or \
        ct.GetColor(shape, XCAFDoc_ColorType.XCAFDoc_ColorGen, col)
    if not has_col:   # colour may sit on the solid / faces
        exs = TopExp_Explorer(shape, TopAbs_SOLID)
        while exs.More() and not has_col:
            has_col = ct.GetColor(exs.Current(), XCAFDoc_ColorType.XCAFDoc_ColorSurf, col)
            exs.Next()
    n = 0; ex = TopExp_Explorer(shape, TopAbs_SOLID)
    while ex.More():
        n += 1; ex.Next()
    valid = BRepCheck_Analyzer(shape).IsValid()
    b = Bnd_Box(); BRepBndLib.AddOptimal_s(shape, b, False, False)
    x0, y0, z0, x1, y1, z1 = b.Get()
    return ap214, name, has_col, n, valid, (x1 - x0, y1 - y0, z1 - z0)


def main():
    bad = 0
    files = sorted(glob.glob(f"{OUT}/SUR-*.step"))
    for f in files:
        pn = os.path.basename(f)[:7]
        ap, name, col, n, valid, size = check(f)
        st = STATED.get(pn)
        ok_size = st is not None and all(abs(a - b) <= 0.15 for a, b in zip(sorted(size), sorted(st)))
        ok = ap and col and n == 1 and valid and ok_size and name.startswith(pn)
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {os.path.basename(f):34s} AP214={ap} solids={n} valid={valid} "
              f"colour={col} size={size[0]:.2f}x{size[1]:.2f}x{size[2]:.2f} stated={st}")
    print(f"\n{len(files)} files, {bad} problems")
    return bad


if __name__ == "__main__":
    sys.exit(main())
