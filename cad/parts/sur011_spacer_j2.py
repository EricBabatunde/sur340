"""SUR-011 SPACER J2 - sheet 111, Steel.  STATED: 22 / 12.2 x 24."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-011", "SPACER_J2", "Steel"


def build():
    return cq.Workplane("XY").circle(11).extrude(24).faces(">Z").workplane().hole(12.2)


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

