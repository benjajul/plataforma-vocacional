# Plataforma de orientación vocacional — Ingeniería y Negocios

Herramienta interactiva para explorar carreras de Ingeniería (y la carrera de Ingeniería Comercial) en 8 universidades chilenas, pensada para un estudiante de 4.º medio que tiene claros sus gustos pero no todavía su área laboral.

Versión 0.1 — 08-11-2026 — Fase 1 (estructura).

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
