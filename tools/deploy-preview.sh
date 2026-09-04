#!/usr/bin/env bash
# Publica una VISTA PREVIA en la rama gh-pages.
#
# La preview lleva noindex y un robots.txt que lo prohíbe todo. Sin eso, Google
# indexaría el contenido literal de digitalizaconia.com en un segundo dominio y
# el que saldría perdiendo sería el sitio real del cliente.
#
# Este script NO toca tu árbol de trabajo ni cambia de rama: construye en un
# directorio temporal, lo convierte en un repo desechable y empuja desde ahí.
# La versión anterior hacía checkout de una rama huérfana en el repo real y,
# cuando algo fallaba a mitad, dejaba el repo colgado y podía descartar
# cambios sin guardar.
#
#   Uso:  bash tools/deploy-preview.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD="$(mktemp -d)"
trap 'rm -rf "$BUILD"' EXIT

REMOTE="$(git -C "$ROOT" remote get-url origin)"
NAME="$(git -C "$ROOT" config user.name  || echo 'DigitalizaConIA deploy')"
MAIL="$(git -C "$ROOT" config user.email || echo 'deploy@digitalizaconia.com')"

# El sitio, sin las herramientas de desarrollo ni el historial
rsync -a --exclude tools --exclude .git --exclude .gitignore --exclude .DS_Store \
      "$ROOT"/ "$BUILD"/

# noindex en cada página
for f in "$BUILD"/*.html; do
  perl -0pi -e 's{(<meta name="viewport"[^>]*>)}{$1\n<meta name="robots" content="noindex, nofollow">}' "$f"
done

cat > "$BUILD/robots.txt" <<'EOF'
# Vista previa privada. La web real es https://digitalizaconia.com
User-agent: *
Disallow: /
EOF

# El sitemap apunta al dominio real: no pinta nada en una preview
rm -f "$BUILD/sitemap.xml"
touch "$BUILD/.nojekyll"   # que Pages no procese nada con Jekyll

git -C "$BUILD" init -q -b gh-pages
git -C "$BUILD" add -A
git -C "$BUILD" -c user.name="$NAME" -c user.email="$MAIL" \
    commit -q -m "Vista previa $(date '+%Y-%m-%d %H:%M')"
git -C "$BUILD" push -q -f "$REMOTE" gh-pages

echo "Vista previa publicada: https://riosdc25.github.io/digitalizaconia/"
