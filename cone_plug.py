#!/usr/bin/env python3
"""Parametric plug for the inside of a traffic cone / funnel.

Fits the narrow end (~38 mm ID) for ~30 mm of height, with grooves that
engage the four internal ribs so the plug cannot rotate when screwing.
"""

from __future__ import annotations

from pathlib import Path

import cadquery as cq

# --- Parameters (mm) ---
D_NARROW = 37.4  # outer Ø at narrow end (38 mm ID minus ~0.3 mm/side)
D_WIDE = 50.0  # outer Ø at wide end (estimated taper; adjust to fit)
HEIGHT = 30.0
RIB_W = 5.0  # rib width on the cone
RIB_H = 2.0  # rib height (protrusion into the cone)
CLEARANCE = 0.2  # extra play in the grooves / vs ribs
HOLE_D = 6.0  # central screw clearance hole
NUM_RIBS = 4
CHAMFER = 0.6  # lead-in chamfer at the narrow end

EXPORT_DIR = Path(__file__).resolve().parent / "exports"


def _groove_cutter(r0: float, r1: float, height: float, groove_w: float, groove_d: float) -> cq.Workplane:
    """Lofted rectangular cutter that follows the frustum outer wall."""
    extra = 4.0

    # Slightly past the ends so the cut is clean through both faces
    z0 = -1.0
    z1 = height + 1.0

    bottom_x_in = r0 - groove_d
    bottom_x_out = r0 + extra
    top_x_in = r1 - groove_d
    top_x_out = r1 + extra

    bottom_cx = (bottom_x_in + bottom_x_out) / 2.0
    top_cx = (top_x_in + top_x_out) / 2.0
    depth = groove_d + extra

    return (
        cq.Workplane("XY")
        .workplane(offset=z0)
        .center(bottom_cx, 0)
        .rect(depth, groove_w)
        .workplane(offset=(z1 - z0))
        .center(top_cx - bottom_cx, 0)
        .rect(depth, groove_w)
        .loft()
    )


def build_plug() -> cq.Workplane:
    r0 = D_NARROW / 2.0
    r1 = D_WIDE / 2.0
    groove_w = RIB_W + 2.0 * CLEARANCE
    groove_d = RIB_H + CLEARANCE

    # Frustum: narrow at z=0, wide at z=HEIGHT
    plug = (
        cq.Workplane("XY")
        .circle(r0)
        .workplane(offset=HEIGHT)
        .circle(r1)
        .loft()
    )

    # Lead-in chamfer at the narrow end (helps insertion)
    if CHAMFER > 0:
        plug = plug.edges("<Z").chamfer(CHAMFER)

    # Four rib grooves, evenly spaced
    base_cutter = _groove_cutter(r0, r1, HEIGHT, groove_w, groove_d)
    for i in range(NUM_RIBS):
        angle = i * (360.0 / NUM_RIBS)
        cutter = base_cutter.rotate((0, 0, 0), (0, 0, 1), angle)
        plug = plug.cut(cutter)

    # Central screw hole
    hole = cq.Workplane("XY").circle(HOLE_D / 2.0).extrude(HEIGHT)
    plug = plug.cut(hole)

    return plug


def export(plug: cq.Workplane) -> tuple[Path, Path]:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    step_path = EXPORT_DIR / "cone_plug.step"
    stl_path = EXPORT_DIR / "cone_plug.stl"

    cq.exporters.export(plug, str(step_path))
    cq.exporters.export(plug, str(stl_path))

    return step_path, stl_path


def _bbox_summary(plug: cq.Workplane) -> str:
    bb = plug.val().BoundingBox()
    return (
        f"bbox X={bb.xlen:.2f} Y={bb.ylen:.2f} Z={bb.zlen:.2f} mm "
        f"(Z {bb.zmin:.2f} .. {bb.zmax:.2f})"
    )


def main() -> None:
    plug = build_plug()
    step_path, stl_path = export(plug)
    print(_bbox_summary(plug))
    print(f"Wrote {step_path}")
    print(f"Wrote {stl_path}")
    print(
        "Params: "
        f"D_NARROW={D_NARROW} D_WIDE={D_WIDE} HEIGHT={HEIGHT} "
        f"groove={RIB_W + 2 * CLEARANCE:.1f}x{RIB_H + CLEARANCE:.1f} "
        f"HOLE_D={HOLE_D} NUM_RIBS={NUM_RIBS}"
    )


if __name__ == "__main__":
    main()
