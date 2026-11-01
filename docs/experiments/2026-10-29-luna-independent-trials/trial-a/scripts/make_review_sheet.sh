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

# All generated previews are diagnostics. The source crop is labelled in the
# pass record; production remains the untrimmed 128x192 candidate.
ffmpeg -hide_banner -loglevel error -y -i "$candidate" \
  -vf "scale=128:192:flags=neighbor" -frames:v 1 "${prefix}-candidate-1x.png"
ffmpeg -hide_banner -loglevel error -y -i "$candidate" \
  -vf "scale=512:768:flags=neighbor" -frames:v 1 "${prefix}-candidate-4x.png"
ffmpeg -hide_banner -loglevel error -y -i "$source" \
  -vf "scale=128:192:flags=neighbor" -frames:v 1 "${prefix}-source-1x-preview.png"
ffmpeg -hide_banner -loglevel error -y -i "$source" \
  -vf "scale=512:768:flags=neighbor" -frames:v 1 "${prefix}-source-4x-preview.png"

for side in candidate source; do
  if [ "$side" = candidate ]; then image="${prefix}-candidate-4x.png"; else image="${prefix}-source-4x-preview.png"; fi
  ffmpeg -hide_banner -loglevel error -y \
    -f lavfi -i color=c=white:s=512x768 \
    -i "$image" -filter_complex '[0][1]overlay=0:0:format=auto' \
    -frames:v 1 "${prefix}-${side}-white-4x.png"
  ffmpeg -hide_banner -loglevel error -y \
    -f lavfi -i color=c=magenta:s=512x768 \
    -i "$image" -filter_complex '[0][1]overlay=0:0:format=auto' \
    -frames:v 1 "${prefix}-${side}-magenta-4x.png"
done

ffmpeg -hide_banner -loglevel error -y \
  -i "${prefix}-source-white-4x.png" \
  -i "${prefix}-candidate-white-4x.png" \
  -filter_complex hstack=inputs=2 -frames:v 1 "${prefix}-source-vs-candidate-white-4x.png"
ffmpeg -hide_banner -loglevel error -y \
  -i "${prefix}-source-magenta-4x.png" \
  -i "${prefix}-candidate-magenta-4x.png" \
  -filter_complex hstack=inputs=2 -frames:v 1 "${prefix}-source-vs-candidate-magenta-4x.png"
