# Cómo funcionan los skills de agentes de IA {#skills-ia}

Un **skill** reúne instrucciones en `SKILL.md` y recursos opcionales para que un agente siga un procedimiento. El agente interpreta el Markdown y usa herramientas para ejecutar los scripts cuando la tarea lo requiere.

- El nombre y la descripción permiten descubrirlo; el contenido completo se carga cuando se utiliza.[](source:spec)
- Claude Code, Codex e IBM Bob tienen rutas de instalación diferentes.[](source:agents)
- Un buen skill define entradas, decisiones, pasos, resultados y cómo comprobarlos.[](source:codex)

@answer scope="Guía en español · consultada el 23 de octubre de 2026"
@meta locale=es style=clean
@source spec title="Agent Skills: especificación abierta" url=https://agentskills.io/specification
@source claude title="Claude Code: crear y usar skills" url=https://code.claude.com/docs/en/skills
@source codex title="OpenAI: Build skills" url=https://learn.chatgpt.com/docs/build-skills
@source agents title="Skills CLI: agentes y rutas de instalación" url=https://github.com/vercel-labs/skills/blob/main/docs/agents.md
@source cli title="Skills CLI: instalación y comandos" url=https://github.com/vercel-labs/skills/blob/main/docs/commands.md
@source skillsmp title="SkillsMP: catálogo de skills" url=https://skillsmp.com/
@source skillssh title="skills.sh: directorio del ecosistema" url=https://skills.sh/
@source anthropicrepo title="Repositorio de skills de Anthropic" url=https://github.com/anthropics/skills
@source openairepo title="Repositorio de skills de OpenAI" url=https://github.com/openai/skills
@source vercelrepo title="Repositorio de skills de Vercel" url=https://github.com/vercel-labs/agent-skills
@source archify title="Archify: skill para diagramas interactivos" url=https://github.com/tt-a1i/archify

## ¿Cómo actúa un skill durante una tarea? {#funcionamiento}

@workflow id=ciclo-skill title="De la petición al resultado"
| lane elegir | Descubrir y activar |
| lane trabajar | Aplicar y comprobar |
| peticion | Usuario | external | elegir |
| catalogo | Metadatos | database | elegir |
| activar | Elegir skill | backend | elegir |
| leer | Leer SKILL.md | backend | trabajar |
| recursos-paso | Evaluar recursos | backend | trabajar |
| aplicar | Aplicar pasos | backend | trabajar |
| verificar | Verificar | frontend | trabajar |
| peticion > catalogo | tarea |
| catalogo > activar | coincidencia |
| activar > leer | activar | emphasis |
| leer > recursos-paso | instrucciones |
| recursos-paso > aplicar | según tarea |
| aplicar > verificar | evidencia | emphasis |

@steps id=pasos-ciclo
| paso-peticion | Usuario | Por ejemplo: «Revisa este archivo y genera un informe». | ciclo-skill | peticion |
| paso-catalogo | Metadatos | El agente conoce el nombre y la descripción de los skills disponibles. | ciclo-skill | catalogo |
| paso-activar | Elegir skill | Se activa por solicitud explícita o por una tarea que coincide con su descripción. | ciclo-skill | activar |
| paso-leer | Leer SKILL.md | El agente lee el procedimiento completo antes de aplicarlo. | ciclo-skill | leer |
| paso-recursos | Evaluar recursos | Decide qué referencias, plantillas o scripts necesita para esta tarea. | ciclo-skill | recursos-paso |
| paso-aplicar | Aplicar pasos | Lee referencias, usa plantillas o ejecuta scripts con herramientas si hacen falta. | ciclo-skill | aplicar |
| paso-verificar | Verificar | Revisa el resultado con los criterios indicados y comunica el producto final. | ciclo-skill | verificar |

La carga progresiva evita incorporar todos los archivos de todos los skills al contexto. El detalle de selección depende del agente.[](source:spec)[](source:codex)

## ¿Qué archivos contiene? {#estructura}

@tree id=carpeta-skill title="Anatomía de un skill"
| raiz | mi-skill/ | - |
| principal | SKILL.md | raiz |
| cabecera | YAML: name y description | principal |
| cuerpo | Markdown: procedimiento | principal |
| scripts | scripts/ | raiz |
| referencias | references/ | raiz |
| recursos | assets/ | raiz |
| interfaz | agents/openai.yaml | raiz |

| Archivo o carpeta | Función | ¿Es obligatorio? |
| --- | --- | --- |
| `SKILL.md` | Metadatos YAML al inicio; instrucciones Markdown después. | Sí, en el formato abierto. |
| `scripts/` | Código para cálculos, conversiones o tareas repetibles. | No. |
| `references/` | Documentación que el agente consulta cuando corresponde. | No. |
| `assets/` | Plantillas, imágenes, ejemplos de salida y otros recursos. | No. |
| `agents/openai.yaml` | Presentación, política de invocación y dependencias en Codex. | No; extensión específica del agente. |

El árbol descompone conceptualmente `SKILL.md` en cabecera y cuerpo; esas dos partes pertenecen al mismo archivo. Las carpetas auxiliares son convenciones recomendadas.[](source:spec)[](source:codex)

## ¿Qué lenguaje se utiliza y quién lo ejecuta? {#lenguajes}

| Formato o lenguaje | Uso dentro del skill | Quién lo interpreta o ejecuta |
| --- | --- | --- |
| Markdown `.md` | Pasos, decisiones, ejemplos y referencias. | El modelo interpreta las instrucciones. |
| YAML | Metadatos entre delimitadores `---`. | El agente o su cargador lee los campos. |
| Python `.py` | Procesar archivos, calcular, transformar datos. | Un intérprete Python mediante una herramienta. |
| JavaScript `.js` o `.mjs` | Automatización, APIs, generación de HTML. | Node.js u otro entorno compatible. |
| TypeScript `.ts` | Automatización con tipos. | Un entorno que soporte TS o código compilado a JS. |
| Bash o Shell `.sh` | Encadenar herramientas de terminal. | Una shell disponible en el sistema. |
| JSON, CSV y otros datos | Configuración, esquemas y ejemplos. | El script o la herramienta que los consuma. |

Un skill puede funcionar solo con Markdown. Los lenguajes de scripts dependen del entorno y de las herramientas del agente. Instalar el skill tampoco instala automáticamente Python, Node.js o sus dependencias.[](source:spec)

```bash title="Ejemplos de ejecución que puede indicar SKILL.md"
python3 scripts/validar.py entrada.json
node scripts/generar.mjs entrada.json
bash scripts/comprobar.sh
```

## ¿Qué cambia entre Claude Code, Codex e IBM Bob? {#agentes}

| Agente | Instalación local en el proyecto | Instalación personal o global |
| --- | --- | --- |
| Claude Code | `.claude/skills/mi-skill/SKILL.md` | `~/.claude/skills/mi-skill/SKILL.md` |
| Codex | `.agents/skills/mi-skill/SKILL.md` | `~/.agents/skills/mi-skill/SKILL.md` |
| IBM Bob | `.bob/skills/mi-skill/SKILL.md` | `~/.bob/skills/mi-skill/SKILL.md` |
| Cursor, vía Skills CLI | `.agents/skills/mi-skill/SKILL.md` | `~/.cursor/skills/mi-skill/SKILL.md` |
| GitHub Copilot, vía Skills CLI | `.agents/skills/mi-skill/SKILL.md` | `~/.copilot/skills/mi-skill/SKILL.md` |

En Claude Code se puede invocar con `/nombre-del-skill`. En Codex CLI y su extensión se puede seleccionar con `/skills` o mencionar con `$nombre-del-skill`. Ambos admiten selección por descripción.[](source:claude)[](source:codex)

Las rutas de IBM Bob, Cursor y Copilot y el identificador `bob` se verificaron en Skills CLI. No se confirmó aquí una sintaxis nativa de invocación de Bob.[](source:agents)

El formato base es compartido; las opciones específicas requieren comprobar compatibilidad. Por ejemplo, `agents/openai.yaml` pertenece a Codex y `context: fork` es una opción de Claude Code.[](source:codex)[](source:claude)

## ¿Cómo escribir un árbol de decisiones en Markdown? {#decisiones}

Define preguntas observables y una acción para cada respuesta. Este método es una recomendación de diseño para evitar instrucciones ambiguas.

@workflow id=decision-skill title="Decidir si hacen falta referencias o scripts"
| lane datos | Comprobar entradas |
| lane ruta | Elegir procedimiento |
| lane accion | Ejecutar la ruta |
| entrada | ¿Entradas completas? | security | datos |
| solicitar | Pedir el dato faltante | external | datos |
| automatizar | ¿Tarea mecánica repetible? | backend | ruta |
| ejecutar | Ejecutar script disponible | backend | accion |
| contexto | ¿Falta contexto de dominio? | backend | ruta |
| consultar | Leer referencia indicada | database | accion |
| instrucciones | Aplicar instrucciones | backend | accion |
| entrada > solicitar | No | security |
| entrada > automatizar | Sí | emphasis |
| automatizar > ejecutar | Sí |
| automatizar > contexto | No |
| contexto > consultar | Sí |
| contexto > instrucciones | No |

```markdown title="Árbol de decisiones copiable para SKILL.md"
## Decisiones
- Si falta la ruta del archivo: pedirla antes de continuar.
- Si la tarea exige un cálculo repetible:
  - Si existe un script adecuado: usarlo.
  - Si no existe: seguir el procedimiento manual documentado.
- Si falta contexto del dominio: leer references/reglas.md.
- Si las entradas están completas: aplicar el procedimiento.
- Después de cualquier ruta: verificar el resultado.
- Si falla la verificación: corregir la causa y volver a verificar.
```

Las condiciones escritas guían al modelo. Para una validación estricta de datos o cálculos, implementa también la comprobación en un script.

## ¿Qué técnicas de Markdown ayudan a crear buenos skills? {#tecnicas}

| Técnica | Cómo escribirla | Para qué sirve |
| --- | --- | --- |
| Contrato de entrada y salida | `## Entradas` y `## Salida` | Define qué recibir y qué entregar. |
| Pasos numerados | `1. Inspecciona...` | Expresa un orden de trabajo. |
| Árbol de decisiones | Listas con condiciones `Si...` | Elige rutas según hechos observables. |
| Tabla de decisión | Condición, acción y comprobación. | Compara varios casos sin repetir pasos. |
| Ejemplos de entrada y salida | Bloques de código con casos concretos. | Aclara el formato esperado. |
| Checklist final | `- [ ] Comprueba...` | Define los criterios de aceptación. |
| Referencias progresivas | Enlace relativo con cuándo leerlo. | Mantiene corto el archivo principal. |
| Límites y recuperación | `Si falla X, haz Y`. | Evita reintentos sin criterio. |

Estas técnicas son recomendaciones de autoría. La especificación permite instrucciones libres y recomienda separar referencias extensas del archivo principal.[](source:spec)

```yaml title="Cabecera portable de SKILL.md"
---
name: revisar-documento
description: Revisa claridad y estructura de un texto y entrega hallazgos priorizados. Usar cuando pidan revisar un borrador. No usar para traducir.
---
```

```markdown title="Cuerpo de SKILL.md después de la cabecera YAML"
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
- Si se requiere una guía de estilo: lee references/estilo.md.

## Salida
Entrega una tabla: ubicación, problema, propuesta y prioridad.

## Verificación
- [ ] Cada hallazgo apunta a un fragmento real.
- [ ] Las propuestas preservan la intención del autor.
- [ ] Los supuestos quedan visibles.
```

## ¿Dónde se encuentran y cómo llegan al agente? {#repositorios}

@architecture id=ecosistema-skill title="Del catálogo al agente"
| skillsmp-nodo | SkillsMP | external |
| skillssh-nodo | skills.sh | external |
| github-nodo | Repositorio GitHub | database |
| revisar-nodo | Revisar archivos | security |
| instalador-nodo | Skills CLI o copia | backend |
| carpetas-nodo | Carpeta local o global | database |
| agente-nodo | Claude, Codex o Bob | backend |
| skillsmp-nodo > github-nodo | descubrir |
| skillssh-nodo > github-nodo | descubrir |
| github-nodo > revisar-nodo | código |
| revisar-nodo > instalador-nodo | elegir |
| instalador-nodo > carpetas-nodo | instalar |
| carpetas-nodo > agente-nodo | descubrir | emphasis |

| Lugar | Qué aporta |
| --- | --- |
| [SkillsMP](https://skillsmp.com/) | Catálogo para descubrir skills y abrir su origen. No certifica ni instala los skills que indexa. |
| [skills.sh](https://skills.sh/) | Directorio del ecosistema y acceso a comandos del instalador Skills CLI. |
| [GitHub](https://github.com/) | Archivos, historial, licencia y versiones del repositorio fuente. |
| [anthropics/skills](https://github.com/anthropics/skills) | Colección de Anthropic. |
| [openai/skills](https://github.com/openai/skills) | Colección de OpenAI. |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Colección de Vercel. |
| [tt-a1i/archify](https://github.com/tt-a1i/archify) | Skill usado para generar esta guía visual. |

También puedes llegar directamente a un repositorio sin pasar por un catálogo. Revisa la licencia, el procedimiento y los scripts antes de instalarlos.[](source:skillsmp)[](source:skillssh)[](source:cli)

## ¿Cómo instalar un skill local o globalmente? {#instalacion}

Skills CLI es un instalador de terceros. Ejecuta los comandos locales desde la raíz del proyecto; `-g` cambia el alcance a tu usuario.[](source:cli)

```bash title="1. Ver skills disponibles antes de instalar"
npx skills add tt-a1i/archify --list
```

```bash title="2. Instalación LOCAL para Claude Code, Codex e IBM Bob"
npx skills add tt-a1i/archify --skill archify --agent claude-code codex bob
```

```bash title="3. Instalación GLOBAL para esos agentes"
npx skills add tt-a1i/archify --skill archify --agent claude-code codex bob -g
```

| Opción | Efecto |
| --- | --- |
| Sin `-g` | Disponible en el proyecto donde ejecutas el comando. |
| `-g` o `--global` | Disponible para tu usuario en varios proyectos de esa máquina. |
| `--skill archify` | Selecciona un skill del repositorio. |
| `--agent codex` | Elige el agente de destino. Admite varios agentes. |
| `--copy` | Crea copias en lugar de enlaces simbólicos. |
| `-y` | Omite los diálogos del instalador; úsalo tras revisar lo que instalarás. |

Global significa el alcance del skill para tu usuario. No equivale a `npm install -g`, ni lo instala para todos los usuarios del equipo. El instalador puede usar una copia compartida y enlaces a las rutas de los agentes.[](source:cli)

```bash title="Consultar, actualizar o retirar skills"
npx skills list
npx skills list -g
npx skills check
npx skills update
npx skills remove archify
```

También puedes crear manualmente la carpeta del skill y guardar allí `SKILL.md` y sus recursos, usando las rutas de la tabla de agentes.[](source:spec)[](source:agents)

## ¿Cómo comprobar que el skill está bien construido? {#comprobacion}

- [ ] El nombre identifica una tarea concreta y coincide con la carpeta.
- [ ] La descripción explica cuándo usarlo y delimita su alcance.
- [ ] La cabecera YAML contiene `name` y `description`.
- [ ] Cada referencia y script mencionado existe en una ruta relativa.
- [ ] Las dependencias de los scripts están documentadas.
- [ ] Se probó con un caso válido, uno incompleto y uno fuera de alcance.
- [ ] La salida cumple criterios que se pueden comprobar.
- [ ] El agente encuentra el skill en el alcance local o global esperado.

Un skill orienta el trabajo del agente; los permisos, herramientas y políticas del entorno siguen determinando qué acciones se pueden ejecutar.[](source:claude)[](source:codex)
