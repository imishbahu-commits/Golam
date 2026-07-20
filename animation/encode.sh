#!/usr/bin/env bash
# Encode a PNG frame sequence into a professional-quality MP4 with ffmpeg.
# Usage: ./encode.sh <frames_dir> <fps> <output.mp4>
set -e
DIR="${1:-animation/output/blender}"
FPS="${2:-24}"
OUT="${3:-animation/output/render.mp4}"

mkdir -p "$(dirname "$OUT")"

# libx264, CRF 18 = visually near-lossless, yuv420p for max compatibility.
# Add -pix_fmt yuv420p and faststart for web playback.
ffmpeg -y -framerate "$FPS" -i "$DIR/frame_%04d.png" \
  -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart \
  -vf "format=yuv420p" "$OUT"

echo "Encoded -> $OUT"
