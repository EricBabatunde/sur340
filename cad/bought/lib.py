"""Simplified bought-out / standard parts for the SUR340 assembly (SUR-026, 039..081).

All are envelope models to catalogue sizes, built along +Z from Z0 unless noted:
  * motors: front face at Z0, body toward -Z, shaft toward +Z.
  * screws: head bearing face at Z0, head toward -Z, shank toward +Z.
  * bearings / rings / circlips: Z0..B, centred on the axis.
Sizes measured from the assembly sheets where the catalogue leaves them open
(motor lengths: NEMA23 56 + 8 cap (sheet 011), NEMA17 48 (sheet 013), NEMA11 38 (sheet 015)).
"""
import math, functools
import cadquery as cq


def _cyl(d, h, z0=0.0):
    return cq.Workplane("XY").workplane(offset=z0).circle(d / 2).extrude(h)


def _ring(od, id_, h, z0=0.0):
    return cq.Workplane("XY").workplane(offset=z0).circle(od / 2).circle(id_ / 2).extrude(h)


def _csq(s, c, h, z0=0.0):
    """square s with 45 deg corner chamfers c, extruded h from z0."""
    a = s / 2
    pts = [(a - c, -a), (a, -a + c), (a, a - c), (a - c, a), (-a + c, a), (-a, a - c), (-a, -a + c), (-a + c, -a)]
    return cq.Workplane("XY").workplane(offset=z0).polyline(pts).close().extrude(h)


# ------------------------------------------------------------------ motors
@functools.lru_cache(None)
def stepper(kind, shaft_len):
    """NEMA stepper. Front face Z0; flange (with screw holes) -> relieved round neck (room for
    screw heads) -> body -> rear cap; pilot boss and shaft toward +Z."""
    P = {   # S, chamfer, flange t, neck d, neck l, body to, cap S, cap l, pilot d, shaft d, hole pitch, hole d
        "NEMA23": (56.4, 4.0, 6.0, 56.0, 10.0, 56.0, 46.7, 8.0, 38.1, 8.0, 47.14, 5.2),
        "NEMA17": (42.3, 3.8, 6.0, 38.0, 8.0, 40.0, 40.0, 8.0, 22.0, 5.0, 31.0, 3.2),
        "NEMA11": (28.2, 2.5, 4.0, 26.0, 6.0, 32.0, 26.0, 6.0, 22.0, 5.0, 23.0, 2.7),
    }[kind]
    S, c, tf, dn, ln, Lb, Sc, Lc, dp, ds, hp, hd = P
    m = _csq(S, c, tf, -tf)                                         # flange
    m = m.union(_cyl(dn, ln, -tf - ln))                             # relieved neck
    m = m.union(_csq(S, c, Lb - tf - ln, -Lb))                      # body
    m = m.union(_csq(Sc, c, Lc, -Lb - Lc))                          # rear cap
    m = m.union(_cyl(dp, 1.6))                                      # pilot boss
    m = m.union(_cyl(ds, shaft_len, 1.6))                           # shaft
    h = hp / 2
    m = m.cut(cq.Workplane("XY").workplane(offset=-tf - 1).pushPoints(
        [(h, h), (-h, h), (h, -h), (-h, -h)]).circle(hd / 2).extrude(tf + 2))
    return m


@functools.lru_cache(None)
def connector():
    """SUR-042 motor connector: 14 (along the motor axis) x 16 x 10 block + 8 x 8 x 6 plug.
    Mounting face at X0, protrudes toward +X; centred on Y, Z (Z = motor axis direction)."""
    b = cq.Workplane("XY").box(10, 16, 14).translate((5, 0, 0))
    return b.union(cq.Workplane("XY").box(6, 8, 8).translate((13, 0, 0)))


# ------------------------------------------------------------------ servo
@functools.lru_cache(None)
def micro_servo():
    """SUR-043 micro servo (SG90 size) as drawn on sheet 016: body 22.7 x 12.2 x 24.7, tabs
    32.2 x 12.2 x 2.5 at Z 18.2 (tab holes 28.2 apart), output spline 4.8 x 4 on top.
    Output shaft axis = +Z at (0,0), 5.55 from the body centre (body centre at X -5.55).
    Body bottom at Z0."""
    body = cq.Workplane("XY").box(22.7, 12.2, 24.7, centered=(True, True, False)).translate((-5.55, 0, 0))
    tabs = cq.Workplane("XY").box(32.2, 12.2, 2.5, centered=(True, True, False)).translate((-5.55, 0, 18.2))
    s = body.union(tabs)
    tabh = cq.Workplane("XY").pushPoints([(-5.55 - 14.1, 0), (-5.55 + 14.1, 0)]).circle(1.0).extrude(30)
    s = s.cut(tabh)
    return s.union(_cyl(4.8, 4.0, 24.7))


# ------------------------------------------------------------------ transmission
@functools.lru_cache(None)
def coupling(d, length, bore0, bore1):
    """SUR-044 / SUR-045 set-screw shaft coupling: cylinder d x length on Z0..L,
    bore0 from the Z0 end and bore1 from the Z=L end (each L/2 deep), one M4/M3 set screw
    hole per half along +X at Z = L/4 and 3L/4."""
    c = _cyl(d, length)
    c = c.cut(_cyl(bore0, length / 2 + 0.01, -0.01)).cut(_cyl(bore1, length / 2, length / 2))
    m = 4.0 if max(bore0, bore1) >= 8 and d >= 18 else 3.0
    for zz in (length / 4, 3 * length / 4):
        c = c.cut(cq.Workplane("YZ").center(0, zz).circle(m / 2).extrude(d))
    return c


@functools.lru_cache(None)
def bearing(od, id_, b):
    """Deep groove ball bearing envelope: outer + inner ring with a shallow seal recess."""
    r = _ring(od, id_, b)
    w = (od - id_) / 2
    rec = _ring(od - 0.3 * w, id_ + 0.3 * w, 0.3, b - 0.3).union(_ring(od - 0.3 * w, id_ + 0.3 * w, 0.3, 0))
    return r.cut(rec)


BEARINGS = {"61816": (100, 80, 10), "6806": (42, 30, 7), "6808": (52, 40, 7),
            "608": (22, 8, 7), "688": (16, 8, 5)}


@functools.lru_cache(None)
def circlip(shaft):
    """DIN 471 external retaining ring (simplified flat ring with a gap)."""
    g, s, w = {80: (76.5, 2.5, 6.0), 30: (28.6, 1.5, 3.8)}[shaft]
    r = _ring(g + 2 * w, g, s)
    return r.cut(cq.Workplane("XY").box(g, 0.2 * g, 10).translate((g / 2, 0, 0)))


@functools.lru_cache(None)
def v_ring(od, id_, w):
    """SUR-057 / SUR-058 V-ring seal envelope (tapered lip)."""
    r = _ring(od, id_, w)
    return r.edges("%CIRCLE and >Z").edges(cq.selectors.RadiusNthSelector(-1)).chamfer(min(2.0, w * 0.4))


# ------------------------------------------------------------------ fasteners
SHCS = {2: (3.8, 2.0, 1.5), 2.5: (4.5, 2.5, 2.0), 3: (5.5, 3.0, 2.5), 4: (7.0, 4.0, 3.0),
        5: (8.5, 5.0, 4.0), 6: (10.0, 6.0, 5.0)}                     # dk, k, socket s
LOWHEAD = {4: (7.0, 2.8, 2.5), 5: (8.5, 3.5, 3.0)}                   # DIN 7984


def _hex(s, depth, z0):
    return cq.Workplane("XY").workplane(offset=z0).polygon(6, s / math.cos(math.pi / 6)).extrude(depth)


@functools.lru_cache(None)
def screw(d, length, low_head=False):
    """ISO 4762 / DIN 7984 socket head cap screw: head on Z<0, shank Z0..L (thread cosmetic)."""
    dk, k, s = (LOWHEAD if low_head else SHCS)[d]
    head = _cyl(dk, k, -k).cut(_hex(s, k * 0.6, -k - 0.01))
    return head.union(_cyl(d, length))


@functools.lru_cache(None)
def set_screw(d, length):
    """ISO 4026 set screw (flat point): Z0..L, hex socket at Z0."""
    s = {3: 1.5, 4: 2.0}[d]
    return _cyl(d, length).cut(_hex(s, min(length * 0.6, 2.5), -0.01))


@functools.lru_cache(None)
def clevis_pin(d, length):
    """DIN 1444 clevis pin: head d+3 x 1.6 on Z<0, shank Z0..L with a 1 mm split-pin hole."""
    p = _cyl(d + 3, 1.6, -1.6).union(_cyl(d, length))
    return p.cut(cq.Workplane("XZ").center(0, length - 1.6).circle(0.5).extrude(d, both=True))


@functools.lru_cache(None)
def dowel(d, length):
    """ISO 8734 dowel pin: Z0..L with 0.4 end chamfers."""
    return _cyl(d, length).faces(">Z or <Z").edges().chamfer(0.4)


@functools.lru_cache(None)
def cable_gland():
    """SUR-056 PG7 cable gland: thread 12.5 x 8 on Z<0, hex 19 AF x 6 and dome nut on Z>0."""
    g = _cyl(12.5, 8, -8)
    g = g.union(cq.Workplane("XY").polygon(6, 19 / math.cos(math.pi / 6)).extrude(6))
    g = g.union(_cyl(15, 8, 6)).union(_cyl(6.5, 4, 14))
    return g.cut(_cyl(5, 30, -9))
