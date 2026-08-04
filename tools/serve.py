#!/usr/bin/env python3
"""Servidor local para previsualizar el sitio. Dev-time, no se sube.

`python3 -m http.server` no arranca en este entorno (llama a os.getcwd() al
importarse y falla), así que montamos el servidor a mano con la ruta explícita.

    python3 tools/serve.py [puerto]
"""
import functools
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # En local nunca queremos caché: rompe la iteración.
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()


if __name__ == "__main__":
    handler = functools.partial(Handler, directory=str(ROOT))
    print(f"Sirviendo {ROOT} en http://localhost:{PORT}/")
    HTTPServer(("127.0.0.1", PORT), handler).serve_forever()
