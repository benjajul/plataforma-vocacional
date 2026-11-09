# Plataforma de orientación vocacional — Ingeniería y Negocios

Herramienta interactiva para explorar carreras de Ingeniería (y la carrera de Ingeniería Comercial) en 8 universidades chilenas, pensada para un estudiante de 4.º medio que tiene claros sus gustos pero no todavía su área laboral.

Versión 0.5 — 08-11-2026 — Inventario con datos DEMRE 2027, planes comunes y análisis de habilidades por carrera.

## Alcance inicial
| id | Universidad |
|---|---|
| uc | Pontificia Universidad Católica de Chile |
| uchile | Universidad de Chile |
| usm | Universidad Técnica Federico Santa María (campus Santiago) |
| usach | Universidad de Santiago de Chile |
| unab | Universidad Andrés Bello |
| udp | Universidad Diego Portales |
| uai | Universidad Adolfo Ibáñez |
| udd | Universidad del Desarrollo |

Carreras: las de la Facultad/Escuela de Ingeniería de cada una + Ingeniería Comercial.

## Fases
1. **Estructura** (esta versión): modelo de datos (`data/schema/carrera.schema.json`), mapa de fuentes, criterios.
2. **Inventario**: lista cerrada de programas por universidad (nombre oficial, URL, código DEMRE, plan común vs. carrera directa).
3. **Recolección**: datos centrales (Mi Futuro, CNA, nómina de gratuidad, oferta DEMRE, rankings) + página de cada carrera (perfil de egreso, malla, campo laboral, dirección). Cada dato con fuente y fecha.
4. **Contenido vocacional**: perfil RIASEC, "te puede gustar si…", habilidades, mitos y realidades por carrera.
5. **Plataforma**: prototipo navegable → repositorio en GitHub (sitio estático: Astro o Next.js export, datos en JSON versionados, despliegue gratis en GitHub Pages / Vercel).

## Mapa de fuentes
| Dato | Fuente principal | Nivel |
|---|---|---|
| Empleabilidad 1.º/2.º año, ingreso 4.º año, retención, duración real | Mi Futuro — Buscador de Empleabilidad e Ingresos (SIES/Mineduc) | carrera × universidad |
| Acreditación institucional (años, nivel, vigencia) | CNA-Chile | universidad |
| Acreditación de carrera | CNA-Chile (en ingeniería es voluntaria: puede no existir) | carrera |
| Gratuidad | Nómina oficial de instituciones adscritas (Mineduc / beneficiosestudiantiles.cl) | universidad |
| Ponderaciones, vacantes, puntaje de corte, código | Oferta académica DEMRE (Admisión 2027) | carrera |
| Arancel y matrícula | Universidad / Mi Futuro | carrera |
| Perfil de egreso, malla, campo laboral, especialidades | Página oficial de la carrera | carrera |
| Dirección de la facultad / campus | Página oficial + geocodificación | carrera |
| Ranking institucional | QS World, QS Latam, THE World, THE Latam | universidad |
| Ranking por disciplina | QS by Subject (Engineering & Technology; Business), THE by Subject | universidad × área |
| Perfil vocacional | Elaboración propia (modelo RIASEC de Holland) | carrera |

## Reglas de datos
- Todo dato publicado lleva `fuente_id` y fecha de consulta; la plataforma las muestra.
- No se copia íntegro el texto de perfiles de egreso: se resume y se enlaza al original.
- Un dato que no se encuentra se muestra como "no informado", nunca se estima.
- Las comparaciones de empleabilidad e ingreso se hacen entre carreras equivalentes (misma carrera genérica de Mi Futuro), no entre plan común y carrera directa sin aclararlo.

## Lógica de planes comunes (v0.3)
`data/planes_comunes.json` modela cada puerta de entrada común como:

    plan común --(regla de selección)--> salida (carrera o título) --> malla

- `seleccion.mecanismo`: `libre` (U. de Chile, UDP), `garantizado` (UDD), `competitivo` (USM: cupos por ranking de 1.er año, irrevocable), `sin_postulacion` (UC: major durante la licenciatura y luego título sin postular), `no_informado` (UAI, USACH).
- `salidas[].programa_directo_id` enlaza con la misma carrera cuando también admite postulación directa.
- `etapa_intermedia` cubre los 22 majors UC.

Prototipo: `web/rutas.html` (generado con `python3 scripts/build_web.py`).

## Análisis de habilidades (v0.5)
- `data/demre_2027.json`: códigos, vacantes y ponderaciones de la Oferta Definitiva DEMRE 2027 (8 universidades), generado con `scripts/parse_demre.py` desde el PDF oficial.
- `data/perfiles/*.json`: una ficha por carrera o salida de plan común con la URL del perfil de egreso oficial y las habilidades detectadas (15, definidas en `scripts/tagger.js`). No se guarda el texto de las universidades, solo las etiquetas.
- `data/habilidades.json`: agrupación en 21 familias de carreras, % de perfiles que mencionan cada habilidad, habilidades distintivas y textos de orientación de elaboración propia (`scripts/build_habilidades.py`).
- Página: `web/habilidades.html`.

## Explorar, simulador y cuestionario (v0.6)
- `data/cortes_2026.json`: puntaje de corte y matriculados/seleccionados de la Admisión 2026. Fuentes oficiales: UC (último matriculado y vacantes ocupadas), U. de Chile, USM (puntaje mínimo de selección) y UAI (corte y convocados). Fuentes secundarias (marcadas con *): UDD y UDP. USACH desde las fichas oficiales de cada carrera (última matrícula; 6 carreras solo con dato 2025). UNAB queda "sin corte publicado". Cada universidad publica una medida distinta, y se indica en cada fila.
- `scripts/build_plataforma.py` → `data/plataforma.json`: agrupa las 21 familias en 7 áreas de ingeniería y une inventario, ponderaciones 2027, requisitos mínimos y cortes 2026.
- `web/index.html` (Explorar): navegación por área o por universidad, con vacantes 2027, corte 2026, ingresados 2026, mínimos y M2.
- `web/simulador.html`: calcula el puntaje ponderado con ponderaciones 2027, revisa requisitos (M2, ponderado mínimo, promedio CL+M1) y lo compara con el corte 2026. Categorías: Alcanzable (≥ corte), Te falta poco (hasta 25 pts bajo), Difícil (hasta 60), Muy difícil (más de 60).
- `web/cuestionario.html`: 17 preguntas cotidianas (escala 0–3) que se traducen a las 15 habilidades y se comparan con el perfil distintivo de cada familia. Sugiere 3 carreras, 2 áreas y universidades; si se usó el simulador, cruza el resultado.
- `web/base.css`: estilos compartidos (claro/oscuro).

## Cómo regenerar
    python3 scripts/build_inventario.py
    python3 scripts/build_planes_comunes.py
    python3 scripts/build_habilidades.py
    python3 scripts/build_plataforma.py
    python3 scripts/build_web.py

## Publicar en GitHub Pages
El workflow `.github/workflows/pages.yml` regenera los datos y publica la carpeta `web/` en cada push a `main`.

1. Crear el repositorio vacío `benjajul/plataforma-vocacional` en GitHub (sin README).
2. Subir este repo:

        git remote add origin https://github.com/benjajul/plataforma-vocacional.git
        git push -u origin main

3. En GitHub: Settings → Pages → Build and deployment → Source: **GitHub Actions**.
4. El sitio queda en https://benjajul.github.io/plataforma-vocacional/

Probar localmente:

        python3 scripts/build_web.py
        python3 -m http.server -d web 8000   # abrir http://localhost:8000
