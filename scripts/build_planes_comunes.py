"""Genera data/planes_comunes.json — cómo funciona cada plan común y a qué carreras lleva.

Ejecutar desde la raíz del repo:  python3 scripts/build_planes_comunes.py
Datos consultados el 08-11-2026 (páginas oficiales; ver 'fuentes' de cada plan).

Lógica de la plataforma:
  plan común (puerta de entrada) --[regla de selección]--> salida (carrera / título) --> malla
  Una salida puede apuntar a 'programa_directo_id' cuando la misma carrera también admite ingreso directo
  (USM, UDP, UDD), para que la plataforma muestre ambas puertas hacia la misma carrera.

Valores de 'seleccion.mecanismo':
  libre          -> el estudiante elige cualquier salida, sin cupos
  garantizado    -> cupo asegurado en cualquier salida de la facultad
  competitivo    -> hay cupos por salida; se asignan por ranking académico
  sin_postulacion-> el título se articula sin postular (UC); ver excepciones
  no_informado   -> la fuente oficial no lo dice
"""
import json, pathlib

CONSULTADO = "2026-11-08"

def salida(nombre, *, titulo=None, malla=None, programa_directo_id=None, tipo="ing_civil", nota=""):
    return {"nombre": nombre, "titulo": titulo or nombre, "tipo": tipo, "malla_url": malla,
            "programa_directo_id": programa_directo_id, "nota": nota}

UCH = "https://uchile.cl/carreras/"
SP = "https://usmcl-my.sharepoint.com/:b:/g/personal/diseno_admision_usm_cl/"
UCMAJ = "https://www.ing.uc.cl/"

PLANES = [
  # ---------------- U. de Chile ----------------
  {
    "programa_id": "uchile-plan-comun",
    "universidad_id": "uchile",
    "nombre": "Ingeniería y Ciencias, Plan Común (FCFM)",
    "resumen": "Todos entran a un mismo plan común de 4 semestres en Beauchef. Al terminar el 4.º semestre cada estudiante elige su especialidad libremente: no hay cupos por especialidad.",
    "duracion_plan_comun_semestres": 4,
    "seleccion": {
      "momento": "Al finalizar el 4.º semestre (plazo obligatorio)",
      "mecanismo": "libre",
      "cupos": "sin_limite",
      "criterio": "No hay selección: el estudiante elige.",
      "requisitos": "Elegir dentro del plazo para conservar beneficios MINEDUC (p. ej. gratuidad).",
      "irrevocable": None,
      "apoyo": "Unidad de Orientación Vocacional e 'Inicia Beauchef' presentan las especialidades.",
    },
    "duracion_total": "11 semestres (Ingeniería Civil, incluye plan común)",
    "grado_intermedio": "Licenciatura en Ciencias de la Ingeniería, mención según especialidad",
    "salidas": [
      salida("Ingeniería Civil", titulo="Ingeniero/a Civil (menciones Estructuras, Construcción y Geotecnia; Hidráulica, Sanitaria y Ambiental; Transporte)", malla=UCH+"4969/ingenieria-civil"),
      salida("Ingeniería Civil de Minas", malla=UCH+"4977/ingenieria-civil-de-minas"),
      salida("Ingeniería Civil en Biotecnología", malla=UCH+"4970/ingenieria-civil-en-biotecnologia"),
      salida("Ingeniería Civil en Computación", malla=UCH+"4971/ingenieria-civil-en-computacion"),
      salida("Ingeniería Civil Eléctrica", malla=UCH+"4972/ingenieria-civil-electrica"),
      salida("Ingeniería Civil Industrial", malla="https://uchile.cl/dam/jcr:cdc0ae92-f9b3-46fb-8aff-4d49fe4c6440/MallaCivilIndustrial2021.jpg",
             nota="Especialización desde el 5.º semestre."),
      salida("Ingeniería Civil Matemática", malla=UCH+"4974/ingenieria-civil-matematica"),
      salida("Ingeniería Civil Mecánica", malla=UCH+"4976/ingenieria-civil-mecanica"),
      salida("Ingeniería Civil Química", malla=UCH+"4978/ingenieria-civil-quimica"),
      salida("Geología", tipo="no_ingenieria"),
      salida("Geofísica", tipo="no_ingenieria"),
      salida("Licenciatura en Ciencias mención Astronomía", tipo="no_ingenieria"),
      salida("Licenciatura en Ciencias mención Física", tipo="no_ingenieria"),
    ],
    "fuentes": [
      {"nombre": "FCFM — Preguntas frecuentes de admisión", "url": "https://ingenieria.uchile.cl/admision/preguntas-frecuentes"},
      {"nombre": "FCFM — Plazo para elegir tu especialidad", "url": "https://ingenieria.uchile.cl/escuela/pregrado/informacion-para-estudiantes/plazo-para-elegir-tu-especialidad"},
      {"nombre": "U. de Chile — Ingeniería Civil", "url": "https://uchile.cl/carreras/4969/ingenieria-civil"},
    ],
  },
  # ---------------- UC ----------------
  {
    "programa_id": "uc-ingenieria",
    "universidad_id": "uc",
    "nombre": "Ingeniería UC (Licenciatura en Ciencias de la Ingeniería + título)",
    "resumen": "Se entra a 'Ingeniería'. Los primeros 4 años son una licenciatura donde cada estudiante arma su perfil con un major (22 opciones) y un minor. Después de la licenciatura se 'articula' con uno de 7 títulos de Ingeniero Civil UC, sin postulación separada; varios títulos tienen 'diplomas' que definen la especialidad.",
    "duracion_plan_comun_semestres": None,
    "seleccion": {
      "momento": "Major y minor durante la licenciatura (4 años); título después de la licenciatura",
      "mecanismo": "sin_postulacion",
      "cupos": "no_informado",
      "criterio": "Para continuar con el título de Ingeniero Civil UC no se necesita postulación separada. La duración de la articulación depende de la combinación major/minor/título.",
      "requisitos": "Completar la Licenciatura en Ciencias de la Ingeniería (major + minor + requisitos adicionales).",
      "irrevocable": None,
      "excepciones": "Las articulaciones con Medicina, Arquitectura y Diseño UC tienen vacantes limitadas y requieren postulación y selección.",
      "pendiente": "Confirmar si algún major tiene cupos o requisitos de entrada, y en qué semestre se declara.",
    },
    "duracion_total": "4 años de licenciatura + articulación al título (duración variable según combinación)",
    "grado_intermedio": "Licenciatura en Ciencias de la Ingeniería",
    "etapa_intermedia": {
      "nombre": "Majors",
      "opciones": [
        {"nombre": "Ingeniería y Ciencias Ambientales", "url": UCMAJ+"major-en-ingenieria-y-ciencias-ambientales/"},
        {"nombre": "Computación y Sistemas de Información", "url": UCMAJ+"major-en-computacion-y-sistemas-de-informacion/"},
        {"nombre": "Ingeniería de Construcción", "url": "http://www.ing.uc.cl/programas-de-estudio/major-ingenieria-construccion/"},
        {"nombre": "Ingeniería Eléctrica", "url": "http://www.ing.uc.cl/programas-de-estudio/major-ingenieria-electrica/"},
        {"nombre": "Ingeniería Estructural", "url": "http://www.ing.uc.cl/programas-de-estudio/major-ingenieria-estructural/"},
        {"nombre": "Ingeniería Geotécnica", "url": "http://www.ing.uc.cl/programas-de-estudio/major-ingenieria-geotecnica/"},
        {"nombre": "Ingeniería y Ciencias del Agua", "url": UCMAJ+"major-ingenieria-y-ciencias-agua/"},
        {"nombre": "Ingeniería Mecánica", "url": "http://www.ing.uc.cl/programas-de-estudio/major-ingenieria-mecanica/"},
        {"nombre": "Ingeniería Minera", "url": "http://www.ing.uc.cl/programas-de-estudio/major-ingenieria-minera/"},
        {"nombre": "Ingeniería Química", "url": UCMAJ+"major-ingenieria-quimica/"},
        {"nombre": "Ingeniería en Investigación Operativa", "url": UCMAJ+"major-investigacion-operativa/"},
        {"nombre": "Ingeniería de Sistemas de Transportes", "url": UCMAJ+"major-sistemas-transporte/"},
        {"nombre": "Ingeniería de Software", "url": UCMAJ+"major-en-ingenieria-de-software/"},
        {"nombre": "Geociencias (interdisciplinario)", "url": UCMAJ+"major-en-geociencias/"},
        {"nombre": "Ingeniería Biológica (interdisciplinario)", "url": UCMAJ+"programas-de-estudio/pregrado/plan-estudios/cuales-los-majors-los-minors-ingenieria-uc/major-ingenieria-biologica/"},
        {"nombre": "Ingeniería Biomédica (interdisciplinario)", "url": UCMAJ+"programas-de-estudio/pregrado/plan-estudios/cuales-los-majors-los-minors-ingenieria-uc/major-ingenieria-biomedica/"},
        {"nombre": "Ingeniería Matemática (interdisciplinario)", "url": UCMAJ+"programas-de-estudio/pregrado/plan-estudios/cuales-los-majors-los-minors-ingenieria-uc/major-ingenieria-matematica/"},
        {"nombre": "Ingeniería y Arquitectura (interdisciplinario)", "url": UCMAJ+"major-en-ingenieria-y-arquitectura/"},
        {"nombre": "Ingeniería, Diseño e Innovación (interdisciplinario)", "url": UCMAJ+"major-ingenieria-diseno-e-innovacion/"},
        {"nombre": "Ingeniería Robótica (interdisciplinario)", "url": UCMAJ+"programas-de-estudio/pregrado/plan-estudios/cuales-los-majors-los-minors-ingenieria-uc/major-ingenieria-robotica/"},
        {"nombre": "Ingeniería Física (interdisciplinario)", "url": UCMAJ+"programas-de-estudio/pregrado/plan-estudios/cuales-los-majors-los-minors-ingenieria-uc/ingenieria-fisica/"},
        {"nombre": "Ingeniería Civil (interdisciplinario)", "url": UCMAJ+"programas-de-estudio/pregrado/plan-estudios/cuales-los-majors-los-minors-ingenieria-uc/major-ingenieria-civil/"},
      ],
    },
    "salidas": [
      salida("Ingeniero Civil", titulo="Ingeniero Civil UC, con Diploma en: Ambiental · Diseño y Construcción de Obras · Ingeniería y Gestión de la Construcción · Estructural · Geotécnica · Hidráulica · Minería · Transporte"),
      salida("Ingeniero Civil de Industrias", titulo="Ingeniero Civil de Industrias UC, con Diploma en: Ambiental · Construcción · Bioprocesos · Computación · Eléctrica · Hidráulica · Matemática · Mecánica · Minería · Química · Tecnologías de la Información · Transporte",
             nota="Es la salida 'industrial' de la UC; se combina con un diploma técnico."),
      salida("Ingeniero Civil de Computación"),
      salida("Ingeniero Civil Electricista"),
      salida("Ingeniero Civil Mecánico"),
      salida("Ingeniero Civil de Biotecnología"),
      salida("Ingeniero Civil Matemático Computacional"),
      salida("Articulación con Médico Cirujano, Arquitecto o Diseñador UC", tipo="no_ingenieria",
             nota="Vacantes limitadas; requiere postulación y selección."),
    ],
    "fuentes": [
      {"nombre": "Ingeniería UC — ¿Cómo es nuestro plan de estudios?", "url": "https://www.ing.uc.cl/programas-de-estudio/pregrado/plan-estudios/plan-estudios-ingenieria-uc/"},
      {"nombre": "Ingeniería UC — Títulos profesionales", "url": "https://www.ing.uc.cl/programas-de-estudio/pregrado/plan-estudios/titulos-profesionales-ingenieria/"},
      {"nombre": "Ingeniería UC — Majors y minors", "url": "https://www.ing.uc.cl/programas-de-estudio/pregrado/plan-estudios/cuales-los-majors-los-minors-ingenieria-uc/"},
    ],
  },
  # ---------------- USM ----------------
  {
    "programa_id": "usm-plan-comun",
    "universidad_id": "usm",
    "nombre": "Ingeniería Civil Plan Común (Campus San Joaquín)",
    "resumen": "Programa para quienes aún no deciden su ingeniería. Tras aprobar el primer año se postula a una especialidad del mismo campus. Hay cupos por cohorte y se asignan por ranking del rendimiento académico de primer año. La asignación es irrevocable.",
    "duracion_plan_comun_semestres": 4,
    "seleccion": {
      "momento": "Al aprobar el primer año (2 semestres); proceso al cierre de semestre vía SIGA",
      "mecanismo": "competitivo",
      "cupos": "limitados",
      "criterio": "Ranking por promedio ponderado de las asignaturas de primer año, frente al resto de la generación. Se deben indicar 6 preferencias en orden.",
      "requisitos": "Aprobar el 100% de los créditos de los dos primeros semestres.",
      "irrevocable": True,
      "detalle": "Cupos no usados quedan para la misma cohorte en el proceso siguiente. Hay simulaciones periódicas para ver las posibilidades. Otros programas de la USM solo por cambio de carrera interno.",
      "cupos_publicos": False,
      "pendiente": "Los cupos por especialidad se publican en un portal interno con clave (SIGA). Confirmar si Civil Industrial (Vitacura) es accesible desde el plan común de San Joaquín.",
    },
    "duracion_total": "Plan común: 2 años (Bachiller). Las carreras de destino duran 10 semestres en total.",
    "grado_intermedio": "Bachiller/Bachillera en Ciencias de la Ingeniería",
    "malla_plan_comun": SP+"IQBnzEjwo1hrS4MvHlyeqZK4AdQ5qWvLM0Ce86i6BALCYsw?e=Z463TE",
    "salidas": [
      salida("Ingeniería Civil", malla=SP+"IQDcpUxPns9GRJq2WgCGaqJPAQYqzYwUZ5pd4KKswDeCVdg?e=9SzTnH", programa_directo_id="usm-civil"),
      salida("Ingeniería Civil de Minas", malla=SP+"IQBVUUO4UA03SqHG4jkxCGxwAenm-FJjo8gBPdxT0ec54Ew?e=DGySzl", programa_directo_id="usm-civil-minas"),
      salida("Ingeniería Civil Eléctrica", titulo="Ingeniero/a Civil Electricista", malla=SP+"IQDZ0sWXoGXvQJrfX6EyQyKYAYJROwzQQzfGTkVx0Bbl7Hs?e=5EwD9O", programa_directo_id="usm-civil-electrica"),
      salida("Ingeniería Civil Física", malla=SP+"IQBnqJYyFZxbQI2jB5dfO87KAcmviiBgOW-x-AjssTh660w?e=vtSKZo", programa_directo_id="usm-civil-fisica"),
      salida("Ingeniería Civil Informática", malla=SP+"IQCz2fCQ-qwoQLp3HpJkE6nCAWQ6F3XeXcswa-qyobhU7Xk?e=9s0YlQ", programa_directo_id="usm-civil-informatica"),
      salida("Ingeniería Civil Matemática", malla=SP+"IQD2zpR9tcUSR7DmKW25d6LdAUUO9Cwk_7SkZ9w5n-pXoJs?e=Kw6lvi", programa_directo_id="usm-civil-matematica"),
      salida("Ingeniería Civil Mecánica", malla=SP+"IQBJHhY7n5h_T5br1QVNCjGQAd5hpN4Tq0iSvTPceZQI0MI?e=hbDbs1", programa_directo_id="usm-civil-mecanica"),
      salida("Ingeniería Civil Química", malla=SP+"IQAb1xZ3jZAvR4Ejdm5nkqxwAegbwjH1cmalYmWGVz7KoyQ?e=5dHFlJ", programa_directo_id="usm-civil-quimica"),
      salida("Ingeniería Civil Telemática", malla=SP+"IQBdlCP7cd-MTp14pTPSSnecAUVvKtLmdGHjJq6P2ZJt-Zg?e=x0qaEJ", programa_directo_id="usm-civil-telematica"),
    ],
    "nota_salidas": "Lista = ingenierías civiles que se dictan en San Joaquín, según la regla 'oferta del campus donde esté matriculado'. La USM no publica la lista ni los cupos por cohorte fuera de su portal interno.",
    "fuentes": [
      {"nombre": "USM — Ingeniería Civil Plan Común", "url": "https://usm.cl/admision/carreras/ingenieria-civil-plan-comun/"},
      {"nombre": "USM — Circular Postulación a Especialidad (dic-2025)", "url": "https://autoservicio.usm.cl/docs/usmtransparente/informaciones/Circular_PostulacionesEspecialidad2.pdf"},
      {"nombre": "USM — Admisión Centralizada PAES (vacantes 2026)", "url": "https://usm.cl/admision/admision-centralizada-paes-3/"},
    ],
  },
  # ---------------- UDP ----------------
  {
    "programa_id": "udp-plan-comun",
    "universidad_id": "udp",
    "nombre": "Ingeniería Civil Plan Común",
    "resumen": "Primer año común. Al terminarlo se elige una de 4 ingenierías civiles sin límite de cupos. Se titula con título profesional + magíster de continuidad.",
    "duracion_plan_comun_semestres": 2,
    "seleccion": {"momento": "Al terminar el primer año", "mecanismo": "libre", "cupos": "sin_limite",
                  "criterio": "Sin selección; también se puede cambiar a otra carrera de la facultad sin cupo si se cumplen requisitos académicos.",
                  "requisitos": "Requisitos académicos del plan común.", "irrevocable": None},
    "duracion_total": "no informado en la fuente",
    "malla_plan_comun": "https://ingenieriayciencias.udp.cl/cms/wp-content/uploads/2025/12/INGENIERIA-CIVIL-PLAN-COMUN_2026.pdf",
    "salidas": [
      salida("Ingeniería Civil Industrial", malla="https://admision.udp.cl/cms/wp-content/uploads/2025/09/INGENIERIA-CIVIL-INDUSTRIAL_2026.pdf", programa_directo_id="udp-civil-industrial"),
      salida("Ingeniería Civil en Obras Civiles", malla="https://eoc.udp.cl/cms/wp-content/uploads/2023/12/MALLA-INGENIERIA-CIVIL-EN-OBRAS-CIVILES.pdf", programa_directo_id="udp-civil-obras-civiles", nota="Malla publicada en 2023."),
      salida("Ingeniería Civil en Informática y Telecomunicaciones", malla="https://eit.udp.cl/cms/wp-content/uploads/2025/12/INGENIERIA-CIVIL-EN-INFORMATICA-Y-TELECOMUNICACIONES.pdf", programa_directo_id="udp-civil-informatica-telecom"),
      salida("Ingeniería Civil en Ciencia de Datos e Inteligencia Artificial", malla="https://admision.udp.cl/cms/wp-content/uploads/2025/09/INGENIERIA-CIVIL-EN-CIENCIA-DE-DATOS-E-INTELIGENCIA-ARTIFICIAL_2026.pdf", programa_directo_id="udp-civil-ciencia-datos-ia"),
    ],
    "fuentes": [{"nombre": "UDP — Malla Ingeniería Civil Plan Común 2026", "url": "https://ingenieriayciencias.udp.cl/cms/wp-content/uploads/2025/12/INGENIERIA-CIVIL-PLAN-COMUN_2026.pdf"}],
  },
  # ---------------- UDD ----------------
  {
    "programa_id": "udd-plan-comun",
    "universidad_id": "udd",
    "nombre": "Ingeniería Civil Plan Común",
    "resumen": "Tres semestres comunes. Luego se elige especialidad con cupo garantizado en cualquier carrera de la facultad (salvo BioMedicina).",
    "duracion_plan_comun_semestres": 3,
    "seleccion": {"momento": "Al terminar el 3.er semestre", "mecanismo": "garantizado", "cupos": "sin_limite",
                  "criterio": "Cupo garantizado.", "requisitos": "no informado", "irrevocable": None,
                  "pendiente": "Fuente de 2024; confirmar si Informática e IA ya es salida del plan común."},
    "duracion_total": "11 semestres",
    "malla_plan_comun": "https://www.udd.cl/mallas/ingenieriacivilplancomun.pdf",
    "salidas": [
      salida("Ingeniería Civil Industrial", malla="https://ingenieria.udd.cl/files/2020/04/12.-ing-civil-pc_ing-civil-industrial.pdf", programa_directo_id="udd-civil-industrial", nota="Malla publicada en 2020."),
      salida("Ingeniería Civil en Obras Civiles", malla="https://ingenieria.udd.cl/files/2020/04/12.-ing-civil-pc_ing-civil-obras-civiles.pdf", programa_directo_id="udd-civil-obras-civiles", nota="Malla publicada en 2020."),
      salida("Ingeniería Civil en Minería", malla="https://ingenieria.udd.cl/files/2020/04/12.-ing-civil-pc_ing-civil-mineria-1.pdf", programa_directo_id="udd-civil-mineria", nota="Malla publicada en 2020."),
      salida("Ingeniería Civil en Informática e Innovación Tecnológica", programa_directo_id="udd-civil-informatica-innovacion"),
      salida("Ingeniería Civil en Informática e Inteligencia Artificial", programa_directo_id="udd-civil-informatica-ia", nota="Por confirmar como salida del plan común."),
      salida("Geología", tipo="no_ingenieria"),
    ],
    "fuentes": [{"nombre": "UDD — Plan común de ingenierías", "url": "https://ingenieria.udd.cl/files/2024/03/07-plan-comun-ingenierias.pdf"},
                {"nombre": "UDD — Facultad de Ingeniería, carreras", "url": "https://ingenieria.udd.cl/carreras/"}],
  },
  # ---------------- UAI ----------------
  {
    "programa_id": "uai-plan-comun",
    "universidad_id": "uai",
    "nombre": "Ingeniería Civil (Plan Común) — Peñalolén",
    "resumen": "En Santiago todas las ingenierías civiles de la UAI se ingresan por plan común, que lleva a 7 especialidades.",
    "duracion_plan_comun_semestres": None,
    "seleccion": {"momento": "no informado", "mecanismo": "no_informado", "cupos": "no_informado",
                  "criterio": "no informado", "requisitos": "no informado", "irrevocable": None,
                  "pendiente": "Buscar reglamento de elección de especialidad UAI."},
    "duracion_total": "no informado",
    "salidas": [salida(n) for n in ["Ingeniería Civil Industrial", "Ingeniería Civil Informática", "Ingeniería Civil en Bioingeniería",
                                    "Ingeniería Civil (Obras Civiles)", "Ingeniería Civil en Energía", "Ingeniería Civil Mecánica",
                                    "Ingeniería Civil en Minería"]],
    "fuentes": [{"nombre": "UAI — Facultad de Ingeniería y Ciencias", "url": "https://www.uai.cl/ingenieria-y-ciencias/carreras/nuestras-carreras"}],
  },
  # ---------------- USACH ----------------
  {
    "programa_id": "usach-civil-informatica-plan-comun",
    "universidad_id": "usach",
    "nombre": "Ingeniería Civil en Informática – Plan Común (nueva 2027)",
    "resumen": "Carrera nueva para Admisión 2027 (90 vacantes según prensa). Aún no hay información oficial sobre sus salidas.",
    "duracion_plan_comun_semestres": None,
    "seleccion": {"momento": "no informado", "mecanismo": "no_informado", "cupos": "no_informado",
                  "criterio": "no informado", "requisitos": "no informado", "irrevocable": None,
                  "pendiente": "Revisar ficha oficial USACH cuando se publique."},
    "duracion_total": "no informado",
    "salidas": [],
    "fuentes": [{"nombre": "USACH Admisión — Facultad de Ingeniería", "url": "https://admision.usach.cl/FING-USACH"}],
  },
]

def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    inv = json.loads((root / "data" / "inventario.json").read_text(encoding="utf-8"))
    ids = {p["id"] for p in inv["programas"]}
    for pc in PLANES:
        assert pc["programa_id"] in ids, f"plan común sin programa en inventario: {pc['programa_id']}"
        for s in pc["salidas"]:
            if s["programa_directo_id"]:
                assert s["programa_directo_id"] in ids, f"salida apunta a programa inexistente: {s['programa_directo_id']}"
        pc["consultado"] = CONSULTADO
    out = {"version": "0.3", "consultado": CONSULTADO, "planes_comunes": PLANES}
    (root / "data" / "planes_comunes.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(PLANES)} planes comunes, {sum(len(p['salidas']) for p in PLANES)} salidas")

if __name__ == "__main__":
    main()
