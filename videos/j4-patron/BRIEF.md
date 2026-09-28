---
workflow: general-video
flow: automation
storyboard: no
message: "Four different careers, the same pattern: Antes → Con IA → Tu criterio. The AI does the heavy lifting; you supply the judgment."
destination: proyector-auditorio
aspect: 1920x1080
language: es
audience: estudiantes universitarios buscando empleo, Semana de la Empleabilidad UFRO
length: 182s
narration: no
---

## Intent

Supporting video for the J4 block ("Cuatro carreras, un mismo patrón") of the talk "Adoptar IA hoy"
(UFRO, 28-09-2026). Jorge narrates live over it; the video is seek-driven by the deck (`odd/tasks/j4-hyperframes.md`
segment contract): each presenter advance plays a short build, then holds on a seamless idle loop until the
next advance. 14 steps (0..13): a title step, 3 steps per case (Antes / Con IA / Tu criterio) × 4 cases, and a
closing step.

Same art direction as the deck ("G · Tablero compartido"): dotted canvas `#F3F5FA`, ink `#161A2E`,
mute `#6B7390`, line `#DCE1EC`, Jorge's blue cursor `#3D6BFF`, the AI's violet cursor `#8B5CF6`.

## Illustrative-only rule

Everything shown (spreadsheets, code, studies, documents, indicators, requirements) is an illustrative
dramatization of the four cases named in `GUION.md` §J4 (Agronomía, Ingeniería, Salud, Negocios y Derecho).
No invented figures — the only numbers on screen are the ones already in the script ("80 páginas",
"una semana", "cada lunes", "semanas").

## Segment contract (seconds) — see `segments.json`

| Step | Start | Build ends | Loop start | Loop end |
|---|---|---|---|---|
| 0 | 0 | 3 | 3 | 11 |
| 1 (Agronomía · Antes) | 11 | 16 | 16 | 24 |
| 2 (Agronomía · Con IA) | 24 | 29 | 29 | 37 |
| 3 (Agronomía · Tu criterio) | 37 | 42 | 42 | 50 |
| 4 (Ingeniería · Antes) | 50 | 55 | 55 | 63 |
| 5 (Ingeniería · Con IA) | 63 | 68 | 68 | 76 |
| 6 (Ingeniería · Tu criterio) | 76 | 81 | 81 | 89 |
| 7 (Salud · Antes) | 89 | 94 | 94 | 102 |
| 8 (Salud · Con IA) | 102 | 107 | 107 | 115 |
| 9 (Salud · Tu criterio) | 115 | 120 | 120 | 128 |
| 10 (Negocios y Derecho · Antes) | 128 | 133 | 133 | 141 |
| 11 (Negocios y Derecho · Con IA) | 141 | 146 | 146 | 154 |
| 12 (Negocios y Derecho · Tu criterio) | 154 | 159 | 159 | 167 |
| 13 (closing) | 167 | 174 | 174 | 182 |

Idle period P = 4s, each loop window is rendered twice back-to-back (8s) so a late `timeupdate` jump during
playback is invisible. Idle motion is limited to: cursor drift ≤ 14 px (yoyo, period 4s), AI comment caret
blink (0.5s steps), and marching-ants selection outlines — nothing else changes during a hold.

## Notes

- No audio track: Jorge narrates live over the video.
- Legible from the back row: title ≥ 64 px, body/comments ≥ 40 px where possible, nothing < 32 px.
- Forbidden: line-by-line text fades, particle/gradient backgrounds, neon glow, number counters, generic
  camera zooms/pans. Only AI comments and the step-13 closing labels use letter-by-letter typed text (with
  caret); everything else is a whole-block reveal.
