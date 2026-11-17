# Data analyst learning assistant — Daniel Nizami

Standalone Review 1 Plan record. This is my individual work, separate from the group content system and from the portfolio application.

- **[Read the research](RESEARCH.md)**: sources, comparisons, decisions and changed/checked/next.
- **[Contributions and AI assistance](LEARNING.md)**.
- **[Checks and limitations](CHECKS.md)**.
- **[Peer review](PEER-REVIEW.md)** — real feedback/response pending.

## Browse the research website locally

Python 3.12+; no Node or extra packages required:

```sh
python build.py
python -m http.server 8010 --directory docs
```

Open http://localhost:8010. Stop with Ctrl+C. Use port 8011 for a second site running at the same time.
The `docs/` output is ready for GitHub Pages. Enable **Settings → Pages → Deploy from a branch → main → /docs → Save**.

Expected address after successful publication: https://dan38-cmyk.github.io/RAG-Research/
This address is not verified live until Pages is enabled and deployment completes.
On GitHub, read RESEARCH.md directly; HTML files display as source.

## State

The written plan was reviewed by Daniel. Peer feedback, independent source verification and final submission remain pending. Models and hosting constraints in the RAG plan are proposals, not implemented behavior. See the source record for specific boundaries.
