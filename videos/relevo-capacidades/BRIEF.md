---
workflow: general-video
flow: automation
storyboard: no
message: "La IA ya sabe hacer estas ocho cosas; la pregunta es dónde aplicarlas."
destination: proyector-auditorio (dentro del recuadro punteado de la slide 19 del deck)
aspect: 1920x1128
language: es
audience: estudiantes universitarios buscando empleo, Semana de la Empleabilidad UFRO
length: 36s (loop continuo)
narration: no
audio: no
---

## Intent

Background loop for slide 19 "Relevo a Gonzalo" (J8, 1 min) of the talk "Adoptar IA hoy"
(UFRO, 28-09-2026). Jorge closes his block asking "¿Dónde aplicarlas?" and hands over to
Gonzalo. The video replaces the static 2x4 grid of eight AI capabilities inside the dashed box.

Concept: four rows of sticky notes (emoji tile + label) drifting slowly left/right in
alternating directions, like a shared whiteboard being browsed. Each row carries two
capabilities, so all eight stay on screen almost all the time and are read in place.

## Constraints

- Muted, seamless loop: each row travels exactly one repeat period (1780 px) in 36 s, so the
  last frame flows into the first.
- Calm: about 50 px/s in video space; it accompanies the speaker, it does not compete.
- Legible from the back row: labels 62 px Figtree 800 in a 1920-wide frame (larger than the
  deck's original notes once scaled into the box).
- Art direction "G · Tablero compartido": blue-soft `#E1E8FF` box background, white notes with
  deck tints for the emoji tiles, ink `#161A2E`. No violet-blue gradients, glow, neon,
  glassmorphism, particles or confetti; emojis stay beside the label, smaller than it.
- Aspect 1920x1128 matches the dashed box on the 16:9 stage (68 % x 71 %).

## Output

`renders/relevo-capacidades.mp4`, copied to `deck/media/relevo-capacidades.mp4`.
