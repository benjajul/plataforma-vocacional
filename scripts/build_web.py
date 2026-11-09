"""Genera el sitio estático en web/ a partir de los templates, web/base.css y los datos.

Páginas: index (Explorar), rutas (planes comunes), habilidades, simulador, cuestionario.
Los templates no traen <html>/<head> (mismo formato que los artifacts); aquí se envuelven en un documento completo.
Marcadores: __DATA__ (JSON), __NAV__ (menú), __BASE_CSS__ (estilos comunes).
"""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
web = root / "web"
PAGINAS = [  # (archivo, etiqueta del menú, template, datos)
    ("index.html", "Explorar", "explorar.template.html", "plataforma.json"),
    ("rutas.html", "Rutas de ingreso", "rutas.template.html", "planes_comunes.json"),
    ("habilidades.html", "Habilidades", "habilidades.template.html", "habilidades.json"),
    ("simulador.html", "Simulador", "simulador.template.html", "plataforma.json"),
    ("cuestionario.html", "Cuestionario", "cuestionario.template.html", "plataforma.json"),
]
BASE_CSS = (web / "base.css").read_text(encoding="utf-8")

def nav(actual, base=""):
    links = "".join(f'<a href="{base}{a}"{" aria-current=\"page\"" if a == actual else ""}>{lbl}</a>' for a, lbl, _, _ in PAGINAS)
    return f'<nav class="topnav" aria-label="Secciones">{links}</nav>'

def cuerpo(archivo, template, datos, base=""):
    data = json.loads((root / "data" / datos).read_text(encoding="utf-8"))
    t = (web / template).read_text(encoding="utf-8")
    return (t.replace("__BASE_CSS__", BASE_CSS).replace("__NAV__", nav(archivo, base))
             .replace("__DATA__", json.dumps(data, ensure_ascii=False)))

def documento(body):
    head_bits = re.findall(r'^(?:<title>.*?</title>|<link [^>]*>)\s*$', body, flags=re.M)
    for b in head_bits:
        body = body.replace(b, "", 1)
    body = re.sub(r'^<meta name="claude:[^>]*>\s*$', "", body, flags=re.M)
    return ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + "\n".join(head_bits) + '\n</head>\n<body>\n' + body.strip() + '\n</body>\n</html>\n')

if __name__ == "__main__":
    for archivo, _, template, datos in PAGINAS:
        (web / archivo).write_text(documento(cuerpo(archivo, template, datos)), encoding="utf-8")
    (web / ".nojekyll").write_text("", encoding="utf-8")
    print("listas:", ", ".join(p[0] for p in PAGINAS))
