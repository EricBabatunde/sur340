"""SUR-024 WRIST HOUSING (J5, carries J6) - sheet 124, Al 6061-T6.
STATED : hub 58 x 46, neck 48 x 46 x 49, J5 shaft bore 30, J6 motor pad, 688 seat 16 x 5.
         Overall 58 x 46 x 80.
MEASURED (sheet 124, 1:2), drawing coords (Z0 = bottom, Y0 = front face):
  hub 58 along Y (Y0..46), J5 axis at Z49;  neck X+-24, Z0..49, R5 on the two bottom edges;
  J5 bore 30 x 13 deep from the back (Y33..46), 20 through to the front;
  dowel hole 4 vertical at X0, Y41, from the hub top (Z78) down to Z34;
  window X+-15, Z11..33, through in Y;
  J6 pad X+-15, Y8..38, up to Z80; pilot recess 23 x 2; bore 18 down to the window (Z33);
  4 x M2.5 (nominal 2.5) x 8 on 23 sq; 688 seat 16 x 5 in the bottom face; 10 from the seat
  to the window (Z5..11).  J6 axis X0, Y23.
Part origin: J5 axis on the front face (drawing point X0, Y0, Z49).
"""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import cadquery as cq
from lib.common import cyl

PART_NO, NAME, MAT = "SUR-024", "WRIST_HOUSING", "Al 6061-T6"


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def build():
    neck = box(-24, 24, 0, 46, 0, 49).edges("|Y and <Z").fillet(5)
    p = neck.union(cyl(58, (0, 0, 49), (0, 1, 0), 46))                           # hub
    p = p.union(box(-15, 15, 8, 38, 60, 80))                                      # J6 pad
    p = p.cut(cyl(30, (0, 33, 49), (0, 1, 0), 14))                                # J5 bore 30 x 13
    p = p.cut(cyl(20, (0, -1, 49), (0, 1, 0), 35))                                # 20 through
    p = p.cut(box(-15, 15, -1, 47, 11, 33))                                       # window
    p = p.cut(cyl(4, (0, 41, 81), (0, 0, -1), 47))                                # dowel hole
    p = p.cut(cyl(23, (0, 23, 78), (0, 0, 1), 3))                                 # pilot recess
    p = p.cut(cyl(18, (0, 23, 32), (0, 0, 1), 47))                                # bore 18
    for dx in (-11.5, 11.5):
        for dy in (-11.5, 11.5):
            p = p.cut(cyl(2.5, (dx, 23 + dy, 81), (0, 0, -1), 9))                 # M2.5 x 8
    p = p.cut(cyl(16, (0, 23, -1), (0, 0, 1), 6))                                 # 688 seat
    p = p.cut(cyl(10, (0, 23, -1), (0, 0, 1), 13))
    return p.translate((0, 0, -49))


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])
