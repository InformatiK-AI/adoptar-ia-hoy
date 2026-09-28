# Prompt para la demo en vivo

Prompt para pegar en un agente de IA (Claude Code, Claude.ai, etc.) junto con
`encuesta_egresados.csv`. Los datos son **ficticios** — una encuesta simulada
a 300 egresados, creada solo para esta charla.

```
Actúa como analista de datos. Te adjunto encuesta_egresados.csv, una encuesta
FICTICIA a 300 egresados sobre su empleabilidad (dejar esto explícito en el
informe). Columnas: id, carrera, anio_egreso, meses_primer_empleo,
trabaja_en_su_area, usa_ia_en_el_trabajo, habilidades_pedidas.

1. Léela y cuéntame qué columnas tiene y cuántas filas.
2. Detecta respuestas incompletas (por ejemplo, meses_primer_empleo o
   usa_ia_en_el_trabajo en blanco). Dime cuántas son y cómo las vas a tratar
   (inclúyelo también en el informe).
3. Calcula el promedio de meses hasta el primer empleo por carrera y grafícalo
   de menor a mayor.
4. Escribe un informe de una página con:
   - 3 hallazgos concretos, con números reales de los datos.
   - Una sección final "Supuestos a validar" que mencione que los datos son
     ficticios, cuántas filas se excluyeron y que correlación no implica
     causalidad.
```
