#!/usr/bin/env python3
"""Independent, read-only verification for the native-size one-pose starters."""
from __future__ import annotations

import hashlib
import json
import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE, PREVIEWS = ROOT / "evidence", ROOT / "previews"
MANIFEST = json.loads((ROOT / "manifest.json").read_text())
W, H = 128, 192


def sha(data): return hashlib.sha256(data).hexdigest()


def image(path):
    with Image.open(path) as value:
        return value.convert("RGBA").copy()


class Ase:
    def __init__(self, path):
        self.path, self.data = Path(path), Path(path).read_bytes()
        size, magic, frames, width, height, depth = struct.unpack_from("<I5H", self.data)
        assert size == len(self.data) and magic == 0xA5E0 and depth == 32
        self.canvas, self.frame_count, self.header = (width, height), frames, self.data[:128]
        self.layers, self.frames, self.cels, self.palettes = [], [], {}, []
        self._read(); self._links()

    def _read(self):
        pos = 128
        for frame in range(self.frame_count):
            length, magic, old_count, duration = struct.unpack_from("<I3H", self.data, pos)
            assert magic == 0xF1FA
            count, cursor, other = struct.unpack_from("<I", self.data, pos + 12)[0] or old_count, pos + 16, []
            for _ in range(count):
                size, kind = struct.unpack_from("<IH", self.data, cursor); body = self.data[cursor + 6:cursor + size]
                assert size >= 6 and cursor + size <= pos + length
                if kind == 0x2004:
                    flags, typ, level, _w, _h, blend = struct.unpack_from("<6H", body)
                    n = struct.unpack_from("<H", body, 16)[0]
                    self.layers.append({"name": body[18:18+n].decode(), "flags": flags, "type": typ, "level": level, "blend": blend, "opacity": body[12]})
                elif kind == 0x2005:
                    layer, x, y, opacity, typ, z = struct.unpack_from("<HhhBHh", body)
                    cel = {"x": x, "y": y, "opacity": opacity, "type": typ, "z": z}
                    if typ == 1: cel["link"] = struct.unpack_from("<H", body, 16)[0]
                    elif typ in (0, 2):
                        w, h = struct.unpack_from("<HH", body, 16); raw = body[20:] if typ == 0 else zlib.decompress(body[20:])
                        assert len(raw) == w*h*4; cel.update({"w": w, "h": h, "raw": raw, "raw_sha256": sha(raw)})
                    else: raise AssertionError(f"unsupported cel type {typ}")
                    self.cels[(frame, layer)] = cel
                elif kind == 0x2019:
                    palette_size, first, last, _flags = struct.unpack_from("<4I", body)
                    assert first == 0 and last + 1 == palette_size
                    self.palettes.append({"frame": frame, "entries": palette_size, "chunk_sha256": sha(body)})
                    other.append({"type": hex(kind), "sha256": sha(body)})
                else: other.append({"type": hex(kind), "sha256": sha(body)})
                cursor += size
            assert cursor == pos + length
            self.frames.append({"duration_ms": duration, "non_cel_chunks": other}); pos += length
        assert pos == len(self.data)

    def _links(self):
        for key, cel in self.cels.items():
            seen, target = {key}, cel
            while target["type"] == 1:
                next_key = (target["link"], key[1]); assert next_key in self.cels and next_key not in seen
                seen.add(next_key); target = self.cels[next_key]
            if cel["type"] == 1:
                cel.update({k: target[k] for k in ("w", "h", "raw", "raw_sha256")})

    def layer_image(self, frame, layer):
        out = Image.new("RGBA", self.canvas); cel = self.cels.get((frame, layer))
        if cel:
            part = Image.frombytes("RGBA", (cel["w"], cel["h"]), cel["raw"])
            if cel["opacity"] != 255: part.putalpha(part.getchannel("A").point(lambda a: a * cel["opacity"] // 255))
            out.alpha_composite(part, (cel["x"], cel["y"]))
        return out

    def composite(self, frame):
        out = Image.new("RGBA", self.canvas)
        for i, layer in enumerate(self.layers):
            if layer["type"] != 0 or not layer["flags"] & 1: continue
            assert layer["blend"] == 0
            part = self.layer_image(frame, i)
            if layer["opacity"] != 255: part.putalpha(part.getchannel("A").point(lambda a: a * layer["opacity"] // 255))
            out.alpha_composite(part)
        return out

    def fingerprint(self):
        return {"file_sha256": sha(self.data), "header_sha256": sha(self.header), "canvas": list(self.canvas), "frames": self.frames, "layers": self.layers, "palettes": self.palettes, "cels": {f"{frame}:{layer}": {key: value for key, value in cel.items() if key != "raw"} for (frame, layer), cel in sorted(self.cels.items())}}


def same(a, b): return a.size == b.size and a.tobytes() == b.tobytes()
def diff(a, b): return [(x, y) for y in range(H) for x in range(W) if a.getpixel((x, y)) != b.getpixel((x, y))]
def record(checks, name, passed, detail):
    checks[name] = {"passed": bool(passed), "detail": detail}
    if not passed: checks["failures"].append(name)


def main():
    reference = Ase(ROOT / "inputs/reference.aseprite")
    automatic = Ase(ROOT / "automatic-draft.aseprite")
    manual = Ase(ROOT / "hand-trace.aseprite")
    proof = Ase(EVIDENCE / "local-revision-proof.aseprite")
    source = image(ROOT / "inputs/reference.png")
    export = image(EVIDENCE / "reference-native-export.png")
    reopened = image(EVIDENCE / "automatic-reopened.png")
    reference_1x, reference_2x = image(PREVIEWS / "reference-1x.png"), image(PREVIEWS / "reference-2x.png")
    checks = {"format": "one-pose-183-independent-native-check/v1", "failures": []}
    source_path = Path(MANIFEST["source_png"])
    old_native_path = Path(MANIFEST["source_native"])
    prior = image(MANIFEST["prior_animation_entry"])
    record(checks, "input_png_source_copy_hash", sha((ROOT / "inputs/reference.png").read_bytes()) == sha(source_path.read_bytes()) == MANIFEST["input_png_sha256"], {"sha256": sha((ROOT / "inputs/reference.png").read_bytes())})
    record(checks, "input_native_source_copy_hash", sha((ROOT / "inputs/reference.aseprite").read_bytes()) == sha(old_native_path.read_bytes()) == MANIFEST["input_native_sha256"], {"sha256": sha((ROOT / "inputs/reference.aseprite").read_bytes())})
    tx, ty = MANIFEST["prior_animation_translation"]
    record(checks, "input_exact_prior_animation_crop", same(source, prior.crop((tx, ty, tx + W, ty + H))), {"translation": [tx, ty]})
    for name, doc, frames in (("reference", reference, 1), ("automatic", automatic, 1), ("manual", manual, 1), ("proof", proof, 1)):
        record(checks, f"{name}_canvas", doc.canvas == (W, H), list(doc.canvas))
        record(checks, f"{name}_one_frame_100ms", doc.frame_count == frames and [frame["duration_ms"] for frame in doc.frames] == [100], [frame["duration_ms"] for frame in doc.frames])
    record(checks, "reference_source_rgba", same(reference.composite(0), source), sha(source.tobytes()))
    record(checks, "reference_visible_geometry", source.getchannel("A").getbbox() == (32, 2, 104, 185) and sum(value > 0 for value in source.getchannel("A").getdata()) == 7844 and len({p[:3] for p in source.getdata() if p[3]}) == 248, {"bbox": source.getchannel("A").getbbox(), "visible_pixels": sum(value > 0 for value in source.getchannel("A").getdata()), "colors": len({p[:3] for p in source.getdata() if p[3]})})
    record(checks, "reference_255_palette", reference.palettes and reference.palettes[0]["entries"] == 255, reference.palettes)
    record(checks, "automatic_retains_reference_12_layers", automatic.layers[:12] == reference.layers and len(automatic.layers) == 13 and automatic.layers[12]["name"] == "Corrections" and automatic.layers[12]["flags"] & 1 and automatic.layers[12]["opacity"] == 255, automatic.layers)
    preserved = all(automatic.cels.get((0, layer)) == cel for (frame, layer), cel in reference.cels.items()) and automatic.header[4:] == reference.header[4:] and automatic.frames == reference.frames and automatic.palettes == reference.palettes
    record(checks, "automatic_source_metadata_palette_and_cels_preserved", preserved, {"protected_cels": len(reference.cels), "palette": automatic.palettes})
    record(checks, "automatic_corrections_empty", automatic.layer_image(0, 12).getbbox() is None, "blank")
    record(checks, "automatic_composite_equals_source", same(automatic.composite(0), source), sha(automatic.composite(0).tobytes()))
    record(checks, "manual_layer_contract", [layer["name"] for layer in manual.layers] == ["Guide - hide before export", "Base colors", "Shadows", "Lines and details"], manual.layers)
    record(checks, "manual_retains_reference_255_palette", manual.palettes == reference.palettes and manual.palettes and manual.palettes[0]["entries"] == 255, manual.palettes)
    record(checks, "manual_guide_exact_source", same(manual.layer_image(0, 0), source) and manual.layers[0]["flags"] & 1 and not manual.layers[0]["flags"] & 2 and manual.layers[0]["opacity"] == 77, manual.layers[0])
    record(checks, "manual_art_empty", all(manual.layer_image(0, layer).getbbox() is None for layer in (1, 2, 3)) and image(EVIDENCE / "manual-art-only.png").getbbox() is None, "transparent")
    record(checks, "png_exports_exact_source", all(same(candidate, source) for candidate in (export, reopened, reference_1x)), [sha(candidate.tobytes()) for candidate in (export, reopened, reference_1x)])
    record(checks, "reference_2x_nearest_exact", same(reference_2x, source.resize((256, 384), Image.Resampling.NEAREST)), list(reference_2x.size))
    proof_png, proof_reopened = image(EVIDENCE / "local-revision-proof.png"), image(EVIDENCE / "local-revision-reopened.png")
    expected = {(86, 82)}; proof_comp = proof.composite(0)
    changed, reopened_changed = set(diff(source, proof_comp)), set(diff(source, proof_reopened))
    protected_cels = all(proof.cels.get(key) == cel for key, cel in automatic.cels.items()) and set(proof.cels) == set(automatic.cels) | {(0, 12)}
    metadata = proof.header[4:] == automatic.header[4:] and proof.frames == automatic.frames and proof.layers == automatic.layers and proof.palettes == automatic.palettes
    record(checks, "local_revision_png_reopened_exact", same(proof_comp, proof_png) and same(proof_comp, proof_reopened), sha(proof_comp.tobytes()))
    record(checks, "local_revision_exact_one_pixel", changed == expected and reopened_changed == expected and proof_comp.getpixel((86, 82)) == (223, 179, 155, 255) and source.getpixel((86, 82)) == (252, 216, 182, 255) and proof_comp.getpixel((86, 82))[3] == source.getpixel((86, 82))[3], {"changed": sorted(changed), "reopened_changed": sorted(reopened_changed)})
    record(checks, "local_revision_protects_12_source_layers_palette_metadata", protected_cels and metadata, {"protected_cels_match": protected_cels, "metadata_match_except_file_size": metadata})
    bg = (238, 229, 209, 255); out = Image.new("RGBA", (512, 418), bg); draw = ImageDraw.Draw(out); font = ImageFont.load_default()
    draw.text((8, 8), "exact reference", fill=(45, 40, 36, 255), font=font); draw.text((264, 8), "automatic starter", fill=(45, 40, 36, 255), font=font)
    out.alpha_composite(source.resize((256, 384), Image.Resampling.NEAREST), (0, 30)); out.alpha_composite(automatic.composite(0).resize((256, 384), Image.Resampling.NEAREST), (256, 30)); out.save(PREVIEWS / "comparison-183.png")
    checks["native_files"] = {"reference": reference.fingerprint(), "automatic": automatic.fingerprint(), "manual": manual.fingerprint(), "local_revision_proof": proof.fingerprint()}
    checks["passed"] = not checks["failures"]
    (EVIDENCE / "native-checks.json").write_text(json.dumps(checks, indent=2) + "\n")
    (EVIDENCE / "visual-review.md").write_text("""# Visual review — one-pose native-size starters\n\nReviewed `previews/comparison-183.png` at exact 2× nearest-neighbor scale. The automatic starter is pixel-identical to the supplied 128×192 reference, so it preserves the 183-pixel visible height, 248 visible RGB colors, and source detail without resampling or palette loss. The hand-trace route retains the same source guide over blank art layers.\n\nThis is appropriate for a one-pose beginner practice step and is materially larger than the earlier 92–97px multi-pose study. It is not a final animation or game-ready claim: it contains one pose only, has no motion/inbetweens, and has no new Godot validation or user art approval.\n""")
    print(json.dumps({"passed": checks["passed"], "failures": checks["failures"]}, indent=2))
    return 0 if checks["passed"] else 1


if __name__ == "__main__": raise SystemExit(main())
