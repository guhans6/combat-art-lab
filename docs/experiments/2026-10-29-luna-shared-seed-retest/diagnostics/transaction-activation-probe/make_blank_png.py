#!/usr/bin/env python3
"""Create the deterministic non-art input for the headless transaction probe."""
import hashlib
import struct
import zlib
from pathlib import Path

out = Path(__file__).with_name("opened-blank-16.png")
rgba = bytes(16 * 16 * 4)
rows = b"".join(b"\0" + rgba[row * 64:(row + 1) * 64] for row in range(16))
def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 16, 16, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b"")
out.write_bytes(png)
print(f"{out}: {hashlib.sha256(png).hexdigest()}")
