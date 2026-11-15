"""Extrae de la base 'Buscador de Empleabilidad e Ingresos' (SIES/Mi Futuro, Mineduc) las filas de las universidades en FOCO.

Uso: python3 scripts/parse_mifuturo.py Buscador_Empleabilidad_ingresos_2025_2026_SIES.xlsx
Salida: data/mifuturo_2025_2026.json (solo las 5 universidades; el xlsx original no se guarda en el repo).
Fuente de descarga: https://www.mifuturo.cl/mi-futuro-buscadores/  (Benjamín la descargó el 15-11-2026)
Datos por institución y carrera, sin distinguir sede.
"""
import json, pathlib, re, sys
import openpyxl

ROOT = pathlib.Path(__file__).resolve().parent.parent
INST = {"UNIVERSIDAD DE CHILE": "uchile", "PONTIFICIA UNIVERSIDAD CATOLICA DE CHILE": "uc",
        "UNIVERSIDAD TECNICA FEDERICO SANTA MARIA": "usm", "UNIVERSIDAD DE SANTIAGO DE CHILE": "usach",
        "UNIVERSIDAD DIEGO PORTALES": "udp"}

def num(v):
    return round(v, 4) if isinstance(v, (int, float)) else None

def millones(txt):
    """'De $2 millones 400 mil a $2 millones 500 mil' -> (2.4, 2.5); 'Sobre $3 millones 500 mil' -> (3.5, None)"""
    if not isinstance(txt, str) or "$" not in txt:
        return None, None
    vals = []
    for m in re.finditer(r"\$(\d+)\s*mill[oó]n(?:es)?(?:\s*(\d+)\s*mil)?|\$(\d+)\s*mil", txt):
        if m.group(3):
            vals.append(int(m.group(3)) / 1000)
        else:
            vals.append(int(m.group(1)) + (int(m.group(2)) / 1000 if m.group(2) else 0))
    if txt.strip().lower().startswith("sobre"):
        return (vals[0] if vals else None), None
    return (vals[0] if vals else None), (vals[1] if len(vals) > 1 else None)

def main(xlsx):
    ws = openpyxl.load_workbook(xlsx, read_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    head = rows[0]
    assert head[2] == "Nombre de institución" and head[12] == "Ingreso Promedio al 4° año", head
    out = []
    for r in rows[1:]:
        if r[2] not in INST:
            continue
        lo, hi = millones(r[12])
        out.append({"universidad_id": INST[r[2]], "area": r[4], "carrera_generica": r[5], "carrera": r[6],
                    "continuidad_estudios": num(r[7]), "retencion_1": num(r[8]), "duracion_real_sem": num(r[9]),
                    "empleabilidad_1": num(r[10]), "empleabilidad_2": num(r[11]),
                    "ingreso_4_texto": r[12] if isinstance(r[12], str) else None, "ingreso_4_min_mm": lo, "ingreso_4_max_mm": hi})
    data = {"fuente": "SIES – Mi Futuro (Mineduc), Buscador de Empleabilidad e Ingresos 2025-2026",
            "url": "https://www.mifuturo.cl/mi-futuro-buscadores/", "hoja": ws.title,
            "notas": ["Datos por institución y carrera, sin distinguir sede.",
                      "Empleabilidad: proporción de titulados con ingresos iguales o superiores al sueldo mínimo al 1.er y 2.º año de titulación.",
                      "Ingreso: rango del ingreso promedio mensual bruto al 4.º año de titulación.",
                      "s/i = sin información (pocos casos); n/a = no aplica."],
            "carreras": out}
    (ROOT / "data" / "mifuturo_2025_2026.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(out)} filas de {len(INST)} universidades")

if __name__ == "__main__":
    main(sys.argv[1])
