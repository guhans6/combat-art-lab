"""Offline analysis of the parent alpha checker findings.

This reads only this contestant's exported frames plus the parent's checker
report. It does not edit native art. The output overlay is a planning aid for
the narrowly scoped native overlap repair performed after a new lease.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT.parent / "luna56-max-parent-check.json"
OUT = ROOT / "prep" / "hole-overlay.png"
PROPOSED = ROOT / "prep" / "proposed-repair-contact.png"
PLAN = ROOT / "prep" / "technical-repair-plan.json"
OPS = ROOT / "prep" / "repair-operations.json"
MATTE = (54, 55, 64, 255)


def load(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def hole_points(check: dict, frame: int) -> list[tuple[int, int]]:
    row = check["alpha"]["frames"][frame - 1]
    return [tuple(point) for point in row["new_enclosed_body_holes_xy"]]


def composite(image: Image.Image) -> Image.Image:
    return Image.alpha_composite(Image.new("RGBA", image.size, MATTE), image)


def main() -> None:
    check = json.loads(CHECK.read_text())
    baseline = load(ROOT / "frames" / "frame-0.png")
    frame_data = {}
    for frame in range(2, 6):
        image = load(ROOT / "frames" / f"frame-{frame - 1}.png")
        points = hole_points(check, frame)
        frame_data[str(frame)] = {
            "hole_count": len(points),
            "baseline_opaque_at_holes": sum(baseline.getpixel(point)[3] > 0 for point in points),
            "candidate_transparent_at_holes": sum(image.getpixel(point)[3] == 0 for point in points),
            "bounds": {
                "x_min": min(x for x, _ in points), "x_max": max(x for x, _ in points),
                "y_min": min(y for _, y in points), "y_max": max(y for _, y in points)
            },
            "points": [[x, y] for x, y in points],
        }

    scale = 4
    crop = (32, 28, 100, 106)
    cw, ch = (crop[2] - crop[0]) * scale, (crop[3] - crop[1]) * scale
    sheet = Image.new("RGBA", (cw * 2, (ch + 24) * 2), (32, 33, 40, 255))
    proposed_sheet = Image.new("RGBA", (cw * 2, (ch + 24) * 2), (32, 33, 40, 255))
    draw = ImageDraw.Draw(sheet)
    proposed_draw = ImageDraw.Draw(proposed_sheet)
    for index, frame in enumerate(range(2, 6)):
        source = load(ROOT / "frames" / f"frame-{frame - 1}.png")
        image = composite(source.crop(crop)).resize((cw, ch), Image.Resampling.NEAREST)
        ox, oy = (index % 2) * cw, (index // 2) * (ch + 24)
        sheet.alpha_composite(image, (ox, oy))
        repaired = source.copy()
        points = hole_points(check, frame)
        for x, y in points:
            if baseline.getpixel((x, y))[3] > 0 and repaired.getpixel((x, y))[3] == 0:
                repaired.putpixel((x, y), baseline.getpixel((x, y)))
            if crop[0] <= x < crop[2] and crop[1] <= y < crop[3]:
                px, py = ox + (x - crop[0]) * scale, oy + (y - crop[1]) * scale
                draw.rectangle((px, py, px + scale - 1, py + scale - 1), outline=(255, 66, 66, 255), width=1)
        draw.text((ox + 4, oy + ch + 5), f"F{frame}: {len(points)} checker holes", fill=(242, 239, 226, 255))
        proposed_sheet.alpha_composite(composite(repaired.crop(crop)).resize((cw, ch), Image.Resampling.NEAREST), (ox, oy))
        proposed_draw.text((ox + 4, oy + ch + 5), f"F{frame}: proposed sparse fill", fill=(242, 239, 226, 255))
    sheet.save(OUT)
    proposed_sheet.save(PROPOSED)

    operations = {
        "status": "prepared_not_executed",
        "sprite_layer": "09-anim-overlap-repair",
        "palette_lock": True,
        "source": "frame-0.png neutral composite, per checker-listed coordinate",
        "frames": {
            str(frame): [
                {"x": x, "y": y, "color": "#%02x%02x%02x" % baseline.getpixel((x, y))[:3]}
                for x, y in hole_points(check, frame)
            ]
            for frame in range(2, 6)
        }
    }
    OPS.write_text(json.dumps(operations, indent=2) + "\n")

    plan = {
        "status": "prepared_waiting_for_explicit_repair_lease",
        "source_native": "luna56-idle.aseprite",
        "parent_check": str(CHECK.relative_to(ROOT.parent)),
        "finding": "The checker finds enclosed transparent pixels in the moved upper-body/tote overlap on frames 2-5; frame 1 and frame 6 have no new enclosed holes.",
        "independent_read": "Every listed coordinate is transparent in the candidate and opaque in the exact neutral composite. Clusters track the intentional one-pixel upper-body and delayed tote/strap moves, so they are seam/overlap gaps rather than a motion redesign request.",
        "relative_part_clusters": [
            "Waistband/chest seam: the repeated x=56..68, y=69 run on frames 2-5.",
            "Jacket hem/pocket overlap: the x=39..55 and x=69..80 stair-step clusters around y=72..80 on frames 2-4.",
            "Delayed strap/tote joins: the x=73..92 vertical/shoulder clusters on frames 2, 4 and 5, plus the x=78..82 hanging-tote tail on frame 3."
        ],
        "repair_strategy": {
            "kind": "declared_normal_blend_backing_layer",
            "name": "09-anim-overlap-repair",
            "purpose": "Sparse per-frame baseline-colored pixels only under the checker-listed enclosed gaps, so existing moved cels retain their motion while exposed seams are closed.",
            "scope": "Frames 2-5 and only the exact checker-listed coordinates; frames 1 and 6 stay untouched and exact neutral.",
            "blend": "normal", "visible": True, "opacity": 255,
            "source_colors": "Read from frame-1 neutral composite at each listed coordinate; no new palette colors.",
            "added_layers": ["09-anim-overlap-repair"]
        },
        "output_policy": {
            "repaired_root": "technical-repair",
            "preserve_original_native": "luna56-idle.aseprite",
            "preserve_original_exports": ["frames/", "proof/", "contacts/"],
            "update_delivery_to_repaired_outputs_only_after_fresh_reopen_and_parent_alpha_recheck": True
        },
        "frame_findings": frame_data,
        "offline_evidence": str(OUT.relative_to(ROOT)),
        "offline_proposed_repair": str(PROPOSED.relative_to(ROOT)),
        "prepared_mcp_operations": str(OPS.relative_to(ROOT)),
        "constraints": [
            "Do not alter timing, tags, source layers, shoes, denim or hidden guide.",
            "Do not fill pixels outside the listed checker coordinates.",
            "Preserve the original native/exports/proofs; write repaired outputs beside them until verified.",
            "After the lease, inspect filmstrip, save, fresh-reopen, re-export, rerun the parent alpha check and update delivery added_layers/hash records."
        ]
    }
    PLAN.write_text(json.dumps(plan, indent=2) + "\n")


if __name__ == "__main__":
    main()
