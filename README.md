# Plugg för konens insida

Parametrisk 3D-plugg som passar i den smala änden av en trafikkon/tratt (~38 mm innerdiameter). Fyra spår tar emot ribborna (5×2 mm) så pluggen inte roterar när man skruvar.

## Färdiga filer

| Fil | Användning |
| --- | --- |
| [exports/cone_plug.step](exports/cone_plug.step) | Öppna i **Fusion 360** (*Insert → Insert STEP*) |
| [exports/cone_plug.stl](exports/cone_plug.stl) | 3D-utskrift / slicer |

## Standardmått

- Höjd: **30 mm**
- Ytterdiameter smal ände: **37.4 mm** (38 mm ID minus spel)
- Ytterdiameter bred ände: **50 mm** (uppskattad lutning)
- Spår: **5.4 × 2.2 mm**, 4 st med 90° mellanrum
- Centrumhål: **Ø6 mm**
- Chamfer på smal ände för enklare isättning

## Justera passform

Ändra parametrarna högst upp i [`cone_plug.py`](cone_plug.py):

- `D_WIDE` — om pluggen tar i eller sitter löst längre upp i konen
- `D_NARROW` — passform vid 38 mm-änden
- `CLEARANCE` — spel i spåren mot ribborna
- `HOLE_D` — skruvhålets diameter
- `HEIGHT` — hur långt upp pluggen går

Kör sedan om:

```bash
pip install -r requirements.txt
python3 cone_plug.py
```

Nya STEP/STL skrivs till `exports/`.

## Fusion 360

1. *Insert → Insert Mesh* (STL) eller importera STEP-filen.
2. STEP ger en solid du kan editera; STL är en mesh.
