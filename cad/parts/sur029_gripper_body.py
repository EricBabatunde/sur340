"""SUR-029 GRIPPER BODY (parallel gripper) - sheet 128, Al 6061-T6.
STATED : 68 x 44 x 48, bay 54 x 31, 4 pivot holes 4, 6 x M4 PCD 36, 2 x M3 front.
MEASURED (sheet 128, 1:1), drawing coords (X0 left, Y0 front, Z0 bottom):
  block 68 x 44 x 48, R3 on the 4 edges along Y;
  bays 54 x 31 (X7..61, Z3..34) 16 deep from the front AND the back face (web Y16..28);
  4 pivot holes 4 through the web at X16 / X52, Z7 / Z19;
  6 x M4 (nominal 4) x 8 in the top face on PCD36 about (X34, Y22), first at +Y;
  2 x M3 (nominal 3) x 8 in the front face at X42 / X62, Z43.
Part origin: top face centre (drawing point X34, Y22, Z48).
"""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import cadquery as cq
from lib.common import pcd, cyl

PART_NO, NAME, MAT = "SUR-029", "GRIPPER_BODY", "Al 6061-T6"


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def build():
    p = box(0, 68, 0, 44, 0, 48).edges("|Y").fillet(3)
    p = p.cut(box(7, 61, -1, 16, 3, 34))                                          # front bay
    p = p.cut(box(7, 61, 28, 45, 3, 34))                                          # back bay
    for x in (16, 52):
        for z in (7, 19):
            p = p.cut(cyl(4, (x, 15, z), (0, 1, 0), 14))                          # pivot holes
    for dx, dy in pcd(6, 36, 90):
        p = p.cut(cyl(4, (34 + dx, 22 + dy, 49), (0, 0, -1), 9))                  # M4 x 8
    for x in (42, 62):
        p = p.cut(cyl(3, (x, -1, 43), (0, 1, 0), 9))                              # M3 x 8
    return p.translate((-34, -22, -48))


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])
