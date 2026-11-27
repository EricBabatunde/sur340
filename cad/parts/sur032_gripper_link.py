"""SUR-032 GRIPPER LINK (parallel link, back) - sheet 131, Steel, laser cut.
STATED : 36 centres, 9 wide, 4 thick, 2 x 4.  Plane XZ as drawn, thickness Y0..4,
origin = left hole centre."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-032", "GRIPPER_LINK", "Steel"


def build():
    p = cq.Workplane("XZ").center(18, 0).slot2D(45, 9).extrude(-4)
    for x in (0, 36):
        p = p.cut(cyl(4, (x, -1, 0), (0, 1, 0), 6))
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

