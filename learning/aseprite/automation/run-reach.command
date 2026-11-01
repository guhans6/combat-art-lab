#!/bin/bash
set -euo pipefail
conversion_dir="$(cd "$(dirname "$0")" && pwd)"
conversion_python='/Users/guhan/.cache/uv/archive-v0/p206aF9kQeX4fKy0/bin/python'
if [[ ! -x "$conversion_python" ]]; then conversion_python=python3; fi
"$conversion_python" -c 'import PIL; from PIL import Image; assert hasattr(Image.Image, "get_flattened_data"), "Pillow 13+ required"'
conversion_output="${1:-$conversion_dir/../practice/reach-run-$(date +%Y%m%d-%H%M%S)}"
exec "$conversion_python" "$conversion_dir/convert_image.py" --recipe "$conversion_dir/reach.json" --out "$conversion_output"
