"""SUR-015 UPPER ARM (J2 -> J3) - sheet 115, Al 6061-T6.
STATED : centres 180, width 72, 22 thick; J3 2 x seat 42 x 7; 6 x M4 PCD 44 at J2;
         J3 motor seat 60 sq, 4 x M5.  Overall 114.7 x 27 x 252.
MEASURED (sheet 115, 1:5) - origin = J2 axis on the front face (Y0), arm along +Z, thickness +Y:
  outline: R36 at J2 (Z0) and J3 (Z180), straight sides X -36 / +36, motor lobe R40 about
  (X -38.71, Z 141.28) (J3 pinion axis, 54.74 from J3 at 45 deg);
  slot 28 wide, R14 ends at Z52 / Z100, through;
  J2: bore 31 through; 6 x M4 (nominal 4) x 12 from the front face, PCD44 from 0 deg;
  J3: bore 31 through + seat 42 x 7 on both faces;
  motor lobe: pilot 39 through; 4 x M5 (nominal 5) x 10 from the back face at R33.33 on the
  X/Z axes (47.14 sq turned 45 deg);
  2 cable-clip pads 14 x 14 x 5 on the back face (Y22-27) at X21..35, Z93..107 / Z133..147,
  each with M3 (nominal 3) x 6 deep.
  The stated '60 sq' motor seat is not visible in any view (flagged).
"""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, cyl

PART_NO, NAME, MAT = "SUR-015", "UPPER_ARM", "Al 6061-T6"
MX, MZ = -38.71, 141.28


def build():
    a0 = math.radians(273.9)
    a1 = math.radians(86.1)
    p_low = (MX + 40 * math.cos(a0), MZ + 40 * math.sin(a0))     # (-36, 101.4)
    p_up = (MX + 40 * math.cos(a1), MZ + 40 * math.sin(a1))      # (-36, 181.2)
    j3_end = (36 * math.cos(math.radians(178.1)), 180 + 36 * math.sin(math.radians(178.1)))
    prof = (cq.Workplane("XZ").moveTo(-36, 0).threePointArc((0, -36), (36, 0))
            .lineTo(36, 180).threePointArc((0, 216), j3_end)
            .threePointArc((MX - 40, MZ), p_low)
            .close())
    # close(): j3_end -> lobe arc -> p_low -> straight down the left side to (-36, 0)
    p = prof.extrude(-22)                                         # Y 0..22
    slot = cq.Workplane("XZ").center(0, 76).slot2D(76, 28, angle=90).extrude(-30).translate((0, -4, 0))
    p = p.cut(slot)
    p = p.cut(cyl(31, (0, -1, 0), (0, 1, 0), 24))                 # J2 bore
    for x, z in pcd(6, 44, 0):
        p = p.cut(cyl(4, (x, -1, z), (0, 1, 0), 13))              # M4 x 12
    p = p.cut(cyl(31, (0, -1, 180), (0, 1, 0), 24))               # J3 bore
    p = p.cut(cyl(42, (0, -1, 180), (0, 1, 0), 8))                # seat front
    p = p.cut(cyl(42, (0, 15, 180), (0, 1, 0), 8))                # seat back
    p = p.cut(cyl(39, (MX, -1, MZ), (0, 1, 0), 24))               # motor pilot
    for dx, dz in pcd(4, 66.67, 0):
        p = p.cut(cyl(5, (MX + dx, 23, MZ + dz), (0, -1, 0), 11))  # M5 x 10 from back
    for zc in (100, 140):
        p = p.union(cq.Workplane("XY").box(14, 5, 14).translate((28, 24.5, zc)))
        p = p.cut(cyl(3, (28, 28, zc), (0, -1, 0), 7))            # M3 x 6
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])
