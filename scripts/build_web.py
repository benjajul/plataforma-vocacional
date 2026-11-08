"""Inserta data/planes_comunes.json en web/rutas.template.html.

Genera web/index.html (portada del sitio publicado) y web/rutas.html (misma página, nombre usado por el prototipo).
"""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root/"data"/"planes_comunes.json").read_text(encoding="utf-8"))
tpl = (root/"web"/"rutas.template.html").read_text(encoding="utf-8")
body = tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False))
# El template está pensado para el artifact (sin <html>/<head>); para GitHub Pages se envuelve en un documento completo.
import re
head_bits = re.findall(r'^(?:<title>.*?</title>|<link [^>]*>)\s*$', body, flags=re.M)
for b in head_bits:
    body = body.replace(b, "", 1)
body = re.sub(r'^<meta name="claude:[^>]*>\s*$', "", body, flags=re.M)
page = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + "\n".join(head_bits) + '\n<style>body{margin:0}</style>\n</head>\n<body>\n' + body.strip() + '\n</body>\n</html>\n')
for name in ("index.html", "rutas.html"):
    (root/"web"/name).write_text(page, encoding="utf-8")
(root/"web"/".nojekyll").write_text("", encoding="utf-8")
print("web/index.html y web/rutas.html listos")
