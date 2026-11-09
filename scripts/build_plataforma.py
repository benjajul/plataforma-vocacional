"""Une inventario, planes comunes, habilidades y cortes en data/plataforma.json (lo usan explorar, simulador y cuestionario).

Áreas: agrupación propia de las 21 familias de carreras según el tipo de problema que resuelven y las habilidades que
comparten (ver data/habilidades.json). 'vinculadas' indica áreas con las que comparten base o se cruzan.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = lambda f: json.loads((ROOT / "data" / f).read_text(encoding="utf-8"))

AREAS = [
 {"id": "gestion", "nombre": "Gestión, industria y negocios", "familias": ["industrial", "comercial", "aviacion"],
  "descripcion": "Carreras que mejoran cómo funcionan las organizaciones: procesos, costos, finanzas, personas y estrategia.",
  "vinculadas": ["computacion", "minerales"]},
 {"id": "computacion", "nombre": "Computación, datos y telecomunicaciones", "familias": ["informatica", "datos_ia", "telecom"],
  "descripcion": "Software, sistemas, inteligencia artificial, redes y seguridad de la información.",
  "vinculadas": ["exactas", "gestion", "energia"]},
 {"id": "exactas", "nombre": "Ciencias exactas y modelamiento", "familias": ["matematica", "fisica"],
  "descripcion": "Matemática y física aplicadas para modelar problemas complejos e investigar.",
  "vinculadas": ["computacion", "energia"]},
 {"id": "energia", "nombre": "Energía, máquinas y automatización", "familias": ["electrica", "mecanica", "automatizacion", "diseno"],
  "descripcion": "Sistemas eléctricos y energéticos, máquinas, robótica, control y diseño de productos.",
  "vinculadas": ["computacion", "infraestructura", "minerales"]},
 {"id": "infraestructura", "nombre": "Infraestructura, construcción y territorio", "familias": ["obras", "construccion", "geomensura"],
  "descripcion": "Edificios, puentes, caminos, obras hidráulicas, su construcción y la medición del territorio.",
  "vinculadas": ["energia", "vida"]},
 {"id": "minerales", "nombre": "Minería, materiales y procesos químicos", "familias": ["minas", "metalurgia", "quimica"],
  "descripcion": "Extracción y procesamiento de recursos, materiales y procesos industriales a gran escala.",
  "vinculadas": ["energia", "vida", "gestion"]},
 {"id": "vida", "nombre": "Vida, salud y medio ambiente", "familias": ["bio", "biomedica", "ambiental"],
  "descripcion": "Biotecnología, tecnología para la salud y cuidado del medio ambiente.",
  "vinculadas": ["minerales", "infraestructura"]},
]

def main():
    inv, pc, hab = D("inventario.json"), D("planes_comunes.json"), D("habilidades.json")
    cortes = D("cortes_2026.json")
    fam_de_area = {f: a["id"] for a in AREAS for f in a["familias"]}
    fam_ids = {f["id"] for f in hab["familias"]}
    assert set(fam_de_area) == fam_ids, set(fam_de_area) ^ fam_ids

    # familia(s) de cada programa: directo por perfil, o por las salidas si es plan común / bachillerato
    familias_prog = {}
    for f in hab["familias"]:
        for c in f["carreras"]:
            key = c["salida_de"] or c["id"]
            familias_prog.setdefault(key, set()).add(f["id"])
    for p in pc["planes_comunes"]:
        for s in p["salidas"]:
            if s.get("programa_directo_id"):
                familias_prog.setdefault(p["programa_id"], set()).update(familias_prog.get(s["programa_directo_id"], set()))
    # casos sin perfil propio
    extra = {"uai-bachillerato-ing-civil": "uai-plan-comun", "uai-doble-arquitectura-industrial": None, "udd-ingenieria-comercial": None,
             "uai-ingenieria-comercial": None, "usach-civil-informatica-plan-comun": None}
    familias_prog["uai-bachillerato-ing-civil"] = set(familias_prog.get("uai-plan-comun", set()))
    familias_prog["uai-doble-arquitectura-industrial"] = {"industrial"}
    familias_prog["udd-ingenieria-comercial"] = {"comercial"}
    familias_prog["uai-ingenieria-comercial"] = {"comercial"}

    pcs = {p["programa_id"]: p for p in pc["planes_comunes"]}
    programas = []
    for x in inv["programas"]:
        if x["en_alcance"] != "si":
            continue
        fams = sorted(familias_prog.get(x["id"], set()))
        assert fams, f"sin familia: {x['id']}"
        c = cortes["programas"].get(x["id"])
        fuente_c = cortes["fuentes"][c["fuente"]] if c else None
        programas.append({
            "id": x["id"], "universidad_id": x["universidad_id"], "nombre": x["nombre_oficial"], "categoria": x["categoria"],
            "tipo_ingreso": x["tipo_ingreso"], "campus": x["campus"] or None, "facultad": x["facultad"],
            "codigo": x["codigo_demre"], "vacantes_2027": x["vacantes_regulares_2027"],
            "ponderaciones": x["ponderaciones_2027"], "hyc_o_ciencias": x["hyc_o_ciencias"], "exige_m2": x["exige_m2"],
            "puntaje_ponderado_minimo": x["puntaje_ponderado_minimo_2027"], "promedio_cl_m1_minimo": x["promedio_cl_m1_minimo_2027"],
            "familias": fams, "areas": sorted({fam_de_area[f] for f in fams}),
            "plan_comun": {"mecanismo": pcs[x["id"]]["seleccion"]["mecanismo"], "cupos": pcs[x["id"]]["seleccion"]["cupos"],
                           "n_salidas": len(pcs[x["id"]]["salidas"])} if x["id"] in pcs else None,
            "corte_2026": ({"valor": c["corte"], "medida": c["medida"], "ingresaron": c.get("ingresaron"),
                            "ingresaron_medida": c.get("ingresaron_medida"), "historico": c.get("historico"),
                            "fuente": fuente_c["nombre"], "url": c.get("url") or fuente_c["url"], "anio": c.get("anio", 2026), "primer_matriculado": c.get("primer_matriculado"), "oficial": fuente_c["oficial"], "nota": c.get("nota")}
                           if c else None),
            "nota": x["nota"],
        })
    out = {
        "version": "0.6", "consultado": "2026-11-08",
        "bases": {"ponderaciones": "Oferta Definitiva DEMRE, Admisión 2027 (24-09-2026)",
                  "cortes": "Admisión 2026 (último proceso con resultados publicados)"},
        "universidades": inv["universidades"],
        "areas": AREAS,
        "familias": [{k: f[k] for k in ("id", "nombre", "n_perfiles", "que_hace", "te_puede_gustar_si", "distintivas", "porcentaje", "diferencia_vs_promedio")}
                     | {"area": fam_de_area[f["id"]]} for f in hab["familias"]],
        "habilidades": hab["habilidades"], "promedio_habilidades": hab["promedio_general"],
        "programas": programas,
        "fuentes": {"demre": "https://demre.cl/publicaciones/pdf/2027-26-09-24-oferta-definitiva-carreras-p2027.pdf", "cortes": cortes["fuentes"]},
        "nota_cortes": cortes["nota"],
    }
    (ROOT / "data" / "plataforma.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    con = sum(1 for p in programas if p["corte_2026"])
    print(f"{len(programas)} programas; {con} con corte 2026; áreas: {len(AREAS)}")

if __name__ == "__main__":
    main()
