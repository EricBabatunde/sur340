"""SUR-034 SERVO BRACKET - sheet 133, Al 6061-T6.
STATED : plate 38 x 43 x 4 + flange 32 x 8 x 4, servo window 24 x 13.2.
MEASURED (1:1): plate X0-38, Y0-4, Z0-43; flange X0-32, Y4-8, Z35-43;
  window X9.5-33.5, Z8.4-21.6; 2 x M2 (nominal 2) through at Z15, X7.4 / X35.6;
  2 x 3.4 with counterbore 6 x 3 from the front (Y0) at Z39, X6 / X26, through plate + flange.
Origin: lower-left-front corner."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-034", "SERVO_BRACKET", "Al 6061-T6"


def build():
    p = cq.Workplane("XY").box(38, 4, 43, centered=False)
    p = p.union(cq.Workplane("XY").box(32, 4, 8, centered=False).translate((0, 4, 35)))
    p = p.cut(cq.Workplane("XY").box(24, 6, 13.2, centered=False).translate((9.5, -1, 8.4)))
    for x in (7.4, 35.6):
        p = p.cut(cyl(2, (x, -1, 15), (0, 1, 0), 6))
    for x in (6, 26):
        p = p.cut(cyl(3.4, (x, -1, 39), (0, 1, 0), 10))
        p = p.cut(cyl(6, (x, -1, 39), (0, 1, 0), 4))              # cbore Y0..3
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

