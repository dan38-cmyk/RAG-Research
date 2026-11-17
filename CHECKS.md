# Actual presentation checks

- Standalone build: passed using Python standard library; no dependency installation.
- Real Chromium: page served successfully; section navigation targets resolved; search returned a matching section and followed its anchor.
- Desktop (1280px) and narrow (390px) screenshots captured; narrow document overflow assertion passed. No JavaScript page errors observed.
- These checks exercise the research presentation only. No RAG import, embedding, retrieval, generation or hosting check has run.
- Independent source verification and actual peer feedback/response remain pending.

## GitHub Pages preparation

Static output moved to `docs/`; builder and local preview instructions updated. Rebuild passed. Live deployment remains pending repository Pages settings and GitHub publication.
