#!/bin/sh
set -eu

if [ "$#" -ne 2 ]; then
  echo "usage: $0 CANDIDATE_PNG OUTPUT_PREFIX" >&2
  exit 2
fi

candidate="$1"
prefix="$2"
run="/Users/guhan/Guhan/Projects/combat-art-lab/docs/experiments/2026-10-29-luna-independent-trials/trial-a"
source="$run/input/primary-clean-cutout-v1.png"

# This version keeps the candidate and source in separate, explicit RGBA inputs,
# composites each onto the same solid background, and emits alpha masks beside the
# color sheets. It is intended to make transparency/framing disagreements auditable.
for side in source candidate; do
  if [ "$side" = candidate ]; then image="$candidate"; else image="$source"; fi
  ffmpeg -hide_banner -loglevel error -y -i "$image" \
    -vf "format=rgba,scale=512:768:flags=neighbor" -frames:v 1 "${prefix}-${side}-rgba-4x.png"
  ffmpeg -hide_banner -loglevel error -y \
    -f lavfi -i color=c=white:s=512x768 -i "${prefix}-${side}-rgba-4x.png" \
    -filter_complex '[0][1]overlay=shortest=1:format=auto,format=rgba' \
    -frames:v 1 "${prefix}-${side}-white-4x.png"
  ffmpeg -hide_banner -loglevel error -y \
    -f lavfi -i color=c=magenta:s=512x768 -i "${prefix}-${side}-rgba-4x.png" \
    -filter_complex '[0][1]overlay=shortest=1:format=auto,format=rgba' \
    -frames:v 1 "${prefix}-${side}-magenta-4x.png"
  ffmpeg -hide_banner -loglevel error -y -i "${prefix}-${side}-rgba-4x.png" \
    -vf "alphaextract,format=gray" -frames:v 1 "${prefix}-${side}-alpha-4x.png"
done

ffmpeg -hide_banner -loglevel error -y \
  -i "${prefix}-source-white-4x.png" -i "${prefix}-candidate-white-4x.png" \
  -filter_complex hstack=inputs=2 -frames:v 1 "${prefix}-source-vs-candidate-white-4x.png"
ffmpeg -hide_banner -loglevel error -y \
  -i "${prefix}-source-magenta-4x.png" -i "${prefix}-candidate-magenta-4x.png" \
  -filter_complex hstack=inputs=2 -frames:v 1 "${prefix}-source-vs-candidate-magenta-4x.png"
ffmpeg -hide_banner -loglevel error -y \
  -i "${prefix}-source-alpha-4x.png" -i "${prefix}-candidate-alpha-4x.png" \
  -filter_complex hstack=inputs=2 -frames:v 1 "${prefix}-source-vs-candidate-alpha-4x.png"

file "${prefix}-source-rgba-4x.png" "${prefix}-candidate-rgba-4x.png" \
  "${prefix}-source-vs-candidate-alpha-4x.png"
