"""SUR-030 GRIPPER GEAR LINK R (front, on the servo) - sheet 129, Steel, laser cut.
See gear_link_common.py.  Teeth phase 0 deg (measured tooth centre 6.24 deg)."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


from gear_link_common import build_link
PART_NO, NAME, MAT = "SUR-030", "GRIPPER_GEAR_LINK_R", "Steel"


def build():
    return build_link(6.24)


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

