#!/bin/sh
set -eu

repo="/Users/guhan/Guhan/Projects/combat-art-lab"
run="$repo/docs/experiments/2026-10-29-luna-independent-trials/trial-a"
source="$run/input/primary-clean-cutout-v1.png"
out="$run/work/converted-seed.png"
clean="$run/work/seed-alpha-clean.png"

# The supplied cutout is exactly 8x the frozen 128x192 target.  Nearest-neighbour
# reduction preserves its deliberate source clusters and alpha without adding a
# filter pass; all authored cleanup happens later in the native editor.
ffmpeg -hide_banner -loglevel error -y -i "$source" \
  -vf "scale=128:192:flags=neighbor,format=rgba" -frames:v 1 "$out"

# The source carries low-alpha halo samples around an otherwise crisp cutout.
# Keep the reviewed spatial silhouette while converting retained coverage to
# opaque native pixels; values at or below 16 become transparent.
ffmpeg -hide_banner -loglevel error -y -i "$out" \
  -vf "lut=a='if(gt(val,16),255,0)'" -frames:v 1 "$clean"

file "$out"
shasum -a 256 "$out"
file "$clean"
shasum -a 256 "$clean"
