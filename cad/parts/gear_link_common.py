"""Shared builder for SUR-030 / SUR-031 gripper gear links (sheets 129/130).
STATED : gear m 1, z 36, 4 thick; arm 36 centres; holes 4.8 and 4; teeth phase 0 / 4 deg.
MEASURED (1:1): tooth form = lib.gear_profile scaled to m1 (half widths 0.182/0.487/0.807,
  root r 16.745); tooth centre angle in the FRONT view: R 6.24 deg, L 2.23 deg (= 4.0 apart);
  4 x 5 lightening holes at (+-7.07, +-7.07) (PCD 20 at 45 deg); arm 9 wide along +X,
  R4.5 end, hole 4 at X36; centre hole 4.8.
Part in the XZ plane as drawn (FRONT view), thickness Y 0..4; origin = gear centre.
"""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import cadquery as cq
from lib.common import pcd, gear_profile


def build_link(phase_deg):
    g = gear_profile(cq.Workplane("XY"), 36, 1.0, phase_deg=phase_deg,
                     hw=(0.182, 0.487, 0.807), r_root=16.745).extrude(4)
    arm = cq.Workplane("XY").center(23, 0).rect(26, 9).extrude(4)
    arm = arm.union(cq.Workplane("XY").center(36, 0).circle(4.5).extrude(4))
    p = g.union(arm)
    p = p.faces(">Z").workplane(origin=(0, 0, 4)).hole(4.8)
    p = p.faces(">Z").workplane(origin=(0, 0, 4)).pushPoints(pcd(4, 20, 45)).hole(5.0)
    p = p.faces(">Z").workplane(origin=(0, 0, 4)).pushPoints([(36, 0)]).hole(4.0)
    # sketch plane XY -> drawing FRONT plane XZ (Y_sketch -> Z), thickness to +Y
    return p.rotate((0, 0, 0), (1, 0, 0), 90).translate((0, 4, 0))
