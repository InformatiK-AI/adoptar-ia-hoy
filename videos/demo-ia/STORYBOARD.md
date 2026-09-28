---
format: 1920x1080
duration: 82s
message: "Un agente de IA convierte una encuesta ficticia en un informe con hallazgos reales, en segundos — y el humano decide qué asumir."
arc: Archivo → Prompt → Lectura → Exclusión → Gráfico → Informe → Punchline
audience: estudiantes UFRO, Semana de la Empleabilidad 2026
mode: autonomous
---

One continuous shot: a shared work-board (dirección "G", ver `../../design/style-frames-3.html#G1/#G2`). A top bar and Jorge/IA cursors persist for the whole clip; a right-hand chat sidebar accumulates messages; the main panel morphs its content per beat. Single composition file (`index.html`), no hard scene cuts — built inline, not dispatched.

## Frame 1 — Archivo ficticio

- status: built
- duration: 9s
- src: index.html (t=0–9)
- scene: Tarjeta de archivo "encuesta_egresados.csv — 300 respuestas (ficticias)" aparece en el tablero; barra superior con badge "Datos ficticios".
- voiceover: (Jorge narra en vivo) "Preparé una encuesta ficticia a trescientos egresados sobre empleabilidad..."

Cita: `waterfall-entry` para la barra y el badge; `spring-pop-entrance` para la tarjeta del archivo.

## Frame 2 — Jorge escribe el prompt

- status: built
- duration: 12s
- src: index.html (t=9–21)
- scene: El cursor azul de Jorge escribe (efecto máquina de escribir) una versión corta del prompt en el panel de chat lateral.
- voiceover: "...Le voy a pedir a un agente de IA que la analice como lo haría un analista."

Cita: `gsap-effects` (typewriter) + `context-sensitive-cursor` para el caret; `multi-cursor-choreography` para el cursor de Jorge.

## Frame 3 — La IA abre el archivo

- status: built
- duration: 12s
- src: index.html (t=21–33)
- scene: El cursor violeta de la IA "abre" el archivo; el panel principal cruza a una vista previa de tabla (columnas + 5 filas de muestra); burbuja IA en el chat: "Leyendo encuesta_egresados.csv — 300 filas, 7 columnas."
- voiceover: "Primero lee el archivo y me cuenta qué columnas tiene…"

Cita: `theme-crossfade-morph` para el cambio de panel; `waterfall-entry` para las filas de la tabla.

## Frame 4 — Detecta las respuestas incompletas

- status: built
- duration: 11s
- src: index.html (t=33–44)
- scene: Una fila de la tabla (meses_primer_empleo en blanco) se resalta en coral; banner "18 filas sin 'meses hasta el primer empleo' → excluidas de los promedios"; burbuja IA en el chat con el mismo mensaje.
- voiceover: "Aquí detecta que hay respuestas incompletas y me dice cómo las va a tratar…"

Cita: `ai-tracking-box`-style highlight (adaptado a fila de tabla, sin bounding box) + `waterfall-entry` para el banner.

## Frame 5 — Gráfico por carrera

- status: built
- duration: 14s
- src: index.html (t=44–58)
- scene: El panel principal cruza a un gráfico de barras horizontales: meses promedio hasta el primer empleo por carrera (8 barras, valores reales, orden ascendente), que crecen una por una.
- voiceover: "Ahora arma el gráfico de meses hasta el primer empleo por carrera…"

Cita: `stat-bars-and-fills` (growth bars, `scaleX` stagger).

## Frame 6 — Informe de una página

- status: built
- duration: 16s
- src: index.html (t=58–74)
- scene: El panel principal cruza a un informe de una página: título, 3 hallazgos con números reales, y una sección final "Supuestos a validar" resaltada que queda en pantalla ≥10s (remate de Jorge).
- voiceover: "Y aquí redacta un informe de una página con tres hallazgos... Pero miren la última sección: 'Supuestos a validar'. La IA me dice qué no sabe. Y quien decide si este informe es correcto… sigo siendo yo."

Cita: `spring-pop-entrance` para el informe; `waterfall-entry` para los 3 hallazgos; hold estático (sin animación nueva) en la caja "Supuestos a validar" durante los últimos 10s.

## Frame 7 — Cierre

- status: built
- duration: 8s
- src: index.html (t=74–82)
- scene: El tablero se despeja; queda centrado "Tú diriges, la IA ejecuta." con un subrayado bicolor (azul Jorge / violeta IA).
- voiceover: (silencio; Jorge ya cerró la idea en el Frame 6; esto es un respiro visual antes de pasar a J6)

Cita: `waterfall-entry` para el titular; `gradient-text-sweep` opcional en el subrayado (no crítico).
