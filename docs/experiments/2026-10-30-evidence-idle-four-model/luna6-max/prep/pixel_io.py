#!/usr/bin/env python3
"""Small standard-library pixel helpers for faithful read-only verification."""
from __future__ import annotations

import hashlib
import struct
import zlib
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else (b if pb <= pc else c)


def read_png(path: str | Path) -> tuple[int, int, bytes]:
    """Decode non-interlaced 8-bit RGBA or RGB PNGs to tightly packed RGBA."""
    data = Path(path).read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError(f"not a PNG: {path}")
    pos = len(PNG_SIGNATURE)
    idat = bytearray()
    width = height = bit_depth = color_type = interlace = None
    while pos < len(data):
        length = struct.unpack_from(">I", data, pos)[0]
        kind = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + length]
        if kind == b"IHDR":
            width, height, bit_depth, color_type, compression, filtering, interlace = struct.unpack(">IIBBBBB", chunk)
            if compression or filtering:
                raise ValueError("unsupported PNG compression/filter method")
        elif kind == b"IDAT":
            idat.extend(chunk)
        elif kind == b"IEND":
            break
        pos += 12 + length
    if bit_depth != 8 or interlace != 0 or color_type not in (2, 6):
        raise ValueError(f"unsupported PNG format: depth={bit_depth}, type={color_type}, interlace={interlace}")
    channels = 4 if color_type == 6 else 3
    bpp = channels
    raw = zlib.decompress(bytes(idat))
    stride = width * channels
    expected = height * (stride + 1)
    if len(raw) != expected:
        raise ValueError(f"bad PNG data size for {path}: {len(raw)} != {expected}")
    rows: list[bytearray] = []
    cursor = 0
    for y in range(height):
        mode = raw[cursor]
        scan = bytearray(raw[cursor + 1:cursor + 1 + stride])
        cursor += 1 + stride
        prior = rows[y - 1] if y else bytearray(stride)
        for i in range(stride):
            left = scan[i - bpp] if i >= bpp else 0
            up = prior[i]
            upper_left = prior[i - bpp] if i >= bpp else 0
            if mode == 1:
                scan[i] = (scan[i] + left) & 255
            elif mode == 2:
                scan[i] = (scan[i] + up) & 255
            elif mode == 3:
                scan[i] = (scan[i] + ((left + up) >> 1)) & 255
            elif mode == 4:
                scan[i] = (scan[i] + _paeth(left, up, upper_left)) & 255
            elif mode != 0:
                raise ValueError(f"unknown PNG filter {mode}")
        rows.append(scan)
    if channels == 4:
        return width, height, b"".join(rows)
    out = bytearray(width * height * 4)
    dst = 0
    for row in rows:
        for i in range(0, len(row), 3):
            out[dst:dst + 4] = bytes((row[i], row[i + 1], row[i + 2], 255))
            dst += 4
    return width, height, bytes(out)


def _chunk(kind: bytes, payload: bytes) -> bytes:
    body = kind + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def write_png(path: str | Path, width: int, height: int, rgba: bytes) -> None:
    if len(rgba) != width * height * 4:
        raise ValueError("RGBA byte length does not match dimensions")
    scanlines = b"".join(b"\x00" + rgba[y * width * 4:(y + 1) * width * 4] for y in range(height))
    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    payload = PNG_SIGNATURE + _chunk(b"IHDR", header) + _chunk(b"IDAT", zlib.compress(scanlines, 9)) + _chunk(b"IEND", b"")
    Path(path).write_bytes(payload)


def matte(rgba: bytes, color: tuple[int, int, int] = (128, 128, 128)) -> bytes:
    out = bytearray(len(rgba))
    mr, mg, mb = color
    for i in range(0, len(rgba), 4):
        a = rgba[i + 3]
        inv = 255 - a
        out[i] = (rgba[i] * a + mr * inv + 127) // 255
        out[i + 1] = (rgba[i + 1] * a + mg * inv + 127) // 255
        out[i + 2] = (rgba[i + 2] * a + mb * inv + 127) // 255
        out[i + 3] = 255
    return bytes(out)


def scale_nearest(width: int, height: int, rgba: bytes, factor: int) -> tuple[int, int, bytes]:
    if factor < 1:
        raise ValueError("scale factor must be a positive integer")
    out_width, out_height = width * factor, height * factor
    out = bytearray(out_width * out_height * 4)
    row_bytes = width * 4
    for y in range(height):
        row = rgba[y * row_bytes:(y + 1) * row_bytes]
        expanded = b"".join(row[x * 4:(x + 1) * 4] * factor for x in range(width))
        for yy in range(y * factor, (y + 1) * factor):
            start = yy * out_width * 4
            out[start:start + len(expanded)] = expanded
    return out_width, out_height, bytes(out)


def pixel_sha256(width: int, height: int, rgba: bytes) -> str:
    return hashlib.sha256(struct.pack(">II", width, height) + rgba).hexdigest()

