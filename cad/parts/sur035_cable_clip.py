"""SUR-035 CABLE CLIP - sheet 134, Steel, bent.
STATED : 28 x 8, saddle 24 / 20, hole 3.4.
MEASURED (2:1): base 28 x 2.5; legs X2-4 and X24-26; saddle R12 outer / R10 inner about
  (X14, Z10); outer legs to Z10.5; hole 3.4 through the base at X14.
Profile in XZ (FRONT), extruded Y0..8; origin = lower-left-front corner."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-035", "CABLE_CLIP", "Steel"


def build():
    outer = (cq.Workplane("XZ").moveTo(0, 0).lineTo(28, 0).lineTo(28, 2.5).lineTo(26, 2.5)
             .lineTo(26, 10.5).threePointArc((14, 22), (2, 10.5)).lineTo(2, 2.5).lineTo(0, 2.5)
             .close().extrude(-8))
    inner = (cq.Workplane("XZ").moveTo(4, 2.5).lineTo(24, 2.5).lineTo(24, 10)
             .threePointArc((14, 20), (4, 10)).close().extrude(-8))
    p = outer.cut(inner)
    return p.cut(cyl(3.4, (14, 4, -1), (0, 0, 1), 4.5))


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

