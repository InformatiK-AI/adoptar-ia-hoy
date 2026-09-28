# Adoptar IA hoy

Charla de 40 minutos para la **Semana de la Empleabilidad 2026** de la **Universidad de La Frontera** (Temuco, 28 de septiembre de 2026). Tres relatores cuentan una misma historia en tres niveles:

| Nivel | Relator | Idea | Duración |
|---|---|---|---|
| 1 · Visibilidad | Camila | Haz que sepan lo que sabes | 15 min |
| 2 · Capacidad | Jorge | Multiplica lo que sabes con IA | 13 min |
| 3 · Valor | Gonzalo | Usa eso para resolver un problema real | 12 min |

El repositorio contiene la presentación (un HTML autocontenido con ventana del presentador), los videos animados que usa, las dos demos de IA y el guion completo.

**▶ Ver la presentación en línea:** https://informatik-ai.github.io/adoptar-ia-hoy/

## Presentar el deck

Abre `deck/index.html` en Chrome o Edge. Funciona sin internet: las fuentes y las imágenes van dentro del HTML y los videos se cargan desde `deck/media/`. Para llevarla en un pendrive, copia la carpeta `deck/` completa.

| Tecla | Acción |
|---|---|
| → · Espacio · Enter · PageDown · clic | Avanzar (fragmento o slide) |
| ← · PageUp · Backspace | Retroceder |
| Home / End | Primera / última slide |
| **P** | Ventana del presentador (arranca el cronómetro) |
| T | Muestra u oculta el cronómetro en la pantalla del público |
| N | Guion en la misma página, si el navegador bloquea la ventana emergente |
| O | Índice de slides |
| F | Pantalla completa |
| L | Tema claro u oscuro |
| ? · Esc | Ayuda · cerrar índice, ayuda o notas |

La **ventana del presentador** muestra la slide actual con el color de su relator, la siguiente, el guion paso a paso (qué decir en cada avance), el tiempo total con el desvío respecto del plan y el aviso de relevo 30 segundos antes de cada cambio de relator. Con dos pantallas: presentador en el notebook y la presentación en pantalla completa en el proyector. El cronómetro se reinicia con doble clic sobre el reloj.

Antes de empezar, conviene abrir la ventana del presentador (permitir la ventana emergente si el navegador la bloquea) y avanzar una vez en las slides con video para confirmar que se reproducen. El reel de la slide 3 tiene sonido: si el navegador bloquea el audio porque se avanzó desde la ventana del presentador, un clic sobre el video lo activa.

`GUION.md` tiene el guion completo de los tres relatores, con tiempos, acotaciones y un plan B por bloque.

## Estructura

```
deck/                 Presentación
  src/index.src.html    Fuente editable (slides, estilos, lógica del presentador)
  build.py              Genera index.html incrustando fuentes e imágenes
  index.html            Deck final autocontenido (generado)
  media/                Videos que reproduce el deck
  fonts/                Schibsted Grotesk y Figtree (woff2)
  tools/                Auditoría de layout y de notas del presentador
videos/               Proyectos HyperFrames (composiciones HTML que se renderizan a MP4)
  demo-ia/              Demo de análisis de datos (slide 16, sin audio)
  j4-patron/            «Cuatro carreras, un mismo patrón», con segmentos por avance
  rag-gonzalo/          Ejercicio RAG, con música y efectos
  relevo-capacidades/   Loop de capacidades de la IA (relevo a Gonzalo)
demo-rag/             RAG local sobre tickets de soporte ficticios (fuente del video rag-gonzalo)
demo-en-vivo/         Demo en vivo con un agente de IA y una encuesta ficticia
design/               Exploración de dirección de arte (style frames)
img/                  Fotos que build.py incrusta en el deck
GUION.md              Guion completo
LEEME.md              Lista de verificación para el día de la charla
```

## Regenerar el deck

Edita `deck/src/index.src.html`, nunca `deck/index.html`, y luego:

```bash
python -m pip install pillow
python deck/build.py
```

Si `ffmpeg` está en el PATH, el build también extrae los pósteres de los videos; sin él, el deck funciona igual, sin póster.

Controles de calidad (requieren Microsoft Edge y `beautifulsoup4`):

```bash
python deck/tools/run_audit.py     # desbordes, solapamientos y grilla en 6 tamaños de pantalla
python deck/tools/check_notes.py   # cada avance tiene su paso en las notas
```

## Regenerar los videos

Cada carpeta de `videos/` es un proyecto [HyperFrames](https://github.com/heygen-com/hyperframes) fijado en la versión 0.8.69 (se ejecuta con `npx`, requiere Node.js y ffmpeg). `BRIEF.md` describe la intención de cada video.

```bash
cd videos/rag-gonzalo
npm run dev                                          # vista previa en el navegador
npm run check                                        # validación de la composición
npm run render -- --output renders/rag-gonzalo.mp4   # render final
```

Después, copia el MP4 de `renders/` a `deck/media/` con el mismo nombre.

- **j4-patron:** el deck salta entre segmentos del video en cada avance, así que se re-codifica con un keyframe cada 0,5 s:
  ```bash
  ffmpeg -i renders/j4-patron.mp4 -c:v libx264 -preset slow -crf 18 -g 15 -keyint_min 15 -sc_threshold 0 -an -movflags +faststart ../../deck/media/j4-patron.mp4
  ```
  Los tiempos de cada segmento están en `segments.json`.
- **rag-gonzalo:** la pista `assets/audio/soundtrack.wav` se genera con `python tools/make_audio.py` (numpy y ffmpeg): una base musical sintetizada más efectos de sonido. Los efectos vienen de la biblioteca `media-use` de HyperFrames (Pixabay) y no se incluyen en el repositorio; cópialos a `assets/sfx/` antes de generar la pista. Los datos en pantalla salen de `data.js`, que exporta `demo-rag`.

## Demos

### RAG local (`demo-rag/`)

Recupera fragmentos de 40 tickets de soporte ficticios con embeddings multilingües locales (`fastembed`) y Chroma, y responde con Claude citando los tickets. El stack, la justificación de cada pieza y los comandos están en [`demo-rag/LEEME.md`](demo-rag/LEEME.md). La respuesta usa `claude -p`, así que requiere [Claude Code](https://claude.com/claude-code) instalado.

```bash
python -m pip install -r demo-rag/requirements.txt
python demo-rag/rag.py index
python demo-rag/rag.py query
```

### Análisis de datos en vivo (`demo-en-vivo/`)

Un agente de IA lee `encuesta_egresados.csv` (300 egresados **ficticios**, generados con `generar_datos.py`), detecta respuestas incompletas, grafica y redacta un informe que termina en «Supuestos a validar». Pasos y prompt en [`demo-en-vivo/LEEME.md`](demo-en-vivo/LEEME.md). Si falla la conexión, el deck ya trae el video de respaldo (`deck/media/demo-ia.mp4`).

## Créditos

- Relatores: Camila, Jorge y Gonzalo.
- Videos animados con [HyperFrames](https://github.com/heygen-com/hyperframes); efectos de sonido de [Pixabay](https://pixabay.com/sound-effects/) bajo su licencia de contenido.
- Tipografías [Schibsted Grotesk](https://fonts.google.com/specimen/Schibsted+Grotesk) y [Figtree](https://fonts.google.com/specimen/Figtree), bajo SIL Open Font License 1.1.
- Embeddings con [paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) vía `fastembed`; base vectorial [Chroma](https://www.trychroma.com/).

## Licencia

El código (scripts, herramientas y composiciones) está bajo [MIT](LICENSE). El contenido (guion, slides, videos y diseño) está bajo [CC BY 4.0](LICENSE-CONTENT.md). Las tipografías conservan su licencia OFL.
