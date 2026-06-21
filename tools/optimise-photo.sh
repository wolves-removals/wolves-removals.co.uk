#!/bin/bash
# Optimise ONE photo straight into images/photos/ — the single image folder.
#
# Bakes EXIF orientation (never sideways), resizes to 1600px longest edge, and encodes
# an upright WebP <=200KB with a quality search. This is the whole "add a photo" workflow
# now: pick the source (from Mark Photos/, a download, anywhere) and run this — it lands
# the finished, site-ready WebP in images/photos/ with your descriptive name. No staging,
# no second folder.
#
#   tools/optimise-photo.sh <source-image> <descriptive-kebab-name>
#   e.g. tools/optimise-photo.sh "Mark Photos/IMG_5107.PNG" wolves-team-loading-van
#
# Then reference it on a page (or add it to data/library_photos.py for the rotation pool).
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/images/photos"
TMP="${TMPDIR:-/tmp}/optimise-photo.$$"
MAX=204800          # 200 KB
EDGE=1600           # longest edge px

src="${1:-}"; name="${2:-}"
if [ -z "$src" ] || [ -z "$name" ]; then
  echo "usage: tools/optimise-photo.sh <source-image> <descriptive-kebab-name>"; exit 1
fi
[ -f "$src" ] || { echo "source not found: $src"; exit 1; }
# enforce a descriptive, kebab-case name (matches the audit's filename rule)
name="${name%.webp}"
if ! printf '%s' "$name" | grep -qE '^[a-z0-9]+(-[a-z0-9]+){2,5}$'; then
  echo "name must be 3-6 kebab-case words, e.g. wolves-team-loading-van (got: $name)"; exit 1
fi
mkdir -p "$TMP" "$OUT"
ext="${src##*.}"; extl=$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')

# normalise -> bake orientation + resize (PNG kept as PNG to preserve transparency)
if [ "$extl" = "png" ]; then
  tmp="$TMP/n.png"; sips -s format png -Z "$EDGE" "$src" --out "$tmp" >/dev/null 2>&1
else
  tmp="$TMP/n.jpg"; sips -s format jpeg -Z "$EDGE" "$src" --out "$tmp" >/dev/null 2>&1
fi
[ -f "$tmp" ] || { echo "could not read $src"; rm -rf "$TMP"; exit 1; }

out="$OUT/$name.webp"
for q in 84 76 68 60 52 44 38; do
  cwebp -quiet -q "$q" -m 6 "$tmp" -o "$out" >/dev/null 2>&1
  [ "$(stat -f%z "$out" 2>/dev/null || echo 999999)" -le "$MAX" ] && break
done
kb=$(( ( $(stat -f%z "$out") + 512 ) / 1024 ))
dims=$(sips -g pixelWidth -g pixelHeight "$out" 2>/dev/null | awk '/pixelWidth/{w=$2}/pixelHeight/{h=$2}END{print w"x"h}')
rm -rf "$TMP"
echo "wrote images/photos/$name.webp  (${kb}KB, ${dims})"
