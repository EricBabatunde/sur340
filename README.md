# SUR340 robot arm: 3D CAD from the 2D drawing set

STEP models of the SUR340 6-axis pick-and-place robot arm. They're built in
[CadQuery](https://github.com/CadQuery/cadquery) from the drawing set
`SUR340_Complete_2D_Drawing_Set.pdf` (Rev C, 2026-11-24, 52 sheets).

The arm has a reach of 340 mm (upper arm 180 mm, forearm 160 mm). It's driven by six stepper motors, with a servo for the gripper.

## What's in here

| Path | Contents |
|---|---|
| `out/01_STEP_parts/` | 37 made parts. Each file holds one solid and is STEP AP214, named `SUR-0xx_NAME.step` and coloured by material |
| `out/03_STEP_assemblies/` | Sub-assemblies SA1–SA7, the robot (`SUR340_ROBOT.step`) and the work cell with fixtures and package (`SUR340_WORKCELL.step`), all in the home pose |
| `out/MEASUREMENT_LOG.md` | Every value not written on the sheets, and how it was obtained, plus the design decisions and the assembly stack |
| `cad/parts/` | One script per part, each with a `build()` function |
| `cad/assy/` | Assembly placement, the bought-out part models are in `cad/bought/` |
| `cad/measure/` | Tools that read geometry out of the vector PDF |
| `cad/` | Build, verify, render and interference-check scripts |

## Using the models

The part files are written for **SolidWorks**. They also open in Fusion 360, FreeCAD, Onshape and other CAD packages that read STEP AP214.

- Each part file opens as a part document. Run Import Diagnostics, then **FeatureWorks** to rebuild an editable feature tree.
- Parts are modelled in a feature-tree order: base extrude or revolve, then cuts, then holes, then fillets and chamfers. That's what lets the features be recognised.
- Tapped holes are plain holes at nominal diameter, which is how the drawing set draws them. Add cosmetic threads in your CAD package if you need them.
- Gear teeth reproduce the tooth form drawn on the sheets, with the stated module and tooth count.
- Run FeatureWorks on the part files, not on the assemblies.

## How the models were made

The part sheets give overall sizes and key dimensions, and refer to source STEP files that weren't available. Every other feature was measured from the PDF's vector linework. The sheets are drawn at the scale in their title blocks, so the measurements are exact to about 0.01 mm. Stated values always take priority. Each part script's docstring lists what was STATED and what was MEASURED.

Every part was checked against its sheet in two ways:
- a hidden-line render of FRONT/LEFT/TOP/ISO laid out next to the sheet;
- an automated re-import checking for one valid solid, AP214, the part name and colour, and a bounding box within ±0.15 mm of the stated overall size.

The assembly checks:
- every gear mesh, with zero interference;
- an interference check across all 192 robot parts;
- the envelope, which comes out at 335 × 267 × 441 mm and matches the general arrangement (GA) sheet;
- part counts against the BOM.

### Changes from the drawing (agreed design decisions)

- **SUR-019 J4 shaft:** the screw counterbores now run from the left end down to the flange. On the drawing they're buried under the shaft body, so the screws couldn't be fitted.
- **SUR-005 shoulder housing:** a Ø40 hole through the base opens the drawn but sealed internal pocket. It lines up with the turntable bore and serves as a cable passage.
- **SA2:** 4 × M6×25 shoulder screws. The BOM lists 6, but the housing has 4 holes.
- **SA7:** the right gripper gear link is turned over so the drawn tooth phases mesh.
- **SUR-013:** the "key" is modelled as the round Ø4 × 10 pin that the views draw.

Bought-out parts (motors, bearings, fasteners, couplings, servo, glands, seals) are simplified models at catalogue sizes. Lengths and sizes the sheets draw were measured from them. The eight cables are not modelled. See `out/MEASUREMENT_LOG.md` for the full list.

## Rebuilding

You need Python 3.12 with CadQuery 2.8 and PyMuPDF:

```bash
mamba create -n cad -c conda-forge python=3.12 cadquery
mamba run -n cad pip install pymupdf matplotlib
```

Then rebuild everything: the parts, the verification, the assemblies and the log. It takes about 45 seconds.

```bash
cd cad
mamba run -n cad python build_all.py
```

Other scripts in `cad/`:

| Command (run from `cad/`) | What it does |
|---|---|
| `python verify.py` | Re-checks every part STEP |
| `python check_assy.py` | Reports the robot envelope and any part-to-part interference |
| `python render.py sur005_shoulder_housing 16` | Renders a part next to its sheet. The arguments are the part module and the PDF page number |

## Source

The drawing set is `SUR340_Complete_2D_Drawing_Set.pdf`, a MUST Mechatronics team project. It's drawn in first-angle projection (ISO 128-30), units are mm, and general tolerances are ISO 2768-m. It's a concept design: strength, motor torque and mass haven't been verified.
