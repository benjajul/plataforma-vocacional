// Etiquetador de habilidades para perfiles de egreso (se ejecuta en el navegador sobre el sitio de cada universidad,
// y también con Node: `node scripts/tagger.js` exporta la taxonomía). Mantener en sincronía con data/habilidades.json.
// Cada habilidad = expresión regular sobre el texto en minúsculas; se cuenta cuántas veces aparece.
const HABILIDADES = {
  MAT:  { nombre: "Modelar con matemáticas y análisis cuantitativo", re: /model(o|os|ar|a|an|ación|amiento|ado)\b|matem[aá]tic|cuantitativ|simulaci|optimiz|estad[ií]stic|c[aá]lculo/g },
  PROG: { nombre: "Programar y desarrollar software", re: /programaci[oó]n|software|algor[ií]tm|computacional|computaci[oó]n|inform[aá]tic|aplicaciones (web|m[oó]viles|inform)|desarrollo de sistemas|c[oó]digo/g },
  DATA: { nombre: "Trabajar con datos e inteligencia artificial", re: /ciencia de datos|\bdatos\b|inteligencia artificial|aprendizaje (autom[aá]tico|de m[aá]quina)|machine learning|anal[ií]tica|big data/g },
  DIS:  { nombre: "Diseñar soluciones, sistemas o productos", re: /dise[ñn](a|ar|o|os|an|ando)\b|concebir|crear soluciones|prototip/g },
  OPER: { nombre: "Operar y mejorar procesos productivos", re: /proceso(s)? (industrial|productiv|de producci)|procesos|operaci[oó]n|operaciones|mantenimiento|producci[oó]n|planta|faena|mejora continua|calidad/g },
  GEST: { nombre: "Gestionar proyectos y recursos", re: /gesti[oó]n|gestion(ar|a|an)\b|administr(ar|a|aci[oó]n)|planific|proyectos?\b|evaluaci[oó]n de proyectos/g },
  NEG:  { nombre: "Entender negocios, economía y finanzas", re: /econ[oó]m|financ|negocio|mercado|marketing|comercial\b|estrateg|inversi[oó]n|contab|empresas?\b/g },
  CIEN: { nombre: "Aplicar ciencias (física, química, biología)", re: /f[ií]sica|qu[ií]mic|biolog|bioproces|biotecnol|laboratorio|experiment|ciencias b[aá]sicas|geolog|materiales/g },
  INFRA:{ nombre: "Trabajar con infraestructura, energía y máquinas", re: /infraestructura|estructura(s|l)?\b|obras?\b|construcci[oó]n|energ[ií]a|energ[eé]tic|el[eé]ctric|m[aá]quinas|equipos mec|mec[aá]nic|hidr[aá]ul|miner(a|o|[ií]a)|yacimiento|redes|telecomunicac/g },
  INV:  { nombre: "Investigar y generar conocimiento", re: /investig|cient[ií]fic|generar conocimiento|postgrado|posgrado/g },
  INNO: { nombre: "Innovar y emprender", re: /innova|emprend|creativ/g },
  EQ:   { nombre: "Trabajar en equipo y liderar", re: /equipos? (de trabajo|multidisciplin|interdisciplin|colaborativ)|trabajo en equipo|lider|colabor|multidisciplin|interdisciplin/g },
  COM:  { nombre: "Comunicar con claridad (también en inglés)", re: /comunic\w* (efectiv|oral|escrit|sus ideas|de manera|en forma)|comunicaci[oó]n efectiva|ingl[eé]s|segunda lengua|idioma/g },
  ETI:  { nombre: "Actuar con ética y responsabilidad social", re: /[eé]tic|responsabilidad social|socialmente responsable|bien com[uú]n|compromiso social|ciudadan|integridad/g },
  SOST: { nombre: "Cuidar el medio ambiente y la sostenibilidad", re: /sustentab|sostenib|medio ?ambient|ambiental(es)?\b|recursos naturales|cambio clim/g },
};
function etiquetar(texto) {
  const t = (texto || "").toLowerCase();
  const out = {};
  for (const [k, h] of Object.entries(HABILIDADES)) {
    const n = (t.match(h.re) || []).length;
    if (n) out[k] = n;
  }
  return out;
}
if (typeof module !== "undefined") {
  module.exports = { HABILIDADES, etiquetar };
  if (require.main === module) console.log(JSON.stringify(Object.fromEntries(Object.entries(HABILIDADES).map(([k, h]) => [k, { nombre: h.nombre, regex: h.re.source }])), null, 1));
}
