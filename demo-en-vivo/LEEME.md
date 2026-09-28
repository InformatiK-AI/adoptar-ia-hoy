# Cómo correr la demo en vivo (J5)

Opción A — Claude Code en una terminal, parado en esta carpeta (`demo-en-vivo/`):

1. Abre una terminal aquí (`cd demo-en-vivo`).
2. Ejecuta `claude` (o el agente de IA que uses) y pega el contenido de
   `prompt.md`.
3. Cuando pregunte por el archivo, indícale `encuesta_egresados.csv`.
4. Deja que lea el CSV, marque las filas incompletas, arme el gráfico y
   redacte el informe de una página.
5. Cierra narrando la última sección del informe: "Supuestos a validar".

Opción B — subir el CSV a claude.ai:

1. Abre una conversación nueva en claude.ai.
2. Sube `encuesta_egresados.csv`.
3. Pega el prompt de `prompt.md`.
4. Sigue los mismos 5 pasos de arriba (leer, marcar incompletos, graficar,
   informe con "Supuestos a validar").
5. Proyecta la respuesta completa en pantalla mientras narras.

**Plan B:** si algo falla (sin wifi, el agente no responde, etc.), reproduce
`deck/media/demo-ia.mp4` (el render de `videos/demo-ia`) y narra encima, tal como en `GUION.md` sección
"J5 · Demo".
