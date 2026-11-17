"""Build the static research reader from the two Review 1 sections in SPEC.md."""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "site"


def inline(value):
    """Render the limited inline Markdown used by the planning record safely."""
    value = html.escape(value)
    value = re.sub(
        r"\[([^\]]+)\]\((https://[^\s)]+)\)",
        r'<a href="\2">\1</a>',
        value,
    )
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)


def slug(value):
    """Return a predictable anchor for section navigation."""
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def render(source):
    """Render headings, paragraphs, lists and tables; return content and outline."""
    lines = source.strip().splitlines()
    blocks, outline = [], []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("#### "):
            title = line[5:]
            anchor = slug(title)
            outline.append((anchor, title))
            blocks.append(f'<h2 id="{anchor}">{inline(title)}</h2>')
        elif line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = lines[index].strip().strip("|").split("|")
                if not all(re.fullmatch(r"\s*:?-+:?\s*", cell) for cell in cells):
                    rows.append(cells)
                index += 1
            table = []
            for row_index, cells in enumerate(rows):
                tag = "th" if row_index == 0 else "td"
                scope = ' scope="col"' if row_index == 0 else ""
                table.append("<tr>" + "".join(
                    f"<{tag}{scope}>{inline(cell.strip())}</{tag}>" for cell in cells
                ) + "</tr>")
            blocks.append('<div class="table-scroll" tabindex="0" role="region" '
                          'aria-label="Research comparison table"><table><thead>'
                          + table[0] + "</thead><tbody>" + "".join(table[1:])
                          + "</tbody></table></div>")
            continue
        elif line.startswith("- ") or re.match(r"\d+\. ", line):
            ordered = bool(re.match(r"\d+\. ", line))
            tag = "ol" if ordered else "ul"
            pattern = r"^\d+\. " if ordered else r"^- "
            items = []
            while index < len(lines) and re.match(pattern, lines[index].strip()):
                items.append("<li>" + inline(re.sub(pattern, "", lines[index].strip())) + "</li>")
                index += 1
            blocks.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        else:
            blocks.append("<p>" + inline(line) + "</p>")
        index += 1
    return "\n".join(blocks), outline


def build():
    """Render this repository's canonical research record into its static site."""
    import json
    config = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    source = (ROOT / "RESEARCH.md").read_text(encoding="utf-8").split("\n", 1)[1]
    content, outline = render(source)
    nav = "".join(f'<a href="#{anchor}">{html.escape(title)}</a>' for anchor, title in outline)
    repository = config["repository"]
    title = html.escape(config["title"])
    document = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · Daniel Nizami</title><link rel="stylesheet" href="research.css"><script src="research.js" defer></script></head>
<body><a class="skip" href="#content">Skip to research</a><header><a class="identity" href="index.html"><span class="monogram">DN</span>Daniel Nizami <span class="identity-label">/ Research</span></a><a href="{repository}">GitHub ↗</a></header>
<div class="layout"><aside><p class="nav-label">REVIEW 1 / PLAN</p><nav aria-label="Research sections">{nav}</nav><label for="research-search">Find a section</label><input id="research-search" type="search" placeholder="Search section titles"><div id="search-results" aria-live="polite"></div><p class="sidebar-note">Standalone research record. Peer feedback pending.</p></aside>
<main id="content"><div class="page-heading"><p class="eyebrow">DANIEL NIZAMI / IS373</p><h1>{title}</h1><p class="status">Reviewed plan · Peer feedback pending</p></div><article>{content}</article><footer>AI-assisted research and drafting. <a href="{repository}/blob/main/RESEARCH.md">Source record</a> · <a href="{repository}/blob/main/LEARNING.md">Contributions and assistance</a><p>Proposed behavior is not an executed test. No hosted RAG application is claimed.</p></footer></main><nav class="toc" aria-label="On this page"><p class="nav-label">ON THIS PAGE</p>{nav}</nav></div></body></html>'''
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "index.html").write_text(document, encoding="utf-8")
    (OUTPUT / "search-index.json").write_text(json.dumps([{"title": title, "url": f"index.html#{anchor}"} for anchor, title in outline]), encoding="utf-8")
    print("Built standalone research site.")

if __name__ == "__main__":
    build()
