#!/usr/bin/env bash
# Publica una VISTA PREVIA en la rama gh-pages.
#
# La preview lleva noindex y un robots.txt que lo prohíbe todo. Sin eso, Google
# indexaría el contenido literal de digitalizaconia.com en un segundo dominio y
# el que saldría perdiendo sería el sitio real del cliente.
#
# La rama main se queda como entregable limpio, sin rastro de la preview.
#
#   Uso:  bash tools/deploy-preview.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD="$(mktemp -d)"
cd "$ROOT"

# El sitio, sin las herramientas de desarrollo ni el repo
rsync -a --exclude tools --exclude .git --exclude .DS_Store ./ "$BUILD/"

# noindex en cada página
for f in "$BUILD"/*.html; do
  perl -0pi -e 's{(<meta name="viewport"[^>]*>)}{$1\n<meta name="robots" content="noindex, nofollow">}' "$f"
done

cat > "$BUILD/robots.txt" <<'EOF'
# Vista previa privada. La web real es https://digitalizaconia.com
User-agent: *
Disallow: /
EOF

rm -f "$BUILD/sitemap.xml"
touch "$BUILD/.nojekyll"   # que Pages no procese nada con Jekyll

git --work-tree="$BUILD" checkout --orphan gh-pages-tmp 2>/dev/null || git checkout --orphan gh-pages-tmp
git --work-tree="$BUILD" add -A
git --work-tree="$BUILD" commit -m "Vista previa $(date +%Y-%m-%d\ %H:%M)" --quiet
git branch -M gh-pages-tmp gh-pages
git push -f origin gh-pages
git checkout main --force --quiet
git reset --quiet

rm -rf "$BUILD"
echo "Vista previa publicada en la rama gh-pages."
