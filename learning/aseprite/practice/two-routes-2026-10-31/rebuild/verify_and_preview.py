#!/usr/bin/env python3
"""Independent verification and presentation for the six-pose starter exercise.

Reads this exercise's Aseprite files directly, including raw, compressed, and linked
cels.  It only writes the scoped evidence and presentation outputs named below.
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys
import zlib
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
PREVIEWS = ROOT / "previews"
MANIFEST = json.loads((ROOT / "manifest.json").read_text())
W = H = 128
RGBA = "RGBA"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def png(path: Path) -> Image.Image:
    with Image.open(path) as source:
        return source.convert(RGBA).copy()


class Aseprite:
    def __init__(self, path: Path):
        self.path = path
        self.data = path.read_bytes()
        size, magic, frames, width, height, depth = struct.unpack_from("<I5H", self.data)
        assert size == len(self.data), f"{path.name}: header size mismatch"
        assert magic == 0xA5E0 and depth == 32, f"{path.name}: expected RGBA Aseprite"
        self.size, self.frame_count, self.canvas = size, frames, (width, height)
        self.header = self.data[:128]
        self.frames, self.layers, self.palette, self.tags, self.cels = [], [], [], [], {}
        self._read()
        self._resolve_links()

    def _read(self):
        pos = 128
        for frame in range(self.frame_count):
            length, magic, old_chunks, duration = struct.unpack_from("<I3H", self.data, pos)
            assert magic == 0xF1FA, f"{self.path.name}: bad frame magic"
            chunks = struct.unpack_from("<I", self.data, pos + 12)[0] or old_chunks
            cursor, noncel = pos + 16, []
            for _ in range(chunks):
                chunk_len, kind = struct.unpack_from("<IH", self.data, cursor)
                assert chunk_len >= 6 and cursor + chunk_len <= pos + length
                body = self.data[cursor + 6:cursor + chunk_len]
                if kind == 0x2004:
                    flags, layer_type, level, _w, _h, blend = struct.unpack_from("<6H", body)
                    opacity = body[12]
                    name_length = struct.unpack_from("<H", body, 16)[0]
                    name = body[18:18 + name_length].decode("utf-8")
                    self.layers.append({"name": name, "flags": flags, "type": layer_type,
                                        "level": level, "blend": blend, "opacity": opacity})
                elif kind == 0x2005:
                    layer, x, y, opacity, cel_type, z = struct.unpack_from("<HhhBHh", body)
                    record = {"x": x, "y": y, "opacity": opacity, "type": cel_type, "z": z}
                    if cel_type == 1:
                        record["linked_frame"] = struct.unpack_from("<H", body, 16)[0]
                    elif cel_type in (0, 2):
                        cw, ch = struct.unpack_from("<HH", body, 16)
                        raw = body[20:] if cel_type == 0 else zlib.decompress(body[20:])
                        assert len(raw) == cw * ch * 4
                        record.update({"w": cw, "h": ch, "raw": raw, "raw_sha256": sha(raw)})
                    else:
                        raise AssertionError(f"{self.path.name}: unsupported cel type {cel_type}")
                    self.cels[(frame, layer)] = record
                elif kind == 0x2019:
                    size, first, last, _flags = struct.unpack_from("<4I", body)
                    assert first == 0 and last + 1 == size, f"{self.path.name}: non-contiguous palette"
                    self.palette.append({"frame": frame, "sha256": sha(body), "size": size,
                                         "first_index": first, "last_index": last})
                    noncel.append({"type": hex(kind), "sha256": sha(body)})
                elif kind == 0x2018:
                    tag_count = struct.unpack_from("<H", body)[0]
                    tag_cursor = 10
                    for _ in range(tag_count):
                        start, end = struct.unpack_from("<HH", body, tag_cursor)
                        direction = body[tag_cursor + 4]
                        repeat = struct.unpack_from("<H", body, tag_cursor + 5)[0]
                        name_length = struct.unpack_from("<H", body, tag_cursor + 17)[0]
                        name = body[tag_cursor + 19:tag_cursor + 19 + name_length].decode("utf-8")
                        tag_cursor += 19 + name_length
                        self.tags.append({"from": start, "to": end, "direction": direction, "repeat": repeat, "name": name})
                    assert tag_cursor == len(body), f"{self.path.name}: malformed tags chunk"
                    noncel.append({"type": hex(kind), "sha256": sha(body)})
                else:
                    noncel.append({"type": hex(kind), "sha256": sha(body)})
                cursor += chunk_len
            assert cursor == pos + length
            self.frames.append({"duration_ms": duration, "non_cel_chunks": noncel})
            pos += length
        assert pos == len(self.data)

    def _resolve_links(self):
        for key, cel in list(self.cels.items()):
            seen = {key}
            base = cel
            while base["type"] == 1:
                target = (base["linked_frame"], key[1])
                assert target in self.cels and target not in seen, f"bad cel link {key} -> {target}"
                seen.add(target)
                base = self.cels[target]
            if cel["type"] == 1:
                for field in ("w", "h", "raw", "raw_sha256"):
                    cel[field] = base[field]

    def layer_image(self, frame: int, layer: int) -> Image.Image:
        result = Image.new(RGBA, self.canvas)
        cel = self.cels.get((frame, layer))
        if not cel:
            return result
        source = Image.frombytes(RGBA, (cel["w"], cel["h"]), cel["raw"])
        if cel["opacity"] != 255:
            alpha = source.getchannel("A").point(lambda value: value * cel["opacity"] // 255)
            source.putalpha(alpha)
        result.alpha_composite(source, (cel["x"], cel["y"]))
        return result

    def composite(self, frame: int) -> Image.Image:
        result = Image.new(RGBA, self.canvas)
        for layer_index, layer in enumerate(self.layers):
            if not (layer["flags"] & 1) or layer["type"] != 0:
                continue
            assert layer["blend"] == 0, f"{self.path.name}: non-normal blend unsupported"
            source = self.layer_image(frame, layer_index)
            if layer["opacity"] != 255:
                alpha = source.getchannel("A").point(lambda value: value * layer["opacity"] // 255)
                source.putalpha(alpha)
            result.alpha_composite(source)
        return result

    def fingerprint(self):
        return {"file_sha256": sha(self.data), "header_sha256": sha(self.header),
                "canvas": list(self.canvas), "frame_count": self.frame_count,
                "durations_ms": [f["duration_ms"] for f in self.frames],
                "layers": self.layers, "palette_chunks": self.palette, "tags": self.tags,
                "cels": {f"{f}:{l}": {k: v for k, v in c.items() if k not in ("raw",)}
                         for (f, l), c in sorted(self.cels.items())}}


def equal(a: Image.Image, b: Image.Image) -> bool:
    return a.size == b.size and a.tobytes() == b.tobytes()


def changed_pixels(a: Image.Image, b: Image.Image):
    return [(x, y) for y in range(H) for x in range(W)
            if a.getpixel((x, y)) != b.getpixel((x, y))]


def payload_image(frame):
    item = json.loads((ROOT / frame["payload"]).read_text())
    legend = {key: (0, 0, 0, 0) if value is None else tuple(bytes.fromhex(value[1:])) + (255,)
              for key, value in item["legend"].items()}
    out = Image.new(RGBA, (W, H))
    out.putdata([legend[symbol] for row in item["rows"] for symbol in row])
    return out


def report_bool(checks, name, passed, detail):
    checks[name] = {"passed": bool(passed), "detail": detail}
    if not passed:
        checks["failures"].append(name)


def make_contact(exports):
    font = ImageFont.load_default()
    bg = (239, 229, 207, 255)
    sheet = Image.new(RGBA, (384 * 3, 416 * 2), bg)
    labels = ["1 neutral", "2 straplift", "3 grip", "4 windup", "5 swing", "6 recovery"]
    for i, (image, label) in enumerate(zip(exports, labels, strict=True)):
        x, y = (i % 3) * 384, (i // 3) * 416
        sheet.alpha_composite(image.resize((384, 384), Image.Resampling.NEAREST), (x, y + 24))
        ImageDraw.Draw(sheet).text((8 + x, 6 + y), label, fill=(52, 43, 37, 255), font=font)
    sheet.save(PREVIEWS / "contact-sheet.png")


def make_source_vs_seed(exports):
    sys.path.insert(0, str(ROOT / "rebuild"))
    from prepare_payloads import sample_source
    source = png(ROOT / "inputs/pose-01.png")
    raw, _ = sample_source(source)
    guide = Image.new(RGBA, (W, H)); guide.putdata(raw)
    seed = exports[0]
    bg = (239, 229, 207, 255)
    out = Image.new(RGBA, (768, 420), bg)
    draw = ImageDraw.Draw(out); font = ImageFont.load_default()
    for x, image, label in ((0, guide, "raw source guide"), (384, seed, "prepared palette seed")):
        draw.text((8 + x, 8), label, fill=(52, 43, 37, 255), font=font)
        out.alpha_composite(image.resize((384, 384), Image.Resampling.NEAREST), (x, 28))
    out.save(EVIDENCE / "source-versus-seed.png")


def gif_checks(exports, checks):
    path = PREVIEWS / "pose-study.gif"
    with Image.open(path) as gif:
        report_bool(checks, "gif_dimensions", gif.size == (384, 384), {"actual": list(gif.size)})
        images, durations = [], []
        for index in range(getattr(gif, "n_frames", 1)):
            gif.seek(index); images.append(gif.convert(RGBA).copy()); durations.append(gif.info.get("duration"))
    report_bool(checks, "gif_frame_count", len(images) == 6, {"actual": len(images)})
    report_bool(checks, "gif_timing", durations == MANIFEST["study"]["durations_ms"], {"actual_ms": durations})
    frame_results = []
    for native, image in zip(exports, images, strict=False):
        target = native.resize((384, 384), Image.Resampling.NEAREST)
        # GIF's transparent palette can alter RGB where alpha is zero; only opaque source pixels count.
        good = all(image.getpixel((x, y))[:3] == target.getpixel((x, y))[:3]
                   for y in range(384) for x in range(384) if target.getpixel((x, y))[3])
        frame_results.append(good)
    report_bool(checks, "gif_opaque_pixels_match_native_3x", all(frame_results), frame_results)


def first_keys_checks(manual, automatic, six_manual, six_automatic, checks):
    selected = (0, 3, 4)
    durations = (600, 350, 150)
    for name, doc in (("first_keys_manual", manual), ("first_keys_automatic", automatic)):
        report_bool(checks, f"{name}_canvas", doc.canvas == (W, H), list(doc.canvas))
        report_bool(checks, f"{name}_frame_count", doc.frame_count == 3, doc.frame_count)
        report_bool(checks, f"{name}_timing", [frame["duration_ms"] for frame in doc.frames] == list(durations), [frame["duration_ms"] for frame in doc.frames])
        report_bool(checks, f"{name}_palette_matches_six_key_source", doc.palette == (six_manual if name.endswith("manual") else six_automatic).palette, doc.palette)
        report_bool(checks, f"{name}_pose_study_tag", doc.tags == [{"from": 0, "to": 2, "direction": 0, "repeat": 0, "name": "pose-study"}], doc.tags)
    report_bool(checks, "first_keys_manual_layers_match", manual.layers == six_manual.layers, manual.layers)
    report_bool(checks, "first_keys_automatic_layers_match", automatic.layers == six_automatic.layers, automatic.layers)
    manual_blank = all(manual.layer_image(frame, layer).getbbox() is None for frame in range(3) for layer in (1, 2, 3))
    report_bool(checks, "first_keys_manual_art_layers_blank", manual_blank, "three art layers have no painted pixels")
    source_match = []
    for dest_frame, source_frame in enumerate(selected):
        source_match.append({
            "manual_guide": equal(manual.layer_image(dest_frame, 0), six_manual.layer_image(source_frame, 0)),
            "automatic_guide": equal(automatic.layer_image(dest_frame, 0), six_automatic.layer_image(source_frame, 0)),
            "automatic_draft": equal(automatic.layer_image(dest_frame, 1), six_automatic.layer_image(source_frame, 1)),
        })
    report_bool(checks, "first_keys_layer_pixels_match_six_key_frames_1_4_5", all(all(row.values()) for row in source_match), source_match)
    with Image.open(PREVIEWS / "first-keys.gif") as gif:
        gif_frames, gif_durations = [], []
        report_bool(checks, "first_keys_gif_dimensions", gif.size == (384, 384), list(gif.size))
        for index in range(getattr(gif, "n_frames", 1)):
            gif.seek(index); gif_frames.append(gif.convert(RGBA).copy()); gif_durations.append(gif.info.get("duration"))
    report_bool(checks, "first_keys_gif_frame_count", len(gif_frames) == 3, len(gif_frames))
    report_bool(checks, "first_keys_gif_timing", gif_durations == list(durations) and sum(gif_durations) == 1100, gif_durations)
    gif_match = []
    for source_frame, image in zip(selected, gif_frames, strict=True):
        target = six_automatic.composite(source_frame).resize((384, 384), Image.Resampling.NEAREST)
        gif_match.append(all(image.getpixel((x, y))[:3] == target.getpixel((x, y))[:3]
                             for y in range(384) for x in range(384) if target.getpixel((x, y))[3]))
    report_bool(checks, "first_keys_gif_opaque_pixels_match_selected_exports_3x", all(gif_match), gif_match)


def main():
    EVIDENCE.mkdir(exist_ok=True); PREVIEWS.mkdir(exist_ok=True)
    checks = {"format": "two-routes-independent-native-check/v1", "failures": []}
    manual = Aseprite(ROOT / "hand-trace.aseprite")
    automatic = Aseprite(ROOT / "automatic-draft.aseprite")
    proof = Aseprite(EVIDENCE / "local-revision-proof.aseprite")
    first_manual = Aseprite(ROOT / "hand-trace-first-keys.aseprite")
    first_automatic = Aseprite(ROOT / "automatic-first-keys.aseprite")
    expected_durations = MANIFEST["study"]["durations_ms"]
    for name, doc in (("manual", manual), ("automatic", automatic), ("local_revision_proof", proof)):
        report_bool(checks, f"{name}_canvas", doc.canvas == (W, H), list(doc.canvas))
        report_bool(checks, f"{name}_frame_count", doc.frame_count == 6, doc.frame_count)
        report_bool(checks, f"{name}_timing", [f["duration_ms"] for f in doc.frames] == expected_durations,
                    [f["duration_ms"] for f in doc.frames])
    manual_names = [l["name"] for l in manual.layers]
    automatic_names = [l["name"] for l in automatic.layers]
    report_bool(checks, "manual_layer_contract", manual_names == ["Guide - hide before export", "Base colors", "Shadows", "Lines and details"], manual.layers)
    report_bool(checks, "automatic_layer_contract", automatic_names == ["Guide - hide before export", "Automatic draft", "Corrections"], automatic.layers)
    guide = manual.layers[0]
    report_bool(checks, "manual_guide_contract", guide["flags"] & 1 and not (guide["flags"] & 2) and guide["opacity"] == 77 and len([k for k in manual.cels if k[1] == 0]) == 6, guide)
    art_empty = all(manual.layer_image(frame, layer).getbbox() is None for frame in range(6) for layer in (1, 2, 3))
    report_bool(checks, "manual_art_layers_empty", art_empty, "Base colors, Shadows, Lines and details have no painted pixels")
    auto_guide = automatic.layers[0]
    report_bool(checks, "automatic_guide_contract", not (auto_guide["flags"] & 1) and not (auto_guide["flags"] & 2) and auto_guide["opacity"] == 77, auto_guide)
    report_bool(checks, "automatic_draft_visible_cels", automatic.layers[1]["flags"] & 1 and len([k for k in automatic.cels if k[1] == 1]) == 6, automatic.layers[1])
    corrections_empty = all(automatic.layer_image(frame, 2).getbbox() is None for frame in range(6))
    report_bool(checks, "automatic_corrections_blank", corrections_empty, "Corrections layer has no painted pixels")
    expected_palette = json.loads((ROOT / "payloads/palette.json").read_text())
    for name, doc in (("manual", manual), ("automatic", automatic), ("local_revision_proof", proof)):
        actual = doc.palette[0] if doc.palette else {}
        report_bool(checks, f"{name}_shared_32_color_palette", actual.get("size") == len(expected_palette) == 32, {"count": actual.get("size"), "sha256": actual.get("sha256")})
    first_keys_checks(first_manual, first_automatic, manual, automatic, checks)
    exports = [png(PREVIEWS / f"pose-{i:02d}.png") for i in range(1, 7)]
    exports_ok = []
    for index, (frame, export) in enumerate(zip(MANIFEST["frames"], exports, strict=True)):
        seed = payload_image(frame)
        actual = automatic.composite(index)
        payload_hash = sha(seed.tobytes()); export_hash = sha(export.tobytes()); composite_hash = sha(actual.tobytes())
        passed = equal(seed, export) and equal(actual, export) and payload_hash == frame["after_alpha_ge_128"]["draft_pixel_hash_canonical_rgba_sha256"]
        exports_ok.append(passed)
        report_bool(checks, f"pose_{index + 1:02d}_payload_native_export", passed,
                    {"payload_rgba_sha256": payload_hash, "native_composite_rgba_sha256": composite_hash,
                     "export_rgba_sha256": export_hash, "manifest_rgba_sha256": frame["after_alpha_ge_128"]["draft_pixel_hash_canonical_rgba_sha256"]})
    report_bool(checks, "all_exports_match_payloads", all(exports_ok), exports_ok)
    heights = []
    for image in exports:
        alpha_bounds = image.getchannel("A").getbbox()
        heights.append(alpha_bounds[3] - alpha_bounds[1] if alpha_bounds else 0)
    report_bool(checks, "native_export_visible_heights", heights == [92, 96, 94, 95, 97, 96], {"heights": heights, "range": [min(heights), max(heights)]})
    for record in MANIFEST["inputs"]:
        actual_hash = sha((ROOT / record["file"]).read_bytes())
        report_bool(checks, f"input_{Path(record['file']).name}_hash", actual_hash == record["sha256"], {"actual": actual_hash, "manifest": record["sha256"]})
    same_guides = [equal(manual.layer_image(frame, 0), automatic.layer_image(frame, 0)) for frame in range(6)]
    report_bool(checks, "manual_auto_guides_match_per_frame", all(same_guides), same_guides)
    proof_frame = proof.composite(0); export_one = exports[0]
    reopened = png(EVIDENCE / "local-revision-reopened.png")
    intended = {(77, 58), (77, 59)}
    proof_changed = set(changed_pixels(export_one, proof_frame)); reopened_changed = set(changed_pixels(export_one, reopened))
    expected_color = (249, 215, 184, 255)
    proof_pixels = {f"{x},{y}": proof_frame.getpixel((x, y)) for x, y in intended}
    # Header byte 0..3 is the overall file size; adding a correction cel changes only that value.
    protected_cels_match = (all(proof.cels.get(key) == cel for key, cel in automatic.cels.items()) and set(proof.cels) == set(automatic.cels) | {(0, 2)})
    proof_metadata_same = (proof.header[4:] == automatic.header[4:] and proof.frames == automatic.frames and proof.layers == automatic.layers and proof.palette == automatic.palette and protected_cels_match)
    protected_frames = [equal(proof.composite(i), automatic.composite(i)) for i in range(1, 6)]
    report_bool(checks, "local_revision_proof_reopened_match", equal(proof_frame, reopened), sha(proof_frame.tobytes()))
    report_bool(checks, "local_revision_exact_two_pixels", proof_changed == intended and reopened_changed == intended and all(value == expected_color for value in proof_pixels.values()), {"proof_changed": sorted(proof_changed), "reopened_changed": sorted(reopened_changed), "pixels": proof_pixels})
    report_bool(checks, "local_revision_alpha_unchanged", all(proof_frame.getpixel(point)[3] == export_one.getpixel(point)[3] for point in intended), [proof_frame.getpixel(point)[3] for point in intended])
    correction_cel = proof.cels.get((0, 2))
    correction_has_exact_marks = correction_cel is not None and set(
        changed_pixels(Image.new(RGBA, (W, H)), proof.layer_image(0, 2))
    ) == intended
    report_bool(checks, "local_revision_only_corrections_layer_changed", proof_metadata_same and all(protected_frames) and correction_has_exact_marks, {"metadata_equal": proof_metadata_same, "protected_cels_match": protected_cels_match, "protected_frames_equal": protected_frames, "correction_has_exact_marks": correction_has_exact_marks})
    gif_checks(exports, checks)
    make_contact(exports); make_source_vs_seed(exports)
    checks["native_files"] = {"manual": manual.fingerprint(), "automatic": automatic.fingerprint(), "local_revision_proof": proof.fingerprint(), "first_keys_manual": first_manual.fingerprint(), "first_keys_automatic": first_automatic.fingerprint()}
    checks["passed"] = not checks["failures"]
    (EVIDENCE / "native-checks.json").write_text(json.dumps(checks, indent=2) + "\n")
    visual = """# Visual review — two-routes starter\n\nReviewed `previews/contact-sheet.png` and `evidence/source-versus-seed.png` from the actual six native exports. The primary three-key natives preserve neutral, windup, and swing, so a beginner can work through a compact trace/cleanup exercise without having to perform a six-key animation around blank artwork.\n\nThis is usable as a beginner-practice starter: the blank hand-trace art layers provide a safe tracing route, while the automatic draft remains visibly separate with an empty Corrections layer for later cleanup. The six labeled keys remain a useful optional pose study.\n\nIt is not suitable as a final game asset. Decoded native figure heights are 92–97 pixels (about 96), with no native clipping. The small face still has little detail; the source guide retains colored-edge artifacts, and nearest sampling plus the shared 31-color palette visibly loses source detail. Foot placement also jitters relative to the source across the keys. The six-key study lacks inbetweens and returns directly from pose 6 to pose 1.\n\nNo Godot playback, final-animation claim, or art approval is claimed. This review asks only whether the starter folders are usable for user cleanup; it does not demand a finished attack or AI art cleanup.\n"""
    (EVIDENCE / "visual-review.md").write_text(visual)
    print(json.dumps({"passed": checks["passed"], "failures": checks["failures"]}, indent=2))
    return 0 if checks["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
