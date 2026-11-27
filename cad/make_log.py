"""Write out/MEASUREMENT_LOG.md from the part-script headers + assembly notes + flags."""
import glob, os, ast
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out", "MEASUREMENT_LOG.md")

FLAGS = """## Items flagged for your decision (modelled as drawn unless noted)

1. **SUR-013 KEY 4x4x10** - the note says *parallel key*, the views draw a round 4 x 10 pin.
   Kept as the round pin (user decision).
2. **SUR-019 J4 SHAFT** - CHANGED (user decision): the sheet draws the 6 x 4.5 cb 8 counterbores at X32-35
   under the 40 body, so the screws could not be fitted. The counterbore 8 is now drilled from the X0
   (LEFT view) end down to X35; it breaks out of the 40 journal as 6 shallow grooves (under the 6808).
3. **SUR-005 SHOULDER HOUSING** - CHANGED (user decision): the pocket X+-30, Y+-26, Z18-30 is drawn sealed.
   A 40 hole through the base on the J1 axis now opens it to the turntable 40 bore (cable passage).
4. **SUR-005 / SA2** - BOM lists 6 x M6x25 (SUR-065); sheet 105 has 4 holes. 4 screws used (user decision).
5. **SUR-015 UPPER ARM** - the note says 'J3 motor seat 60 sq'; no 60 sq feature appears in any view.
   Not modelled (only what is drawn: 39 pilot + 4 x M5).
6. **SUR-017 ELBOW HOUSING** - the 56 bore (Y8-72) is closed by an 8 mm front wall and is only reachable
   through the 24 / 42 holes. Modelled as drawn (not machinable as a turned bore).
7. **Gripper gear links (SA7)** - with both links installed the same way round, the drawn tooth phases
   (0 / 4 deg) interfere. With **SUR-030 (R) turned over** they mesh with zero interference over the whole
   stroke - the assembly uses that. (Part geometry unchanged.)
8. **Motor screws** - several motor mounts are tapped on both sides (e.g. J4 pad M3 x 12 and the NEMA17
   face). Screws are placed from the motor side, through a clearance flange in the simplified motor.
9. **Threads** - per sheets 000/001 tapped holes are drawn and modelled at NOMINAL diameter (M6 = 6.0 etc.),
   not at tap-drill size. Add cosmetic threads in SolidWorks if wanted.
10. **Bought-out parts** are simplified envelopes (catalogue sizes, motor lengths measured from the sheets).
    The 8 PUR cables (SUR-082..089) are not modelled. NEMA shaft lengths are not given anywhere: J1/J3 28,
    J2 21, J4 22, J5 18, J6 18 were chosen so the couplings / pinions engage without clashing.
11. **Dowel SUR-026 4x48** - the wrist hole (sheet 124) is 44 deep from the hub top; the 48 pin stands 4 mm proud.
"""

ASSY = """## Assembly stack (home pose, world frame of sheet 001)

Origin = floor on the J1 axis, Z up, +X toward the reach. All checked against the GA / sub-assembly
sheets (side view 1:2.5 calibrated on the J2/J3/J5 markers: J2 Z192.0, J2-J3 180.0, J3-J5 160.0).

| Item | Position |
|---|---|
| Base plate / pedestal / 61816 | Z0-12 / Z12-96 / Z86-96 |
| Turntable (journal down) / circlip 80 | Z82-127 / Z83.5-86 |
| J1 ring gear | Z97-107 (bolted under the turntable, M5x20) |
| J1 bracket, motor, pinion | axis X-90.73 (= (156+25.5)/2), motor face Z88, pinion teeth Z97-109 |
| Shoulder housing | Z127 -> J2 at Z192 |
| J2 cartridge | housing flange Y36-42, 6806 Y14-21, spacer Y21-45, gear Y45-55, washer Y55-58 |
| J2 motor / coupling / pinion shaft / 608 / pinion | face Y-42 / Y-30..-5 / Y-17..63 / Y29-36 / teeth Y43-55 |
| Upper arm | Y55-77 (plan view), J3 at Z372 |
| J3 drum / gear / pivot / circlip | Y-40..44 / Y44-54 / Y32-80 / Y77.5-79 (plan view) |
| J3 motor (turned 45 deg) | face Y77, body to Y133, cap to 141, connector to Y157 (plan view) |
| J4 motor / coupling / drive shaft | face X-46 / X-34..-9 / X-21..29 |
| 6808 / J4 shaft / roll ring | X45-52 / X20-58 / X52-58 (sheet 013 TOP) |
| Forearm | collar face X58 -> J5 at X160 |
| J5 bearings / shaft / circlip / motor plate | Y24-31, 37-44 / Y10-47 / Y44 / Y44-49 |
| Wrist | Y-23..23 (J6 on Y0), bottom Z323 |
| J6 ring / tool flange | Z317-323 / Z309-317 (flange top = J5 - 55) |
| J6 motor | face Z403, top Z441 (= 441 overall) |
| Gripper | body Z261-309; links at (-+16, -32.2) from the body pivots (sheet 016); grip point (160,0,217) |
| Envelope (model) | 334.9 x 267.0 x 441.0 (sheet 001: 335 x 267 x 441) |
"""


def main():
    lines = ["# SUR340 - measurement log\n",
             "Source: SUR340_Complete_2D_Drawing_Set.pdf (Rev C, 2026-11-24). Every value that is not written on "
             "the sheets was measured from the true-scale vector views (part sheets are A4 at the title-block "
             "scale; extractor cad/measure/extract.py). STATED = written on the sheet, MEASURED = taken from the "
             "views. Stated values always win.\n", FLAGS, ASSY, "## Part by part\n"]
    for f in sorted(glob.glob(f"{HERE}/parts/sur0*.py")) + [f"{HERE}/parts/gear_link_common.py"]:
        doc = ast.get_docstring(ast.parse(open(f).read())) or ""
        lines.append(f"### {os.path.basename(f)}\n```\n{doc}\n```\n")
    open(OUT, "w").write("\n".join(lines))
    print("wrote", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
