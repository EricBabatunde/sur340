"""SUR-007 DRIVE HOUSING (J2 drive cartridge) - sheet 107, Steel S355 (turned).
STATED : flange 84 x 6, body 58 x 22, seat 42 H7 x 7, 8 x 5.5 cb 10 x 3.6 on PCD 72.
MEASURED (1:2): bore 30 through (z0-21), seat 42 from top (z21-28);
  counterbores on the flange underside (z0-3.6); PCD72 holes start +X.
Origin: flange underside centre, Z up."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-007", "DRIVE_HOUSING", "Steel S355"


def build():
    prof = [(0, 0), (42, 0), (42, 6), (29, 6), (29, 28), (0, 28)]
    p = cq.Workplane("XZ").polyline(prof).close().revolve(360, (0, 0, 0), (0, 1, 0))
    p = p.faces(">Z").workplane().hole(42, 7)                     # bearing seat 42 H7
    p = p.faces("<Z").workplane().hole(30)                        # bore
    p = p.faces("<Z").workplane().pushPoints([(x, -y) for x, y in pcd(8, 72, 0)]).cboreHole(5.5, 10, 3.6, 6)
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

