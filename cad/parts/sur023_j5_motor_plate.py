"""SUR-023 J5 MOTOR PLATE - sheet 123, Al 6061-T6.
STATED : 56 x 56 x 5, hole 32 + recess 40 x 2, 4 x 4.5 cb 8, 4 x M3 on 31 sq at 45 deg.
MEASURED (1:1): plate in XZ (as drawn), thickness Y0..5; corners R5; recess on the Y0 (front)
  face; 4.5 holes at (+-18, +-18) with counterbore 8 x 3 from the BACK (Y5) face;
  M3 (nominal 3) through at R21.92 on the X/Z axes (= 31 sq turned 45 deg).
Origin: front face centre."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-023", "J5_MOTOR_PLATE", "Al 6061-T6"


def build():
    p = cq.Workplane("XZ").rect(56, 56).extrude(-5).edges("|Y").fillet(5)
    p = p.cut(cyl(32, (0, -1, 0), (0, 1, 0), 7))
    p = p.cut(cyl(40, (0, -1, 0), (0, 1, 0), 3))                  # recess Y0..2
    for x in (-18, 18):
        for z in (-18, 18):
            p = p.cut(cyl(4.5, (x, -1, z), (0, 1, 0), 7))
            p = p.cut(cyl(8, (x, 2, z), (0, 1, 0), 4))            # cbore Y2..5
    for x, z in pcd(4, 31 * math.sqrt(2), 0):
        p = p.cut(cyl(3, (x, -1, z), (0, 1, 0), 7))
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

