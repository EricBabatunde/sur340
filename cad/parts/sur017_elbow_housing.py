"""SUR-017 ELBOW HOUSING + forearm root (J3, J4) - sheet 117, Al 6061-T6.
STATED : drum 80 x 84 (bore 56), pivot bore 30, root 64 with 6808 seat 52 x 7,
         J4 drive hole 24, 8 x M4 PCD 64, 6 x M4 PCD 44.  Overall 98 x 84 x 80.
MEASURED (sheet 117, 1:2) - origin = J3 (drum) axis on the front face, drum along +Y:
  drum 80, Y0..84; internal bore 56 Y8..72 (front wall 8, back wall 12);
  pivot bore 30 x 12 from the back face (Y72..84);
  root = cylinder 64 along +X (J4 axis at Y40, Z0), X0..52;
  J4 line: recess 29 x 3 (X-46..-43), drive hole 24 (X-46..-28, into the bore),
  42 (X0..45), 6808 seat 52 x 7 (X45..52);
  motor pad 50 x 50 on -X (X-46.., Y15..65, Z-25..25), 4 x M3 (nominal 3) x 12 on 31 sq;
  8 x M4 (nominal 4) x 10 in the front face, PCD64 at 22.5 + n*45 deg;
  6 x M4 x 10 in the back face, PCD44 from 0 deg.
"""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import cadquery as cq
from lib.common import pcd, cyl

PART_NO, NAME, MAT = "SUR-017", "ELBOW_HOUSING", "Al 6061-T6"


def build():
    p = cyl(80, (0, 0, 0), (0, 1, 0), 84)                                        # drum
    p = p.union(cyl(64, (0, 40, 0), (1, 0, 0), 52))                              # root
    p = p.union(cq.Workplane("XY").box(16, 50, 50).translate((-38, 40, 0)))       # motor pad X-46..-30
    p = p.cut(cyl(56, (0, 8, 0), (0, 1, 0), 64))                                 # internal bore
    p = p.cut(cyl(30, (0, 72, 0), (0, 1, 0), 13))                                # pivot bore
    p = p.cut(cyl(29, (-47, 40, 0), (1, 0, 0), 4))                               # recess 29 x 3
    p = p.cut(cyl(24, (-47, 40, 0), (1, 0, 0), 20))                              # J4 drive hole
    p = p.cut(cyl(42, (0, 40, 0), (1, 0, 0), 45))
    p = p.cut(cyl(52, (45, 40, 0), (1, 0, 0), 8))                                # 6808 seat
    for dy in (-15.5, 15.5):
        for dz in (-15.5, 15.5):
            p = p.cut(cyl(3, (-47, 40 + dy, dz), (1, 0, 0), 13))                 # M3 x 12
    for x, z in pcd(8, 64, 22.5):
        p = p.cut(cyl(4, (x, -1, z), (0, 1, 0), 11))                             # M4 x 10 front
    for x, z in pcd(6, 44, 0):
        p = p.cut(cyl(4, (x, 85, z), (0, -1, 0), 11))                            # M4 x 10 back
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])
