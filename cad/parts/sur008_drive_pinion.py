"""SUR-008 DRIVE PINION (J1, J2, J3) - sheet 108, Steel 42CrMo4.
STATED : m 1.5, z 17, pitch dia 25.5, width 12, hub 22 x 8, bore 8, M4 set screw.
MEASURED (1:1): teeth z0-12, hub 22 z12-20 on top, bore 8 through,
  M4 set screw hole (nominal 4) radial along +X at z16; tooth form per lib.gear_profile.
Origin: bottom centre, Z up."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-008", "DRIVE_PINION", "Steel 42CrMo4"


def build():
    p = gear_profile(cq.Workplane("XY"), 17, 1.5).extrude(12)
    p = p.faces(">Z").workplane().circle(11).extrude(8)          # hub
    p = p.faces(">Z").workplane().hole(8)                        # bore
    ss = cq.Workplane("YZ").workplane(offset=3).center(0, 16).circle(2).extrude(10)
    return p.cut(ss)                                             # M4 set screw hole


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

