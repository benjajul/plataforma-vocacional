"""Análisis de habilidades a partir de los perfiles de egreso → data/habilidades.json

Entrada: data/perfiles/*.json (una ficha por carrera o salida de plan común, con 'tags' = habilidades detectadas).
Método:
  1. Cada perfil se reduce a presencia/ausencia de las 15 habilidades (scripts/tagger.js). Se usa presencia, no
     conteo, porque parte de los perfiles se etiquetó con el texto oficial (regex) y parte leyendo un resumen.
  2. Los perfiles se agrupan en familias de carreras (misma disciplina en distintas universidades).
  3. Para cada familia: % de perfiles que mencionan cada habilidad y diferencia contra el promedio de todos los
     perfiles. Las habilidades con mayor diferencia positiva son las que DISTINGUEN a la familia; las que aparecen
     en casi todas las carreras (>=70% del total) se informan aparte como "base común".
Los textos en lenguaje simple ('que_hace', 'te_puede_gustar_si', 'para_tener_en_cuenta') son de elaboración propia,
escritos a partir de los perfiles revisados; no reproducen texto de las universidades.
"""
import glob, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONSULTADO = "2026-11-08"

HAB = {
    "MAT": "Modelar con matemáticas y análisis cuantitativo",
    "PROG": "Programar y desarrollar software",
    "DATA": "Trabajar con datos e inteligencia artificial",
    "DIS": "Diseñar soluciones, sistemas o productos",
    "OPER": "Operar y mejorar procesos productivos",
    "GEST": "Gestionar proyectos y recursos",
    "NEG": "Entender negocios, economía y finanzas",
    "CIEN": "Aplicar ciencias (física, química, biología)",
    "INFRA": "Trabajar con infraestructura, energía y máquinas",
    "INV": "Investigar y generar conocimiento",
    "INNO": "Innovar y emprender",
    "EQ": "Trabajar en equipo y liderar",
    "COM": "Comunicar con claridad (también en inglés)",
    "ETI": "Actuar con ética y responsabilidad social",
    "SOST": "Cuidar el medio ambiente y la sostenibilidad",
}

# familia -> (nombre, [ids de perfiles], textos propios)
FAM = {
 "industrial": ("Ingeniería Industrial", [
    "uc-t-industrias","uchile-civil-industrial","usm-civil-industrial","usach-civil-industrial","unab-civil-industrial",
    "udp-civil-industrial","uai-civil-industrial","udd-civil-industrial","unab-industrial","usach-ejecucion-industrial",
    "unab-engineering-technology-management"],
   dict(que_hace="Mejora cómo funcionan las organizaciones: procesos, logística, costos y decisiones. Usa modelos matemáticos y datos para encontrar la mejor forma de hacer algo con los recursos disponibles.",
        gustos=["Te gusta organizar cosas y encontrar la forma más eficiente de hacerlas.","Disfrutas resolver problemas con números, pero también te interesa cómo funcionan las empresas y las personas.","Te atrae la idea de tener muchas puertas abiertas: finanzas, operaciones, tecnología o consultoría."],
        ojo="Es la ingeniería más amplia y una de las más postuladas. Al ser tan versátil, conviene ir eligiendo un área (finanzas, operaciones, datos) durante la carrera.")),
 "informatica": ("Ingeniería Informática y Computación", [
    "uc-t-computacion","uchile-civil-computacion","usm-civil-informatica","unab-civil-informatica","udd-civil-informatica-innovacion",
    "uai-civil-informatica","uai-computer-science","unab-computacion-informatica","unab-computer-science-engineering",
    "usach-ejecucion-en-computacion-e-informatica","usach-civil-informatica-plan-comun","uc-lic-ciencia-computacion"],
   dict(que_hace="Diseña y construye software y sistemas computacionales: aplicaciones, plataformas, bases de datos, seguridad informática. Combina lógica, matemáticas y trabajo con equipos y clientes.",
        gustos=["Te entretiene entender cómo funcionan los programas, juegos o apps por dentro.","Te gusta resolver problemas paso a paso y no te frustra probar varias veces hasta que algo funcione.","Te interesa crear cosas que otras personas usen."],
        ojo="No es solo programar: también incluye diseñar sistemas, gestionar proyectos y entender lo que necesita una organización. Las carreras de Computer Science se enfocan más en los fundamentos teóricos.")),
 "datos_ia": ("Ciencia de Datos e Inteligencia Artificial", [
    "udp-civil-ciencia-datos-ia","udd-civil-informatica-ia","uc-lic-ciencia-datos"],
   dict(que_hace="Convierte grandes volúmenes de datos en decisiones y crea sistemas de inteligencia artificial: modelos que predicen, recomiendan o reconocen patrones.",
        gustos=["Te gusta buscar patrones y sacar conclusiones a partir de información.","Te interesan la estadística, la probabilidad y la programación por igual.","Te llama la atención cómo funcionan los sistemas de IA y quieres construirlos, no solo usarlos."],
        ojo="Son carreras nuevas. Comparten mucho con Informática y con Ingeniería Matemática, así que vale la pena compararlas.")),
 "telecom": ("Telemática y Telecomunicaciones", [
    "usm-civil-telematica","usach-civil-en-telematica","udp-civil-informatica-telecom"],
   dict(que_hace="Diseña y administra redes y sistemas de comunicación: internet, redes móviles, servicios en la nube y su seguridad.",
        gustos=["Te interesa cómo viaja la información entre dispositivos y por qué una red funciona o falla.","Te gusta la tecnología tanto en el hardware como en el software.","Te atrae la ciberseguridad."],
        ojo="Está a medio camino entre Informática y Eléctrica: si dudas entre ambas, revisa esta opción.")),
 "obras": ("Ingeniería Civil en Obras Civiles", [
    "uc-t-civil","uchile-civil","usm-civil","unab-civil","usach-civil-en-obras-civiles","udp-civil-obras-civiles",
    "uai-civil-obras-civiles","udd-civil-obras-civiles"],
   dict(que_hace="Diseña, calcula y dirige la construcción de infraestructura: edificios, puentes, carreteras, obras hidráulicas y sistemas de transporte, cuidando su seguridad y su impacto.",
        gustos=["Te llaman la atención los edificios, puentes o caminos y te preguntas cómo se sostienen.","Te gusta la física aplicada a cosas concretas que se pueden ver y tocar.","Te imaginas trabajando entre la oficina y la obra."],
        ojo="En Chile 'Ingeniería Civil' a secas suele significar obras civiles; distinto de 'ingeniero civil' como título general de las ingenierías de 5-6 años.")),
 "construccion": ("Construcción", [
    "uc-construccion-civil","unab-construccion"],
   dict(que_hace="Gestiona proyectos de construcción: planifica, presupuesta, coordina equipos y controla costos, plazos y calidad en obra.",
        gustos=["Te gusta organizar personas y recursos para que un proyecto avance.","Prefieres lo práctico y ver resultados concretos.","Te interesa el mundo de la construcción más desde la gestión que desde el cálculo."],
        ojo="Se enfoca más en dirigir obras que en el diseño estructural, que es propio de Ingeniería Civil en Obras Civiles.")),
 "minas": ("Ingeniería de Minas", [
    "uchile-civil-minas","usm-civil-minas","unab-civil-minas","usach-civil-en-minas","udd-civil-mineria","uai-civil-mineria",
    "usach-ejecucion-en-minas"],
   dict(que_hace="Planifica y dirige la extracción de minerales: evalúa yacimientos, diseña la mina, optimiza las operaciones y cuida la seguridad y el entorno.",
        gustos=["Te interesan la geología y cómo se obtienen los recursos que usa la sociedad.","Te gusta pensar en grandes operaciones donde se combinan técnica, economía y equipos de personas.","No te complica la idea de trabajar en terreno o en regiones."],
        ojo="Es una de las ingenierías con mejores ingresos en Chile, pero parte importante del trabajo está en faenas fuera de Santiago.")),
 "metalurgia": ("Ingeniería en Metalurgia", [
    "usach-civil-en-metalurgia","usach-ejecucion-en-metalurgia"],
   dict(que_hace="Transforma minerales en metales y desarrolla materiales: procesos de refinación, fundición y control de calidad.",
        gustos=["Te interesa la química aplicada a materiales reales.","Te llaman la atención las plantas industriales y sus procesos.","Te gusta entender por qué un material resiste o falla."],
        ojo="En este proyecto solo la USACH la ofrece como carrera propia en Santiago.")),
 "electrica": ("Ingeniería Eléctrica y Energía", [
    "uchile-civil-electrica","usm-civil-electrica","uc-t-electricista","unab-civil-electrica","usach-civil-en-electricidad",
    "usach-ejecucion-en-electricidad","uai-civil-energia"],
   dict(que_hace="Diseña y opera sistemas eléctricos y energéticos: generación (incluida la renovable), transmisión, electrónica, automatización y control.",
        gustos=["Te interesa la electricidad, la electrónica o las energías renovables.","Te gusta la física y las matemáticas aplicadas a sistemas que se pueden medir.","Te atrae la transición energética y la electromovilidad."],
        ojo="Tiene una base matemática y física exigente. Las carreras de energía combinan eléctrica, mecánica y sostenibilidad.")),
 "mecanica": ("Ingeniería Mecánica", [
    "uchile-civil-mecanica","usm-civil-mecanica","uc-t-mecanico","usach-civil-en-mecanica","uai-civil-mecanica",
    "usach-ejecucion-en-mecanica","usach-ejecucion-en-climatizacion"],
   dict(que_hace="Diseña, fabrica y mantiene máquinas, equipos y sistemas térmicos: desde motores y robots hasta plantas industriales y climatización.",
        gustos=["Te gusta desarmar cosas para entender cómo funcionan.","Te interesan las máquinas, los vehículos o la fabricación.","Disfrutas la física aplicada (fuerzas, calor, movimiento)."],
        ojo="Es muy amplia: puede llevar a minería, energía, manufactura o diseño de productos.")),
 "automatizacion": ("Mecatrónica, Automatización y Robótica", [
    "usach-civil-mecatronica","unab-automatizacion-robotica"],
   dict(que_hace="Integra mecánica, electrónica y programación para crear sistemas automáticos y robots.",
        gustos=["Te gusta la robótica o armar proyectos con sensores y motores.","Te interesan tanto el hardware como el software.","Te atrae la automatización de procesos industriales."],
        ojo="Mezcla tres disciplinas; conviene revisar la malla para ver el peso de cada una.")),
 "quimica": ("Ingeniería Química", [
    "uchile-civil-quimica","usm-civil-quimica","usach-civil-en-quimica","usach-ejecucion-en-quimica"],
   dict(que_hace="Diseña y optimiza procesos industriales que transforman materias primas en productos: energía, alimentos, minería, farmacéutica y tratamiento de residuos.",
        gustos=["Te gusta la química, pero te interesa más aplicarla a gran escala que en un laboratorio.","Disfrutas los balances, las ecuaciones y entender procesos paso a paso.","Te interesa producir de forma más limpia y eficiente."],
        ojo="No es lo mismo que la carrera de Química: aquí el foco está en procesos industriales y su diseño.")),
 "bio": ("Biotecnología y Bioingeniería", [
    "uchile-civil-biotecnologia","uc-t-biotecnologia","usach-civil-en-biotecnologia","uai-civil-bioingenieria","unab-biotecnologia"],
   dict(que_hace="Usa organismos vivos y procesos biológicos para crear productos y soluciones: alimentos, medicamentos, biocombustibles o descontaminación.",
        gustos=["Te interesan la biología y la química, y también la ingeniería.","Te gusta el trabajo de laboratorio y la investigación.","Te atrae aplicar la ciencia a problemas de salud, alimentación o medio ambiente."],
        ojo="Tiene un componente científico y de investigación más fuerte que otras ingenierías.")),
 "biomedica": ("Ingeniería Biomédica", [
    "usach-civil-biomedica","unab-civil-biomedica","udd-civil-biomedicina"],
   dict(que_hace="Aplica la ingeniería a la salud: dispositivos médicos, imágenes, biomecánica, sensores, datos clínicos y gestión de tecnología en hospitales.",
        gustos=["Te interesa la salud, pero te atrae más la tecnología que la atención directa de pacientes.","Te gustan la biología y la física por igual.","Te motiva crear soluciones que mejoren la vida de las personas."],
        ojo="Son carreras recientes en varias universidades; vale la pena revisar con qué hospitales o clínicas tienen convenios de práctica.")),
 "ambiental": ("Ingeniería Ambiental y Recursos Naturales", [
    "usach-civil-en-ambiente","usach-civil-en-territorio-y-medio-ambiente","unab-ambiental","uc-ing-recursos-naturales"],
   dict(que_hace="Evalúa y reduce el impacto ambiental de proyectos y empresas: agua, residuos, contaminación, cambio climático y ordenamiento del territorio.",
        gustos=["Te preocupan el cambio climático y el cuidado de la naturaleza.","Te gusta combinar ciencia con normativa y trabajo con comunidades.","Te interesa el trabajo en terreno además de la oficina."],
        ojo="Algunas de estas carreras se dictan en facultades de ciencias, no de ingeniería; revisa el énfasis de cada malla.")),
 "matematica": ("Ingeniería Matemática", [
    "uchile-civil-matematica","usm-civil-matematica","uc-t-matematico"],
   dict(que_hace="Usa matemáticas avanzadas y computación para modelar problemas complejos: finanzas, logística, ciencia de datos, clima o investigación.",
        gustos=["Las matemáticas son de lo que más disfrutas, incluso los problemas difíciles.","Te gusta entender el porqué de las cosas, no solo aplicar fórmulas.","Te atrae la investigación o los problemas abiertos."],
        ojo="Es la ingeniería más cercana a las ciencias exactas; muchos egresados siguen un postgrado.")),
 "fisica": ("Ingeniería Física", [
    "usm-civil-fisica","unab-fisica"],
   dict(que_hace="Aplica la física para desarrollar tecnología: instrumentación, óptica, materiales, energía o astronomía.",
        gustos=["La física es tu ramo favorito y quieres llevarla a la práctica.","Te gusta experimentar y medir.","Te atrae la investigación aplicada y la tecnología de punta."],
        ojo="Es una carrera de nicho, con fuerte componente de investigación.")),
 "geomensura": ("Geomensura y Geomática", [
    "usach-civil-en-geomensura-y-geomatica"],
   dict(que_hace="Mide y representa el territorio: topografía, mapas digitales, sistemas de información geográfica, drones y satélites.",
        gustos=["Te gustan los mapas y la geografía.","Te interesa la tecnología de medición (GPS, drones, imágenes satelitales).","Te atrae el trabajo en terreno."],
        ojo="En este proyecto solo la USACH la ofrece.")),
 "diseno": ("Ingeniería en Diseño de Productos", [
    "usm-diseno-productos"],
   dict(que_hace="Diseña productos y servicios desde la idea hasta el prototipo, combinando creatividad, tecnología de fabricación y estrategia.",
        gustos=["Te gusta dibujar, crear y construir prototipos.","Te interesa cómo las personas usan los objetos.","Quieres combinar lo creativo con lo técnico."],
        ojo="En este proyecto solo la USM la ofrece en Santiago.")),
 "aviacion": ("Ingeniería en Aviación Comercial", [
    "usm-aviacion-comercial"],
   dict(que_hace="Gestiona empresas y operaciones del transporte aéreo: aerolíneas, aeropuertos, seguridad y normativa aeronáutica.",
        gustos=["Te apasiona el mundo de la aviación.","Te interesa la gestión de operaciones y negocios.","Te atraen los entornos internacionales."],
        ojo="Es una carrera de gestión aplicada a la aviación, no de diseño de aeronaves ni de pilotaje.")),
 "comercial": ("Ingeniería Comercial y Negocios", [
    "uchile-ingenieria-comercial","uc-ingenieria-comercial","usm-ingenieria-comercial","usach-ingenieria-comercial",
    "unab-ingenieria-comercial","udp-ingenieria-comercial","uai-negocios-tecnologia"],
   dict(que_hace="Forma para dirigir organizaciones y entender la economía: finanzas, marketing, personas, estrategia y emprendimiento.",
        gustos=["Te interesan la economía, las empresas o emprender.","Te gusta analizar situaciones y tomar decisiones.","Te atrae trabajar con personas y liderar."],
        ojo="Tiene más matemáticas de lo que suele pensarse (estadística, finanzas, economía), y varias universidades piden o ponderan M2.")),
}

def main():
    perf = {}
    for f in sorted(glob.glob(str(ROOT / "data" / "perfiles" / "*.json"))):
        for k, v in json.load(open(f, encoding="utf-8")).items():
            if k in perf and perf[k].get("tags") and not v.get("tags"):
                continue
            perf[k] = v
    usados = {i for _, ids, _ in FAM.values() for i in ids}
    falt = [i for _, ids, _ in FAM.values() for i in ids if i not in perf]
    assert not falt, f"perfiles faltantes: {falt}"
    sin_familia = sorted(set(perf) - usados)
    pres = {k: set(v.get("tags", {})) for k, v in perf.items() if k in usados}
    n = len(pres)
    prom = {h: sum(h in s for s in pres.values()) / n for h in HAB}
    base = [h for h, p in sorted(prom.items(), key=lambda x: -x[1]) if p >= 0.70]

    inv = json.loads((ROOT / "data" / "inventario.json").read_text(encoding="utf-8"))
    uni_nombre = inv["universidades"]
    familias = []
    for fid, (nombre, ids, txt) in FAM.items():
        pct = {h: sum(h in pres[i] for i in ids) / len(ids) for h in HAB}
        dif = {h: pct[h] - prom[h] for h in HAB}
        distintivas = [h for h in sorted(HAB, key=lambda h: (-dif[h], -pct[h])) if pct[h] >= 0.5 and dif[h] > 0.05 and h not in base][:4]
        if len(ids) < 3:   # con 1-2 perfiles el % no discrimina: ordenar por cuántas veces se menciona cada habilidad
            cuenta = {h: sum(perf[i].get("tags", {}).get(h, 0) for i in ids) for h in HAB}
            distintivas = [h for h in sorted(HAB, key=lambda h: (-cuenta[h], -dif[h])) if h not in base and cuenta[h] > 0][:4]
        carreras = []
        for i in ids:
            p = perf[i]
            uid = i.split("-")[0]
            carreras.append({"id": i, "universidad_id": uid, "universidad": uni_nombre.get(uid, uid),
                             "nombre": p.get("nombre") or next((x["nombre_oficial"] for x in inv["programas"] if x["id"] == i), i),
                             "salida_de": p.get("salida_de"), "url": p["url"], "tipo_fuente": p["tipo"],
                             "habilidades": sorted(pres[i], key=lambda h: list(HAB).index(h))})
        familias.append({"id": fid, "nombre": nombre, "n_perfiles": len(ids),
                         "porcentaje": {h: round(pct[h], 2) for h in HAB},
                         "diferencia_vs_promedio": {h: round(dif[h], 2) for h in HAB},
                         "distintivas": distintivas,
                         "que_hace": txt["que_hace"], "te_puede_gustar_si": txt["gustos"], "para_tener_en_cuenta": txt["ojo"],
                         "carreras": carreras})
    out = {"version": "0.5", "consultado": CONSULTADO,
           "metodo": __doc__.strip(),
           "habilidades": HAB, "promedio_general": {h: round(prom[h], 2) for h in HAB},
           "base_comun": base, "n_perfiles": n, "perfiles_sin_familia": sin_familia,
           "familias": familias}
    (ROOT / "data" / "habilidades.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{n} perfiles en {len(familias)} familias; base común: {base}; sin familia: {sin_familia}")
    for f in familias:
        print(f"  {f['nombre'][:38]:38} n={f['n_perfiles']:2}  distintivas: {', '.join(f['distintivas'])}")

if __name__ == "__main__":
    main()
