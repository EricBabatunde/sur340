"""SUR-016 J3 PIVOT - sheet 116, Steel C45, ground.
STATED : 30 h6 / 16 x 48, circlip groove 28.6.
MEASURED (1:1): axis along Y (as drawn), Y 0..48; groove 28.6 x 1.5 wide at Y 45.5-47.0.
Origin: -Y end centre."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-016", "J3_PIVOT", "Steel C45"


def build():
    prof = [(8, 0), (15, 0), (15, 45.5), (14.3, 45.5), (14.3, 47), (15, 47), (15, 48), (8, 48)]
    # revolve profile (r, y) about the Y axis
    return cq.Workplane("XY").polyline(prof).close().revolve(360, (0, 0, 0), (0, 1, 0))


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

