---
workflow: general-video
flow: automation
storyboard: no
message: "Un agente de IA convierte una encuesta ficticia en un informe con hallazgos reales, en segundos — y el humano decide qué asumir."
destination: proyector-aula
aspect: 1920x1080
language: es
audience: estudiantes universitarios buscando empleo, Semana de la Empleabilidad UFRO
length: 80s
narration: no
---

## Intent

Apoyo visual para la diapositiva J5 ("Demo: de un problema a un entregable") del
bloque de Jorge en la charla "Adoptar IA hoy" (UFRO, Semana de la Empleabilidad
2026). El clip es **silencioso por diseño**: Jorge narra en vivo, siguiendo el
video paso a paso (ver `GUION.md` sección "J5 · Demo"). El video no debe
concluir nada por sí solo — muestra el proceso, Jorge cierra la idea hablando.

Se ve un tablero de trabajo colaborativo (misma dirección de arte que el resto
del deck: "G · Tablero compartido") donde el cursor azul de Jorge y el cursor
violeta de la IA analizan `encuesta_egresados.csv`, una encuesta ficticia a
300 egresados. La IA abre el archivo, detecta filas incompletas, arma un
gráfico y redacta un informe de una página que termina en "Supuestos a
validar". Todos los números que aparecen son reales, calculados desde
`demo-en-vivo/resultados.json` — nada se inventa en pantalla.

## Assets

- `../../design/style-frames-3.html` (secciones `.G`, `#G1`, `#G2`) — dirección de arte de referencia, paleta y layout de tablero compartido.
- `../../design/frames/G1.png`, `../../design/frames/G2.png` — renders de referencia de esa dirección de arte.
- `../../deck/fonts/SchibstedGrotesk-latin.woff2`, `Figtree-latin.woff2` — tipografías locales del deck (se copian al proyecto, sin fuentes de red).
- `../../demo-en-vivo/resultados.json` — números reales que alimentan el video (medias, %, conteos).
- `../../demo-en-vivo/encuesta_egresados.csv` — dataset ficticio de origen (para la vista previa de tabla).
- `../../demo-en-vivo/prompt.md` — prompt real que se muestra (versión corta) en el panel de chat.

## Notes

- **Sin audio.** Sin narración, sin música, sin SFX. Jorge habla encima, en vivo.
- **Datos ficticios, siempre rotulados.** Badge "Datos ficticios" visible en la barra superior todo el video.
- **Orden de beats fijo, calcado del guion J5** (ver `STORYBOARD.md`): tarjeta de archivo → prompt escrito por Jorge → vista previa de tabla → aviso de exclusión de filas incompletas → gráfico de barras → informe de una página con "Supuestos a validar" (≥10s de hold, el remate de Jorge cae aquí) → tarjeta final "Tú diriges, la IA ejecuta."
- Cada beat dura ≥8s para dejar espacio a la narración en vivo. Duración total 75–90s.
- Paleta y tokens heredados del deck: fondo `#F3F5FA` con canvas punteado, tinta `#161A2E`, tinta suave `#6B7390`, línea `#DCE1EC`, azul Jorge `#3D6BFF`, violeta IA `#8B5CF6`, coral `#FF7A6B` y ámbar `#FFB938` como acentos puntuales.
- Tipografía grande y legible desde el fondo de un auditorio (cuerpo ≥28px a 1080p). Sin mayúsculas sostenidas en eyebrows, sin botones tipo pill, sin fondos crema.
- Movimiento deliberado y legible, no efectos gratuitos.
- Bloque comprimible de la charla (tiene plan B: `demo-en-vivo/LEEME.md` para la demo en vivo), pero el video mismo no se puede recortar — el orden de beats sigue el guion palabra por palabra.
