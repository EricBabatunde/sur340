"""SUR-009 J2 OUTPUT GEAR - sheet 109, Brass CuZn39Pb3.
STATED : m 1.5, z 56, pitch 84, width 10, bore 12 + keyway 4, 6 x 4.5 cb 8 x 3 PCD 44,
         4 x 10 PCD 62; ratio 56:17.
MEASURED (1:1): keyway 4 wide at +Y to 8.3 from axis; counterbores on the BOTTOM face;
  PCD44 holes start +X; PCD62 holes at 45 deg.
Origin: bottom centre, Z up."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-009", "J2_OUTPUT_GEAR", "Brass CuZn39Pb3"


def build():
    p = gear_profile(cq.Workplane("XY"), 56, 1.5).extrude(10)
    p = p.faces(">Z").workplane().hole(12)
    p = p.cut(cq.Workplane("XY").center(0, 5.15).rect(4, 6.3).extrude(10))   # keyway to y=8.3
    p = p.faces("<Z").workplane().pushPoints([(x, -y) for x, y in pcd(6, 44, 0)]).cboreHole(4.5, 8, 3)
    p = p.faces(">Z").workplane().pushPoints(pcd(4, 62, 45)).hole(10)
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

