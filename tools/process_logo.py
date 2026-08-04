#!/usr/bin/env python3
"""Dev-time: convierte el logo original (PNG 1600x1600, fondo blanco, 3 MB)
en un logo con fondo transparente listo para el fondo oscuro del sitio.

No se sube al hosting. Uso:
    python3 tools/process_logo.py <origen.png>
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"


def strip_white(im, threshold=228):
    """Hace transparente todo pixel casi blanco, con alfa progresivo en el borde
    para que no queden dientes de sierra."""
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            lum = max(r, g, b)
            if lum >= 250:
                px[x, y] = (r, g, b, 0)
            elif lum >= threshold:
                # borde: alfa proporcional a lo lejos que esté del blanco
                fade = int(255 * (250 - lum) / (250 - threshold))
                px[x, y] = (r, g, b, min(a, fade))
    return im


def drop_greys(im):
    """El original lleva el wordmark 'DCIA' en gris oscuro (#404040), que sobre
    fondo oscuro no se ve. La marca del cerebro es teal/verde saturada, así que
    la saturación separa limpiamente una cosa de la otra: fuera los grises."""
    im = im.convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            hi, lo = max(r, g, b), min(r, g, b)
            sat = 0 if hi == 0 else (hi - lo) / hi
            if sat < 0.22:
                px[x, y] = (r, g, b, 0)
    return im


def trim(im, pad=8):
    box = im.getbbox()
    if not box:
        return im
    l, t, r, b = box
    l, t = max(0, l - pad), max(0, t - pad)
    r, b = min(im.width, r + pad), min(im.height, b + pad)
    return im.crop((l, t, r, b))


def square(im):
    """Centra sobre un lienzo cuadrado transparente."""
    side = max(im.size)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2), im)
    return canvas


def main():
    src = Path(sys.argv[1])
    im = square(trim(drop_greys(strip_white(Image.open(src)))))
    OUT.mkdir(parents=True, exist_ok=True)

    # En el sitio se muestra a ~40px de alto; 256 cubre pantallas 2x de sobra.
    im.resize((256, 256), Image.LANCZOS).save(
        OUT / "logo-dcia.webp", "WEBP", quality=86, method=6
    )
    # Favicon: se ve a 16-32px, así que 64 colores sobran y pesa una cuarta parte.
    fav = im.resize((180, 180), Image.LANCZOS).quantize(
        colors=64, method=Image.FASTOCTREE
    )
    fav.save(OUT / "favicon.png", "PNG", optimize=True)

    for f in ("logo-dcia.webp", "favicon.png"):
        p = OUT / f
        print(f"  {f:20} {p.stat().st_size / 1024:7.1f} KB")


if __name__ == "__main__":
    main()
