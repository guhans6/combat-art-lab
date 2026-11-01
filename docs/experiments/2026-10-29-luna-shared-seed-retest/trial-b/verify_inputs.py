#!/usr/bin/env python3
"""Independently verify trial-b's copied shared fixture and extract its ordered palette."""
from __future__ import annotations

import hashlib
import json
import struct
import zlib
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "input"
EXPECTED = {
    "seed": "074168d9bfc5b2a2f2751810152bb0c31a71e7027a5368c0b393e17449fb84eb",
    "native": "b1d91f6f87f650cbd2cae3edb69704d195bbdcf8d6b679b287d01e8a7283cc19",
    "baseline_png": "7353611071482ea1e879ab9c247fb1d92c7bd90050b8eb99cbec4cdbdf612d12",
    "decoded_rgba": "8839680f1bc70c1c99653a28c76c6f8ea41f401d2755c93146d765523cb5806c",
    "palette_chunk": "f2d4907a7493af8e6557f933e3c2c40d73f733658fc8250d925f79678ffb5b81",
    "references": {
        "character-scene.png": "a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae",
        "character-closeup.png": "0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7",
        "clean-generated-cutout-v1.png": "12e971cc9e3cbfa7add2a17a62ff53d1f45b3c55197ce23c336a6447bed1f49e",
    },
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_aseprite(path: Path) -> dict:
    data = path.read_bytes()
    if struct.unpack_from("<H", data, 4)[0] != 0xA5E0:
        raise ValueError("Unexpected Aseprite file magic")
    frame_count = struct.unpack_from("<H", data, 6)[0]
    width, height, depth = struct.unpack_from("<HHH", data, 8)
    offset = 128
    frames = []
    for _ in range(frame_count):
        frame_size, frame_magic, chunk_count, duration = struct.unpack_from("<IHHH", data, offset)
        if frame_magic != 0xF1FA:
            raise ValueError("Unexpected frame magic")
        cursor = offset + 16
        chunks = []
        for _ in range(chunk_count):
            size, kind = struct.unpack_from("<IH", data, cursor)
            payload = data[cursor + 6 : cursor + size]
            chunks.append((kind, payload))
            cursor += size
        if cursor != offset + frame_size:
            raise ValueError("Frame size does not match parsed chunks")
        frames.append({"duration_ms": duration, "chunks": chunks})
        offset += frame_size
    if offset != len(data):
        raise ValueError("File size does not match parsed frames")
    return {"bytes": data, "frame_count": frame_count, "width": width, "height": height, "depth": depth, "frames": frames}


def main() -> None:
    seed_path = INPUT / "seed.png"
    baseline_png_path = INPUT / "seed-baseline.png"
    native_path = INPUT / "seed-baseline.aseprite"
    seed_file = seed_path.read_bytes()
    baseline_png_file = baseline_png_path.read_bytes()
    native = read_aseprite(native_path)

    assert sha(seed_file) == EXPECTED["seed"]
    assert sha(baseline_png_file) == EXPECTED["baseline_png"]
    assert sha(native["bytes"]) == EXPECTED["native"]
    assert (native["width"], native["height"], native["depth"], native["frame_count"]) == (128, 192, 32, 1)

    chunks = native["frames"][0]["chunks"]
    palettes = [p for kind, p in chunks if kind == 0x2019]
    layers = [p for kind, p in chunks if kind == 0x2004]
    cels = [p for kind, p in chunks if kind == 0x2005]
    assert len(palettes) == len(layers) == len(cels) == 1

    palette_payload = palettes[0]
    assert sha(palette_payload) == EXPECTED["palette_chunk"]
    palette_size, first_index, last_index = struct.unpack_from("<III", palette_payload, 0)
    assert (palette_size, first_index, last_index) == (255, 0, 254)
    cursor = 20
    entries = []
    for index in range(first_index, last_index + 1):
        flags = struct.unpack_from("<H", palette_payload, cursor)[0]
        rgba = list(palette_payload[cursor + 2 : cursor + 6])
        cursor += 6
        name = None
        if flags & 1:
            name_len = struct.unpack_from("<H", palette_payload, cursor)[0]
            cursor += 2
            name = palette_payload[cursor : cursor + name_len].decode("utf-8")
            cursor += name_len
        entries.append({"index": index, "flags": flags, "rgba": rgba, "name": name})
    assert cursor == len(palette_payload)
    (INPUT / "palette-chunk.bin").write_bytes(palette_payload)
    (INPUT / "ordered-palette.json").write_text(
        json.dumps({"source": "seed-baseline.aseprite palette chunk 0x2019", "sha256": sha(palette_payload), "entries": entries}, indent=2) + "\n",
        encoding="utf-8",
    )

    layer = layers[0]
    name_len = struct.unpack_from("<H", layer, 16)[0]
    layer_name = layer[18 : 18 + name_len].decode("utf-8")
    assert layer_name == "shared-source-seed", layer_name

    cel = cels[0]
    layer_index, cel_x, cel_y, opacity, cel_type, z_index = struct.unpack_from("<HhhBHh", cel, 0)
    cel_width, cel_height = struct.unpack_from("<HH", cel, 16)
    assert (layer_index, cel_x, cel_y, opacity, cel_type, z_index, cel_width, cel_height) == (0, 0, 0, 255, 2, 0, 128, 192)
    decoded = zlib.decompress(cel[20:])
    assert len(decoded) == 128 * 192 * 4
    assert sha(decoded) == EXPECTED["decoded_rgba"]

    seed = Image.open(seed_path).convert("RGBA")
    baseline_png = Image.open(baseline_png_path).convert("RGBA")
    assert seed.size == baseline_png.size == (128, 192)
    assert seed.tobytes() == baseline_png.tobytes() == decoded
    alpha_values = sorted(set(seed.getchannel("A").getdata()))
    visible_count = sum(a != 0 for a in seed.getchannel("A").getdata())
    visible_colors = len({pixel[:3] for pixel in seed.getdata() if pixel[3] != 0})
    assert alpha_values == [0, 255]
    assert (visible_count, visible_colors) == (7844, 254)

    ref_hashes = {}
    for name, expected in EXPECTED["references"].items():
        path = INPUT / "references" / name
        actual = sha(path.read_bytes())
        assert actual == expected
        image = Image.open(path)
        ref_hashes[name] = {"sha256": actual, "dimensions": list(image.size)}

    manifest = {
        "verification": "PASS",
        "method": "Python binary parsing of the copied Aseprite baseline plus Pillow RGBA decode; no editor operation",
        "python_version": __import__("sys").version.split()[0],
        "pillow_version": __import__("PIL").__version__,
        "native_baseline": {"sha256": sha(native["bytes"]), "dimensions": [128, 192], "depth": 32, "frames": 1, "layers": [layer_name], "decoded_rgba_sha256": sha(decoded), "palette_chunk_sha256": sha(palette_payload), "palette_entry_count": len(entries)},
        "seed_png": {"sha256": sha(seed_file), "dimensions": list(seed.size), "decoded_rgba_sha256": sha(seed.tobytes()), "visible_pixel_count": visible_count, "visible_rgb_color_count": visible_colors, "alpha_values": alpha_values},
        "baseline_export_png": {"sha256": sha(baseline_png_file), "decoded_rgba_equal_seed_and_native_cel": True},
        "references": ref_hashes,
    }
    (INPUT / "input-verification.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    print("ordered palette entries:", len(entries))


if __name__ == "__main__":
    main()
