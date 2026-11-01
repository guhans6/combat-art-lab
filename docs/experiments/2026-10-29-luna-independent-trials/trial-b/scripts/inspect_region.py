from collections import Counter
from pathlib import Path
import sys

from PIL import Image

path = Path(sys.argv[1])
x0, y0, x1, y1 = map(int, sys.argv[2:6])
image = Image.open(path).convert("RGBA")
colors = [
    image.getpixel((x, y))[:3]
    for y in range(y0, y1)
    for x in range(x0, x1)
    if image.getpixel((x, y))[3]
]
ordered = [color for color, _ in Counter(colors).most_common()]
alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
if len(ordered) > len(alphabet):
    raise SystemExit("Too many colors for compact legend")
glyph = dict(zip(ordered, alphabet))
print(f"x={x0}..{x1-1} y={y0}..{y1-1}")
print("   " + "".join(str((x // 10) % 10) for x in range(x0, x1)))
print("   " + "".join(str(x % 10) for x in range(x0, x1)))
for y in range(y0, y1):
    row = "".join(
        glyph.get(image.getpixel((x, y))[:3], ".") if image.getpixel((x, y))[3] else "."
        for x in range(x0, x1)
    )
    print(f"{y:3} {row}")
print("\n".join(f"{glyph[c]} #{c[0]:02x}{c[1]:02x}{c[2]:02x}" for c in ordered))
