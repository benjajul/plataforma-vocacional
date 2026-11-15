"""Cruce de cada programa (y cada salida de plan común) con su fila de Mi Futuro 2025-2026.

Se cruza por universidad + 'Nombre carrera (del título)' tal como aparece en la base. Si una carrera no tiene fila
(carreras nuevas, o que la base agrupa de otra forma), queda sin dato: no se aproxima con otra carrera.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_MF = None

def mf():
    global _MF
    if _MF is None:
        p = ROOT / "data" / "mifuturo_2025_2026.json"
        _MF = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"carreras": []}
    return _MF

# programa_id -> (universidad, carrera del título en Mi Futuro[, nota])
PROGRAMAS = {
 "uc-construccion-civil": ("uc", "Construcción Civil"),
 "uc-ingenieria-comercial": ("uc", "Ingeniería Comercial"),
 "uchile-ingenieria-comercial": ("uchile", "Ingeniería Comercial"),
 "usm-civil": ("usm", "Ingeniería Civil"),
 "usm-civil-minas": ("usm", "Ingeniería Civil de Minas"),
 "usm-civil-electrica": ("usm", "Ingeniería Civil Eléctrica"),
 "usm-civil-informatica": ("usm", "Ingeniería Civil Informática"),
 "usm-civil-matematica": ("usm", "Ingeniería Civil Matemática"),
 "usm-civil-mecanica": ("usm", "Ingeniería Civil Mecánica"),
 "usm-civil-quimica": ("usm", "Ingeniería Civil Química"),
 "usm-civil-telematica": ("usm", "Ingeniería Civil Telemática"),
 "usm-civil-industrial": ("usm", "Ingeniería Civil Industrial"),
 "usm-ingenieria-comercial": ("usm", "Ingeniería Comercial"),
 "usach-civil-en-electricidad": ("usach", "Ingeniería Civil en Electricidad"),
 "usach-civil-en-mecanica": ("usach", "Ingeniería Civil en Mecánica"),
 "usach-civil-en-metalurgia": ("usach", "Ingeniería Civil en Metalurgia"),
 "usach-civil-en-minas": ("usach", "Ingeniería Civil en Minas"),
 "usach-civil-en-obras-civiles": ("usach", "Ingeniería Civil en Obras Civiles"),
 "usach-civil-en-quimica": ("usach", "Ingeniería Civil en Química"),
 "usach-civil-industrial": ("usach", "Ingeniería Civil Industrial"),
 "usach-civil-informatica-plan-comun": ("usach", "Ingeniería Civil en Informática", "Dato de la carrera de Ingeniería Civil en Informática anterior al plan común (nuevo en 2027)."),
 "usach-ejecucion-en-computacion-e-informatica": ("usach", "Ingeniería de Ejecución en Computación e Informática"),
 "usach-ejecucion-en-electricidad": ("usach", "Ingeniería de Ejecución en Electricidad"),
 "usach-ejecucion-en-mecanica": ("usach", "Ingeniería de Ejecución en Mecánica"),
 "usach-ejecucion-en-metalurgia": ("usach", "Ingeniería de Ejecución en Metalurgia"),
 "usach-ejecucion-en-minas": ("usach", "Ingeniería de Ejecución en Minas"),
 "usach-ejecucion-en-quimica": ("usach", "Ingeniería de Ejecución en Química"),
 "usach-ejecucion-industrial": ("usach", "Ingeniería de Ejecución Industrial"),
 "usach-ingenieria-comercial": ("usach", "Ingeniería Comercial"),
 "udp-civil-industrial": ("udp", "Ingeniería Civil Industrial"),
 "udp-civil-obras-civiles": ("udp", "Ingeniería Civil en Obras Civiles"),
 "udp-civil-informatica-telecom": ("udp", "Ingeniería Civil en Informática y Telecomunicaciones"),
 "udp-ingenieria-comercial": ("udp", "Ingeniería Comercial"),
}

# (plan_comun programa_id, nombre de la salida) -> carrera del título en Mi Futuro
SALIDAS = {
 ("uchile-plan-comun", "Ingeniería Civil"): "Ingeniería Civil",
 ("uchile-plan-comun", "Ingeniería Civil de Minas"): "Ingeniería Civil de Minas",
 ("uchile-plan-comun", "Ingeniería Civil en Biotecnología"): "Ingeniería Civil en Biotecnología",
 ("uchile-plan-comun", "Ingeniería Civil en Computación"): "Ingeniería Civil en Computación",
 ("uchile-plan-comun", "Ingeniería Civil Eléctrica"): "Ingeniería Civil Eléctrica",
 ("uchile-plan-comun", "Ingeniería Civil Industrial"): "Ingeniería Civil Industrial",
 ("uchile-plan-comun", "Ingeniería Civil Matemática"): "Ingeniería Civil Matemática",
 ("uchile-plan-comun", "Ingeniería Civil Mecánica"): "Ingeniería Civil Mecánica",
 ("uchile-plan-comun", "Ingeniería Civil Química"): "Ingeniería Civil Química",
 ("uchile-plan-comun", "Geología"): "Geología",
 ("uc-ingenieria", "Ingeniero Civil"): "Ingeniería Civil, Diplomas en Diseño y Construcción de Obras e Ingeniería y Gestión de la Construcción",
 ("uc-ingenieria", "Ingeniero Civil de Industrias"): "Ingeniería Civil de Industrias",
 ("uc-ingenieria", "Ingeniero Civil de Computación"): "Ingeniería Civil de Computación",
 ("uc-ingenieria", "Ingeniero Civil Electricista"): "Ingeniería Civil Electricista",
 ("uc-ingenieria", "Ingeniero Civil Mecánico"): "Ingeniería Civil Mecánico",
 ("uc-ingenieria", "Ingeniero Civil de Biotecnología"): "Ingeniería Civil en Biotecnología",
 ("udp-plan-comun", "Ingeniería Civil Industrial"): "Ingeniería Civil Industrial",
 ("udp-plan-comun", "Ingeniería Civil en Obras Civiles"): "Ingeniería Civil en Obras Civiles",
 ("udp-plan-comun", "Ingeniería Civil en Informática y Telecomunicaciones"): "Ingeniería Civil en Informática y Telecomunicaciones",
}
SALIDA_USM = {"Ingeniería Civil": "usm-civil", "Ingeniería Civil de Minas": "usm-civil-minas", "Ingeniería Civil Eléctrica": "usm-civil-electrica",
              "Ingeniería Civil Informática": "usm-civil-informatica", "Ingeniería Civil Matemática": "usm-civil-matematica",
              "Ingeniería Civil Mecánica": "usm-civil-mecanica", "Ingeniería Civil Química": "usm-civil-quimica",
              "Ingeniería Civil Telemática": "usm-civil-telematica"}

def _fila(uni, carrera, nota=None):
    for c in mf()["carreras"]:
        if c["universidad_id"] == uni and c["carrera"] == carrera:
            d = {k: c[k] for k in ("carrera", "empleabilidad_1", "empleabilidad_2", "ingreso_4_texto", "ingreso_4_min_mm",
                                   "ingreso_4_max_mm", "retencion_1", "duracion_real_sem", "continuidad_estudios")}
            if nota:
                d["nota"] = nota
            return d
    raise KeyError(f"Mi Futuro sin fila: {uni} / {carrera}")

def programa(pid):
    if pid not in PROGRAMAS or not mf()["carreras"]:
        return None
    return _fila(*PROGRAMAS[pid])

def salida(plan_id, uni, nombre):
    if not mf()["carreras"]:
        return None
    if plan_id == "usm-plan-comun" and nombre in SALIDA_USM:
        return programa(SALIDA_USM[nombre])
    k = (plan_id, nombre)
    return _fila(uni, SALIDAS[k]) if k in SALIDAS else None

def resumen_plan(filas):
    """Rango de empleabilidad e ingreso entre las salidas con dato."""
    xs = [f for f in filas if f]
    if not xs:
        return None
    e = [f["empleabilidad_1"] for f in xs if f["empleabilidad_1"] is not None]
    lo = [f["ingreso_4_min_mm"] for f in xs if f["ingreso_4_min_mm"] is not None]
    hi = [f["ingreso_4_max_mm"] or f["ingreso_4_min_mm"] for f in xs if f["ingreso_4_min_mm"] is not None]
    return {"rango": True, "n_salidas_con_dato": len(xs), "empleabilidad_1_min": min(e) if e else None, "empleabilidad_1_max": max(e) if e else None,
            "ingreso_4_min_mm": min(lo) if lo else None, "ingreso_4_max_mm": max(hi) if hi else None,
            "ingreso_abierto": any(f["ingreso_4_min_mm"] is not None and f["ingreso_4_max_mm"] is None for f in xs)}
