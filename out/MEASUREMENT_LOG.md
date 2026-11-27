# SUR340 - measurement log

Source: SUR340_Complete_2D_Drawing_Set.pdf (Rev C, 2026-11-24). Every value that is not written on the sheets was measured from the true-scale vector views (part sheets are A4 at the title-block scale; extractor cad/measure/extract.py). STATED = written on the sheet, MEASURED = taken from the views. Stated values always win.

## Items flagged for your decision (modelled as drawn unless noted)

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

## Assembly stack (home pose, world frame of sheet 001)

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

## Part by part

### sur001_base_plate.py
```
SUR-001 BASE PLATE - sheet 101, Al 6061-T6.

STATED : 220 x 220 x 12, R16; 4 x 6.6 cbore 11 x 6.5 on 176 sq; 6 x M6 on PCD 140;
         2 x M6 for the J1 bracket.
MEASURED (sheet 101, 1:5):
  - 1 x 45 deg chamfer on the top perimeter edge (FRONT/LEFT, TOP inner arc R15)
  - PCD 140 holes at 30/90/150/210/270/330 deg (holes at +-Y on the axis)
  - J1 bracket holes M6 at X = -90.73, Y = +-48.0  (origin = plate centre)
  - M6 holes through (12)
Origin: centre of the bottom face, Z up.
```

### sur002_base_pedestal.py
```
SUR-002 BASE PEDESTAL - sheet 102, Al 6061-T6 (turned).
STATED : flange 160, body 114, top 120, height 84; bearing seat 100.2 x 10;
         6 x 6.6 spot face 11.5 on PCD 140.
MEASURED (sheet 102, 1:2): flange 160 x 4 + 45deg-ish taper to R75 at z7 (5 x 3),
  cone R75 z7 -> R57 z10; body to z78; collar 120 z78-84; bore 80 through,
  90 from z68 to 74; spot faces flat at z7; holes start at +Y (90 deg);
  PG7 gland hole 12.5 on -Y wall at z41 (Y -57, matches sheet 002 "gland at Y-58").
Origin: bottom centre, Z up.
```

### sur003_j1_ring_gear.py
```
SUR-003 J1 RING GEAR - sheet 103, Brass CuZn39Pb3.
STATED : m 1.5, z 104, pitch dia 156, width 10, bore 92, 6 x M5 on PCD 100.
MEASURED: tip 159 (overall), root dia 152.25, tooth form per lib.gear_profile;
  M5 holes drawn at nominal 5.0, through, first hole at +Y (90 deg).
Origin: bottom centre, Z up.
```

### sur004_turntable.py
```
SUR-004 TURNTABLE - sheet 104, Al 6061-T6.
STATED : disc 152 x 14, spigot 116 x 6, hub 88, journal 80 (61816), circlip groove 76.5;
         6 x 5.5 cb 9.5 PCD 100; 6 x M6 PCD 112.
MEASURED (1:2): journal 80 x 14 (z0-14), hub 88 (z14-25), spigot (z25-31), disc (z31-45);
  groove 76.5 x 2.5 wide at z1.5-4.0; top edge chamfer 1.5; bore 40 through;
  cbore 9.5 depth 5.5 from top, PCD100 holes start +Y; M6 (nominal 6) through z25-45,
  PCD112 holes start +X (they break out of the spigot wall, as drawn).
Origin: journal end centre (bottom), Z up (disc on top).
```

### sur005_shoulder_housing.py
```
SUR-005 SHOULDER HOUSING (J2) - sheet 105, Al 6061-T6.
STATED : base 126 x 18, tower 80 x 72, J2 boss 96 x 72 at 65, cartridge bore 58.2
         + 8 x M5 PCD 72, 608 seat for the pinion shaft.  Overall 153 x 126 x 113.
MEASURED (sheet 105, 1:2) - origin = base bottom centre, Z up, J2 axis along Y at Z65:
  base 126 x 18; 4 x 6.6 cbore 11 x 6.5 at R56 on 0/60/120/180 deg;
  PG7 gland hole 12.5 vertical through the base at (-52, 26) (breaks the rim);
  tower X -40..40, Y -36..36; boss 96 (Y -36..36); bore 58.2 through;
  8 x M5 (nominal 5) x 12 deep in the back face (Y36), PCD72 from 0 deg (XZ);
  NEMA23 plate X -90..-22, Z 31..99, Y -42..-36, R6 corners, pilot recess 40 x 3 deep + 10 through,
  4 x M5 through on 47.14 sq; motor/pinion axis X -54.74, Z 65 (= centre distance 54.75);
  608 block X -72..-45.25, Y 26..36, Z 49..81: seat 22 x 7 from Y36, 10 through;
  coupling pocket X -48..-42.74, Y -36..0, Z 55.76..74.25;
  internal pocket X -30..30, Y -26..26, Z 18..30 (drawn enclosed); opened to the bottom with a
  40 hole through the base on the J1 axis, in line with the turntable 40 bore (user decision
  2026-11-27, cable passage; not on the sheet).
```

### sur006_j1_motor_bracket.py
```
SUR-006 J1 MOTOR BRACKET - sheet 106, Al 6061-T6, 6 mm.
STATED : U bracket 64 x 112 x 82, 6 mm; pilot 40; 4 x M5 on 47.14 sq; 2 x 6.6 in the feet.
MEASURED (1:2): top plate X -34..30 (motor axis 2 mm off the plate centre, as drawn),
  Y -40..40, Z 76..82; walls X -15..15, Y +-(34..40), Z 0..76; feet X -15..15,
  Y +-(40..56), Z 0..6 with 6.6 holes at Y +-48.
Origin: motor axis, bottom (feet underside) at Z0.
```

### sur007_drive_housing.py
```
SUR-007 DRIVE HOUSING (J2 drive cartridge) - sheet 107, Steel S355 (turned).
STATED : flange 84 x 6, body 58 x 22, seat 42 H7 x 7, 8 x 5.5 cb 10 x 3.6 on PCD 72.
MEASURED (1:2): bore 30 through (z0-21), seat 42 from top (z21-28);
  counterbores on the flange underside (z0-3.6); PCD72 holes start +X.
Origin: flange underside centre, Z up.
```

### sur008_drive_pinion.py
```
SUR-008 DRIVE PINION (J1, J2, J3) - sheet 108, Steel 42CrMo4.
STATED : m 1.5, z 17, pitch dia 25.5, width 12, hub 22 x 8, bore 8, M4 set screw.
MEASURED (1:1): teeth z0-12, hub 22 z12-20 on top, bore 8 through,
  M4 set screw hole (nominal 4) radial along +X at z16; tooth form per lib.gear_profile.
Origin: bottom centre, Z up.
```

### sur009_j2_output_gear.py
```
SUR-009 J2 OUTPUT GEAR - sheet 109, Brass CuZn39Pb3.
STATED : m 1.5, z 56, pitch 84, width 10, bore 12 + keyway 4, 6 x 4.5 cb 8 x 3 PCD 44,
         4 x 10 PCD 62; ratio 56:17.
MEASURED (1:1): keyway 4 wide at +Y to 8.3 from axis; counterbores on the BOTTOM face;
  PCD44 holes start +X; PCD62 holes at 45 deg.
Origin: bottom centre, Z up.
```

### sur010_j3_output_gear.py
```
SUR-010 J3 OUTPUT GEAR - sheet 110, Brass CuZn39Pb3.
STATED : m 1.5, z 56, pitch 84, width 10, bore 30.2, 6 x 4.5 cb 8 x 3 PCD 44, 4 x 10 PCD 62.
MEASURED (1:1): counterbores on the TOP face; PCD44 holes start +X; PCD62 at 45 deg.
Origin: bottom centre, Z up.
```

### sur011_spacer_j2.py
```
SUR-011 SPACER J2 - sheet 111, Steel.  STATED: 22 / 12.2 x 24.
```

### sur012_j2_output_shaft.py
```
SUR-012 J2 OUTPUT SHAFT - sheet 112, Steel C45.
STATED : 12 x 45 + journal 30 x 7 + collar 16 x 4; keyway 4 x 3; M5 end hole.
MEASURED (1:1): shaft 12 z0-34, journal 30 z34-41, collar 16 z41-45;
  keyway 4 wide x 3 deep x 10 long from the shaft end, on +Y;
  M5 end hole (nominal 5) x 12 deep in the shaft end.
Origin: shaft end centre (bottom), Z up.
```

### sur013_key_4x4x10.py
```
SUR-013 KEY 4x4x10 - sheet 113, Steel C45.
STATED : parallel key 4 x 4 x 10.
DRAWN  : the sheet views show a round 4 x 10 body (TOP view is a circle, iso a cylinder).
         Modelled AS DRAWN (cylinder 4 x 10) - flagged to the user.
Origin: bottom centre, Z up.
```

### sur014_end_washer.py
```
SUR-014 END WASHER - sheet 114, Steel.  STATED: 28 x 3, hole 5.5.
```

### sur015_upper_arm.py
```
SUR-015 UPPER ARM (J2 -> J3) - sheet 115, Al 6061-T6.
STATED : centres 180, width 72, 22 thick; J3 2 x seat 42 x 7; 6 x M4 PCD 44 at J2;
         J3 motor seat 60 sq, 4 x M5.  Overall 114.7 x 27 x 252.
MEASURED (sheet 115, 1:5) - origin = J2 axis on the front face (Y0), arm along +Z, thickness +Y:
  outline: R36 at J2 (Z0) and J3 (Z180), straight sides X -36 / +36, motor lobe R40 about
  (X -38.71, Z 141.28) (J3 pinion axis, 54.74 from J3 at 45 deg);
  slot 28 wide, R14 ends at Z52 / Z100, through;
  J2: bore 31 through; 6 x M4 (nominal 4) x 12 from the front face, PCD44 from 0 deg;
  J3: bore 31 through + seat 42 x 7 on both faces;
  motor lobe: pilot 39 through; 4 x M5 (nominal 5) x 10 from the back face at R33.33 on the
  X/Z axes (47.14 sq turned 45 deg);
  2 cable-clip pads 14 x 14 x 5 on the back face (Y22-27) at X21..35, Z93..107 / Z133..147,
  each with M3 (nominal 3) x 6 deep.
  The stated '60 sq' motor seat is not visible in any view (flagged).
```

### sur016_j3_pivot.py
```
SUR-016 J3 PIVOT - sheet 116, Steel C45, ground.
STATED : 30 h6 / 16 x 48, circlip groove 28.6.
MEASURED (1:1): axis along Y (as drawn), Y 0..48; groove 28.6 x 1.5 wide at Y 45.5-47.0.
Origin: -Y end centre.
```

### sur017_elbow_housing.py
```
SUR-017 ELBOW HOUSING + forearm root (J3, J4) - sheet 117, Al 6061-T6.
STATED : drum 80 x 84 (bore 56), pivot bore 30, root 64 with 6808 seat 52 x 7,
         J4 drive hole 24, 8 x M4 PCD 64, 6 x M4 PCD 44.  Overall 98 x 84 x 80.
MEASURED (sheet 117, 1:2) - origin = J3 (drum) axis on the front face, drum along +Y:
  drum 80, Y0..84; internal bore 56 Y8..72 (front wall 8, back wall 12);
  pivot bore 30 x 12 from the back face (Y72..84);
  root = cylinder 64 along +X (J4 axis at Y40, Z0), X0..52;
  J4 line: recess 29 x 3 (X-46..-43), drive hole 24 (X-46..-28, into the bore),
  42 (X0..45), 6808 seat 52 x 7 (X45..52);
  motor pad 50 x 50 on -X (X-46.., Y15..65, Z-25..25), 4 x M3 (nominal 3) x 12 on 31 sq;
  8 x M4 (nominal 4) x 10 in the front face, PCD64 at 22.5 + n*45 deg;
  6 x M4 x 10 in the back face, PCD44 from 0 deg.
```

### sur018_elbow_cap.py
```
SUR-018 ELBOW CAP - sheet 118, Al 6061-T6.
STATED : 80 x 6, 8 x 4.5 on PCD 64.
MEASURED (1:1): axis along Y (as drawn), Y 0..6; 0.8 x 45 chamfer both faces;
  recess 22 x 2 deep on the Y=0 (front) face; PCD64 holes at 22.5 + n*45 deg (in XZ).
Origin: front face centre.
```

### sur019_j4_shaft.py
```
SUR-019 J4 SHAFT (J4 roll shaft, bolted to the forearm) - sheet 119, Steel C45.
STATED : 40 x 32 in 6808, flange 44 x 6, bore 24, drive hole 8, 6 x 4.5 cb 8 PCD 34.
MEASURED (1:1): axis along X (as drawn): body 40 X0-32, flange 44 X32-38;
  bore 24 from the flange end, 28 deep (X10-38); drive hole 8 X0-10;
  M3 set screw hole (nominal 3) radial from +Z at X5 into the drive hole (for SUR-073);
  PCD34 holes in the YZ plane, first at +-Y; 4.5 through the flange X35-38,
  counterbore 8 drilled from the X0 (LEFT view) end down to X35, so the DIN 7984 screws can be
  fitted from that side (user decision 2026-11-27; the sheet draws the counterbore 8 x 3 at X32-35,
  buried under the 40 body). It breaks out of the 40 journal as 6 shallow grooves.
Origin: X0 end centre.
```

### sur020_j4_drive_shaft.py
```
SUR-020 J4 DRIVE SHAFT - sheet 120, Steel C45 h6.  STATED: 8 x 50 (axis X as drawn).
```

### sur021_forearm.py
```
SUR-021 FOREARM (J4 roll -> J5) - sheet 121, Al 6061-T6.
STATED : J3 -> J5 160, collar 58, root box 42 x 70 x 52, plate 60 x 20, J5 2 x seat 42 x 7,
         4 x M4 for the motor plate.  Overall 132 x 73 x 60.
MEASURED (sheet 121, 1:2), drawing coords (X0 = collar face, Y0 = front, Z0 = bottom):
  collar 58, X0..18, axis (Y29, Z30) = J4 axis; 6 x M4 (nominal 4) x 15 on PCD34 (first at +-Y);
  root box X18..60, Y3..73, Z4..56, R8 on the 4 edges along X; top pocket X24..44, Y11..47,
  12 deep;  plate = stadium in XZ, centres X42 / X102 at Z30, R30, Y53..73;
  J5 axis X102, Z30 along Y: bore 31 through + seat 42 x 7 on both faces;
  4 x M4 x 12 from the back face (Y73) at X102+-18, Z30+-18;
  cable slot R11, centres X54 / X68 at Z30, through the plate (Y53..73);
  PG7 gland hole 12.5 x 10 deep at X64, Y63 from the top (Z60);
  M3 (nominal 3) x 8 at X42, Y63 from the top (cable clip).
Part origin: J4 axis on the collar face (drawing point X0, Y29, Z30).
```

### sur022_j5_shaft.py
```
SUR-022 J5 SHAFT (pinned in the wrist) - sheet 122, Steel C45, ground.
STATED : 30 x 37, collar 36 x 1, circlip groove 28.6, motor bore 5, pin hole 4.
MEASURED (1:1): axis along Y (as drawn), Y0..37; collar 36 at Y13-14;
  groove 28.6 x 1.5 at Y34-35.5; motor bore 5 from the Y37 end, 18 deep;
  pin hole 4 through along Z at Y8; M3 set screw hole (nominal 3) along +X at Y30
  from the motor bore to the surface (for SUR-075).
Origin: Y0 end centre.
```

### sur023_j5_motor_plate.py
```
SUR-023 J5 MOTOR PLATE - sheet 123, Al 6061-T6.
STATED : 56 x 56 x 5, hole 32 + recess 40 x 2, 4 x 4.5 cb 8, 4 x M3 on 31 sq at 45 deg.
MEASURED (1:1): plate in XZ (as drawn), thickness Y0..5; corners R5; recess on the Y0 (front)
  face; 4.5 holes at (+-18, +-18) with counterbore 8 x 3 from the BACK (Y5) face;
  M3 (nominal 3) through at R21.92 on the X/Z axes (= 31 sq turned 45 deg).
Origin: front face centre.
```

### sur024_wrist_housing.py
```
SUR-024 WRIST HOUSING (J5, carries J6) - sheet 124, Al 6061-T6.
STATED : hub 58 x 46, neck 48 x 46 x 49, J5 shaft bore 30, J6 motor pad, 688 seat 16 x 5.
         Overall 58 x 46 x 80.
MEASURED (sheet 124, 1:2), drawing coords (Z0 = bottom, Y0 = front face):
  hub 58 along Y (Y0..46), J5 axis at Z49;  neck X+-24, Z0..49, R5 on the two bottom edges;
  J5 bore 30 x 13 deep from the back (Y33..46), 20 through to the front;
  dowel hole 4 vertical at X0, Y41, from the hub top (Z78) down to Z34;
  window X+-15, Z11..33, through in Y;
  J6 pad X+-15, Y8..38, up to Z80; pilot recess 23 x 2; bore 18 down to the window (Z33);
  4 x M2.5 (nominal 2.5) x 8 on 23 sq; 688 seat 16 x 5 in the bottom face; 10 from the seat
  to the window (Z5..11).  J6 axis X0, Y23.
Part origin: J5 axis on the front face (drawing point X0, Y0, Z49).
```

### sur025_pinion_shaft.py
```
SUR-025 PINION SHAFT (J2) - sheet 125, Steel C45 h6.  STATED: 8 x 80 (axis Z).
```

### sur027_j6_shaft.py
```
SUR-027 J6 SHAFT - sheet 126, Steel C45 h6.  STATED: 8 x 74 (axis Z).
```

### sur028_tool_flange.py
```
SUR-028 TOOL FLANGE - sheet 127, Al 6061-T6.
STATED : 50 x 8, 6 x 4.5 cb 8 on PCD 36, bore 8 + M3 set screw.
MEASURED (1:1): counterbore 8 x 3 from the top; PCD36 holes start +Y;
  M3 set screw hole (nominal 3) along +X at z4 from the bore to the rim.
Origin: bottom centre, Z up.
```

### sur029_gripper_body.py
```
SUR-029 GRIPPER BODY (parallel gripper) - sheet 128, Al 6061-T6.
STATED : 68 x 44 x 48, bay 54 x 31, 4 pivot holes 4, 6 x M4 PCD 36, 2 x M3 front.
MEASURED (sheet 128, 1:1), drawing coords (X0 left, Y0 front, Z0 bottom):
  block 68 x 44 x 48, R3 on the 4 edges along Y;
  bays 54 x 31 (X7..61, Z3..34) 16 deep from the front AND the back face (web Y16..28);
  4 pivot holes 4 through the web at X16 / X52, Z7 / Z19;
  6 x M4 (nominal 4) x 8 in the top face on PCD36 about (X34, Y22), first at +Y;
  2 x M3 (nominal 3) x 8 in the front face at X42 / X62, Z43.
Part origin: top face centre (drawing point X34, Y22, Z48).
```

### sur030_gripper_gear_link_r.py
```
SUR-030 GRIPPER GEAR LINK R (front, on the servo) - sheet 129, Steel, laser cut.
See gear_link_common.py.  Teeth phase 0 deg (measured tooth centre 6.24 deg).
```

### sur031_gripper_gear_link_l.py
```
SUR-031 GRIPPER GEAR LINK L (front) - sheet 130, Steel, laser cut.
See gear_link_common.py.  Teeth phase 4 deg (measured tooth centre 2.23 deg).
```

### sur032_gripper_link.py
```
SUR-032 GRIPPER LINK (parallel link, back) - sheet 131, Steel, laser cut.
STATED : 36 centres, 9 wide, 4 thick, 2 x 4.  Plane XZ as drawn, thickness Y0..4,
origin = left hole centre.
```

### sur033_gripper_finger.py
```
SUR-033 GRIPPER FINGER (serrated pad) - sheet 132, Al 7075 hard anodised.
STATED : 12 x 32 x 50, 6 serrations, 2 x 4.
MEASURED (1:1): profile in XZ (FRONT) 12 x 50 with R2 corners, extruded Y 0..32;
  6 serrations on the X0 face: 1.5 deep x 2 high at Z 3-5, 7-9 ... 23-25;
  holes 4 through along Y at (X8, Z30) and (X8, Z42).
Origin: lower-left-front corner.
```

### sur034_servo_bracket.py
```
SUR-034 SERVO BRACKET - sheet 133, Al 6061-T6.
STATED : plate 38 x 43 x 4 + flange 32 x 8 x 4, servo window 24 x 13.2.
MEASURED (1:1): plate X0-38, Y0-4, Z0-43; flange X0-32, Y4-8, Z35-43;
  window X9.5-33.5, Z8.4-21.6; 2 x M2 (nominal 2) through at Z15, X7.4 / X35.6;
  2 x 3.4 with counterbore 6 x 3 from the front (Y0) at Z39, X6 / X26, through plate + flange.
Origin: lower-left-front corner.
```

### sur035_cable_clip.py
```
SUR-035 CABLE CLIP - sheet 134, Steel, bent.
STATED : 28 x 8, saddle 24 / 20, hole 3.4.
MEASURED (2:1): base 28 x 2.5; legs X2-4 and X24-26; saddle R12 outer / R10 inner about
  (X14, Z10); outer legs to Z10.5; hole 3.4 through the base at X14.
Profile in XZ (FRONT), extruded Y0..8; origin = lower-left-front corner.
```

### sur036_package.py
```
SUR-036 PACKAGE (tube) - sheet 135, PA6.
STATED : 36 / 18 x 40.  MEASURED: 0.8 x 45 chamfers on all four circular edges.
```

### sur037_pick_fixture.py
```
SUR-037 PICK FIXTURE - sheet 136, Al 6061-T6.
STATED : 90 x 90 x 10, pin 17.6 x 14, 4 x 6.6.
MEASURED (1:2): corners R6; holes through at (+-34, +-34); pin top chamfer 1.2.
Origin: bottom centre, Z up.
```

### sur038_place_fixture.py
```
SUR-038 PLACE FIXTURE - sheet 137, Al 6061-T6.
STATED : 90 x 90 x 22, pocket 36.5 x 12, 4 x 6.6 cb 11 x 6.
MEASURED (1:2): corners R6; holes at (+-34, +-34), counterbore from the top.
Origin: bottom centre, Z up.
```

### gear_link_common.py
```
Shared builder for SUR-030 / SUR-031 gripper gear links (sheets 129/130).
STATED : gear m 1, z 36, 4 thick; arm 36 centres; holes 4.8 and 4; teeth phase 0 / 4 deg.
MEASURED (1:1): tooth form = lib.gear_profile scaled to m1 (half widths 0.182/0.487/0.807,
  root r 16.745); tooth centre angle in the FRONT view: R 6.24 deg, L 2.23 deg (= 4.0 apart);
  4 x 5 lightening holes at (+-7.07, +-7.07) (PCD 20 at 45 deg); arm 9 wide along +X,
  R4.5 end, hole 4 at X36; centre hole 4.8.
Part in the XZ plane as drawn (FRONT view), thickness Y 0..4; origin = gear centre.
```
