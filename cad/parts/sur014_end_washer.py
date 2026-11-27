"""SUR-014 END WASHER - sheet 114, Steel.  STATED: 28 x 3, hole 5.5."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-014", "END_WASHER", "Steel"


def build():
    return cq.Workplane("XY").circle(14).extrude(3).faces(">Z").workplane().hole(5.5)


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

