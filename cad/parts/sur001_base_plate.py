"""SUR-001 BASE PLATE - sheet 101, Al 6061-T6.

STATED : 220 x 220 x 12, R16; 4 x 6.6 cbore 11 x 6.5 on 176 sq; 6 x M6 on PCD 140;
         2 x M6 for the J1 bracket.
MEASURED (sheet 101, 1:5):
  - 1 x 45 deg chamfer on the top perimeter edge (FRONT/LEFT, TOP inner arc R15)
  - PCD 140 holes at 30/90/150/210/270/330 deg (holes at +-Y on the axis)
  - J1 bracket holes M6 at X = -90.73, Y = +-48.0  (origin = plate centre)
  - M6 holes through (12)
Origin: centre of the bottom face, Z up.
"""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import cadquery as cq
from lib.common import pcd

PART_NO, NAME, MAT = "SUR-001", "BASE_PLATE", "Al 6061-T6"


def build():
    p = (cq.Workplane("XY").rect(220, 220).extrude(12)          # base extrude
         .edges("|Z").fillet(16))                                 # R16 corners
    top = p.faces(">Z").workplane(origin=(0, 0, 12))
    p = top.rect(176, 176, forConstruction=True).vertices().cboreHole(6.6, 11.0, 6.5)
    p = p.faces(">Z").workplane(origin=(0, 0, 12)).pushPoints(pcd(6, 140, 30)).hole(6.0)
    p = p.faces(">Z").workplane(origin=(0, 0, 12)).pushPoints([(-90.73, 48.0), (-90.73, -48.0)]).hole(6.0)
    p = p.faces(">Z").edges("not %CIRCLE").chamfer(1.0)          # top perimeter chamfer
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])
