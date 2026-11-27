"""SUR-012 J2 OUTPUT SHAFT - sheet 112, Steel C45.
STATED : 12 x 45 + journal 30 x 7 + collar 16 x 4; keyway 4 x 3; M5 end hole.
MEASURED (1:1): shaft 12 z0-34, journal 30 z34-41, collar 16 z41-45;
  keyway 4 wide x 3 deep x 10 long from the shaft end, on +Y;
  M5 end hole (nominal 5) x 12 deep in the shaft end.
Origin: shaft end centre (bottom), Z up."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-012", "J2_OUTPUT_SHAFT", "Steel C45"


def build():
    prof = [(0, 0), (6, 0), (6, 34), (15, 34), (15, 41), (8, 41), (8, 45), (0, 45)]
    p = cq.Workplane("XZ").polyline(prof).close().revolve(360, (0, 0, 0), (0, 1, 0))
    p = p.cut(cq.Workplane("XY").center(0, 4.5).rect(4, 3).extrude(10))     # keyway, y 3..6
    p = p.faces("<Z").workplane().hole(5.0, 12)                            # M5 end hole
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

