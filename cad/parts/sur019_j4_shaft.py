"""SUR-019 J4 SHAFT (J4 roll shaft, bolted to the forearm) - sheet 119, Steel C45.
STATED : 40 x 32 in 6808, flange 44 x 6, bore 24, drive hole 8, 6 x 4.5 cb 8 PCD 34.
MEASURED (1:1): axis along X (as drawn): body 40 X0-32, flange 44 X32-38;
  bore 24 from the flange end, 28 deep (X10-38); drive hole 8 X0-10;
  M3 set screw hole (nominal 3) radial from +Z at X5 into the drive hole (for SUR-073);
  PCD34 holes in the YZ plane, first at +-Y; 4.5 through the flange X35-38,
  counterbore 8 drilled from the X0 (LEFT view) end down to X35, so the DIN 7984 screws can be
  fitted from that side (user decision 2026-11-27; the sheet draws the counterbore 8 x 3 at X32-35,
  buried under the 40 body). It breaks out of the 40 journal as 6 shallow grooves.
Origin: X0 end centre."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-019", "J4_SHAFT", "Steel C45"


def build():
    p = cq.Workplane("YZ").circle(20).extrude(32)
    p = p.union(cq.Workplane("YZ").workplane(offset=32).circle(22).extrude(6))
    p = p.cut(cyl(24, (10, 0, 0), (1, 0, 0), 29))                 # bore 24
    p = p.cut(cyl(8, (-1, 0, 0), (1, 0, 0), 11.5))                # drive hole 8
    p = p.cut(cyl(3, (5, 0, 3), (0, 0, 1), 20))                   # M3 set screw
    for y, z in pcd(6, 34, 0):
        p = p.cut(cyl(8, (-1, y, z), (1, 0, 0), 36))              # counterbore 8 from the X0 end to X35
        p = p.cut(cyl(4.5, (35, y, z), (1, 0, 0), 4))
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

