"""SUR-020 J4 DRIVE SHAFT - sheet 120, Steel C45 h6.  STATED: 8 x 50 (axis X as drawn)."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-020", "J4_DRIVE_SHAFT", "Steel C45"


def build():
    return cq.Workplane("YZ").circle(4).extrude(50)


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

