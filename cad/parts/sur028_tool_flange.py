"""SUR-028 TOOL FLANGE - sheet 127, Al 6061-T6.
STATED : 50 x 8, 6 x 4.5 cb 8 on PCD 36, bore 8 + M3 set screw.
MEASURED (1:1): counterbore 8 x 3 from the top; PCD36 holes start +Y;
  M3 set screw hole (nominal 3) along +X at z4 from the bore to the rim.
Origin: bottom centre, Z up."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-028", "TOOL_FLANGE", "Al 6061-T6"


def build():
    p = cq.Workplane("XY").circle(25).extrude(8)
    p = p.faces(">Z").workplane().hole(8)
    p = p.faces(">Z").workplane().pushPoints(pcd(6, 36, 90)).cboreHole(4.5, 8, 3)
    p = p.cut(cyl(3, (3, 0, 4), (1, 0, 0), 25))
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

