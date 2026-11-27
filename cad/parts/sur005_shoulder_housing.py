"""SUR-005 SHOULDER HOUSING (J2) - sheet 105, Al 6061-T6.
STATED : base 126 x 18, tower 80 x 72, J2 boss 96 x 72 at 65, cartridge bore 58.2
         + 8 x M5 PCD 72, 608 seat for the pinion shaft.  Overall 153 x 126 x 113.
MEASURED (sheet 105, 1:2) - origin = base bottom centre, Z up, J2 axis along Y at Z65:
  base 126 x 18; 4 x 6.6 cbore 11 x 6.5 at R56 on 0/60/120/180 deg;
  PG7 gland hole 12.5 vertical through the base at (-52, 26) (breaks the rim);
  tower X -40..40, Y -36..36; boss 96 (Y -36..36); bore 58.2 through;
  8 x M5 (nominal 5) x 12 deep in the back face (Y36), PCD72 from 0 deg (XZ);
  NEMA23 plate X -90..-22, Z 31..99, Y -42..-36, R6 corners, pilot recess 40 x 3 deep + 10 through,
  4 x M5 through on 47.14 sq; motor/pinion axis X -54.74, Z 65 (= centre distance 54.75);
  608 block X -72..-45.25, Y 26..36, Z 49..81: seat 22 x 7 from Y36, 10 through;
  coupling pocket X -48..-42.74, Y -36..0, Z 55.76..74.25;
  internal pocket X -30..30, Y -26..26, Z 18..30 (drawn enclosed); opened to the bottom with a
  40 hole through the base on the J1 axis, in line with the turntable 40 bore (user decision
  2026-11-27, cable passage; not on the sheet).
"""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, cyl

PART_NO, NAME, MAT = "SUR-005", "SHOULDER_HOUSING", "Al 6061-T6"
MX, MZ = -54.74, 65.0


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def build():
    p = cq.Workplane("XY").circle(63).extrude(18)                                  # base
    p = p.union(box(-40, 40, -36, 36, 18, 65))                                     # tower
    p = p.union(cyl(96, (0, -36, 65), (0, 1, 0), 72))                              # J2 boss
    plate = (cq.Workplane("XZ").workplane(offset=36).center(-56, 65).rect(68, 68)
             .extrude(6).edges("|Y").fillet(6))                                    # Y -42..-36
    p = p.union(plate)
    p = p.union(box(-72, -45.25, 26, 36, 49, 81))                                  # 608 block
    # cuts
    p = p.cut(cyl(58.2, (0, -40, 65), (0, 1, 0), 80))                              # cartridge bore
    p = p.cut(box(-49, -42.74, -36.5, 0, 55.76, 74.25))                            # coupling pocket
    p = p.cut(box(-30, 30, -26, 26, 18, 30))                                       # void (as drawn)
    p = p.cut(cyl(40, (0, 0, -1), (0, 0, 1), 20))                                  # 40 hole base -> void (user decision)
    for x, z in pcd(8, 72, 0):
        p = p.cut(cyl(5, (x, 37, 65 + z), (0, -1, 0), 13))                         # M5 x 12
    p = p.cut(cyl(40, (MX, -43, MZ), (0, 1, 0), 4))                                # pilot recess 40 x 3
    p = p.cut(cyl(10, (MX, -43, MZ), (0, 1, 0), 8))                                # shaft hole 10 through plate
    for dx in (-23.57, 23.57):
        for dz in (-23.57, 23.57):
            p = p.cut(cyl(5, (MX + dx, -43, MZ + dz), (0, 1, 0), 8))
    p = p.cut(cyl(22, (MX, 29, MZ), (0, 1, 0), 8))                                 # 608 seat
    p = p.cut(cyl(10, (MX, 25, MZ), (0, 1, 0), 5))
    for a in (0, 60, 120, 180):
        x, y = 56 * math.cos(math.radians(a)), 56 * math.sin(math.radians(a))
        p = p.cut(cyl(6.6, (x, y, -1), (0, 0, 1), 20))
        p = p.cut(cyl(11, (x, y, 11.5), (0, 0, 1), 7))
    p = p.cut(cyl(12.5, (-52, 26, -1), (0, 0, 1), 20))                             # gland
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])
