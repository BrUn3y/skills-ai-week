# Skills de agentes de IA · guía visual en español

Guía creada con el [skill Archify](https://github.com/tt-a1i/archify) sobre Claude Code, Codex, IBM Bob y el formato abierto Agent Skills.

Incluye cuatro diagramas interactivos, estructura de archivos, lenguajes, técnicas de Markdown, árbol de decisiones, repositorios, instalación local y global, y una plantilla descargable.

- [Guía en Markdown con diagramas Mermaid](GUIA-SKILLS.md)
- [Página HTML](site/index.html)
- [Plantilla descargable de skill](site/plantilla-skill.zip)
- [Fuente editable de Archify](.archify/explainer-skills-20261023-092000/candidate.archify.md)

Las fuentes están citadas en la guía. Las rutas de Bob se verificaron en Skills CLI; no se confirmó una sintaxis nativa de invocación en la documentación de IBM.

## Vista local

```bash
python3 -m http.server 8765 --directory site
```

Abre http://localhost:8765. El sitio es estático y no necesita servicios de IA ni claves de API.

## Regenerar

Se utilizó Archify 3.2, commit `25cf37080fc8b1dbe758a4efc3935b55f3327083`. Conserva el HTML original y sus recibos en `.archify/`. La copia de publicación añade traducciones de interfaz, descargas y ajustes para pantallas pequeñas.

```bash
git clone https://github.com/tt-a1i/archify.git /tmp/archify-skills
git -C /tmp/archify-skills checkout 25cf37080fc8b1dbe758a4efc3935b55f3327083
node /tmp/archify-skills/archify/bin/archify.mjs finalize explainer \
  .archify/explainer-skills-20261023-092000/candidate.archify.md \
  .archify/explainer-skills-20261023-092000/skills.html --json
python3 scripts/preparar-sitio.py
```

## GitHub Pages

El workflow publica `site/` en cada push a `main`. En el repositorio, selecciona **Settings → Pages → Source → GitHub Actions**. El primer despliegue puede requerir habilitar Pages antes de ejecutar el workflow.

Para crear un repositorio personal nuevo y activar el despliegue, con GitHub CLI autenticado y el trabajo ya guardado en un commit:

```bash
bash scripts/publicar.sh
```

El contenido se consultó el 23 de octubre de 2026. Los comandos y rutas pueden cambiar con las versiones de cada herramienta.

## Identidad visual

La edición de AI Week usa IBM Plex Sans, IBM Plex Mono y una paleta azul marino, morada, azul y turquesa tomada de las referencias del usuario. La cabecera reutiliza un recorte de la marca de la agenda y del fondo; el símbolo del Pilar de Skills proviene de la plantilla PowerPoint. Los archivos originales y los datos de los participantes no se publican.

`site/ajustes.css` define la apariencia de la página y `site/diagramas.css` la de los diagramas abiertos. El generador incorpora esta última en los visores conservando sus fuentes, datos, conexiones y sandbox. Las fuentes se sirven localmente y sus licencias se incluyen en `site/assets/`.
