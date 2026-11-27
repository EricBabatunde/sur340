"""SUR-018 ELBOW CAP - sheet 118, Al 6061-T6.
STATED : 80 x 6, 8 x 4.5 on PCD 64.
MEASURED (1:1): axis along Y (as drawn), Y 0..6; 0.8 x 45 chamfer both faces;
  recess 22 x 2 deep on the Y=0 (front) face; PCD64 holes at 22.5 + n*45 deg (in XZ).
Origin: front face centre."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-018", "ELBOW_CAP", "Al 6061-T6"


def build():
    p = cq.Workplane("XZ").circle(40).extrude(-6)                 # Y 0..6
    p = p.cut(cyl(22, (0, -1, 0), (0, 1, 0), 3))                  # recess 22 x 2
    for x, z in pcd(8, 64, 22.5):
        p = p.cut(cyl(4.5, (x, -1, z), (0, 1, 0), 8))
    p = p.edges(cq.selectors.RadiusNthSelector(-1)).chamfer(0.8)
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

