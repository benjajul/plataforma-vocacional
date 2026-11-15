"""Genera data/oportunidades.json: lo que cada universidad ofrece además del título.

Secciones por universidad: en qué destaca, seguir estudiando (magíster), al extranjero (doble título e intercambio),
prácticas, rankings y una lectura de orientación (interpretación propia, marcada como tal).
Datos consultados el 09-11-2026 en fuentes oficiales salvo que la fuente diga lo contrario.
Solo universidades en FOCO (scripts/config.py).
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from config import FOCO

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONSULTADO = "2026-11-09"

F = {  # fuentes
 "qs26": ("Emol — QS World University Rankings by Subject 2026 (25-03-2026)", "https://www.emol.com/noticias/Nacional/2026/03/25/1195345/universidades-chilenas-ranking-mundial-materia.html", False),
 "qs25": ("Meganoticias — QS by Subject 2025, Ingeniería y Tecnología (12-03-2025)", "https://www.meganoticias.cl/nacional/478718-mejores-universidades-chilenas-en-ingeneria-pdp-12-03-2025.html", False),
 "uch_art": ("FCFM — Articulación pregrado y magíster (EPEC 2024)", "https://ingenieria.uchile.cl/dam/jcr:ec5338a6-a331-459a-8a5a-f1329a994b43/ARTICULACION%20EPEC%20FCFM%202024.pdf", True),
 "uch_dt": ("U. de Chile — Doble titulación con las Écoles Centrales (28-03-2024)", "https://www.uchile.cl/noticias/214599/programa-doble-titulacion-visita-institucional-de-ecoles-centrales", True),
 "uch_prac": ("FCFM DIMEC — Normativa de prácticas profesionales (2024)", "https://dimec.uchile.cl/wp-content/uploads/2024/11/Normativa_practicas_profesionales_de_DIMEC.pdf", True),
 "uc_dt": ("Ingeniería UC — Guía Doble Título 2025", "https://dobletitulo.ing.uc.cl/wp-content/uploads/2025/08/Guia-Doble-Titulo-2025.pdf", True),
 "uc_ext": ("Ingeniería UC — Estudia en el extranjero", "https://www.ing.uc.cl/programas-de-estudio/estudia-en-el-extranjero/", True),
 "uc_plan": ("Ingeniería UC — Plan de estudios (majors y minors)", "https://www.ing.uc.cl/en/programas-de-estudio/pregrado/plan-estudios/plan-estudios-ingenieria-uc", True),
 "uc_abet": ("Ingeniería UC — Títulos profesionales y acreditación ABET", "https://www.ing.uc.cl/en/programas-de-estudio/pregrado/plan-estudios/titulos-profesionales-ingenieria/", True),
 "uc_prac": ("Ingeniería UC — Actividades del alumno (prácticas)", "https://www.ing.uc.cl/wp-content/uploads/2021/01/Actividades-Alumno-Ingenier%C3%ADa-UC.pdf", True),
 "uc_brochure": ("Admisión UC — Ingeniería y Tecnología", "https://admision.uc.cl/htdocs/content/uploads/2023/06/Brochure-Ingenieria-y-Tecnologia.pdf", True),
 "usm_dt": ("USM Internacional — Convenios de doble título", "https://internacional.usm.cl/movilidad/desde-la-usm-internacional/doble-titulacion/convenios-de-doble-titulo/", True),
 "usm_prac": ("USM Departamento de Industrias — Manual de prácticas (2026)", "https://www.industrias.usm.cl/wp-content/uploads/2026/08/Manual_practicas_DI.pdf", True),
 "usm_acr": ("Acreditaci — Programas acreditados con criterios internacionales", "https://www.acreditaci.cl/en/accredited-programs/accredited-under-international-criteria/", True),
 "usm_emp": ("USM — Dashboard Ing. Civil Informática (estudio de empleabilidad 2022)", "https://gestal.usm.cl/wp-content/uploads/2023/05/Dashboard-Carreras-Ingenieria-Civil-Informatica-Casa-Central-San-Joaquin-2022.pdf", True),
 "usach_art": ("USACH — Acuerdo de articulación Ing. Civil Industrial y Magíster", "https://mcii.usach.cl/sites/mcii/files/acuerdoarticulacionvipo_vra_mcii_ici2012_ici2020_firmadotodos.pdf", True),
 "usach_pol": ("USACH — Política institucional de articulación (2026)", "https://proyectoipg.usach.cl/ipg/wp-content/uploads/2026/04/POLITICA-INSTITUCIONAL-DE-ARTICULACION.pdf", True),
 "usach_mov": ("USACH DRII — Reglamento de movilidad estudiantil internacional", "https://www.drii.usach.cl/sites/drii/files/resolucion_reglamento_de_movilidad_estudiantil_internacional.pdf", True),
 "usach_conv": ("USACH FING — Proceso de convenios internacionales", "https://vimefing.usach.cl/wp-content/uploads/2023/11/Infografia_proceso_convenios_internacionales.pdf", True),
 "usach_prac": ("USACH FING — Normativa de prácticas profesionales (2019)", "https://finginternacional.usach.cl/sites/ingenieriaglobal/files/resolucion_ndeg6151_de_22.08.19_practicas_profesionales.pdf", True),
 "udp_ici": ("Admisión UDP — Ingeniería Civil Industrial 2026", "https://admision.udp.cl/cms/wp-content/uploads/2025/09/INGENIERIA-CIVIL-INDUSTRIAL_2026.pdf", True),
 "udp_pos": ("UDP — Feria de posgrados, Facultad de Ingeniería y Ciencias", "https://feriavirtualposgrados.udp.cl/cms/wp-content/uploads/2023/09/ingenieria_feria.pdf", True),
 "udp_int": ("UDP Internacional — Folleto Globaliza UDP", "https://internacional.udp.cl/cms/wp-content/uploads/2023/07/230711_Folleto_GlobalizaUDP.pdf", True),
 "udp_fic": ("UDP — Cuenta pública Facultad de Ingeniería y Ciencias 2022", "https://ingenieriayciencias.udp.cl/cms/wp-content/uploads/2023/05/Cuenta-FIC-2022-10.05.2023.pdf", True),
}

# Comparación rápida (una celda por universidad)
FILAS = [
 ("doble", "Doble título en el extranjero"),
 ("intercambio", "Intercambio semestral"),
 ("magister", "Título + magíster articulado"),
 ("practicas", "Prácticas obligatorias"),
 ("qs", "QS 2026 Ingeniería y Tecnología"),
 ("acred", "Acreditación internacional"),
]

U = {
 "uchile": {
  "resumen": "Facultad de ciencias e ingeniería con plan común amplio (incluye Geología, Geofísica, Astronomía y Física) y mucha investigación. Primera de Chile en minería en el ranking QS por materia.",
  "tabla": {"doble": ("si", "Écoles Centrales (Francia), desde 2014"), "intercambio": ("si", "Sí (cifras no publicadas en lo consultado)"),
            "magister": ("si", "Sí, una sola tesis para ambos"), "practicas": ("si", "2 prácticas, mín. 180 h cada una*"),
            "qs": ("si", "=132 del mundo · 2.ª de Chile"), "acred": ("na", "No encontrada")},
  "destaca": [
   ("Ingeniería en Minas y Mineralurgia: 16.ª del mundo y 1.ª de Latinoamérica (QS 2026).", "qs26"),
   ("Ciencias de la Computación: =118 del mundo, la mejor ubicada de Chile (QS 2026).", "qs26"),
   ("Ingeniería y Tecnología en general: =132 del mundo (QS 2026).", "qs26"),
  ],
  "magister": [("Articulación pregrado–magíster: en la etapa de especialidad se puede cursar en paralelo un magíster de la FCFM (de la misma u otra área) y obtener título y magíster con una sola tesis, un examen y un informe final. Requiere situación académica regular y aprobación del comité del magíster.", "uch_art")],
  "extranjero": [("Doble titulación con el Groupe des Écoles Centrales (CentraleSupélec, Lyon, Nantes, Lille y Marsella): unos 2 años en Francia y regreso a Chile para titularse. Convenio desde 2014; más de 50 estudiantes lo han cursado (marzo 2024).", "uch_dt")],
  "practicas": [("Prácticas Profesional I (4.º año) y II (5.º año), mínimo 180 horas cada una (unas 4 semanas), recomendadas en vacaciones de verano. *Dato de Ingeniería Civil Mecánica; cada departamento fija su norma.", "uch_prac")],
  "orientacion": "Fuerte en ciencias e investigación: es la opción que más abre la puerta a magíster, doctorado y carreras científicas, sin dejar de lado la industria (minería, energía, computación).",
 },
 "uc": {
  "resumen": "Licenciatura de 4 años con major y minor, que permite combinar una ingeniería con otra área (por ejemplo, gestión o datos). Primera de Chile en Ingeniería y Tecnología en el ranking QS por materia.",
  "tabla": {"doble": ("si", "4 instituciones (Francia e Italia)"), "intercambio": ("si", "Más de 350 universidades socias"),
            "magister": ("si", "Título + magíster UC"), "practicas": ("si", "2 prácticas: ≥4 semanas y ≥360 h"),
            "qs": ("si", "=99 del mundo · 1.ª de Chile"), "acred": ("si", "ABET en 5 títulos (dato 2021)")},
  "destaca": [
   ("Ingeniería y Tecnología: =99 del mundo, 1.ª de Chile (QS 2026).", "qs26"),
   ("Ingeniería Civil y Estructural: 41.ª del mundo y 1.ª de Latinoamérica (QS 2026).", "qs26"),
   ("Negocios y Estudios de Gestión: =64 del mundo (QS 2026), útil si se combina ingeniería con un minor de gestión.", "qs26"),
   ("Acreditación ABET (EE.UU.) desde 2007 en Ingeniería Civil y en los títulos de Ingeniero Civil de Industrias con diploma en Química, Mecánica, Eléctrica y Computación. La página es de 2021: conviene confirmar vigencia.", "uc_abet"),
   ("Flexibilidad: 13 majors disciplinarios, 9 interdisciplinarios, 20 minors de profundidad y 19 de amplitud.", "uc_plan"),
   ("Además del título de ingeniero, se puede postular a un segundo título UC (Medicina, Arquitectura o Diseño), con cupos limitados.", "uc_plan"),
  ],
  "magister": [("Tras la licenciatura, una de las rutas es título profesional + magíster en Ingeniería UC. Se pueden iniciar programas de magíster y doctorado UC mientras se cursa el título.", "uc_brochure")],
  "extranjero": [
   ("Doble título con el Groupe des Écoles Centrales, École Polytechnique, Mines Saint-Étienne (Francia) y Politecnico di Milano (Italia). Se va después de 8 semestres (400 créditos) y se estudian 4 semestres afuera. Requisitos: promedio 5,0 a 5,5, inglés y, para Francia, francés A2. Lo han cursado 297 estudiantes.", "uc_dt"),
   ("Intercambio de uno o dos semestres con más de 350 universidades.", "uc_ext"),
  ],
  "practicas": [("Práctica I (trabajo operativo, al menos 4 semanas) y Práctica II (profesional, al menos 360 horas, unos 2 meses).", "uc_prac")],
  "orientacion": "La más flexible: el sistema de major y minor permite armar un perfil técnico, de gestión o mixto. El título de Ingeniero Civil de Industrias con diplomas mezcla ingeniería y gestión; junto al buen ranking en Negocios, facilita orientarse a cargos de gestión.",
 },
 "usm": {
  "resumen": "Universidad tecnológica con tradición industrial. Tiene las prácticas más largas del grupo y doble título con Politecnico di Milano para casi todas sus ingenierías.",
  "tabla": {"doble": ("si", "4 instituciones (Italia y Francia)"), "intercambio": ("si", "Sí (cifras no publicadas en lo consultado)"),
            "magister": ("na", "No se encontró programa formal"), "practicas": ("si", "2 prácticas de 8 semanas (320 h)*"),
            "qs": ("si", "=273 del mundo · 3.ª de Chile"), "acred": ("si", "Ing. Civil Informática (desde dic. 2024)")},
  "destaca": [
   ("Ingeniería y Tecnología: =273 del mundo, 3.ª de Chile (QS 2026). También aparece en Civil y Estructural (201-275), Eléctrica (251-300) y Computación (351-400).", "qs26"),
   ("Ingeniería Civil Informática tiene acreditación con criterios internacionales (equivalentes al Acuerdo de Washington), vigente desde diciembre de 2024.", "usm_acr"),
   ("Ing. Civil Informática: empleabilidad de 97 % (Casa Central) y 95 % (San Joaquín). El 38 % y 22 % de los titulados sigue estudiando (estudio propio 2022).", "usm_emp"),
  ],
  "magister": [("No se encontró un programa formal de título + magíster articulado. Sí hay magíster en la USM, pero la continuidad depende de cada programa.", None)],
  "extranjero": [("Doble título con:\n• Politecnico di Milano: todas las ingenierías de Casa Central y Campus Santiago, salvo Diseño de Productos y Obras Civiles; 4 semestres.\n• INSA Lyon: Informática y Mecánica; 2 años.\n• IMT Atlantique: Telemática.\n• Audencia Nantes: Ingeniería Comercial.", "usm_dt")],
  "practicas": [("Práctica Industrial y Práctica Profesional, de 8 semanas (320 horas) cada una: la primera tras aprobar el 5.º semestre y la segunda tras el 8.º. *Dato de Ingeniería Civil Industrial.", "usm_prac")],
  "orientacion": "Perfil técnico y de planta: prácticas largas y tradición en la industria y la ingeniería aplicada. Prepara sobre todo para cargos técnicos y operativos.",
 },
 "usach": {
  "resumen": "Universidad estatal con la oferta de ingeniería más amplia del grupo, que incluye carreras civiles y de ejecución (más cortas y aplicadas). Tiene un magíster articulado con cupos para Industrial.",
  "tabla": {"doble": ("warn", "Contemplado en sus convenios; no publica lista"), "intercambio": ("si", "Sí, tras aprobar 1.er año; becas"),
            "magister": ("si", "Industrial: hasta 10 cupos/año"), "practicas": ("si", "Mín. 180 h; se pueden hacer afuera"),
            "qs": ("warn", "353 del mundo (QS 2025)"), "acred": ("na", "No encontrada")},
  "destaca": [
   ("Ingeniería Mecánica: 351-400 del mundo (QS 2026).", "qs26"),
   ("Ingeniería y Tecnología en general: puesto 353 del mundo (QS 2025; en la nota de 2026 no aparece entre las 3 chilenas mejor ubicadas).", "qs25"),
   ("Junto a las ingenierías civiles ofrece ingenierías de ejecución: carreras más cortas y aplicadas, con su propio corte de ingreso.", None),
  ],
  "magister": [
   ("Ingeniería Civil Industrial → Magíster en Ciencias de la Ingeniería, mención Industrial: hasta 10 estudiantes por año, 8 cursos y el trabajo de graduación compartidos (90 créditos SCT), en los últimos semestres.", "usach_art"),
   ("La universidad aprobó una política institucional de articulación (2026) para extender este tipo de rutas; todavía no detalla programas de ingeniería.", "usach_pol"),
  ],
  "extranjero": [
   ("Intercambio semestral con universidades con convenio, después de aprobar el primer año. Hay becas según vulnerabilidad y mérito, y los cursos se reconocen con un contrato de estudios previo.", "usach_mov"),
   ("La Facultad de Ingeniería contempla convenios de doble titulación, pero no se encontró una lista pública de socios.", "usach_conv"),
  ],
  "practicas": [("Prácticas obligatorias de al menos 180 horas, tras aprobar el 5.º nivel. Se pueden hacer en el extranjero (jornada completa, hasta 3 meses).", "usach_prac")],
  "orientacion": "Perfil aplicado e industrial. Las carreras de ejecución apuntan a roles operativos; las civiles abren también la puerta a la gestión.",
 },
 "udp": {
  "resumen": "Facultad más pequeña, con plan común de 1 año, pasantías laborales tempranas y magíster de continuidad con un solo semestre adicional.",
  "tabla": {"doble": ("na", "No se encontró para ingeniería"), "intercambio": ("si", "Más de 150 instituciones (toda la UDP)"),
            "magister": ("si", "1 semestre adicional"), "practicas": ("si", "2 pasantías de 200 h"),
            "qs": ("na", "No aparece entre las chilenas destacadas"), "acred": ("na", "No encontrada")},
  "destaca": [
   ("Ingeniería Civil Industrial con tres menciones: Operaciones y Logística, Análisis de Datos y Energía Sostenible.", "udp_ici"),
   ("Red de empresas: en 2022 hubo 696 estudiantes en práctica en 494 empresas, y 334 titulados de ingeniería.", "udp_fic"),
  ],
  "magister": [("Magíster de continuidad: se postula al obtener la licenciatura (tras el 8.º semestre) y se cursa con solo un semestre adicional.", "udp_pos"), ("Detalle en Ingeniería Civil Industrial: se postula al magíster tras el 8.º semestre, incluida la Pasantía Laboral II.", "udp_ici")],
  "extranjero": [
   ("La UDP tiene convenios con más de 150 instituciones extranjeras (cifra de toda la universidad).", "udp_int"),
   ("En ingeniería la movilidad saliente ha sido baja: entre 2 y 10 estudiantes por año en 2016-2021.", "udp_fic"),
  ],
  "practicas": [("Pasantía Laboral I (entre los semestres 4 y 5) y Pasantía Laboral II (entre el 8 y el 9), de al menos 200 horas cada una.", "udp_ici")],
  "orientacion": "Orientada a la gestión y a la empresa: pasantías desde el 2.º año, menciones aplicadas y discurso centrado en personas y sostenibilidad. Es la más cercana al perfil de gestión o gerencial entre las cinco.",
 },
}

def main():
    unis = json.loads((ROOT / "data" / "inventario.json").read_text(encoding="utf-8"))["universidades"]
    salida = []
    for uid in FOCO:
        u = U[uid]
        def items(xs):
            return [{"texto": t, "fuente": k} for t, k in xs]
        salida.append({"id": uid, "nombre": unis[uid] if isinstance(unis[uid], str) else unis[uid].get("nombre", uid),
                       "resumen": u["resumen"], "tabla": {k: {"estado": v[0], "texto": v[1]} for k, v in u["tabla"].items()},
                       "destaca": items(u["destaca"]), "magister": items(u["magister"]), "extranjero": items(u["extranjero"]),
                       "practicas": items(u["practicas"]), "orientacion": u["orientacion"]})
    out = {"version": "0.7", "consultado": CONSULTADO, "filas": [{"id": a, "nombre": b} for a, b in FILAS],
           "universidades": salida,
           "fuentes": {k: {"nombre": n, "url": url, "oficial": of} for k, (n, url, of) in F.items()},
           "pendiente": "Empleabilidad al 1.er año e ingreso al 4.º año por carrera (Mi Futuro, Mineduc): mifuturo.cl no se pudo consultar desde esta sesión. Se agregará cuando se pueda leer el buscador.",
           "nota_orientacion": "La 'orientación' es una lectura nuestra a partir de los datos de esta página (prácticas, menciones, rankings, rutas de continuidad), no una clasificación oficial. Ninguna fuente pública mide qué tan 'gerencial' o 'técnico' es el egresado de cada universidad."}
    (ROOT / "data" / "oportunidades.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(salida)} universidades; {len(F)} fuentes")

if __name__ == "__main__":
    main()
