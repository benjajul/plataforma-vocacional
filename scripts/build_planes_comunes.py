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

def salida(nombre, *, titulo=None, malla=None, programa_directo_id=None, tipo="ing_civil", nota="", **extra):
    """extra (opcional, hoy solo U. de Chile): titulo_profesional, grado, duracion_semestres, menciones, grupo, despues"""
    return {"nombre": nombre, "titulo": titulo or nombre, "tipo": tipo, "malla_url": malla,
            "programa_directo_id": programa_directo_id, "nota": nota, **extra}

def uch(nombre, n, slug, titulo_prof, mencion_grado, *, sem=11, menciones=None, grupo="ingenieria", ciencias=False, tipo="ing_civil", despues=None, nota=""):
    grado = f"Licenciado/a en Ciencias{'' if ciencias else ' de la Ingeniería'}, mención {mencion_grado}"
    return salida(nombre, titulo=titulo_prof or grado, malla=UCH+f"{n}/{slug}", tipo=tipo, nota=nota,
                  titulo_profesional=titulo_prof, grado=grado, duracion_semestres=sem,
                  menciones=menciones or [], grupo=grupo, despues=despues)

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
    "duracion_total": "11 semestres en las ingenierías civiles y Geología; 10 en Geofísica; 8 en las licenciaturas de Astronomía y Física (todas incluyen el plan común)",
    "grado_intermedio": "Licenciatura en Ciencias de la Ingeniería (o en Ciencias), con la mención de la especialidad",
    "etapas": [
      {"nombre": "Plan Común", "ciclo": "ciclo inicial", "semestres": [1, 4], "que_pasa": "Matemática, física, programación y cursos de introducción a la ingeniería, iguales para todos. Al terminar se elige especialidad."},
      {"nombre": "Licenciatura", "ciclo": "ciclo especializado", "semestres": [5, 8], "que_pasa": "Cursos de base de la especialidad elegida. Se obtiene el grado de Licenciado/a (grado académico)."},
      {"nombre": "Especialidad", "ciclo": "ciclo especializado profesional", "semestres": [9, 11], "que_pasa": "Cursos profesionales, electivos y la memoria o trabajo de título. Se obtiene el título profesional."},
    ],
    "etapas_nota": "Los nombres de los tres ciclos aparecen en las mallas oficiales FCFM (malla de Geofísica: 'Especialidad' en los semestres IX y X). La división exacta 1–4 / 5–8 / 9–11 es la estructura de referencia; cada malla la ajusta.",
    "glosario": [
      {"termino": "Grado académico (licenciatura)", "explicacion": "Certifica la formación en ciencias de la especialidad. Permite postular a magíster y doctorado, en Chile o el extranjero."},
      {"termino": "Título profesional", "explicacion": "Habilita para ejercer la profesión (por ejemplo, firmar como Ingeniero/a Civil). Se obtiene al final, después de la memoria o trabajo de título."},
    ],
    "continuidad": [
      {"nombre": "Articulación pregrado–magíster", "detalle": "Un estudiante de la etapa de especialidad puede cursar en paralelo un magíster de la FCFM (de su área o de otra) y obtener título profesional y grado de magíster con una sola tesis, un examen y un informe final. Requiere situación académica regular y aprobación del comité del magíster y de la Escuela.",
       "url": "https://ingenieria.uchile.cl/dam/jcr:ec5338a6-a331-459a-8a5a-f1329a994b43/ARTICULACION%20EPEC%20FCFM%202024.pdf"},
      {"nombre": "Doble titulación en Francia", "detalle": "La FCFM tiene programas de doble titulación con escuelas de ingeniería francesas, dentro de su programa de movilidad internacional. Las condiciones se publican en cada convocatoria.",
       "url": "https://ingenieria.uchile.cl/dam/jcr:d32271bf-3772-4c9e-8e58-ea95cb128c3b/Revista_2026_final.pdf"},
    ],
    "salidas": [
      uch("Ingeniería Civil", 4969, "ingenieria-civil", "Ingeniero/a Civil", "Civil",
          menciones=["Estructuras, Construcción y Geotecnia", "Hidráulica, Sanitaria y Ambiental", "Transporte"]),
      uch("Ingeniería Civil de Minas", 4977, "ingenieria-civil-de-minas", "Ingeniero/a Civil de Minas", "Minas y Metalurgia Extractiva"),
      uch("Ingeniería Civil en Biotecnología", 4970, "ingenieria-civil-en-biotecnologia", "Ingeniero/a Civil en Biotecnología", "Biotecnología"),
      uch("Ingeniería Civil en Computación", 4971, "ingenieria-civil-en-computacion", "Ingeniero/a Civil en Computación", "Computación"),
      uch("Ingeniería Civil Eléctrica", 4972, "ingenieria-civil-electrica", "Ingeniero/a Civil Eléctrico/a", "Eléctrica",
          menciones=["Automática y Bioingeniería", "Energía Eléctrica", "Telecomunicaciones y Electrónica", "Robótica", "Instrumentación Astronómica", "Procesamiento de Voz e Imágenes"]),
      uch("Ingeniería Civil Industrial", 4973, "ingenieria-civil-industrial", "Ingeniero/a Civil Industrial", "Industrial"),
      uch("Ingeniería Civil Matemática", 4974, "ingenieria-civil-matematica", "Ingeniero/a Civil Matemático/a", "Matemática",
          despues="La propia carrera destaca la continuación a magíster y doctorado para quienes siguen la carrera científica."),
      uch("Ingeniería Civil Mecánica", 4976, "ingenieria-civil-mecanica", "Ingeniero/a Civil Mecánico/a", "Mecánica"),
      uch("Ingeniería Civil Química", 4978, "ingenieria-civil-quimica", "Ingeniero/a Civil Químico/a", "Química"),
      uch("Geología", 4979, "geologia", "Geólogo/a", "Geología", ciencias=True, grupo="tierra", tipo="no_ingenieria"),
      uch("Geofísica", 4982, "geofisica", "Geofísico/a", "Geofísica", sem=10, ciencias=True, grupo="tierra", tipo="no_ingenieria",
          menciones=["Tierra Sólida", "Atmósfera"]),
      uch("Licenciatura en Ciencias mención Astronomía", 4980, "astronomia", None, "Astronomía", sem=8, ciencias=True, grupo="licenciatura", tipo="no_ingenieria",
          despues="El camino habitual es seguir un magíster o doctorado en astronomía o áreas afines."),
      uch("Licenciatura en Ciencias mención Física", 8450, "fisica", None, "Física", sem=8, ciencias=True, grupo="licenciatura", tipo="no_ingenieria",
          despues="El camino habitual es seguir un magíster o doctorado en física o áreas afines."),
    ],
    "fuentes": [
      {"nombre": "FCFM — Preguntas frecuentes de admisión", "url": "https://ingenieria.uchile.cl/admision/preguntas-frecuentes"},
      {"nombre": "FCFM — Plazo para elegir tu especialidad", "url": "https://ingenieria.uchile.cl/escuela/pregrado/informacion-para-estudiantes/plazo-para-elegir-tu-especialidad"},
      {"nombre": "U. de Chile — fichas de cada carrera (título, grado y duración)", "url": "https://uchile.cl/carreras"},
      {"nombre": "FCFM — Malla Geofísica (ciclos Plan Común, Licenciatura y Especialidad)", "url": "https://portaluchile.uchile.cl/dam/jcr:460ebcc8-9b64-412f-bab0-946e6bf1c6fc/Malla%20Geof%C3%ADsica%20Tierra%20s%C3%B3lida.pdf"},
      {"nombre": "FCFM — Articulación pregrado y magíster (EPEC 2024)", "url": "https://ingenieria.uchile.cl/dam/jcr:ec5338a6-a331-459a-8a5a-f1329a994b43/ARTICULACION%20EPEC%20FCFM%202024.pdf"},
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
    "resumen": "Tres semestres comunes. Luego se elige una de las seis carreras de la facultad con cupo garantizado (BioMedicina no se alcanza desde el plan común según la fuente de 2024).",
    "duracion_plan_comun_semestres": 3,
    "seleccion": {"momento": "Al terminar el 3.er semestre", "mecanismo": "garantizado", "cupos": "sin_limite",
                  "criterio": "Cupo garantizado.", "requisitos": "no informado", "irrevocable": None,
                  "pendiente": "La página actual habla de seis carreras con cupo garantizado; se asume que incluye Informática e IA. Confirmar si BioMedicina también."},
    "duracion_total": "11 semestres",
    "malla_plan_comun": "https://www.udd.cl/mallas/ingenieriacivilplancomun.pdf",
    "salidas": [
      salida("Ingeniería Civil Industrial", malla="https://ingenieria.udd.cl/files/2020/04/12.-ing-civil-pc_ing-civil-industrial.pdf", programa_directo_id="udd-civil-industrial", nota="Malla publicada en 2020."),
      salida("Ingeniería Civil en Obras Civiles", malla="https://ingenieria.udd.cl/files/2020/04/12.-ing-civil-pc_ing-civil-obras-civiles.pdf", programa_directo_id="udd-civil-obras-civiles", nota="Malla publicada en 2020."),
      salida("Ingeniería Civil en Minería", malla="https://ingenieria.udd.cl/files/2020/04/12.-ing-civil-pc_ing-civil-mineria-1.pdf", programa_directo_id="udd-civil-mineria", nota="Malla publicada en 2020."),
      salida("Ingeniería Civil en Informática e Innovación Tecnológica", programa_directo_id="udd-civil-informatica-innovacion"),
      salida("Ingeniería Civil en Informática e Inteligencia Artificial", programa_directo_id="udd-civil-informatica-ia"),
      salida("Geología", tipo="no_ingenieria"),
    ],
    "fuentes": [{"nombre": "UDD — Plan común de ingenierías", "url": "https://ingenieria.udd.cl/files/2024/03/07-plan-comun-ingenierias.pdf"},
                {"nombre": "UDD — Facultad de Ingeniería, carreras", "url": "https://ingenieria.udd.cl/carreras/"},
                {"nombre": "UDD — Ingeniería Civil Plan Común", "url": "https://ingenieria.udd.cl/carrera/plan-comun/"}],
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
    "resumen": "Carrera nueva para Admisión 2027 (90 vacantes). Tras una formación inicial común se postula a una de tres especializaciones en informática.",
    "duracion_plan_comun_semestres": None,
    "seleccion": {"momento": "Después de la formación inicial (semestre no informado)", "mecanismo": "no_informado", "cupos": "no_informado",
                  "criterio": "La universidad indica que se postula a la especialización; no publica criterio ni cupos.", "requisitos": "no informado", "irrevocable": None,
                  "pendiente": "Confirmar semestre, cupos y criterio de asignación."},
    "duracion_total": "no informado",
    "salidas": [salida(n) for n in ["Ingeniería Civil en Informática y Computación", "Ingeniería Civil en Informática y Ciberseguridad",
                                    "Ingeniería Civil en Informática e Inteligencia Artificial"]],
    "fuentes": [{"nombre": "USACH Admisión — Ingeniería Civil en Informática Plan Común", "url": "https://admision.usach.cl/carreras/ingenieria-civil-en-informatica-plan-comun"}],
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
    from config import FOCO
    planes = [pc for pc in PLANES if pc["universidad_id"] in FOCO]
    import empleo
    for pc in planes:
        for sal in pc["salidas"]:
            sal["empleo"] = empleo.salida(pc["programa_id"], pc["universidad_id"], sal["nombre"])
    out = {"version": "0.4", "consultado": CONSULTADO, "foco": FOCO, "planes_comunes": planes}
    (root / "data" / "planes_comunes.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(planes)} planes comunes en foco, {sum(len(p['salidas']) for p in planes)} salidas")

if __name__ == "__main__":
    main()
