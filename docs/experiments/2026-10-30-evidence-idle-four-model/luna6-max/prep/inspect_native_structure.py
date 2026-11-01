#!/usr/bin/env python3
"""Read-only structural inventory for the frozen Aseprite input files.

This parses only headers/chunk metadata. Native drawing and production export are
reserved for the dedicated Aseprite MCP lease.
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys
from pathlib import Path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inspect(path: Path) -> dict:
    data = path.read_bytes()
    file_size, magic, frame_count, width, height, depth = struct.unpack_from("<I5H", data)
    if file_size != len(data) or magic != 0xA5E0:
        raise ValueError(f"invalid Aseprite header: {path}")
    result = {
        "path": str(path),
        "sha256": sha256(data),
        "canvas": [width, height],
        "depth": depth,
        "header_flags": struct.unpack_from("<I", data, 14)[0],
        "frame_count": frame_count,
        "frames": [],
        "layers": [],
    }
    offset = 128
    for frame_number in range(1, frame_count + 1):
        frame_length, frame_magic, old_count, duration = struct.unpack_from("<I3H", data, offset)
        if frame_magic != 0xF1FA:
            raise ValueError(f"invalid frame header at {frame_number}")
        chunks_count = struct.unpack_from("<I", data, offset + 12)[0] or old_count
        q = offset + 16
        frame = {"frame": frame_number, "duration_ms": duration, "chunks": []}
        for _ in range(chunks_count):
            length, kind = struct.unpack_from("<IH", data, q)
            chunk = data[q + 6:q + length]
            row = {"type": f"0x{kind:04x}", "bytes": length}
            if kind == 0x2004:
                flags, layer_type, level, default_width, default_height, blend_mode = struct.unpack_from("<6H", chunk)
                name_length = struct.unpack_from("<H", chunk, 16)[0]
                row.update({
                    "name": chunk[18:18 + name_length].decode("utf-8"),
                    "flags": flags,
                    "layer_type": layer_type,
                    "level": level,
                    "default_size": [default_width, default_height],
                    "blend_mode": blend_mode,
                    "opacity": chunk[12],
                })
                result["layers"].append(row)
            elif kind == 0x2005:
                layer_index, x, y, opacity, cel_type, z_index = struct.unpack_from("<HhhBHh", chunk)
                row.update({"layer_index": layer_index, "x": x, "y": y, "opacity": opacity,
                            "cel_type": cel_type, "z_index": z_index})
                if cel_type in (0, 2):
                    cel_width, cel_height = struct.unpack_from("<HH", chunk, 16)
                    row["size"] = [cel_width, cel_height]
                else:
                    row["unsupported_payload"] = "linked or tilemap cel"
            frame["chunks"].append(row)
            q += length
        if q != offset + frame_length:
            raise ValueError(f"invalid chunk boundary at frame {frame_number}")
        result["frames"].append(frame)
        offset += frame_length
    if offset != len(data):
        raise ValueError("trailing bytes after final frame")
    return result


if __name__ == "__main__":
    print(json.dumps([inspect(Path(p)) for p in sys.argv[1:]], indent=2))
