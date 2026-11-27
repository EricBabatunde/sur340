"""SUR-033 GRIPPER FINGER (serrated pad) - sheet 132, Al 7075 hard anodised.
STATED : 12 x 32 x 50, 6 serrations, 2 x 4.
MEASURED (1:1): profile in XZ (FRONT) 12 x 50 with R2 corners, extruded Y 0..32;
  6 serrations on the X0 face: 1.5 deep x 2 high at Z 3-5, 7-9 ... 23-25;
  holes 4 through along Y at (X8, Z30) and (X8, Z42).
Origin: lower-left-front corner."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-033", "GRIPPER_FINGER", "Al 7075"


def build():
    p = cq.Workplane("XZ").center(6, 25).rect(12, 50).extrude(-32).edges("|Y").fillet(2)
    for i in range(6):
        z0 = 3 + 4 * i
        p = p.cut(cq.Workplane("XY").box(1.5, 34, 2, centered=False).translate((-0.01, -1, z0)))
    for z in (30, 42):
        p = p.cut(cyl(4, (8, -1, z), (0, 1, 0), 34))
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

