# Validation evidence

Executed on macOS, 2026-10-05, Node 24.16.0, Python 3.14.5, NumPy 2.3.5, Pillow 11.3.0, FFmpeg/ffprobe 8.1.2 and Playwright 1.63.0 Chromium.

- Agent Skills frontmatter validator: PASS.
- Three unit tests: inclusive shot coverage; gap/overlap/duplicate/missing-end rejection; independent scaffold in a path with spaces and overwrite refusal.
- End-to-end smoke: generated an original 640×360/30 FPS/60-frame reference with synthesized audio; extracted all frames; proposed cuts and contact sheets; rendered six diagnostic frames and all 60 frames; verified complete coverage and dimensions; encoded the replica and reference-left/render-right comparison.
- ffprobe confirmed output geometry, 60 frames and 30/1 FPS for both videos.
- Repeated seek after visiting other frames produced identical PNG bytes on this runtime.
- Extra stale frame blocked verification/export.
- Offline skill installer copied to an independent temporary directory without node_modules/.venv/films and without overwriting an existing installation.
- Repository scan: no user-specific absolute filesystem paths or credentials in distributed source. Original upstream engine is preserved with SHA256 provenance.

The smoke verifies execution and timing structure, not a quantitative visual identity claim. Demo PIL/Chromium edge rasterization differs slightly. GitHub Actions subsequently passed the complete unit + smoke matrix on macos-latest, ubuntu-latest and windows-latest using Node 22 and Python 3.11. Run: https://github.com/psiotavio/remake-epic-motion-graphics/actions/runs/37345318374 (tested commit 8cc0d87). All three jobs succeeded in the 1m 42s run. Docker was not built here. Licensed custom fonts, TTS, transcription and external commercial music services are not part of this smoke.
