"""SUR-004 TURNTABLE - sheet 104, Al 6061-T6.
STATED : disc 152 x 14, spigot 116 x 6, hub 88, journal 80 (61816), circlip groove 76.5;
         6 x 5.5 cb 9.5 PCD 100; 6 x M6 PCD 112.
MEASURED (1:2): journal 80 x 14 (z0-14), hub 88 (z14-25), spigot (z25-31), disc (z31-45);
  groove 76.5 x 2.5 wide at z1.5-4.0; top edge chamfer 1.5; bore 40 through;
  cbore 9.5 depth 5.5 from top, PCD100 holes start +Y; M6 (nominal 6) through z25-45,
  PCD112 holes start +X (they break out of the spigot wall, as drawn).
Origin: journal end centre (bottom), Z up (disc on top)."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import math
import cadquery as cq
from lib.common import pcd, gear_profile, cyl


PART_NO, NAME, MAT = "SUR-004", "TURNTABLE", "Al 6061-T6"


def build():
    prof = [(0, 0), (40, 0), (40, 14), (44, 14), (44, 25), (58, 25), (58, 31), (76, 31), (76, 45), (0, 45)]
    p = cq.Workplane("XZ").polyline(prof).close().revolve(360, (0, 0, 0), (0, 1, 0))
    g = cq.Workplane("XZ").polyline([(38.25, 1.5), (41, 1.5), (41, 4), (38.25, 4)]).close().revolve(360, (0, 0, 0), (0, 1, 0))
    p = p.cut(g)                                                  # circlip groove
    p = p.faces(">Z").workplane().hole(40)                        # bore
    p = p.faces(">Z").workplane().pushPoints(pcd(6, 100, 90)).cboreHole(5.5, 9.5, 5.5)
    p = p.faces(">Z").workplane().pushPoints(pcd(6, 112, 0)).hole(6.0, 20)
    p = p.faces(">Z").edges("%CIRCLE").edges(cq.selectors.RadiusNthSelector(-1)).chamfer(1.5)
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])

