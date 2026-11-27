"""SUR-022 J5 SHAFT (pinned in the wrist) - sheet 122, Steel C45, ground.
STATED : 30 x 37, collar 36 x 1, circlip groove 28.6, motor bore 5, pin hole 4.
MEASURED (1:1): axis along Y (as drawn), Y0..37; collar 36 at Y13-14;
  groove 28.6 x 1.5 at Y34-35.5; motor bore 5 from the Y37 end, 18 deep;
  pin hole 4 through along Z at Y8; M3 set screw hole (nominal 3) along +X at Y30
  from the motor bore to the surface (for SUR-075).
Origin: Y0 end centre."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-022", "J5_SHAFT", "Steel C45"


def build():
    prof = [(0, 0), (15, 0), (15, 13), (18, 13), (18, 14), (15, 14), (15, 34), (14.3, 34),
            (14.3, 35.5), (15, 35.5), (15, 37), (0, 37)]
    p = cq.Workplane("XY").polyline(prof).close().revolve(360, (0, 0, 0), (0, 1, 0))
    p = p.cut(cyl(5, (0, 19, 0), (0, 1, 0), 19))                  # motor bore 5 x 18
    p = p.cut(cyl(4, (0, 8, -16), (0, 0, 1), 32))                 # pin hole 4
    p = p.cut(cyl(3, (2, 30, 0), (1, 0, 0), 15))                  # M3 set screw
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

