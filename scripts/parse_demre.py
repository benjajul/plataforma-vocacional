"""Extrae de la Oferta Definitiva DEMRE (Admisión 2027) las filas de las 8 universidades del proyecto.

Uso:
    pdftotext -layout 2027-26-09-24-oferta-definitiva-carreras-p2027.pdf oferta.txt
    python3 scripts/parse_demre.py oferta.txt
Escribe data/demre_2027.json (todas las carreras de esas universidades, no solo ingeniería).

Columnas de la tabla DEMRE: NEM, Ranking, Competencia Lectora, M1, Historia y Cs. Sociales [o] Ciencias, M2,
luego requisitos (puntajes mínimos) y vacantes regulares del 1.er semestre. El número de columnas de
requisitos entre M2 y las vacantes varía por universidad (VAC_OFFSET), verificado a mano con una carrera
conocida de cada una (ver comentario).
"""
import json, re, sys, pathlib

PREFIX = {"12": "uc", "11": "uchile", "15": "usm", "16": "usach", "41": "unab", "38": "udp", "42": "uai", "44": "udd"}
# posición de la vacante regular contada desde el token siguiente a M2
# (UC 12039=650, U.Chile 11045=710, UNAB 41047=110 -> 3 ; UDP 38176=85, USACH 16008=90, USM 15361=75, UAI 42202=35, UDD 44051=25 -> 2)
VAC_OFFSET = {"uc": 3, "uchile": 3, "unab": 3, "udp": 2, "usach": 2, "usm": 2, "uai": 2, "udd": 2}

CODE = re.compile(r"^\s{0,10}(\d{5})\)?(\s.*)$")
VAL = re.compile(r"^(\d{1,3}|---|o)$")
CAPS = re.compile(r"^[A-ZÁÉÍÓÚÑÜ0-9 ,\-\+\.\(\)/:'’]+$")

def parse(path):
    lines = pathlib.Path(path).read_text(encoding="utf-8").replace("\f", "\n").splitlines()
    out = []
    for i, line in enumerate(lines):
        m = CODE.match(line)
        if not m or m.group(1)[:2] not in PREFIX:
            continue
        uni = PREFIX[m.group(1)[:2]]
        body = m.group(2)
        parts = re.split(r"\s{2,}", body.strip())
        # nombre = primeros fragmentos de texto en mayúscula que no son valores
        name_parts, rest = [], []
        for p in parts:
            if not rest and not VAL.match(p.split()[0]) and re.search(r"[A-ZÁÉÍÓÚÑ]{3}", p):
                name_parts.append(p)
            else:
                rest.append(p)
        tokens = " ".join(rest).split()
        # quitar sede / notas al pie que quedaron al inicio
        sede = []
        while tokens and not VAL.match(tokens[0]):
            sede.append(tokens.pop(0))
        name = " ".join(name_parts)
        sede_txt = " ".join(t for t in sede if not t.startswith("("))
        SEDES = {"SANTIAGO", "VIÑA DEL MAR", "CONCEPCIÓN", "TALCA", "TEMUCO", "CURICÓ", "CHILLÁN", "LOS ÁNGELES"}
        if len(name_parts) == 1 and name_parts[0] in SEDES:   # nombre partido en líneas vecinas
            sede_txt, name, name_parts = name_parts[0], "", []
        if len(name_parts) >= 2:          # 'NOMBRE   SEDE' en dos fragmentos
            sede_txt = name_parts[-1] if not sede_txt else sede_txt
            name = " ".join(name_parts[:-1])
        if not name or not re.search(r"[A-Z]{3}", name):
            # nombre partido en líneas vecinas (arriba y abajo)
            up = lines[i - 1].strip() if i else ""
            dn = lines[i + 1].strip() if i + 1 < len(lines) else ""
            frag = [s for s in (up, dn) if s and CAPS.match(s) and not CODE.match(s)]
            name = " ".join(frag)
        elif i + 1 < len(lines):
            dn = lines[i + 1].strip()
            if dn and CAPS.match(dn) and not CODE.match(dn) and len(dn) < 60 and not re.search(r"\d{3}", dn):
                name = f"{name} {dn}"
        if len(tokens) < 7:
            continue
        try:
            if tokens[5] == "o":
                w = dict(nem=tokens[0], ranking=tokens[1], cl=tokens[2], m1=tokens[3], hyc=tokens[4], ciencias=tokens[6], m2=tokens[7])
                after = tokens[8:]
            else:
                w = dict(nem=tokens[0], ranking=tokens[1], cl=tokens[2], m1=tokens[3], hyc=tokens[4], ciencias=tokens[5], m2=tokens[6])
                after = tokens[7:]
            k = VAC_OFFSET[uni]
            vac = after[k] if len(after) > k else None
            # requisitos: el primer token tras M2 es el puntaje ponderado mínimo de postulación y el último antes de
            # las vacantes es el promedio mínimo CL+M1 (verificado: USM 15300 600/485, USACH 16008 550/485, UC 12039 ---/485)
            pond_min = after[0] if after else None
            prom_min = after[k - 1] if len(after) >= k else None
        except IndexError:
            continue
        num = lambda v: int(v) if v and v.isdigit() else None
        pond = {kk: num(vv) for kk, vv in w.items()}
        total = sum(v for v in pond.values() if v) - (pond["ciencias"] if w["hyc"] != "---" and tokens[5] == "o" else 0)
        out.append({
            "codigo": m.group(1), "universidad_id": uni,
            "nombre": re.sub(r"\s*\(\d+\)|\s*\(\*\)", "", name).strip(),
            "sede": sede_txt or None,
            "ponderaciones": pond, "hyc_o_ciencias": tokens[5] == "o",
            "suma_ponderaciones": total,
            "vacantes_regulares": num(vac),
            "puntaje_ponderado_minimo": num(pond_min),
            "promedio_cl_m1_minimo": num(prom_min),
            "exige_m2": pond["m2"] is not None,
        })
    return out

if __name__ == "__main__":
    rows = parse(sys.argv[1])
    root = pathlib.Path(__file__).resolve().parent.parent
    ok = sum(1 for r in rows if r["suma_ponderaciones"] == 100)
    (root / "data" / "demre_2027.json").write_text(json.dumps({
        "fuente": "DEMRE — Oferta Definitiva de Carreras, Vacantes y Ponderaciones, Admisión 2027 (24-09-2026)",
        "url": "https://demre.cl/publicaciones/pdf/2027-26-09-24-oferta-definitiva-carreras-p2027.pdf",
        "carreras": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(rows)} filas; {ok} con ponderaciones que suman 100")
