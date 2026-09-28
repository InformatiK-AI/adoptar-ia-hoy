"""Minimal local RAG over the Obsidian vault of resolved tickets (fictitious data).

Pipeline: Markdown notes -> chunks (by heading) -> embeddings (fastembed, ONNX, local)
-> Chroma (local vector DB) -> retrieve top-k -> answer + workflow via `claude -p`
(the model only sees the retrieved chunks and has no tools).

Usage:
  python demo-rag/rag.py index  [--vault PATH]
  python demo-rag/rag.py query  [--q "question"]
  python demo-rag/rag.py export          # writes videos/rag-gonzalo/data.js
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "salida"
DB_DIR = HERE / "chroma"
VIDEO_DATA = ROOT / "videos" / "rag-gonzalo" / "data.js"
DEFAULT_VAULT = HERE / "vault"
MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
COLLECTION = "tickets"
EXAMPLE_NOTE = "TK-2025-0112"
DEFAULT_QUERY = ("Los pagos del fin de semana no aparecen en el CRM y a clientes que ya pagaron "
                 "les llegó la orden de corte. ¿Cómo se resolvió antes?")
TOP_K = 10


def embedder():
    from fastembed import TextEmbedding
    return TextEmbedding(model_name=MODEL)


def collection(reset=False):
    import chromadb
    client = chromadb.PersistentClient(path=str(DB_DIR))
    if reset:
        try:
            client.delete_collection(COLLECTION)
        except Exception:
            pass
    return client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


def read_note(path):
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if m:
        meta, body = yaml.safe_load(m.group(1)) or {}, m.group(2)
    body = re.sub(r"!\[\[[^\]]+\]\]\n?", "", body)          # drop image embeds
    body = re.sub(r"\[\[([^\]|]+)(\|[^\]]+)?\]\]", r"\1", body)  # [[link]] -> link
    return meta, body.strip()


def chunk_note(meta, body):
    from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
    by_heading = MarkdownHeaderTextSplitter([("#", "h1"), ("##", "seccion")]).split_text(body)
    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=100)
    head = f"{meta['id']}: {meta.get('titulo', '')}"
    chunks = []
    for doc in by_heading:
        section = doc.metadata.get("seccion", "Encabezado")
        for piece in splitter.split_text(doc.page_content):
            chunks.append({"seccion": section, "texto": piece, "doc": f"{head}\n## {section}\n{piece}"})
    return chunks


def cmd_index(args):
    vault = Path(args.vault)
    notes = sorted((vault / "raw" / "tickets").rglob("TK-*.md"))
    ids, docs, metas, example = [], [], [], []
    for path in notes:
        meta, body = read_note(path)
        for i, c in enumerate(chunk_note(meta, body)):
            ids.append(f"{meta['id']}#{i}")
            docs.append(c["doc"])
            metas.append({"ticket": meta["id"], "titulo": str(meta.get("titulo", "")),
                          "sistema": str(meta.get("sistema", "")), "seccion": c["seccion"],
                          "archivo": str(path.relative_to(vault)).replace("\\", "/")})
            if meta["id"] == EXAMPLE_NOTE:
                example.append({"seccion": c["seccion"], "chars": len(c["texto"]),
                                "inicio": c["texto"][:90]})
    vectors = [v.tolist() for v in embedder().embed(docs)]
    col = collection(reset=True)
    col.add(ids=ids, documents=docs, embeddings=vectors, metadatas=metas)
    OUT.mkdir(exist_ok=True)
    first = ids.index(f"{EXAMPLE_NOTE}#0")
    stats = {"modelo": MODEL, "notas": len(notes), "fragmentos": len(ids), "dimensiones": len(vectors[0]),
             "ejemplo_nota": EXAMPLE_NOTE, "ejemplo_fragmentos": example,
             "ejemplo_vector": [round(x, 3) for x in vectors[first][:8]],
             "notas_lista": [p.stem for p in notes]}
    (OUT / "indice.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"indexed {len(notes)} notes -> {len(ids)} chunks x {len(vectors[0])} dims into {DB_DIR}")


PROMPT = """Eres el asistente de soporte de TI de una empresa sanitaria. Responde SOLO con la
información del CONTEXTO (fragmentos de tickets resueltos). Si algo no está en el contexto, no lo inventes.

PREGUNTA: {q}

CONTEXTO:
{ctx}

Devuelve SOLO un JSON válido, sin texto adicional ni bloques de código, con esta forma:
{{"respuesta": "máximo 45 palabras, en español, explicando la causa probable y cómo se resolvió; cita todos los tickets en que te basas así [TK-AAAA-NNNN]",
  "flujo": [{{"paso": "máximo 4 palabras", "detalle": "máximo 9 palabras", "fuente": "TK-AAAA-NNNN"}}]}}
El flujo tiene entre 4 y 5 pasos accionables, en orden, cubre también el impacto en los clientes,
y la fuente de cada paso es el ticket del contexto que mejor lo documenta."""


def ask_claude(prompt):
    exe = shutil.which("claude.cmd") or shutil.which("claude")
    res = subprocess.run([exe, "-p", "--model", "sonnet", "--tools", "", "--safe-mode",
                          "--no-session-persistence", "--output-format", "json"],
                         input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=300)
    if res.returncode != 0:
        sys.exit(f"claude -p failed: {res.stderr[:500]}")
    text = json.loads(res.stdout)["result"].strip()
    text = re.sub(r"^```(json)?|```$", "", text, flags=re.M).strip()
    return json.loads(text)


def cmd_query(args):
    import numpy as np
    from sklearn.manifold import TSNE
    col = collection()
    qvec = list(embedder().embed([args.q]))[0].tolist()
    hits = col.query(query_embeddings=[qvec], n_results=TOP_K, include=["documents", "metadatas", "distances"])
    chunks = [{"id": i, "ticket": m["ticket"], "titulo": m["titulo"], "seccion": m["seccion"],
               "archivo": m["archivo"], "similitud": round(1 - d, 3), "texto": doc}
              for i, m, d, doc in zip(hits["ids"][0], hits["metadatas"][0], hits["distances"][0], hits["documents"][0])]
    tickets = []
    for c in chunks:
        if c["ticket"] not in [t["ticket"] for t in tickets]:
            tickets.append({k: c[k] for k in ("ticket", "titulo", "archivo", "similitud")})
    ctx = "\n\n---\n\n".join(c["texto"] for c in chunks)
    out = ask_claude(PROMPT.format(q=args.q, ctx=ctx))
    retrieved = {t["ticket"] for t in tickets}
    cited = set(re.findall(r"TK-\d{4}-\d{4}", out["respuesta"])) | {p["fuente"] for p in out["flujo"]}
    if not cited <= retrieved:
        sys.exit(f"answer cites tickets not retrieved: {sorted(cited - retrieved)}")
    # 2-D map of every chunk plus the query (t-SNE keeps local neighbourhoods)
    everything = col.get(include=["embeddings", "metadatas"])
    X = np.vstack([np.array(everything["embeddings"]), np.array(qvec)])
    xy = TSNE(n_components=2, perplexity=30, init="pca", random_state=42).fit_transform(X)
    xy = (xy - xy.min(0)) / (xy.max(0) - xy.min(0))
    points = [{"id": i, "ticket": m["ticket"], "sistema": m["sistema"], "x": round(float(p[0]), 4), "y": round(float(p[1]), 4)}
              for i, m, p in zip(everything["ids"], everything["metadatas"], xy[:-1])]
    result = {"consulta": args.q, "top_k": TOP_K, "fragmentos": chunks, "tickets": tickets,
              "respuesta": out["respuesta"], "flujo": out["flujo"], "citados": sorted(cited),
              "mapa": {"puntos": points, "consulta": {"x": round(float(xy[-1][0]), 4), "y": round(float(xy[-1][1]), 4)}}}
    OUT.mkdir(exist_ok=True)
    (OUT / "consulta.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("tickets:", [(t["ticket"], t["similitud"]) for t in tickets])
    print("respuesta:", out["respuesta"])
    for p in out["flujo"]:
        print(" -", p["paso"], "|", p["detalle"], "|", p["fuente"])


def cmd_export(_args):
    indice = json.loads((OUT / "indice.json").read_text(encoding="utf-8"))
    consulta = json.loads((OUT / "consulta.json").read_text(encoding="utf-8"))
    for c in consulta["fragmentos"]:
        c.pop("texto")
    data = {"indice": indice, "consulta": consulta}
    VIDEO_DATA.parent.mkdir(parents=True, exist_ok=True)
    VIDEO_DATA.write_text("window.RAG = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"wrote {VIDEO_DATA}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("index"); p.add_argument("--vault", default=str(DEFAULT_VAULT)); p.set_defaults(fn=cmd_index)
    p = sub.add_parser("query"); p.add_argument("--q", default=DEFAULT_QUERY); p.set_defaults(fn=cmd_query)
    p = sub.add_parser("export"); p.set_defaults(fn=cmd_export)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
