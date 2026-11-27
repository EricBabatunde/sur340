"""SUR-013 KEY 4x4x10 - sheet 113, Steel C45.
STATED : parallel key 4 x 4 x 10.
DRAWN  : the sheet views show a round 4 x 10 body (TOP view is a circle, iso a cylinder).
         Modelled AS DRAWN (cylinder 4 x 10) - flagged to the user.
Origin: bottom centre, Z up."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-013", "KEY_4x4x10", "Steel C45"


def build():
    return cq.Workplane("XY").circle(2).extrude(10)


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

