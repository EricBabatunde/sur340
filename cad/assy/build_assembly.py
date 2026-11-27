"""SUR340 assemblies in the home pose (all joints 0 deg) -> STEP AP214 with names + colours.

World frame (sheet 001): origin = floor (base plate underside) on the J1 axis, Z up,
+X toward the reach (pick/place at X 220), +Y = back.  Key positions (all checked against
sheets 001/002/010-016): J2 (0, 0, 192); J3 (0, 0, 372); J4 axis Y0 Z372; J5 (160, 0, 372);
tool flange top Z317 (J5 - 55); grip point (160, 0, 217) (flange - 100).
See ASSEMBLY_NOTES in out/MEASUREMENT_LOG.md for the derivation of each stack.
"""
import sys, math, os, importlib
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad")
sys.path.insert(0, "/home/eric/Documents/projects/sur340/cad/parts")
import cadquery as cq
from lib.common import pcd, color, MAT, OUT_ASSY, write_step
from bought import lib as B

V = cq.Vector


def P(name):
    return importlib.import_module(name)


_part_cache = {}


def part_shape(mod):
    if mod not in _part_cache:
        m = P(mod)
        _part_cache[mod] = (m.build().val().clean(), m.PART_NO, m.NAME, m.MAT)
    return _part_cache[mod]


def loc(origin=(0, 0, 0), xdir=(1, 0, 0), zdir=(0, 0, 1)):
    return cq.Location(cq.Plane(V(*origin), V(*xdir), V(*zdir)))


def sh(x):
    return x.val() if isinstance(x, cq.Workplane) else x


class SA:
    def __init__(self, name):
        self.name = name
        self.a = cq.Assembly(name=name)
        self.n = {}

    def add(self, shape, label, mat, L):
        self.n[label] = self.n.get(label, 0) + 1
        self.a.add(sh(shape).moved(L), name=f"{label}-{self.n[label]}", color=color(mat))
        return sh(shape).moved(L)

    def part(self, mod, L):
        s, pn, nm, mat = part_shape(mod)
        return self.add(s, f"{pn}_{nm}", mat, L)


# bought-out labels
def screw(sa, d, l, origin, zdir, low=False, xdir=None):
    pn = {(6, 20): "SUR-059", (6, 16): "SUR-060", (6, 12): "SUR-061", (5, 12): "SUR-062",
          (5, 20): "SUR-064", (6, 25): "SUR-065", (5, 10): "SUR-067", (5, 16): "SUR-069",
          (4, 12): "SUR-070", (3, 10): "SUR-071", (2.5, 8): "SUR-076", (3, 12): "SUR-079",
          (2, 6): "SUR-080", (3, 8): "SUR-081"}
    lpn = {(4, 16): "SUR-066", (5, 12): "SUR-068", (4, 10): "SUR-074", (4, 12): "SUR-078"}
    p = (lpn if low else pn)[(d, l)]
    std = "DIN7984" if low else "ISO4762"
    xd = xdir or _perp(zdir)
    return sa.add(B.screw(d, l, low), f"{p}_{std}_M{d}x{l}", "black 8.8", loc(origin, xd, zdir))


def setscrew(sa, d, l, origin, zdir):
    p = {(4, 6): "SUR-063", (3, 4): "SUR-072", (3, 16): "SUR-073", (3, 12): "SUR-075", (3, 6): "SUR-077"}[(d, l)]
    return sa.add(B.set_screw(d, l), f"{p}_ISO4026_M{d}x{l}", "set screw", loc(origin, _perp(zdir), zdir))


def _perp(z):
    z = V(*z)
    a = V(1, 0, 0) if abs(z.x) < 0.9 else V(0, 1, 0)
    x = a - z * (a.dot(z) / z.dot(z))
    return (x.x, x.y, x.z)


def bearing(sa, kind, origin, zdir):
    pn = {"61816": "SUR-046", "6806": "SUR-047", "6808": "SUR-048", "608": "SUR-049", "688": "SUR-050"}[kind]
    return sa.add(B.bearing(*B.BEARINGS[kind]), f"{pn}_BEARING_{kind}", "bearing", loc(origin, _perp(zdir), zdir))


def motor(sa, kind, origin, zdir, xdir, shaft, conn_side, conn_axial):
    pn = {"NEMA23": "SUR-039", "NEMA17": "SUR-040", "NEMA11": "SUR-041"}[kind]
    m = sa.add(B.stepper(kind, shaft), f"{pn}_{kind}_MOTOR", "motor", loc(origin, xdir, zdir))
    S = {"NEMA23": 56.4, "NEMA17": 42.3, "NEMA11": 28.2}[kind]
    o, z, s = V(*origin), V(*zdir), V(*conn_side)
    c_or = o + s * (S / 2) + z * conn_axial
    sa.add(B.connector(), "SUR-042_CONNECTOR", "connector", loc((c_or.x, c_or.y, c_or.z), conn_side, zdir))
    return m


def mesh_pinion(sa_shape_gear, pinion_shape, L_of_phi, z):
    """Pick the pinion rotation (about its own axis) with the least overlap with the gear."""
    pitch = 360.0 / z
    best = None
    for i in range(24):
        phi = i * pitch / 24
        p = pinion_shape.moved(L_of_phi(phi))
        try:
            v = sa_shape_gear.intersect(p).Volume()
        except Exception:
            v = 1e9
        if best is None or v < best[0]:
            best = (v, phi)
    return best[1], best[0]


def rot_x(phi, base_x, axis):
    """rotate base_x about axis by phi degrees (Rodrigues)."""
    a = math.radians(phi)
    k, v = V(*axis).normalized(), V(*base_x)
    r = v * math.cos(a) + k.cross(v) * math.sin(a) + k * (k.dot(v) * (1 - math.cos(a)))
    return (r.x, r.y, r.z)


# ===================================================================== SA1 base + J1
def sa1():
    s = SA("SA1_BASE_J1")
    s.part("sur001_base_plate", loc((0, 0, 0)))
    s.part("sur002_base_pedestal", loc((0, 0, 12)))
    bearing(s, "61816", (0, 0, 86), (0, 0, 1))
    s.part("sur004_turntable", loc((0, 0, 82)))
    s.add(B.circlip(80), "SUR-051_CIRCLIP_DIN471_80", "Steel", loc((0, 0, 83.5)))
    ring = s.part("sur003_j1_ring_gear", loc((0, 0, 97)))
    s.part("sur006_j1_motor_bracket", loc((-90.73, 0, 12)))
    motor(s, "NEMA23", (-90.73, 0, 88), (0, 0, 1), (1, 0, 0), 28, (-1, 0, 0), -38)
    pin = part_shape("sur008_drive_pinion")[0]
    Lp = lambda phi: loc((-90.73, 0, 97), rot_x(phi, (1, 0, 0), (0, 0, 1)), (0, 0, 1))
    phi, ov = mesh_pinion(ring, pin, Lp, 17)
    s.part("sur008_drive_pinion", Lp(phi))
    xd = V(*rot_x(phi, (1, 0, 0), (0, 0, 1)))
    o = V(-90.73, 0, 113) + xd * 11
    setscrew(s, 4, 6, (o.x, o.y, o.z), (-xd.x, -xd.y, -xd.z))
    for dx in (-23.57, 23.57):
        for dy in (-23.57, 23.57):
            screw(s, 5, 12, (-90.73 + dx, dy, 82), (0, 0, 1))
    for y in (-48, 48):
        screw(s, 6, 12, (-90.73, y, 18), (0, 0, -1))
    for x in (-88, 88):
        for y in (-88, 88):
            screw(s, 6, 20, (x, y, 5.5), (0, 0, -1))
    for x, y in pcd(6, 140, 30):
        screw(s, 6, 16, (x, y, 19), (0, 0, -1))
    for x, y in pcd(6, 100, 90):
        screw(s, 5, 20, (x, y, 121.5), (0, 0, -1))
    s.add(B.cable_gland(), "SUR-056_CABLE_GLAND_PG7", "gland", loc((0, -57, 53), (1, 0, 0), (0, -1, 0)))
    return s, ov


# ===================================================================== SA2 shoulder + J2
def sa2():
    s = SA("SA2_SHOULDER_J2")
    s.part("sur005_shoulder_housing", loc((0, 0, 127)))
    for a in (0, 60, 120, 180):
        screw(s, 6, 25, (56 * math.cos(math.radians(a)), 56 * math.sin(math.radians(a)), 138.5), (0, 0, -1))
    s.add(B.cable_gland(), "SUR-056_CABLE_GLAND_PG7", "gland", loc((-52, 26, 145)))
    # J2 drive cartridge (sheet 011A)
    s.part("sur007_drive_housing", loc((0, 42, 192), (1, 0, 0), (0, -1, 0)))
    bearing(s, "6806", (0, 14, 192), (0, 1, 0))
    Ls = loc((0, 55, 192), (1, 0, 0), (0, -1, 0))
    s.part("sur012_j2_output_shaft", Ls)
    s.part("sur013_key_4x4x10", Ls * loc((0, 5, 0)))
    s.part("sur011_spacer_j2", loc((0, 21, 192), (1, 0, 0), (0, 1, 0)))
    gear = s.part("sur009_j2_output_gear", loc((0, 45, 192), (-1, 0, 0), (0, 1, 0)))
    for x, y in pcd(8, 72, 0):
        screw(s, 5, 12, (x, 38.4, 192 + y), (0, -1, 0), low=True)
    for x, y in pcd(6, 44, 0):
        screw(s, 4, 16, (-x, 48, 192 + y), (0, 1, 0), low=True)
    s.part("sur014_end_washer", loc((0, 55, 192), (1, 0, 0), (0, 1, 0)))
    screw(s, 5, 10, (0, 58, 192), (0, -1, 0))
    # J2 motor, coupling, pinion shaft, 608, pinion
    MX, MZ = -54.74, 192
    motor(s, "NEMA23", (MX, -42, MZ), (0, 1, 0), (1, 0, 0), 21, (-1, 0, 0), -35)
    for dx in (-23.57, 23.57):
        for dz in (-23.57, 23.57):
            screw(s, 5, 12, (MX + dx, -48, MZ + dz), (0, 1, 0))
    s.add(B.coupling(18, 25, 8, 8), "SUR-044_COUPLING_8x8", "coupling", loc((MX, -30, MZ), (0, 0, 1), (0, 1, 0)))
    for y in (-30 + 6.25, -30 + 18.75):
        setscrew(s, 4, 6, (MX, y, MZ + 10), (0, 0, -1))
    s.part("sur025_pinion_shaft", loc((MX, -17, MZ), (1, 0, 0), (0, 1, 0)))
    bearing(s, "608", (MX, 29, MZ), (0, 1, 0))
    pin = part_shape("sur008_drive_pinion")[0]
    Lp = lambda phi: loc((MX, 43, MZ), rot_x(phi, (1, 0, 0), (0, 1, 0)), (0, 1, 0))
    phi, ov = mesh_pinion(gear, pin, Lp, 17)
    s.part("sur008_drive_pinion", Lp(phi))
    xd = V(*rot_x(phi, (1, 0, 0), (0, 1, 0)))
    o = V(MX, 59, MZ) + xd * 11
    setscrew(s, 4, 6, (o.x, o.y, o.z), (-xd.x, -xd.y, -xd.z))
    return s, ov


# ===================================================================== SA3 upper arm + J3
def sa3():
    s = SA("SA3_UPPER_ARM_J3")
    s.part("sur015_upper_arm", loc((0, 55, 192)))
    bearing(s, "6806", (0, 55, 372), (0, 1, 0))
    bearing(s, "6806", (0, 70, 372), (0, 1, 0))
    s.part("sur016_j3_pivot", loc((0, 32, 372)))
    s.add(B.circlip(30), "SUR-052_CIRCLIP_DIN471_30", "Steel", loc((0, 77.5, 372), (1, 0, 0), (0, 1, 0)))
    gear = s.part("sur010_j3_output_gear", loc((0, 44, 372), (1, 0, 0), (0, 1, 0)))
    for x, y in pcd(6, 44, 0):
        screw(s, 4, 16, (x, 51, 372 - y), (0, -1, 0), low=True)
    MX, MZ = -38.71, 333.28
    c45 = (math.cos(math.radians(45)), 0, math.sin(math.radians(45)))
    s.add(B.stepper("NEMA23", 28), "SUR-039_NEMA23_MOTOR", "motor", loc((MX, 77, MZ), c45, (0, -1, 0)))
    s.add(B.connector(), "SUR-042_CONNECTOR", "connector", loc((MX, 141, MZ), (0, 1, 0), (1, 0, 0)))
    for dx, dz in ((33.33, 0), (-33.33, 0), (0, 33.33), (0, -33.33)):
        screw(s, 5, 16, (MX + dx, 83, MZ + dz), (0, -1, 0))
    pin = part_shape("sur008_drive_pinion")[0]
    Lp = lambda phi: loc((MX, 42, MZ), rot_x(phi, (1, 0, 0), (0, 1, 0)), (0, 1, 0))
    phi, ov = mesh_pinion(gear, pin, Lp, 17)
    s.part("sur008_drive_pinion", Lp(phi))
    xd = V(*rot_x(phi, (1, 0, 0), (0, 1, 0)))
    o = V(MX, 58, MZ) + xd * 11
    setscrew(s, 4, 6, (o.x, o.y, o.z), (-xd.x, -xd.y, -xd.z))
    for zc in (292, 332):
        s.part("sur035_cable_clip", loc((14, 82, zc + 4), (1, 0, 0), (0, 1, 0)))
        screw(s, 3, 8, (28, 84.5, zc), (0, -1, 0))
    return s, ov


# ===================================================================== SA4 elbow + J4
def sa4():
    s = SA("SA4_ELBOW_J4")
    s.part("sur017_elbow_housing", loc((0, -40, 372)))
    s.part("sur018_elbow_cap", loc((0, -46, 372)))
    for x, z in pcd(8, 64, 22.5):
        screw(s, 4, 12, (x, -46, 372 + z), (0, 1, 0))
    motor(s, "NEMA17", (-46, 0, 372), (1, 0, 0), (0, 1, 0), 22, (0, 0, 1), -24)
    for dy in (-15.5, 15.5):
        for dz in (-15.5, 15.5):
            screw(s, 3, 10, (-52, dy, 372 + dz), (1, 0, 0))
    s.add(B.coupling(16, 25, 5, 8), "SUR-045_COUPLING_5x8", "coupling", loc((-34, 0, 372), (0, 0, 1), (1, 0, 0)))
    for x in (-34 + 6.25, -34 + 18.75):
        setscrew(s, 3, 4, (x, 0, 380), (0, 0, -1))
    s.part("sur020_j4_drive_shaft", loc((-21, 0, 372)))
    setscrew(s, 3, 16, (25, 0, 392), (0, 0, -1))
    bearing(s, "6808", (45, 0, 372), (1, 0, 0))
    s.part("sur019_j4_shaft", loc((20, 0, 372)))
    s.add(B.v_ring(66, 44, 6), "SUR-057_ROLL_RING", "rubber", loc((52, 0, 372), (0, 1, 0), (1, 0, 0)))
    for y, z in pcd(6, 34, 0):
        screw(s, 4, 16, (55, y, 372 + z), (1, 0, 0), low=True)
    return s


# ===================================================================== SA5 forearm + J5
def sa5():
    s = SA("SA5_FOREARM_J5")
    s.part("sur021_forearm", loc((58, 0, 372)))
    bearing(s, "6806", (160, 24, 372), (0, 1, 0))
    bearing(s, "6806", (160, 37, 372), (0, 1, 0))
    s.part("sur022_j5_shaft", loc((160, 10, 372)))
    s.add(B.circlip(30), "SUR-052_CIRCLIP_DIN471_30", "Steel", loc((160, 44, 372), (1, 0, 0), (0, 1, 0)))
    s.part("sur023_j5_motor_plate", loc((160, 44, 372)))
    for dx in (-18, 18):
        for dz in (-18, 18):
            screw(s, 4, 10, (160 + dx, 46, 372 + dz), (0, -1, 0), low=True)
    c45 = (math.cos(math.radians(45)), 0, math.sin(math.radians(45)))
    motor(s, "NEMA17", (160, 49, 372), (0, -1, 0), c45, 18, (-0.7071068, 0, 0.7071068), -24)
    for dx, dz in ((21.92, 0), (-21.92, 0), (0, 21.92), (0, -21.92)):
        screw(s, 3, 10, (160 + dx, 55, 372 + dz), (0, -1, 0))
    setscrew(s, 3, 12, (175, 40, 372), (-1, 0, 0))
    s.add(B.dowel(4, 48), "SUR-026_DOWEL_4x48", "Steel", loc((160, 18, 357)))
    s.part("sur035_cable_clip", loc((104, 20, 402), (0, 1, 0), (0, 0, 1)))
    screw(s, 3, 8, (100, 34, 404.5), (0, 0, -1))
    s.add(B.cable_gland(), "SUR-056_CABLE_GLAND_PG7", "gland", loc((122, 34, 402)))
    return s


# ===================================================================== SA6 wrist + J6 + flange
def sa6():
    s = SA("SA6_WRIST_J6_FLANGE")
    s.part("sur024_wrist_housing", loc((160, -23, 372)))
    bearing(s, "688", (160, 0, 323), (0, 0, 1))
    s.add(B.v_ring(54, 8.5, 6), "SUR-058_J6_RING", "rubber", loc((160, 0, 317)))
    s.part("sur028_tool_flange", loc((160, 0, 309)))
    for x, y in pcd(6, 36, 90):
        screw(s, 4, 12, (160 + x, y, 314), (0, 0, -1), low=True)
    setscrew(s, 3, 6, (170, 0, 313), (-1, 0, 0))
    s.part("sur027_j6_shaft", loc((160, 0, 309)))
    s.add(B.coupling(16, 25, 8, 5), "SUR-045_COUPLING_5x8", "coupling", loc((160, 0, 372)))
    for z in (372 + 6.25, 372 + 18.75):
        setscrew(s, 3, 4, (164.0 + 4.0, 0, z), (-1, 0, 0))
    motor(s, "NEMA11", (160, 0, 403), (0, 0, -1), (1, 0, 0), 18, (1, 0, 0), -24)
    for dx in (-11.5, 11.5):
        for dy in (-11.5, 11.5):
            screw(s, 2.5, 8, (160 + dx, dy, 407), (0, 0, -1))
    return s


# ===================================================================== SA7 gripper
def sa7():
    s = SA("SA7_GRIPPER")
    s.part("sur029_gripper_body", loc((160, 0, 309)))
    s.part("sur034_servo_bracket", loc((162, -30, 265)))
    for x in (168, 188):
        screw(s, 3, 12, (x, -27, 304), (0, 1, 0))
    s.add(B.micro_servo(), "SUR-043_MICRO_SERVO", "servo", loc((178, -50.7, 280), (-1, 0, 0), (0, 1, 0)))
    for x in (169.4, 197.6):
        screw(s, 2, 6, (x, -32.5, 280), (0, 1, 0))

    def link(mod, ang, at, flip=False):
        sh0 = part_shape(mod)[0]
        if flip:   # turned over about its arm axis (needed for the drawn tooth phases to mesh)
            sh0 = sh0.rotate((0, 0, 0), (1, 0, 0), 180)
        sh0 = sh0.rotate((0, 0, 0), (0, 1, 0), ang)
        pn, nm, mat = part_shape(mod)[1:]
        return s.add(sh0, f"{pn}_{nm}", mat, loc(at))
    gR = link("sur030_gripper_gear_link_r", 63.6, (178, -22, 280), flip=True)
    gL = link("sur031_gripper_gear_link_l", 116.4, (142, -26, 280))
    link("sur032_gripper_link", 116.4, (142, 22, 268))
    link("sur032_gripper_link", 63.6, (178, 22, 268))
    s.part("sur033_gripper_finger", loc((134, 16, 205.8), (-1, 0, 0), (0, 0, 1)))
    s.part("sur033_gripper_finger", loc((186, -16, 205.8)))
    for x in (126, 194):
        s.add(B.clevis_pin(4, 42), "SUR-053_PIN_4x42", "Steel", loc((x, -26, 247.8), (1, 0, 0), (0, 1, 0)))
        s.add(B.clevis_pin(4, 42), "SUR-053_PIN_4x42", "Steel", loc((x, 26, 235.8), (1, 0, 0), (0, -1, 0)))
    s.add(B.clevis_pin(4, 48), "SUR-055_PIN_4x48", "Steel", loc((142, -26, 280), (1, 0, 0), (0, 1, 0)))
    s.add(B.clevis_pin(4, 44), "SUR-054_PIN_4x44", "Steel", loc((178, 22, 280), (1, 0, 0), (0, -1, 0)))
    for x in (142, 178):
        s.add(B.clevis_pin(4, 48), "SUR-055_PIN_4x48", "Steel", loc((x, 26, 268), (1, 0, 0), (0, -1, 0)))
    try:
        ov = gR.intersect(gL).Volume()
    except Exception:
        ov = -1
    return s, ov


def workcell_parts():
    s = SA("WORKCELL_FIXTURES")
    s.part("sur037_pick_fixture", loc((220, -150, 0)))
    s.part("sur036_package", loc((220, -150, 10)))
    s.part("sur038_place_fixture", loc((220, 150, 0)))
    for x in (-34, 34):
        for y in (-34, 34):
            screw(s, 6, 16, (220 + x, -150 + y, 10), (0, 0, -1))
            screw(s, 6, 16, (220 + x, 150 + y, 16), (0, 0, -1))
    return s


def main():
    os.makedirs(OUT_ASSY, exist_ok=True)
    s1, ov1 = sa1()
    s2, ov2 = sa2()
    s3, ov3 = sa3()
    s4, s5, s6 = sa4(), sa5(), sa6()
    s7, ov7 = sa7()
    print(f"pinion overlaps (mm^3): J1 {ov1:.3f}  J2 {ov2:.3f}  J3 {ov3:.3f};  gripper gears {ov7:.3f}")
    subs = [s1, s2, s3, s4, s5, s6, s7]
    for sa in subs:
        write_step(sa.a, f"{OUT_ASSY}/{sa.name}.step")
        print("wrote", sa.name, sum(sa.n.values()), "parts")
    robot = cq.Assembly(name="SUR340_ROBOT")
    for sa in subs:
        robot.add(sa.a, name=sa.name)
    write_step(robot, f"{OUT_ASSY}/SUR340_ROBOT.step")
    wc = workcell_parts()
    cell = cq.Assembly(name="SUR340_WORKCELL")
    cell.add(robot, name="SUR340_ROBOT")
    cell.add(wc.a, name=wc.name)
    write_step(cell, f"{OUT_ASSY}/SUR340_WORKCELL.step")
    # part counts for the BOM check
    counts = {}
    for sa in subs + [wc]:
        for k, v in sa.n.items():
            counts[k] = counts.get(k, 0) + v
    with open(f"{OUT_ASSY}/part_counts.txt", "w") as f:
        for k in sorted(counts):
            f.write(f"{k:45s} {counts[k]}\n")
    print("robot parts:", sum(sum(sa.n.values()) for sa in subs), " cell:", sum(counts.values()))


if __name__ == "__main__":
    main()
