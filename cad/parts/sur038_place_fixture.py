"""SUR-038 PLACE FIXTURE - sheet 137, Al 6061-T6.
STATED : 90 x 90 x 22, pocket 36.5 x 12, 4 x 6.6 cb 11 x 6.
MEASURED (1:2): corners R6; holes at (+-34, +-34), counterbore from the top.
Origin: bottom centre, Z up."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-038", "PLACE_FIXTURE", "Al 6061-T6"


def build():
    p = cq.Workplane("XY").rect(90, 90).extrude(22).edges("|Z").fillet(6)
    p = p.faces(">Z").workplane().hole(36.5, 12)
    p = p.faces(">Z").workplane().rect(68, 68, forConstruction=True).vertices().cboreHole(6.6, 11, 6)
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

