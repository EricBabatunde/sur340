"""SUR-003 J1 RING GEAR - sheet 103, Brass CuZn39Pb3.
STATED : m 1.5, z 104, pitch dia 156, width 10, bore 92, 6 x M5 on PCD 100.
MEASURED: tip 159 (overall), root dia 152.25, tooth form per lib.gear_profile;
  M5 holes drawn at nominal 5.0, through, first hole at +Y (90 deg).
Origin: bottom centre, Z up."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-003", "J1_RING_GEAR", "Brass CuZn39Pb3"


def build():
    p = gear_profile(cq.Workplane("XY"), 104, 1.5).extrude(10)
    p = p.faces(">Z").workplane().hole(92)
    p = p.faces(">Z").workplane().pushPoints(pcd(6, 100, 90)).hole(5.0)
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

