#!/usr/bin/env python3
"""Read-only semantic checker for the native idle candidate and its frozen inputs."""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import zlib
from pathlib import Path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_aseprite(path: Path) -> dict:
    data = path.read_bytes()
    file_size, magic, frame_count, width, height, depth = struct.unpack_from("<I5H", data)
    if file_size != len(data) or magic != 0xA5E0 or depth != 32:
        raise ValueError(f"invalid or unsupported native file: {path}")
    if width <= 0 or height <= 0:
        raise ValueError(f"invalid canvas in {path}")
    doc = {
        "path": str(path), "sha256": sha256(data), "canvas": [width, height],
        "depth": depth, "frame_count": frame_count, "header_tail": data[8:128],
        "layers": [], "frames": [], "cels": {},
    }
    offset = 128
    for frame_index in range(frame_count):
        frame_length, frame_magic, old_count, duration = struct.unpack_from("<I3H", data, offset)
        if frame_magic != 0xF1FA:
            raise ValueError(f"invalid frame header in {path} at {frame_index + 1}")
        count = struct.unpack_from("<I", data, offset + 12)[0] or old_count
        q = offset + 16
        frame = {"duration_ms": duration, "non_cel": [], "palette_chunks": []}
        deferred_links = []
        for _ in range(count):
            length, kind = struct.unpack_from("<IH", data, q)
            if length < 6 or q + length > offset + frame_length:
                raise ValueError(f"bad chunk size in {path} at frame {frame_index + 1}")
            payload = data[q + 6:q + length]
            if kind == 0x2004:
                flags, layer_type, level, child_width, child_height, blend = struct.unpack_from("<6H", payload)
                opacity = payload[12]
                name_len = struct.unpack_from("<H", payload, 16)[0]
                layer = {"name": payload[18:18 + name_len].decode("utf-8"), "flags": flags,
                         "type": layer_type, "level": level, "child_size": [child_width, child_height],
                         "blend": blend, "opacity": opacity}
                doc["layers"].append(layer)
                frame["non_cel"].append({"kind": kind, "payload_sha256": sha256(payload)})
            elif kind == 0x2005:
                layer, x, y, opacity, cel_type, z_index = struct.unpack_from("<HhhBHh", payload)
                key = (frame_index, layer)
                cel = {"layer": layer, "x": x, "y": y, "opacity": opacity, "type": cel_type,
                       "z_index": z_index, "geometry": None, "pixels": None}
                if cel_type in (0, 2):
                    cel_width, cel_height = struct.unpack_from("<HH", payload, 16)
                    raw = payload[20:] if cel_type == 0 else zlib.decompress(payload[20:])
                    if len(raw) != cel_width * cel_height * 4:
                        raise ValueError(f"bad RGBA cel payload at frame {frame_index + 1}, layer {layer}")
                    canvas_pixels = bytearray(width * height * 4)
                    src = 0
                    for cy in range(cel_height):
                        dy = y + cy
                        if not 0 <= dy < height:
                            src += cel_width * 4
                            continue
                        for cx in range(cel_width):
                            dx = x + cx
                            if 0 <= dx < width:
                                dst = (dy * width + dx) * 4
                                canvas_pixels[dst:dst + 4] = raw[src:src + 4]
                            src += 4
                    cel["geometry"] = [x, y, cel_width, cel_height]
                    cel["pixels"] = bytes(canvas_pixels)
                elif cel_type == 1:
                    linked_frame = struct.unpack_from("<H", payload, 16)[0]
                    cel["linked_frame"] = linked_frame
                else:
                    raise ValueError(f"unsupported cel type {cel_type} in {path}")
                doc["cels"][key] = cel
            else:
                entry = {"kind": kind, "payload_sha256": sha256(payload)}
                frame["non_cel"].append(entry)
                if kind == 0x2019:
                    frame["palette_chunks"].append(sha256(payload))
            q += length
        if q != offset + frame_length:
            raise ValueError(f"frame chunk boundary mismatch in {path} at frame {frame_index + 1}")
        frame["non_cel"] = sorted(frame["non_cel"], key=lambda x: (x["kind"], x["payload_sha256"]))
        doc["frames"].append(frame)
        offset += frame_length
    if offset != len(data):
        raise ValueError(f"trailing data in {path}")
    # Resolve any linked cels after all physical cels have been read.
    for key, cel in list(doc["cels"].items()):
        if cel["type"] == 1:
            target = (cel["linked_frame"], cel["layer"])
            if target not in doc["cels"]:
                raise ValueError(f"dangling linked cel in {path}: {key} -> {target}")
            visited = {key}
            while doc["cels"][target]["type"] == 1:
                if target in visited:
                    raise ValueError(f"linked cel cycle in {path}")
                visited.add(target)
                linked = doc["cels"][target]
                target = (linked["linked_frame"], linked["layer"])
            base = doc["cels"][target]
            cel["pixels"] = base["pixels"]
            cel["geometry"] = base["geometry"]
    return doc


def changed_pixels(a: bytes, b: bytes) -> list[int]:
    return [i // 4 for i in range(0, len(a), 4) if a[i:i + 4] != b[i:i + 4]]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--blink", required=True)
    ap.add_argument("--durations", required=True, help="JSON array of expected candidate frame durations")
    ap.add_argument("--edit-box", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"), required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    baseline = read_aseprite(Path(args.baseline))
    candidate = read_aseprite(Path(args.candidate))
    blink = read_aseprite(Path(args.blink))
    expected_durations = json.loads(args.durations)
    x0, y0, x1, y1 = args.edit_box
    failures = []
    layer_names = [l["name"] for l in baseline["layers"]]
    name_to_index = {name: i for i, name in enumerate(layer_names)}
    moving_layers = {"03-shirt"}
    blink_layer = "08-hair-tie-and-hair"
    static_layers = set(layer_names) - moving_layers - {blink_layer}
    if baseline["canvas"] != candidate["canvas"]:
        failures.append("canvas changed")
    if baseline["depth"] != candidate["depth"]:
        failures.append("color depth changed")
    # Aseprite's header stores the first-frame speed at bytes 18–21, in addition
    # to the per-frame durations.  That value is expected to follow the authored
    # first-frame hold; compare all other header bytes after the standard frame
    # count/file-size fields.
    base_header_metadata = baseline["header_tail"][:10] + baseline["header_tail"][14:]
    candidate_header_metadata = candidate["header_tail"][:10] + candidate["header_tail"][14:]
    if base_header_metadata != candidate_header_metadata:
        failures.append("non-timing header metadata changed")
    if baseline["layers"] != candidate["layers"]:
        failures.append("layer definitions/order/visibility changed")
    if candidate["frame_count"] != len(expected_durations):
        failures.append("frame count differs from duration profile")
    actual_durations = [f["duration_ms"] for f in candidate["frames"]]
    if actual_durations != expected_durations:
        failures.append("frame durations differ from declared profile")
    baseline_frame_non_cel = [x for x in baseline["frames"][0]["non_cel"] if x["kind"] not in (0x2018, 0x2020)]
    candidate_frame_non_cel = [x for x in candidate["frames"][0]["non_cel"] if x["kind"] not in (0x2018, 0x2020)]
    if candidate_frame_non_cel != baseline_frame_non_cel:
        failures.append("frame-one non-cel chunks changed outside the declared idle tag")
    baseline_tag_chunks = [x for x in baseline["frames"][0]["non_cel"] if x["kind"] == 0x2018]
    candidate_tag_chunks = [x for x in candidate["frames"][0]["non_cel"] if x["kind"] == 0x2018]
    if baseline_tag_chunks or len(candidate_tag_chunks) != 1:
        failures.append("candidate must add exactly one declared animation tag chunk")
    baseline_tag_user_data = [x for x in baseline["frames"][0]["non_cel"] if x["kind"] == 0x2020]
    candidate_tag_user_data = [x for x in candidate["frames"][0]["non_cel"] if x["kind"] == 0x2020]
    if baseline_tag_user_data or len(candidate_tag_user_data) != 1:
        failures.append("candidate must add exactly one tag user-data chunk for the colored idle tag")
    candidate_palette = [digest for frame in candidate["frames"] for digest in frame["palette_chunks"]]
    baseline_palette = [digest for frame in baseline["frames"] for digest in frame["palette_chunks"]]
    if sorted(candidate_palette) != sorted(baseline_palette) * candidate["frame_count"]:
        # Palette chunks may be stored only once. In that case require the exact same
        # unique payload; if copied to each frame, every copy must match the input.
        if set(candidate_palette) != set(baseline_palette):
            failures.append("palette chunk differs or an extra palette was introduced")
    if baseline["sha256"] == candidate["sha256"]:
        failures.append("candidate unexpectedly has the exact baseline file hash")

    reports = []
    if candidate["frame_count"] >= 10 and blink["frame_count"] >= 7:
        for frame_number in range(1, candidate["frame_count"] + 1):
            frame_index = frame_number - 1
            layer_changes = []
            for name, layer_index in name_to_index.items():
                base_cel = baseline["cels"].get((0, layer_index))
                cand_cel = candidate["cels"].get((frame_index, layer_index))
                if base_cel is None or cand_cel is None:
                    failures.append(f"missing cel for frame {frame_number}, layer {name}")
                    continue
                diffs = changed_pixels(base_cel["pixels"], cand_cel["pixels"])
                if not diffs:
                    continue
                xs = [p % baseline["canvas"][0] for p in diffs]
                ys = [p // baseline["canvas"][0] for p in diffs]
                row = {"layer": name, "changed_pixels": len(diffs), "bounds": [min(xs), min(ys), max(xs) + 1, max(ys) + 1]}
                if name in moving_layers and frame_number in range(2, 7):
                    if any(not (x0 <= x < x1 and y0 <= y < y1) for p in diffs for x, y in [(p % baseline["canvas"][0], p // baseline["canvas"][0])]):
                        failures.append(f"breathing edit outside declared torso box in frame {frame_number}, layer {name}")
                elif name == blink_layer and frame_number in (8, 9, 10):
                    blink_index = frame_number - 8 + 4  # candidate F8–10 <- blink source F5–7
                    expected = blink["cels"].get((blink_index, layer_index))
                    if expected is None or cand_cel["pixels"] != expected["pixels"]:
                        failures.append(f"inherited blink head does not match blink-source frame {blink_index + 1}")
                else:
                    failures.append(f"unexpected native pixel change in frame {frame_number}, layer {name}")
                layer_changes.append(row)
            reports.append({"frame": frame_number, "duration_ms": actual_durations[frame_index] if frame_index < len(actual_durations) else None,
                            "changed_layers": layer_changes})
    else:
        failures.append("candidate or blink source has too few frames for the declared profile")
    result = {
        "passed": not failures,
        "failures": failures,
        "baseline_sha256": baseline["sha256"],
        "candidate_sha256": candidate["sha256"],
        "canvas": candidate["canvas"],
        "layers_equal": baseline["layers"] == candidate["layers"],
        "header_timing_speed_ms": {"baseline": struct.unpack_from("<I", Path(baseline["path"]).read_bytes(), 18)[0],
                                    "candidate": struct.unpack_from("<I", Path(candidate["path"]).read_bytes(), 18)[0]},
        "added_tag_chunks": len(candidate_tag_chunks),
        "tag_user_data_chunks_0x2020": candidate_tag_user_data,
        "candidate_frame_count": candidate["frame_count"],
        "actual_durations_ms": actual_durations,
        "expected_durations_ms": expected_durations,
        "edit_box": [x0, y0, x1, y1],
        "frame_diffs": reports,
    }
    Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
