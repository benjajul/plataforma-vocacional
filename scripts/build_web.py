"""Inserta data/planes_comunes.json en web/rutas.template.html -> web/rutas.html (prototipo autocontenido)."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root/"data"/"planes_comunes.json").read_text(encoding="utf-8"))
tpl = (root/"web"/"rutas.template.html").read_text(encoding="utf-8")
(root/"web"/"rutas.html").write_text(tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False)), encoding="utf-8")
print("web/rutas.html listo")
