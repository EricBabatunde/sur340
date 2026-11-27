"""SUR-036 PACKAGE (tube) - sheet 135, PA6.
STATED : 36 / 18 x 40.  MEASURED: 0.8 x 45 chamfers on all four circular edges."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-036", "PACKAGE", "PA6"


def build():
    p = cq.Workplane("XY").circle(18).extrude(40).faces(">Z").workplane().hole(18)
    return p.edges("%CIRCLE").chamfer(0.8)


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

