"""Genera data/inventario.json y data/inventario.csv (Fase 2 — inventario de programas).

Ejecutar desde la raíz del repo:  python3 scripts/build_inventario.py
Datos consultados el 08-11-2026. Cada programa lleva la(s) fuente(s) donde se verificó.

Campos:
  categoria   : plan_comun | ing_civil | ing_no_civil | ing_comercial
  en_alcance  : si -> entra en la plataforma
                no -> se revisó y Benjamín decidió excluirlo (08-11-2026); queda registrado por transparencia
  tipo_ingreso: plan_comun | carrera_directa
"""
import csv, json, pathlib

CONSULTADO = "2026-11-08"

FUENTES = {
    "demre_2027": ("DEMRE — Oferta definitiva de carreras, vacantes y ponderaciones, Admisión 2027",
                   "https://demre.cl/publicaciones/pdf/2027-26-09-24-oferta-definitiva-carreras-p2027.pdf"),
    "uc_majors": ("Ingeniería UC — Majors y minors",
                  "https://www.ing.uc.cl/en/programas-de-estudio/pregrado/plan-estudios/cuales-los-majors-los-minors-ingenieria-uc/"),
    "uchile_oferta": ("U. de Chile — Oferta de carreras Admisión regular",
                      "https://uchile.cl/admision-y-matriculas/admision-regular-pregrado/oferta-de-carreras"),
    "uchile_civil": ("U. de Chile — Ingeniería Civil (plan común FCFM)",
                     "https://uchile.cl/carreras/4969/ingenieria-civil"),
    "usm_uch": ("universidadeschile.cl — USM (nómina preliminar DEMRE 2027, verificada 15-10-2026)",
                "https://universidadeschile.cl/universidad/universidad-tecnica-federico-santa-maria"),
    "usm_paes": ("USM — Admisión Centralizada PAES (códigos y vacantes)",
                 "https://usm.cl/admision/admision-centralizada-paes-3/"),
    "usach_fing": ("USACH Admisión — Facultad de Ingeniería", "https://admision.usach.cl/FING-USACH"),
    "usach_uch": ("universidadeschile.cl — USACH (nómina preliminar DEMRE 2027)",
                  "https://universidadeschile.cl/universidad/universidad-de-santiago-de-chile"),
    "unab_folleto": ("UNAB — Folleto Admisión 2026",
                     "https://unabwps3.s3.amazonaws.com/exploraunab/wp-content/uploads/2025/04/02113053/FOLLETO-ADMISION-2026-1.pdf"),
    "unab_uch": ("universidadeschile.cl — UNAB (nómina preliminar DEMRE 2027)",
                 "https://universidadeschile.cl/universidad/universidad-andres-bello"),
    "nuevas_2027": ("Meganoticias — Nuevas carreras Admisión 2027 (25-09-2026)",
                    "https://www.meganoticias.cl/nacional/532470-admision-2027-nuevas-carreras-chile-universidades-vacantes-25-09-2026.html"),
    "udp_uch": ("universidadeschile.cl — UDP (nómina preliminar DEMRE 2027)",
                "https://universidadeschile.cl/universidad/universidad-diego-portales"),
    "udp_plancomun": ("UDP — Malla Ingeniería Civil Plan Común 2026",
                      "https://ingenieriayciencias.udp.cl/cms/wp-content/uploads/2025/12/INGENIERIA-CIVIL-PLAN-COMUN_2026.pdf"),
    "uai_fic": ("UAI — Facultad de Ingeniería y Ciencias, nuestras carreras",
                "https://www.uai.cl/ingenieria-y-ciencias/carreras/nuestras-carreras"),
    "uai_uch": ("universidadeschile.cl — UAI (nómina preliminar DEMRE 2027)",
                "https://universidadeschile.cl/universidad/universidad-adolfo-ibanez"),
    "udd_fing": ("UDD — Facultad de Ingeniería, carreras", "https://ingenieria.udd.cl/carreras/"),
    "udd_plancomun": ("UDD — Plan común de ingenierías (2024)",
                      "https://ingenieria.udd.cl/files/2024/03/07-plan-comun-ingenierias.pdf"),
    "udd_uch": ("universidadeschile.cl — UDD (nómina preliminar DEMRE 2027)",
                "https://universidadeschile.cl/universidad/universidad-del-desarrollo"),
}

UNIVERSIDADES = {
    "uc": "Pontificia Universidad Católica de Chile",
    "uchile": "Universidad de Chile",
    "usm": "Universidad Técnica Federico Santa María",
    "usach": "Universidad de Santiago de Chile",
    "unab": "Universidad Andrés Bello",
    "udp": "Universidad Diego Portales",
    "uai": "Universidad Adolfo Ibáñez",
    "udd": "Universidad del Desarrollo",
}

def p(uni, slug, nombre, categoria, *, ingreso="carrera_directa", facultad="", campus="",
      codigo=None, vacantes=None, especialidades=None, alcance="si", nota="", fuentes=()):
    return {
        "id": f"{uni}-{slug}", "universidad_id": uni, "universidad": UNIVERSIDADES[uni],
        "nombre_oficial": nombre, "categoria": categoria, "tipo_ingreso": ingreso,
        "facultad": facultad, "campus": campus, "codigo_demre": codigo,
        "vacantes_regulares_2027": vacantes, "especialidades": especialidades or [],
        "en_alcance": alcance, "nota": nota, "fuentes": list(fuentes), "consultado": CONSULTADO,
    }

FING_UC = "Facultad de Ingeniería"
P = []

# ---------- UC ----------
P += [
    p("uc", "ingenieria", "Ingeniería", "plan_comun", ingreso="plan_comun", facultad=FING_UC,
      campus="San Joaquín", codigo="12039", vacantes=650,
      especialidades=[  # majors — detalle en data/planes_comunes.json (traducidos al español desde la página en inglés)
          "Ingeniería y Ciencias Ambientales", "Computación y Sistemas de Información", "Ingeniería en Construcción",
          "Ingeniería Eléctrica", "Ingeniería Estructural", "Ingeniería Geotécnica", "Ingeniería Hidráulica",
          "Ingeniería Mecánica", "Ingeniería en Minería", "Ingeniería Química", "Investigación Operativa",
          "Ingeniería de Sistemas de Transporte", "Ingeniería de Software",
          "Geociencias (interdisciplinario)", "Ingeniería Biológica (interdisciplinario)",
          "Ingeniería Biomédica (interdisciplinario)", "Ingeniería Matemática (interdisciplinario)",
          "Ingeniería y Arquitectura (interdisciplinario)", "Ingeniería, Diseño e Innovación (interdisciplinario)",
          "Ingeniería Robótica (interdisciplinario)", "Ingeniería Física (interdisciplinario)",
          "Ingeniería Civil (interdisciplinario)"],
      nota="Ingreso único a Licenciatura en Ciencias de la Ingeniería con major; luego título de Ingeniero Civil UC en su especialidad. Exige M2 (pondera 15%).",
      fuentes=("demre_2027", "uc_majors")),
    p("uc", "lic-ciencia-datos", "Licenciatura en Ingeniería en Ciencia de Datos", "ing_no_civil", facultad=FING_UC,
      campus="San Joaquín", codigo="12089", vacantes=80,
      nota="Licenciatura (no título de ingeniero civil). Exige M2. Confirmar si es programa conjunto Ingeniería–Matemáticas.",
      fuentes=("demre_2027",)),
    p("uc", "lic-ciencia-computacion", "Licenciatura en Ingeniería en Ciencia de la Computación", "ing_no_civil",
      facultad=FING_UC, campus="San Joaquín", codigo="12100", vacantes=100,
      nota="Licenciatura (no título de ingeniero civil). Exige M2.", fuentes=("demre_2027",)),
    p("uc", "construccion-civil", "Construcción Civil", "ing_no_civil", facultad=FING_UC + " (Escuela de Construcción Civil)",
      campus="San Joaquín", codigo="12038", vacantes=205,
      nota="No lleva 'ingeniería' en el nombre pero se dicta en la Facultad de Ingeniería. No exige M2.",
      fuentes=("demre_2027",)),
    p("uc", "ing-recursos-naturales", "Ingeniería en Recursos Naturales", "ing_no_civil",
      facultad="Por confirmar (programa interdisciplinario)", campus="San Joaquín", codigo="12101", vacantes=85,
      alcance="si", nota="Confirmar facultad responsable antes de incluir.", fuentes=("demre_2027",)),
    p("uc", "ingenieria-comercial", "Ingeniería Comercial", "ing_comercial",
      facultad="Facultad de Economía y Administración", campus="San Joaquín", codigo="12014", vacantes=418,
      nota="No exige M2.", fuentes=("demre_2027",)),
]

# ---------- U. de Chile ----------
FCFM = "Facultad de Ciencias Físicas y Matemáticas (FCFM)"
P += [
    p("uchile", "plan-comun", "Ingeniería y Ciencias, Plan Común", "plan_comun", ingreso="plan_comun", facultad=FCFM,
      campus="Beauchef", codigo="11045", vacantes=710,
      especialidades=["Ingeniería Civil (menciones Estructuras, Construcción y Geotecnia; Hidráulica, Sanitaria y Ambiental; Transporte)",
                      "Ingeniería Civil de Minas", "Ingeniería Civil en Biotecnología", "Ingeniería Civil en Computación",
                      "Ingeniería Civil Eléctrica", "Ingeniería Civil Industrial", "Ingeniería Civil Matemática",
                      "Ingeniería Civil Mecánica", "Ingeniería Civil Química",
                      "Geología (no ingeniería)", "Lic. en Ciencias mención Astronomía (no ingeniería)",
                      "Lic. en Ciencias mención Física (no ingeniería)", "Geofísica (no ingeniería)"],
      nota="Especialidad se elige tras dos años. Ingeniería Civil dura 11 semestres. Ponderaciones: NEM 10, Ranking 25, CL 10, M1 20, M2 20, Ciencias 15.",
      fuentes=("uchile_oferta", "uchile_civil")),
    p("uchile", "ingenieria-comercial", "Ingeniería Comercial", "ing_comercial",
      facultad="Facultad de Economía y Negocios (FEN)", codigo="11042", vacantes=405, fuentes=("uchile_oferta",)),
    p("uchile", "ing-informacion-control-gestion", "Ingeniería en Información y Control de Gestión", "ing_no_civil",
      facultad="Facultad de Economía y Negocios (FEN)", codigo="11027", vacantes=146, alcance="no",
      nota="Ingeniería del área de negocios, no de la FCFM.", fuentes=("uchile_oferta",)),
]

# ---------- USM (solo Santiago) ----------
SJ, VIT = "San Joaquín", "Vitacura"
usm_civiles_sj = [("plan-comun", "Ingeniería Civil Plan Común", "plan_comun"),
                  ("civil", "Ingeniería Civil", "ing_civil"),
                  ("civil-minas", "Ingeniería Civil de Minas", "ing_civil"),
                  ("civil-electrica", "Ingeniería Civil Eléctrica", "ing_civil"),
                  ("civil-fisica", "Ingeniería Civil Física", "ing_civil"),
                  ("civil-informatica", "Ingeniería Civil Informática", "ing_civil"),
                  ("civil-matematica", "Ingeniería Civil Matemática", "ing_civil"),
                  ("civil-mecanica", "Ingeniería Civil Mecánica", "ing_civil"),
                  ("civil-quimica", "Ingeniería Civil Química", "ing_civil"),
                  ("civil-telematica", "Ingeniería Civil Telemática", "ing_civil")]
# Códigos de postulación USM (tabla Admisión 2026 en usm.cl; los códigos se mantienen entre procesos)
USM_COD = {"plan-comun": "15300", "civil": "15311", "civil-minas": "15312", "civil-electrica": "15330",
           "civil-fisica": "15384", "civil-informatica": "15360", "civil-matematica": "15301",
           "civil-mecanica": "15340", "civil-quimica": "15350", "civil-telematica": "15361",
           "diseno-productos": "15381", "civil-industrial": "15270", "aviacion-comercial": "15220",
           "ingenieria-comercial": "15271"}
for slug, nombre, cat in usm_civiles_sj:
    P.append(p("usm", slug, nombre, cat, ingreso="plan_comun" if cat == "plan_comun" else "carrera_directa",
               facultad="USM (organizada por departamentos, sin facultades)", campus=SJ, codigo=USM_COD[slug],
               fuentes=("usm_uch", "usm_paes"),
               nota="Ver data/planes_comunes.json: selección competitiva por ranking de primer año." if cat == "plan_comun" else ""))
P += [
    p("usm", "diseno-productos", "Ingeniería en Diseño de Productos", "ing_no_civil", facultad="USM (departamentos)",
      campus=SJ, codigo=USM_COD["diseno-productos"], fuentes=("usm_uch", "usm_paes")),
    p("usm", "civil-industrial", "Ingeniería Civil Industrial", "ing_civil", facultad="USM (departamentos)",
      campus=VIT, codigo=USM_COD["civil-industrial"], fuentes=("usm_uch", "usm_paes")),
    p("usm", "aviacion-comercial", "Ingeniería en Aviación Comercial", "ing_no_civil", facultad="USM (departamentos)",
      campus=VIT, codigo=USM_COD["aviacion-comercial"], fuentes=("usm_uch", "usm_paes")),
    p("usm", "ingenieria-comercial", "Ingeniería Comercial", "ing_comercial",
      facultad="USM — Departamento de Ingeniería Comercial", campus=VIT, codigo=USM_COD["ingenieria-comercial"],
      fuentes=("usm_uch", "usm_paes")),
]

# ---------- USACH ----------
FING_USACH = "Facultad de Ingeniería"
usach_civ = ["Ingeniería Civil Biomédica", "Ingeniería Civil en Ambiente", "Ingeniería Civil en Biotecnología",
             "Ingeniería Civil en Electricidad", "Ingeniería Civil en Geomensura y Geomática",
             "Ingeniería Civil en Mecánica", "Ingeniería Civil en Metalurgia", "Ingeniería Civil en Minas",
             "Ingeniería Civil en Obras Civiles", "Ingeniería Civil en Química", "Ingeniería Civil en Telemática",
             "Ingeniería Civil en Territorio y Medio Ambiente", "Ingeniería Civil Industrial",
             "Ingeniería Civil Mecatrónica"]
usach_ejec = ["Ingeniería de Ejecución en Climatización", "Ingeniería de Ejecución en Computación e Informática",
              "Ingeniería de Ejecución en Electricidad", "Ingeniería de Ejecución en Mecánica",
              "Ingeniería de Ejecución en Metalurgia", "Ingeniería de Ejecución en Minas",
              "Ingeniería de Ejecución en Química", "Ingeniería de Ejecución Industrial"]

def slugify(s):
    import unicodedata, re
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

for n in usach_civ:
    P.append(p("usach", slugify(n.replace("Ingeniería ", "")), n, "ing_civil", facultad=FING_USACH,
               campus="Campus Usach, Estación Central", fuentes=("usach_fing", "usach_uch")))
P.append(p("usach", "civil-informatica-plan-comun", "Ingeniería Civil en Informática – Plan Común", "plan_comun",
           ingreso="plan_comun", facultad=FING_USACH, campus="Campus Usach, Estación Central",
           nota="Carrera nueva Admisión 2027 (90 vacantes según prensa). Especialidades por confirmar en Fase 3.",
           vacantes=90, fuentes=("usach_fing", "nuevas_2027")))
for n in usach_ejec:
    P.append(p("usach", slugify(n.replace("Ingeniería de ", "")), n, "ing_no_civil", facultad=FING_USACH,
               campus="Campus Usach, Estación Central", fuentes=("usach_fing", "usach_uch")))
P.append(p("usach", "ingenieria-comercial", "Ingeniería Comercial", "ing_comercial",
           facultad="Facultad de Administración y Economía (FAE)", campus="Campus Usach, Estación Central",
           fuentes=("usach_uch",)))

# ---------- UNAB (solo Santiago) ----------
FING_UNAB = "Facultad de Ingeniería"
P += [
    p("unab", "civil", "Ingeniería Civil", "ing_civil", facultad=FING_UNAB, fuentes=("unab_folleto", "unab_uch")),
    p("unab", "civil-electrica", "Ingeniería Civil Eléctrica", "ing_civil", facultad=FING_UNAB, fuentes=("unab_folleto", "unab_uch")),
    p("unab", "civil-minas", "Ingeniería Civil en Minas", "ing_civil", facultad=FING_UNAB, fuentes=("unab_folleto", "unab_uch")),
    p("unab", "civil-industrial", "Ingeniería Civil Industrial", "ing_civil", facultad=FING_UNAB,
      campus="Antonio Varas y Casona de Las Condes", nota="Diurno y vespertino.", fuentes=("unab_folleto", "unab_uch")),
    p("unab", "civil-informatica", "Ingeniería Civil Informática", "ing_civil", facultad=FING_UNAB,
      campus="Antonio Varas y Casona de Las Condes", fuentes=("unab_folleto", "unab_uch")),
    p("unab", "civil-biomedica", "Ingeniería Civil Biomédica", "ing_civil", facultad="Por confirmar",
      campus="Las Condes", vacantes=100, alcance="si",
      nota="Carrera nueva Admisión 2027; no aparece aún en la nómina preliminar ni en el folleto 2026.", fuentes=("nuevas_2027",)),
    p("unab", "automatizacion-robotica", "Ingeniería en Automatización y Robótica", "ing_no_civil", facultad=FING_UNAB,
      nota="Diurno y vespertino.", fuentes=("unab_folleto", "unab_uch")),
    p("unab", "computacion-informatica", "Ingeniería en Computación e Informática", "ing_no_civil", facultad=FING_UNAB,
      nota="Diurno y vespertino.", fuentes=("unab_folleto", "unab_uch")),
    p("unab", "construccion", "Ingeniería en Construcción", "ing_no_civil", facultad=FING_UNAB, fuentes=("unab_folleto", "unab_uch")),
    p("unab", "industrial", "Ingeniería Industrial", "ing_no_civil", facultad=FING_UNAB,
      nota="Diurno y vespertino.", fuentes=("unab_folleto", "unab_uch")),
    p("unab", "ambiental", "Ingeniería Ambiental", "ing_no_civil", facultad="Por confirmar", alcance="si", fuentes=("unab_uch",)),
    p("unab", "fisica", "Ingeniería Física", "ing_no_civil", facultad="Por confirmar", alcance="si", fuentes=("unab_uch",)),
    p("unab", "biotecnologia", "Ingeniería en Biotecnología", "ing_no_civil", facultad="Por confirmar", alcance="si", fuentes=("unab_uch",)),
    p("unab", "engineering-technology-management", "Engineering and Technology Management", "ing_no_civil",
      facultad="Por confirmar", campus="Las Condes", vacantes=60, alcance="si",
      nota="Carrera nueva Admisión 2027.", fuentes=("nuevas_2027",)),
    p("unab", "computer-science-engineering", "Computer Science Engineering", "ing_no_civil", facultad="Por confirmar",
      campus="Las Condes", nota="Carrera detectada en la oferta DEMRE 2027 (no figuraba en folleto 2026 ni en la nómina preliminar).",
      fuentes=("demre_2027",)),
    p("unab", "ingenieria-comercial", "Ingeniería Comercial", "ing_comercial", facultad="Facultad de Economía y Negocios",
      campus="Bellavista y Casona de Las Condes", nota="Diurno y vespertino; 5 años.", fuentes=("unab_folleto", "unab_uch")),
]

# ---------- UDP ----------
FIC_UDP = "Facultad de Ingeniería y Ciencias"
P += [
    p("udp", "plan-comun", "Ingeniería Civil Plan Común", "plan_comun", ingreso="plan_comun", facultad=FIC_UDP,
      especialidades=["Ingeniería Civil Industrial", "Ingeniería Civil en Obras Civiles",
                      "Ingeniería Civil en Informática y Telecomunicaciones",
                      "Ingeniería Civil en Ciencia de Datos e Inteligencia Artificial"],
      nota="Primer año común; especialidad sin límite de cupos. Título profesional + magíster de continuidad.",
      fuentes=("udp_plancomun", "udp_uch")),
    p("udp", "civil-industrial", "Ingeniería Civil Industrial", "ing_civil", facultad=FIC_UDP, fuentes=("udp_uch",)),
    p("udp", "civil-obras-civiles", "Ingeniería Civil en Obras Civiles", "ing_civil", facultad=FIC_UDP, fuentes=("udp_uch",)),
    p("udp", "civil-informatica-telecom", "Ingeniería Civil en Informática y Telecomunicaciones", "ing_civil",
      facultad=FIC_UDP, fuentes=("udp_uch",)),
    p("udp", "civil-ciencia-datos-ia", "Ingeniería Civil en Ciencia de Datos e Inteligencia Artificial", "ing_civil",
      facultad=FIC_UDP, fuentes=("udp_uch",)),
    p("udp", "ingenieria-comercial", "Ingeniería Comercial", "ing_comercial",
      facultad="Facultad de Administración y Economía", campus="Huechuraba", fuentes=("udp_uch",)),
    p("udp", "control-gestion", "Ingeniería en Control de Gestión", "ing_no_civil",
      facultad="Facultad de Administración y Economía", campus="Huechuraba", alcance="no",
      nota="Ingeniería del área de negocios, no de la Facultad de Ingeniería.", fuentes=("udp_uch",)),
]

# ---------- UAI (solo Santiago) ----------
FIC_UAI = "Facultad de Ingeniería y Ciencias"
P += [
    p("uai", "plan-comun", "Ingeniería Civil (Plan Común)", "plan_comun", ingreso="plan_comun", facultad=FIC_UAI,
      campus="Peñalolén",
      especialidades=["Ingeniería Civil Industrial", "Ingeniería Civil Informática", "Ingeniería Civil en Bioingeniería",
                      "Ingeniería Civil (Obras Civiles)", "Ingeniería Civil en Energía", "Ingeniería Civil Mecánica",
                      "Ingeniería Civil en Minería"],
      nota="En Santiago todas las ingenierías civiles entran por plan común (7 especialidades).",
      fuentes=("uai_fic", "uai_uch")),
    p("uai", "computer-science", "Ingeniería en Computer Science", "ing_no_civil", facultad=FIC_UAI, campus="Peñalolén",
      nota="Ingreso directo. Exige M2.", fuentes=("uai_fic", "uai_uch")),
    p("uai", "bachillerato-ing-civil", "Bachillerato de Ingeniería Civil", "plan_comun", ingreso="plan_comun",
      facultad=FIC_UAI, campus="Peñalolén", alcance="si",
      nota="Programa de entrada alternativo; confirmar diferencia con el plan común.", fuentes=("uai_fic", "uai_uch")),
    p("uai", "doble-arquitectura-industrial", "Doble Título Arquitectura + Ingeniería Civil Industrial", "ing_civil",
      facultad=FIC_UAI + " / Escuela de Arquitectura", campus="Peñalolén", alcance="si",
      nota="Doble título.", fuentes=("uai_fic", "uai_uch")),
    p("uai", "negocios-tecnologia", "Ingeniería en Negocios y Tecnología", "ing_no_civil", facultad="Por confirmar",
      alcance="si", fuentes=("uai_uch",)),
    p("uai", "aeroespacial", "Ingeniería Aeroespacial", "ing_no_civil", facultad=FIC_UAI,
      campus="Base Aérea El Bosque (FACh)", alcance="no",
      nota="Aparece en la facultad pero no en la nómina DEMRE de Santiago; confirmar vía de ingreso.", fuentes=("uai_fic",)),
    p("uai", "ingenieria-comercial", "Ingeniería Comercial", "ing_comercial", facultad="Escuela de Negocios",
      campus="Peñalolén", nota="También existen Bachillerato de Ing. Comercial y dobles títulos (Derecho, Sociología).",
      fuentes=("uai_uch",)),
]

# ---------- UDD (solo Santiago) ----------
FING_UDD = "Facultad de Ingeniería"
CAMPUS_UDD = "Campus Rector Ernesto Silva Bafalluy, Las Condes"
P += [
    p("udd", "plan-comun", "Ingeniería Civil Plan Común", "plan_comun", ingreso="plan_comun", facultad=FING_UDD,
      campus=CAMPUS_UDD,
      especialidades=["Ingeniería Civil Industrial", "Ingeniería Civil en Obras Civiles", "Ingeniería Civil en Minería",
                      "Ingeniería Civil en Informática e Innovación Tecnológica",
                      "Ingeniería Civil en Informática e Inteligencia Artificial (por confirmar)",
                      "Geología (no ingeniería)"],
      nota="Especialidad se elige tras 3 semestres; conduce a todas las carreras de la facultad salvo BioMedicina. Dura 11 semestres. Lista de especialidades basada en documento 2024.",
      fuentes=("udd_fing", "udd_plancomun", "udd_uch")),
    p("udd", "civil-industrial", "Ingeniería Civil Industrial", "ing_civil", facultad=FING_UDD, campus=CAMPUS_UDD, fuentes=("udd_fing", "udd_uch")),
    p("udd", "civil-obras-civiles", "Ingeniería Civil en Obras Civiles", "ing_civil", facultad=FING_UDD, campus=CAMPUS_UDD, fuentes=("udd_fing", "udd_uch")),
    p("udd", "civil-mineria", "Ingeniería Civil en Minería", "ing_civil", facultad=FING_UDD, campus=CAMPUS_UDD, fuentes=("udd_fing", "udd_uch")),
    p("udd", "civil-informatica-innovacion", "Ingeniería Civil en Informática e Innovación Tecnológica", "ing_civil",
      facultad=FING_UDD, campus=CAMPUS_UDD, fuentes=("udd_fing", "udd_uch")),
    p("udd", "civil-informatica-ia", "Ingeniería Civil en Informática e Inteligencia Artificial", "ing_civil",
      facultad=FING_UDD, campus=CAMPUS_UDD, nota="Carrera nueva.", fuentes=("udd_fing", "udd_uch")),
    p("udd", "civil-biomedicina", "Ingeniería Civil en Biomedicina", "ing_civil", facultad=FING_UDD, campus=CAMPUS_UDD,
      nota="Carrera nueva; no se accede por plan común.", fuentes=("udd_fing", "udd_uch")),
    p("udd", "ingenieria-comercial", "Ingeniería Comercial", "ing_comercial", facultad="Facultad de Economía y Negocios",
      campus=CAMPUS_UDD, nota="Nuevos dobles títulos 2027 con Derecho, Psicología y Diseño; también Bachillerato en Ing. Comercial.",
      fuentes=("udd_uch", "nuevas_2027")),
]

# ---------- Fuera de alcance (ingenierías en otras facultades), para transparencia ----------
FUERA = [
    ("uchile", "Ingeniería en Biotecnología Molecular", "Facultad de Ciencias"),
    ("uchile", "Ingeniería en Sonido", "Facultad de Artes"),
    ("uchile", "Ingeniería Agronómica", "Facultad de Ciencias Agronómicas"),
    ("uchile", "Ingeniería en Recursos Naturales Renovables", "Facultad de Ciencias Agronómicas"),
    ("uchile", "Ingeniería Forestal", "Facultad de Ciencias Forestales y de la Conservación de la Naturaleza"),
    ("uchile", "Ingeniería en Recursos Hídricos", "Facultad de Ciencias Forestales y de la Conservación de la Naturaleza"),
    ("uchile", "Ingeniería en Alimentos", "Facultad de Ciencias Químicas y Farmacéuticas"),
    ("uc", "Agronomía e Ingeniería Forestal", "Facultad de Agronomía y Sistemas Naturales"),
    ("usach", "Ingeniería de Alimentos", "Otra facultad (por confirmar)"),
    ("usach", "Ingeniería en Agronegocios", "Otra facultad (por confirmar)"),
    ("usach", "Ingeniería Estadística", "Otra facultad (por confirmar)"),
    ("usach", "Ingeniería Física", "Otra facultad (por confirmar)"),
    ("usach", "Ingeniería Matemática", "Otra facultad (por confirmar)"),
    ("unab", "Ingeniería en Administración de Empresas", "Área de negocios"),
    ("unab", "Ingeniería en Negocios Internacionales", "Área de negocios"),
    ("unab", "Ingeniería en Administración Hotelera Internacional", "Área de turismo"),
    ("unab", "Ingeniería en Turismo y Hotelería", "Área de turismo"),
]

# Códigos DEMRE Admisión 2027 (verificados contra data/demre_2027.json). Varios códigos = mismo programa en distintos campus de Santiago.
DEMRE = {
 "uc-ingenieria":["12039"],"uc-lic-ciencia-datos":["12089"],"uc-lic-ciencia-computacion":["12100"],"uc-construccion-civil":["12038"],
 "uc-ing-recursos-naturales":["12101"],"uc-ingenieria-comercial":["12014"],
 "uchile-plan-comun":["11045"],"uchile-ingenieria-comercial":["11042"],
 "usm-plan-comun":["15300"],"usm-civil":["15311"],"usm-civil-minas":["15312"],"usm-civil-electrica":["15330"],"usm-civil-fisica":["15384"],
 "usm-civil-informatica":["15360"],"usm-civil-matematica":["15301"],"usm-civil-mecanica":["15340"],"usm-civil-quimica":["15350"],
 "usm-civil-telematica":["15361"],"usm-diseno-productos":["15381"],"usm-civil-industrial":["15270"],"usm-aviacion-comercial":["15220"],
 "usm-ingenieria-comercial":["15271"],
 "usach-civil-biomedica":["16101"],"usach-civil-en-ambiente":["16105"],"usach-civil-en-biotecnologia":["16104"],
 "usach-civil-en-electricidad":["16001"],"usach-civil-en-geomensura-y-geomatica":["16107"],"usach-civil-en-mecanica":["16005"],
 "usach-civil-en-metalurgia":["16006"],"usach-civil-en-minas":["16007"],"usach-civil-en-obras-civiles":["16008"],"usach-civil-en-quimica":["16009"],
 "usach-civil-en-telematica":["16102"],"usach-civil-en-territorio-y-medio-ambiente":["16111"],"usach-civil-industrial":["16003"],
 "usach-civil-mecatronica":["16103"],"usach-civil-informatica-plan-comun":["16113"],
 "usach-ejecucion-en-climatizacion":["16021"],"usach-ejecucion-en-computacion-e-informatica":["16014"],"usach-ejecucion-en-electricidad":["16011"],
 "usach-ejecucion-en-mecanica":["16015"],"usach-ejecucion-en-metalurgia":["16016"],"usach-ejecucion-en-minas":["16017"],
 "usach-ejecucion-en-quimica":["16019"],"usach-ejecucion-industrial":["16013"],"usach-ingenieria-comercial":["16035"],
 "unab-civil":["41044"],"unab-civil-electrica":["41204"],"unab-civil-minas":["41130"],"unab-civil-industrial":["41046","41206"],
 "unab-civil-informatica":["41045","41207"],"unab-civil-biomedica":["41227"],"unab-automatizacion-robotica":["41047"],
 "unab-computacion-informatica":["41048"],"unab-construccion":["41049"],"unab-industrial":["41055"],"unab-ambiental":["41024"],
 "unab-fisica":["41011"],"unab-biotecnologia":["41006"],"unab-engineering-technology-management":["41226"],
 "unab-computer-science-engineering":["41222"],"unab-ingenieria-comercial":["41129","41028"],
 "udp-plan-comun":["38080"],"udp-civil-industrial":["38174"],"udp-civil-obras-civiles":["38176"],"udp-civil-informatica-telecom":["38175"],
 "udp-civil-ciencia-datos-ia":["38346"],"udp-ingenieria-comercial":["38003"],"udp-control-gestion":["38292"],
 "uai-plan-comun":["42002"],"uai-computer-science":["42202"],"uai-bachillerato-ing-civil":["42012"],"uai-doble-arquitectura-industrial":["42106"],
 "uai-negocios-tecnologia":["42101"],"uai-ingenieria-comercial":["42001"],
 "udd-plan-comun":["44043"],"udd-civil-industrial":["44015"],"udd-civil-obras-civiles":["44014"],"udd-civil-mineria":["44039"],
 "udd-civil-informatica-innovacion":["44046"],"udd-civil-informatica-ia":["44052"],"udd-civil-biomedicina":["44051"],
 "udd-ingenieria-comercial":["44008"],
}

def enriquecer(root):
    path = root / "data" / "demre_2027.json"
    if not path.exists():
        print("aviso: falta data/demre_2027.json (correr scripts/parse_demre.py)"); return
    filas = {r["codigo"]: r for r in json.loads(path.read_text(encoding="utf-8"))["carreras"]}
    for x in P:
        cods = DEMRE.get(x["id"])
        if not cods: continue
        rs = [filas[c] for c in cods if c in filas]
        assert len(rs) == len(cods), f"código no encontrado para {x['id']}: {cods}"
        x["codigo_demre"] = cods[0] if len(cods) == 1 else cods
        vac = [r["vacantes_regulares"] for r in rs if r["vacantes_regulares"] is not None]
        x["vacantes_regulares_2027"] = sum(vac) if vac else None
        x["ponderaciones_2027"] = rs[0]["ponderaciones"]
        x["exige_m2"] = rs[0]["exige_m2"]
        x["hyc_o_ciencias"] = rs[0]["hyc_o_ciencias"]
        x["puntaje_ponderado_minimo_2027"] = rs[0].get("puntaje_ponderado_minimo")
        x["promedio_cl_m1_minimo_2027"] = rs[0].get("promedio_cl_m1_minimo")
        if len(rs) > 1:
            x["codigos_detalle"] = [{"codigo": r["codigo"], "nombre": r["nombre"], "vacantes": r["vacantes_regulares"]} for r in rs]
        if "demre_2027" not in x["fuentes"]: x["fuentes"].append("demre_2027")

def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    data = root / "data"
    data.mkdir(exist_ok=True)
    ids = [x["id"] for x in P]
    assert len(ids) == len(set(ids)), "ids duplicados"
    enriquecer(root)
    for x in P:
        for f in x["fuentes"]:
            assert f in FUENTES, f"fuente desconocida {f}"
    out = {
        "version": "0.5", "consultado": CONSULTADO,
        "alcance": "Facultad/Escuela de Ingeniería (sede Santiago) + Ingeniería Comercial, 8 universidades",
        "fuentes": {k: {"nombre": v[0], "url": v[1]} for k, v in FUENTES.items()},
        "universidades": UNIVERSIDADES,
        "programas": P,
        "fuera_de_alcance": [{"universidad_id": u, "nombre": n, "facultad": f} for u, n, f in FUERA],
    }
    (data / "inventario.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    cols = ["id", "universidad", "nombre_oficial", "categoria", "tipo_ingreso", "en_alcance", "facultad",
            "campus", "codigo_demre", "vacantes_regulares_2027", "exige_m2", "nota"]
    with open(data / "inventario.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(P)
    print(f"{len(P)} programas escritos")

if __name__ == "__main__":
    main()
