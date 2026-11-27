"""SUR-002 BASE PEDESTAL - sheet 102, Al 6061-T6 (turned).
STATED : flange 160, body 114, top 120, height 84; bearing seat 100.2 x 10;
         6 x 6.6 spot face 11.5 on PCD 140.
MEASURED (sheet 102, 1:2): flange 160 x 4 + 45deg-ish taper to R75 at z7 (5 x 3),
  cone R75 z7 -> R57 z10; body to z78; collar 120 z78-84; bore 80 through,
  90 from z68 to 74; spot faces flat at z7; holes start at +Y (90 deg);
  PG7 gland hole 12.5 on -Y wall at z41 (Y -57, matches sheet 002 "gland at Y-58").
Origin: bottom centre, Z up."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-002", "BASE_PEDESTAL", "Al 6061-T6"


def build():
    prof = [(0, 0), (80, 0), (80, 4), (75, 7), (57, 10), (57, 78), (60, 78), (60, 84), (0, 84)]
    p = cq.Workplane("XZ").polyline(prof).close().revolve(360, (0, 0, 0), (0, 1, 0))
    p = p.faces(">Z").workplane().hole(100.2, 10)                 # bearing seat
    p = p.faces(">Z").workplane(offset=-10).hole(90, 6)           # step
    p = p.faces("<Z").workplane().hole(80)                       # bore through
    sf = cq.Workplane("XY").workplane(offset=7).pushPoints(pcd(6, 140, 90)).circle(11.5 / 2).extrude(10)
    p = p.cut(sf)                                                # spot faces at z7
    p = p.faces("<Z").workplane().pushPoints([(x, -y) for x, y in pcd(6, 140, 90)]).hole(6.6, 10)
    p = p.cut(cyl(12.5, (0, -35, 41), (0, -1, 0), 30))                                                # PG7 gland hole, -Y wall
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

