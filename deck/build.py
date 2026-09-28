#!/usr/bin/env python3
"""Build script for the "Adoptar IA hoy" deck.

Reads deck/src/index.src.html, inlines fonts (woff2 -> base64) and images
(JPEG -> resized + base64), and writes the single self-contained
deck/index.html. No network access is used or required at build time or at
runtime: everything ends up embedded as data: URIs.
"""
import base64
import io
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src" / "index.src.html"
OUT = ROOT / "index.html"
FONTS = ROOT / "fonts"
IMG_DIR = ROOT.parent / "img"
DEMO_VIDEO = ROOT / "media" / "demo-ia.mp4"
RAG_VIDEO = ROOT / "media" / "rag-gonzalo.mp4"
RELEVO_VIDEO = ROOT / "media" / "relevo-capacidades.mp4"
J4_VIDEO = ROOT / "media" / "j4-patron.mp4"

MAX_LONG_SIDE = 1400
JPEG_QUALITY = 82


def font_data_uri(path: Path) -> str:
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:font/woff2;base64,{b64}"


def image_data_uri(path: Path) -> str:
    im = Image.open(path)
    if im.mode != "RGB":
        im = im.convert("RGB")
    w, h = im.size
    long_side = max(w, h)
    if long_side > MAX_LONG_SIDE:
        scale = MAX_LONG_SIDE / long_side
        im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


def video_poster_attr(video: Path, timestamp_sec: int, label: str) -> str:
    """Best-effort poster frame for a video slide, extracted with ffmpeg if
    both the mp4 and ffmpeg are available. Never required: if either is
    missing, the video/fallback logic in the page already covers it, so this
    just returns an empty string (no poster attribute) and the build still
    succeeds without network access or a hard dependency on ffmpeg."""
    if not video.exists() or shutil.which("ffmpeg") is None:
        return ""
    try:
        with tempfile.TemporaryDirectory() as tmp:
            frame_path = Path(tmp) / "poster.jpg"
            subprocess.run(
                [
                    "ffmpeg", "-y", "-ss", str(timestamp_sec), "-i", str(video),
                    "-frames:v", "1", "-q:v", "3", str(frame_path),
                ],
                check=True, capture_output=True, timeout=30,
            )
            uri = image_data_uri(frame_path)
            return f' poster="{uri}"'
    except Exception as exc:  # pragma: no cover - best effort only
        print(f"Warning: could not extract {label} poster frame ({exc}); continuing without one.")
        return ""


def main() -> None:
    html = SRC.read_text(encoding="utf-8")

    replacements = {
        "{{FONT_SCHIBSTED}}": font_data_uri(FONTS / "SchibstedGrotesk-latin.woff2"),
        "{{FONT_FIGTREE}}": font_data_uri(FONTS / "Figtree-latin.woff2"),
        "{{IMG_CAMILA}}": image_data_uri(IMG_DIR / "WhatsApp Image 2026-09-23 at 12.09.28 AM.jpeg"),
        "{{IMG_CCHIA}}": image_data_uri(IMG_DIR / "WhatsApp Image 2026-09-23 at 12.10.23 AM.jpeg"),
        "{{IMG_STAND}}": image_data_uri(IMG_DIR / "WhatsApp Image 2026-09-23 at 12.11.40 AM.jpeg"),
        "{{IMG_COMUNIDAD}}": image_data_uri(IMG_DIR / "WhatsApp Image 2026-09-23 at 12.14.51 AM.jpeg"),
        "{{DEMO_POSTER_ATTR}}": video_poster_attr(DEMO_VIDEO, 68, "demo video"),
        "{{RAG_POSTER_ATTR}}": video_poster_attr(RAG_VIDEO, 84, "rag video"),
        "{{RELEVO_POSTER_ATTR}}": video_poster_attr(RELEVO_VIDEO, 0, "relevo video"),
        "{{J4_POSTER_ATTR}}": video_poster_attr(J4_VIDEO, 3.5, "j4 video"),
    }

    missing = [k for k in replacements if k not in html]
    if missing:
        raise SystemExit(f"Placeholders not found in source (check src file): {missing}")

    for placeholder, uri in replacements.items():
        html = html.replace(placeholder, uri)

    OUT.write_text(html, encoding="utf-8")
    size_kb = OUT.stat().st_size / 1024
    print(f"Wrote {OUT} ({size_kb:.1f} KiB)")


if __name__ == "__main__":
    main()
