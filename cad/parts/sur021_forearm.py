"""SUR-021 FOREARM (J4 roll -> J5) - sheet 121, Al 6061-T6.
STATED : J3 -> J5 160, collar 58, root box 42 x 70 x 52, plate 60 x 20, J5 2 x seat 42 x 7,
         4 x M4 for the motor plate.  Overall 132 x 73 x 60.
MEASURED (sheet 121, 1:2), drawing coords (X0 = collar face, Y0 = front, Z0 = bottom):
  collar 58, X0..18, axis (Y29, Z30) = J4 axis; 6 x M4 (nominal 4) x 15 on PCD34 (first at +-Y);
  root box X18..60, Y3..73, Z4..56, R8 on the 4 edges along X; top pocket X24..44, Y11..47,
  12 deep;  plate = stadium in XZ, centres X42 / X102 at Z30, R30, Y53..73;
  J5 axis X102, Z30 along Y: bore 31 through + seat 42 x 7 on both faces;
  4 x M4 x 12 from the back face (Y73) at X102+-18, Z30+-18;
  cable slot R11, centres X54 / X68 at Z30, through the plate (Y53..73);
  PG7 gland hole 12.5 x 10 deep at X64, Y63 from the top (Z60);
  M3 (nominal 3) x 8 at X42, Y63 from the top (cable clip).
Part origin: J4 axis on the collar face (drawing point X0, Y29, Z30).
"""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import cadquery as cq
from lib.common import pcd, cyl

PART_NO, NAME, MAT = "SUR-021", "FOREARM", "Al 6061-T6"


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def build():
    p = cyl(58, (0, 29, 30), (1, 0, 0), 18)                                       # collar
    p = p.union(box(18, 60, 3, 73, 4, 56).edges("|X").fillet(8))                  # root box
    plate = cq.Workplane("XZ").workplane(offset=-53).center(72, 30).slot2D(120, 60).extrude(-20)
    p = p.union(plate)                                                            # Y53..73
    p = p.cut(box(24, 44, 11, 47, 44, 57))                                        # pocket
    p = p.cut(cyl(31, (102, 50, 30), (0, 1, 0), 26))                              # J5 bore
    p = p.cut(cyl(42, (102, 52, 30), (0, 1, 0), 8))                               # seat Y53..60
    p = p.cut(cyl(42, (102, 66, 30), (0, 1, 0), 8))                               # seat Y66..73
    for dx in (-18, 18):
        for dz in (-18, 18):
            p = p.cut(cyl(4, (102 + dx, 74, 30 + dz), (0, -1, 0), 13))            # M4 x 12
    slot = cq.Workplane("XZ").workplane(offset=-50).center(61, 30).slot2D(36, 22).extrude(-26)
    p = p.cut(slot)                                                               # cable slot
    p = p.cut(cyl(12.5, (64, 63, 61), (0, 0, -1), 11))                            # PG7 x 10
    p = p.cut(cyl(3, (42, 63, 61), (0, 0, -1), 9))                                # M3 x 8
    for y, z in pcd(6, 34, 0):
        p = p.cut(cyl(4, (-1, 29 + y, 30 + z), (1, 0, 0), 16))                    # M4 x 15
    return p.translate((0, -29, -30))


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])
