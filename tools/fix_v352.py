#!/usr/bin/env python3
"""Repair publication metadata and the latest automatically generated eBook."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "notizie" / "borse-asiatiche-sell-off-titoli-intelligenza-artificiale-14-settembre-2026.html"
EBOOK = ROOT / "biblioteca" / "vita-relazioni" / "domande-per-conoscersi" / "quale-abitudine-difendi-come-parte-del-tuo-carattere-anche-se-ormai-limita-la-persona-che-potresti-diventare" / "index.html"
OLD = '"datePublished":"2026-09-14T06:00:00+02:00","dateModified":"2026-09-14T06:00:00+02:00"'
NEW = '"datePublished":"2026-09-14T06:51:05+02:00","dateModified":"2026-09-14T06:51:05+02:00"'


def main() -> None:
    text = ARTICLE.read_text(encoding="utf-8")
    if NEW in text:
        print("Metadati già corretti")
    else:
        if text.count(OLD) != 1:
            raise SystemExit("Coppia di metadati attesa non trovata in modo univoco")
        ARTICLE.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
        print("Metadati di pubblicazione corretti")

    ebook = EBOOK.read_text(encoding="utf-8")
    title = "L&#x27;abitudine che trattieni: identità, limite e tregua"
    old_first = '<section class="cm-book-page" data-book-page>'
    new_first = f'<section class="cm-book-page is-active" data-book-page><h1>{title}</h1>'
    if "<h1" not in ebook:
        if ebook.count(old_first) < 1:
            raise SystemExit("Prima pagina eBook non trovata")
        ebook = ebook.replace(old_first, new_first, 1)
        remaining = ebook.split("</section>", 1)[1]
        remaining = remaining.replace(old_first, '<section class="cm-book-page" data-book-page aria-hidden="true">')
        ebook = ebook.split("</section>", 1)[0] + "</section>" + remaining
        EBOOK.write_text(ebook, encoding="utf-8")
        print("Gerarchia e accessibilità eBook corrette")
    else:
        print("eBook già corretto")


if __name__ == "__main__":
    main()
