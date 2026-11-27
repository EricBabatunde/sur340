"""SUR-025 PINION SHAFT (J2) - sheet 125, Steel C45 h6.  STATED: 8 x 80 (axis Z)."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-025", "PINION_SHAFT", "Steel C45"


def build():
    return cq.Workplane("XY").circle(4).extrude(80)


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

