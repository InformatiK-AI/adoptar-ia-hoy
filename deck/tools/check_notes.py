"""Validate that speaker notes are split per fragment step.

Contract per <section class="slide">:
- every .frag has an explicit integer data-f >= 1 (no implicit numbering);
- groups are contiguous 1..M (M = max data-f; M may be 0);
- .notas contains exactly M+1 <div class="paso" data-paso="k"> for k = 0..M, in order;
- every paso with k >= 1 starts with <p class="cue"> containing "aparece:";
- the last paso contains a <p class="cue"> with "siguiente:" (hand-off to the next slide),
  except on the final slide;
- every paso contains at least one spoken <p> (no class) or a <p class="esc">.

Usage: python deck/tools/check_notes.py [path/to/index.src.html]   (exit 1 on any violation)
"""
import pathlib
import sys

from bs4 import BeautifulSoup

DECK = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DECK / "src" / "index.src.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    slides = soup.select("section.slide")
    errors = []
    for n, s in enumerate(slides, 1):
        sid = f"{n} {s.get('data-title', '')}"
        frags = s.select(".frag")
        groups = []
        for f in frags:
            if f.find_parent(class_="notas"):
                continue
            v = f.get("data-f")
            if v is None or not v.isdigit() or int(v) < 1:
                errors.append(f"{sid}: .frag without explicit data-f -> {f.get_text(' ', strip=True)[:40]!r}")
                continue
            groups.append(int(v))
        m = max(groups) if groups else 0
        missing = sorted(set(range(1, m + 1)) - set(groups))
        if missing:
            errors.append(f"{sid}: fragment groups not contiguous, missing {missing}")
        notas = s.select_one(".notas")
        if notas is None:
            errors.append(f"{sid}: no .notas")
            continue
        pasos = notas.select("div.paso")
        idx = [p.get("data-paso") for p in pasos]
        if idx != [str(k) for k in range(m + 1)]:
            errors.append(f"{sid}: expected pasos 0..{m}, found {idx}")
        for p in pasos:
            k = int(p.get("data-paso", "-1"))
            ps = p.find_all("p", recursive=False)
            if k >= 1:
                if not ps or "cue" not in (ps[0].get("class") or []) or "aparece:" not in ps[0].get_text():
                    errors.append(f"{sid}: paso {k} must start with <p class=\"cue\">… aparece: …</p>")
            if not any(("cue" not in (q.get("class") or [])) for q in ps):
                errors.append(f"{sid}: paso {k} has no spoken text or stage direction")
        if n < len(slides) and pasos:
            last = pasos[-1]
            if not any("siguiente:" in c.get_text() for c in last.select("p.cue")):
                errors.append(f"{sid}: last paso needs a <p class=\"cue\">… siguiente: <title></p>")
    for e in errors:
        print(e)
    print(f"{len(slides)} slides, {len(errors)} violations")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
