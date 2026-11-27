"""SUR-006 J1 MOTOR BRACKET - sheet 106, Al 6061-T6, 6 mm.
STATED : U bracket 64 x 112 x 82, 6 mm; pilot 40; 4 x M5 on 47.14 sq; 2 x 6.6 in the feet.
MEASURED (1:2): top plate X -34..30 (motor axis 2 mm off the plate centre, as drawn),
  Y -40..40, Z 76..82; walls X -15..15, Y +-(34..40), Z 0..76; feet X -15..15,
  Y +-(40..56), Z 0..6 with 6.6 holes at Y +-48.
Origin: motor axis, bottom (feet underside) at Z0."""
import sys
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
import cadquery as cq
from lib.common import cyl

PART_NO, NAME, MAT = "SUR-006", "J1_MOTOR_BRACKET", "Al 6061-T6"


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def build():
    # U profile in YZ, extruded 30 in X, then the wider top plate
    prof = [(-56, 0), (-34, 0), (-34, 76), (34, 76), (34, 0), (56, 0), (56, 6), (40, 6),
            (40, 82), (-40, 82), (-40, 6), (-56, 6)]
    p = cq.Workplane("YZ").workplane(offset=-15).polyline(prof).close().extrude(30)
    p = p.union(box(-34, 30, -40, 40, 76, 82))
    p = p.cut(cyl(40, (0, 0, 70), (0, 0, 1), 20))
    for dx in (-23.57, 23.57):
        for dy in (-23.57, 23.57):
            p = p.cut(cyl(5, (dx, dy, 70), (0, 0, 1), 20))
    for y in (-48, 48):
        p = p.cut(cyl(6.6, (0, y, -1), (0, 0, 1), 8))
    return p


if __name__ == "__main__":
    from lib.common import export_part
    print(export_part(build(), PART_NO, NAME, MAT)[0])
