#!/usr/bin/env python3
"""Prepare the checked Archify artifact for Pages and export standard Markdown."""
from html.parser import HTMLParser
import base64
import hashlib
import json
from pathlib import Path
import re
import shlex
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / '.archify/explainer-skills-20261023-092000'
SITE = ROOT / 'site'
SITE.mkdir(exist_ok=True)

WORDS = {
    'answer': 'Respuesta', 'scope': 'Alcance', 'sources': 'Fuentes',
    'print': 'Imprimir / PDF', 'image': 'Imagen completa',
    'imageHints': ['Mayor nitidez', 'Menor tamaño', 'Formato compatible'],
    'export': 'Exportar', 'style': 'Estilo', 'auto': 'Sistema',
    'light': 'Claro', 'dark': 'Oscuro', 'typical': 'Valor habitual',
    'explore': 'Abrir vista interactiva',
    'exploreTitle': 'Ampliar, buscar nodos, recorrer conexiones y exportar',
    'close': 'Cerrar', 'loading': 'Abriendo diagrama…',
    'graph': 'Estructura del diagrama', 'changes': 'Cambios de estructura',
    'added': 'Añadido', 'removed': 'Eliminado', 'modified': 'Modificado',
    'copy': 'Copiar', 'copied': 'Copiado', 'walk': 'Recorrer paso a paso',
    'walkMessages': 'Reproducir mensajes', 'walkFlow': 'Recorrer el flujo',
    'prev': 'Anterior', 'next': 'Siguiente', 'end': 'Terminar',
    'ask': 'Consultar', 'askQuote': 'Consultar sobre esto',
    'askPlaceholder': '¿Qué debería aclarar o ampliar esta sección?',
    'askCopy': 'Copiar pregunta', 'askCopied': 'Copiado. Pégalo en tu agente.',
    'askCancel': 'Cancelar',
    'askChips': ['No entiendo esta parte', 'Profundiza', 'Dame un ejemplo', '¿Cuál es la fuente?'],
    'askPage': 'Página', 'askFile': 'Archivo', 'askWhere': 'Ubicación',
    'askQuoteLabel': 'Cita', 'askQuestion': 'Pregunta',
    'askNote': 'Copia la página y la sección para que tu agente pueda revisarla.',
    'tagline': 'Convierte lo que quieres comprender en un diagrama interactivo.',
    'styles': {'clean': 'Limpio', 'editorial': 'Editorial', 'product': 'Producto', 'swiss': 'Suizo'},
}

raw = (ARTIFACT / 'skills.html').read_text()
pattern = r'(<script\b(?=[^>]*\bid="explainer-reader-words")[^>]*>)(.*?)(</script>)'
match = re.search(pattern, raw, re.S)
if not match:
    raise SystemExit('Missing Archify reader translation dictionary')
english = json.loads(match.group(2))
translated = {**english, **WORDS}
raw = raw[:match.start(2)] + json.dumps(translated, ensure_ascii=False) + raw[match.end(2):]
text_map = {v: WORDS[k] for k, v in english.items() if isinstance(v, str) and isinstance(WORDS.get(k), str)}
text_map.update({'Skip to content': 'Saltar al contenido', 'Theme': 'Tema', 'Clean': 'Limpio', 'Product': 'Producto', 'Swiss': 'Suizo'})


class Localize(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts = []
        self.literal = []

    def handle_starttag(self, tag, attrs):
        self.parts.append(self.get_starttag_text())
        if tag in ('script', 'style', 'pre', 'code', 'textarea'):
            self.literal.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.parts.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        self.parts.append('</' + tag + '>')
        if self.literal and self.literal[-1] == tag:
            self.literal.pop()

    def handle_data(self, data):
        key = data.strip()
        if not self.literal and key in text_map:
            data = data.replace(key, text_map[key])
        self.parts.append(data)

    def handle_entityref(self, name):
        self.parts.append('&' + name + ';')

    def handle_charref(self, name):
        self.parts.append('&#' + name + ';')

    def handle_decl(self, decl):
        self.parts.append('<!' + decl + '>')

    def handle_comment(self, data):
        self.parts.append('<!--' + data + '-->')


scripts = []
def protect_script(match):
    scripts.append(match.group(0))
    return '<!--ARCHIFY_SCRIPT_' + str(len(scripts) - 1) + '-->'

markup = re.sub(r'<script\b[^>]*>.*?</script>', protect_script, raw, flags=re.S)
parser = Localize()
parser.feed(markup)
parser.close()
page = ''.join(parser.parts)
for script_index, script in enumerate(scripts):
    page = page.replace('<!--ARCHIFY_SCRIPT_' + str(script_index) + '-->', script, 1)
css_version = hashlib.sha256((SITE / 'ajustes.css').read_bytes()).hexdigest()[:10]
js_version = hashlib.sha256((SITE / 'ajustes.js').read_bytes()).hexdigest()[:10]
page = page.replace('</head>', '<link rel="preload" href="assets/ibm-plex-sans.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="ajustes.css?v=' + css_version + '"></head>', 1)
downloads = '<nav class="recursos" aria-label="Descargas"><a href="GUIA-SKILLS.md" download>Descargar guía Markdown</a><a href="plantilla-skill.zip" download>Descargar plantilla de skill</a><a href="fuente.archify.md" download>Descargar fuente Archify</a></nav>'
hero = '''<section class="event-hero" aria-labelledby="event-heading">
  <div class="event-brands">
    <img class="event-wordmark" src="assets/ai-week-2026.webp" width="985" height="213" alt="AI week 2026">
    <div class="pillar-brand"><img src="assets/pilar-skills.svg" width="40" height="44" alt=""><span>Pilar de Skills<small>Campus Guadalajara</small></span></div>
  </div>
  <div class="event-content">
    <p class="event-eyebrow">APRENDE · CREA · AUTOMATIZA</p>
    <h1 id="event-heading">Cómo funcionan los <span>skills de agentes de IA</span></h1>
    <p class="event-description">De las instrucciones en Markdown a un flujo de trabajo reutilizable.</p>
    <div class="event-agents" aria-label="Agentes incluidos"><span>Claude Code</span><span>Codex</span><span>IBM Bob</span></div>
  </div>
  <a class="event-start" href="#funcionamiento">Explorar la guía <span aria-hidden="true">↓</span></a>
</section>'''
page = re.sub(r'<h1>.*?</h1>', '', page, count=1, flags=re.S)
page = page.replace('<header class="masthead">', hero + '<header class="masthead">' + downloads, 1)

# Adapt the iframe appearance without changing native sources or the sandbox.
handoff = 'frame.srcdoc = end < 0 ? html + script : html.slice(0,end) + script + html.slice(end);'
styled_handoff = 'frame.srcdoc = window.aiWeekStyleViewer(end < 0 ? html + script : html.slice(0,end) + script + html.slice(end));'
if page.count(handoff) != 1:
    raise SystemExit('Archify viewer handoff changed; review the style adapter.')
page = page.replace(handoff, styled_handoff, 1)
native_css = (SITE / 'diagramas.css').read_text()
for name in ['ibm-plex-sans', 'ibm-plex-mono']:
    font_data = base64.b64encode((SITE / 'assets' / (name + '.woff2')).read_bytes()).decode()
    native_css = native_css.replace('assets/' + name + '.woff2', 'data:font/woff2;base64,' + font_data)
theme_payload = json.dumps({'css': native_css}, ensure_ascii=False).replace('<', '\\u003c')
enhancements = '<script id="aiweek-native-theme" type="application/json">' + theme_payload + '</script><script src="ajustes.js?v=' + js_version + '"></script></body>'
page = enhancements.join(page.rsplit('</body>', 1))
(SITE / 'index.html').write_text(page)

source = (ARTIFACT / 'candidate.archify.md').read_text()
(SITE / 'fuente.archify.md').write_text(source)
sources = {}
for line in source.splitlines():
    if line.startswith('@source '):
        parts = shlex.split(line)
        sources[parts[1]] = dict(part.split('=', 1) for part in parts[2:])

lines = source.splitlines()
output = []
index = 0
fenced = False
while index < len(lines):
    line = lines[index]
    if line.startswith('```'):
        fenced = not fenced
        output.append(line.split(' title=')[0] if fenced else line)
        index += 1
        continue
    if fenced:
        output.append(line)
        index += 1
        continue
    if re.match(r'@(workflow|architecture|tree)\b', line):
        kind = line.split()[0][1:]
        index += 1
        rows = []
        while index < len(lines) and lines[index].startswith('|'):
            rows.append([cell.strip() for cell in lines[index].strip('|').split('|')])
            index += 1
        output.extend(['```mermaid', 'flowchart TD' if kind == 'tree' else 'flowchart LR'])
        for row in rows:
            if row[0].startswith('lane '):
                continue
            if ' > ' in row[0]:
                left, right = row[0].split(' > ')
                label = row[1]
                output.append(f'  {left} -->|{label}| {right}' if label else f'  {left} --> {right}')
            else:
                ident, label = row[:2]
                quoted = json.dumps(label, ensure_ascii=False)
                output.append(f'  {ident}{{{quoted}}}' if label.endswith('?') else f'  {ident}[{quoted}]')
                if kind == 'tree' and row[2] != '-':
                    output.append(f'  {row[2]} --> {ident}')
        output.extend(['```', ''])
        continue
    if line.startswith('@steps '):
        index += 1
        step = 1
        while index < len(lines) and lines[index].startswith('|'):
            row = [cell.strip() for cell in lines[index].strip('|').split('|')]
            output.append(f'{step}. **{row[1]}:** {row[2]}')
            step += 1
            index += 1
        continue
    if line.startswith('@'):
        index += 1
        continue
    line = re.sub(r'\s+\{#[^}]+\}', '', line)
    line = re.sub(r'\[([^\]]*)\]\(source:([\w-]+)\)', lambda m: (m[1] or '') + '[^' + m[2] + ']', line)
    output.append(line)
    index += 1
output.extend(['', '## Fuentes', '', 'Consultadas el 23 de octubre de 2026.', ''])
for ident, entry in sources.items():
    output.append(f'[^{ident}]: [{entry["title"]}]({entry["url"]})')
guide = '\n'.join(output) + '\n'
(ROOT / 'GUIA-SKILLS.md').write_text(guide)
(SITE / 'GUIA-SKILLS.md').write_text(guide)

template = '''---
name: revisar-documento
description: Revisa claridad y estructura de un texto y entrega hallazgos priorizados. Usar cuando pidan revisar un borrador. No usar para traducir.
---

# Revisar documento

## Entradas
Recibe el texto o su ruta, el público y el objetivo.

## Procedimiento
1. Lee el documento completo.
2. Identifica el objetivo y los criterios de revisión.
3. Aplica las decisiones de la sección siguiente.
4. Entrega hallazgos con ubicación y una propuesta concreta.

## Decisiones
- Si falta el texto o el archivo: solicita ese dato.
- Si el público no se conoce: declara el supuesto que usarás.
- Si se requiere una guía de estilo: lee [la referencia](references/estilo.md).

## Salida
Entrega una tabla: ubicación, problema, propuesta y prioridad.

## Verificación
- [ ] Cada hallazgo apunta a un fragmento real.
- [ ] Las propuestas preservan la intención del autor.
- [ ] Los supuestos quedan visibles.
'''
(SITE / 'plantilla-skill.md').write_text(template)
with zipfile.ZipFile(SITE / 'plantilla-skill.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    archive.writestr('revisar-documento/SKILL.md', template)
    archive.writestr('revisar-documento/references/estilo.md', '# Criterios de estilo\n\n- Usa frases claras y verbos concretos.\n- Conserva nombres, cifras y la intención del autor.\n- Distingue errores de preferencias editoriales.\n')
(SITE / '.nojekyll').touch()
print('Sitio listo en site/; guía Markdown y plantilla ZIP generadas.')
