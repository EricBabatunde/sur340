"""SUR-031 GRIPPER GEAR LINK L (front) - sheet 130, Steel, laser cut.
See gear_link_common.py.  Teeth phase 4 deg (measured tooth centre 2.23 deg)."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


from gear_link_common import build_link
PART_NO, NAME, MAT = "SUR-031", "GRIPPER_GEAR_LINK_L", "Steel"


def build():
    return build_link(2.23)


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

