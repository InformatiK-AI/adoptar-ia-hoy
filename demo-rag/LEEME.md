# Demo RAG — «Cuando el que sabe no está» (bloque de Gonzalo, G5)

RAG mínimo y local sobre el vault de Obsidian de tickets resueltos (datos ficticios y anonimizados).
Los 40 tickets de la empresa ficticia Sanitaria Los Coihues están en `vault/raw/tickets/`.
Es la fuente de todo lo que aparece en pantalla en `deck/media/rag-gonzalo.mp4`.

## Stack

| Paso | Herramienta | Por qué |
|---|---|---|
| Fragmentos | `langchain-text-splitters` (por encabezado `##`, máx. 900 caracteres) | Cada sección del ticket (Diagnóstico, Causa raíz, Resolución…) queda como una unidad con sentido |
| Embeddings | `fastembed` + `paraphrase-multilingual-MiniLM-L12-v2` (384 dim, ONNX, local) | Entiende español, corre en CPU y no necesita torch |
| Base vectorial | Chroma `PersistentClient` (carpeta `chroma/`) | Una carpeta local, sin servidor |
| Respuesta | `claude -p` sin herramientas y en modo seguro | Solo ve los fragmentos recuperados y tiene que citar `[TK-…]`; el script aborta si cita un ticket que no recuperó |

## Cómo correrlo

```bash
python -m pip install -r demo-rag/requirements.txt
python demo-rag/rag.py index                 # 40 tickets -> 304 fragmentos x 384 dim
python demo-rag/rag.py query                 # consulta por defecto (la del video)
python demo-rag/rag.py query --q "..."       # cualquier otra pregunta
python demo-rag/rag.py export                # regenera videos/rag-gonzalo/data.js
```

Salidas: `salida/indice.json` (estadísticas, troceo del TK-2025-0112, primeros valores del vector) y
`salida/consulta.json` (fragmentos recuperados con similitud, respuesta, flujo y mapa t-SNE 2D).

## Opción en vivo (si sobra tiempo o alguien pregunta)

Con internet, `python demo-rag/rag.py query --q "la OT de una fuga no llega a la tablet de la cuadrilla"`
responde en unos 20–40 s. El video no depende de esto: ya trae la corrida real grabada.
