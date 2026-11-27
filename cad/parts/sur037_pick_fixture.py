"""SUR-037 PICK FIXTURE - sheet 136, Al 6061-T6.
STATED : 90 x 90 x 10, pin 17.6 x 14, 4 x 6.6.
MEASURED (1:2): corners R6; holes through at (+-34, +-34); pin top chamfer 1.2.
Origin: bottom centre, Z up."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-037", "PICK_FIXTURE", "Al 6061-T6"


def build():
    p = cq.Workplane("XY").rect(90, 90).extrude(10).edges("|Z").fillet(6)
    p = p.faces(">Z").workplane().circle(8.8).extrude(14)
    p = p.faces(">Z").edges().chamfer(1.2)
    p = p.faces("<Z").workplane().rect(68, 68, forConstruction=True).vertices().hole(6.6)
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

