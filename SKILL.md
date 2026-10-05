---
name: remake-epic-motion-graphics
description: Recreate a reference motion graphics or SaaS promotional video frame by frame with brand, text, UI and mascot swaps. Use when asked to remake a video, match its cuts and motion, measure reference frames, add motion blur, animate SVG logos or validate a replica side by side. Includes a portable HTML/Chromium toolkit, analysis tools, templates and verification workflow.
---

# Remake Epic Motion Graphics

Reconstruct a video from measured frames. Deliver an editable deterministic scene, an encoded video, a synchronized comparison and an honest residual-difference report. Read [workflow](references/workflow.md), [quality](references/quality.md) and [runtime](references/runtime.md) before building. Read [original specification example](examples/GOJI_SPEC.md) for the measurement detail expected.

## Establish the contract

Resolve the reference video, new film directory, brand name, logo, palette, interface substitutions, faces/screens/video sources, final line, language and audio policy. Ask only for unresolved required values; never infer answers from placeholders. A swap may explicitly be `none`. Explain the difference between strict reconstruction (only specified swaps) and an adapted film (additional requested changes). Record each intentional deviation. Follow the user's accepted choices over templates.

Use `python scripts/bootstrap.py` once, then the virtual-environment Python listed in references/runtime.md. Run `scripts/remake.py doctor`. The agent needs filesystem, command execution and image/video inspection capabilities. Browser rendering may need a tool's sandbox escalation; follow that tool's actual policy. Never disable a sandbox globally.

## Phase 0 — measure before building

Initialize with `scripts/remake.py init --reference REF --output FILM --name NAME`. Edit FILM/film.json with the resolved swap contract. Run `analyze FILM`: probe geometry, rational FPS and timestamps; extract every frame and available audio; create contact sheets and proposed cuts. Verify the extracted frame count. VFR is rejected until the user chooses a documented constant-rate normalization and frame mapping.

Inspect every proposed cut and both neighboring frames. Correct measure/cuts.csv; detection is a proposal, never the truth. Build SPEC.md with continuous inclusive shot ranges covering every frame, measured component boxes and camera keys, verbatim text, fonts and sampled colors, cursor tracks/clicks, typing counts, audio timing and a list of unmeasured estimates. Use per-frame CSV columns `frame,x0,y0,x1,y1,cx,cy,w,h,scale` for major movement. Run `csv-to-js FILM` to emit plain-script globals; do not fetch CSV over file://. For narration use prompts/SCRIPT_TEMPLATE.md and genuine word timestamps from an available transcription tool; report unavailable transcription rather than inventing it.

Show the shot table and six representative comparison frames: opening, typing, camera movement, swapped UI, transition and end card. Respect an explicit approval gate before building. An existing approval remains valid for its scope.

## Phase 1 — deterministic engine

Use film/page.html, shots/_data.js, shots/_shared.js and shots/A.js through D.js. Register SHOT({id,f0,f1,render(lf,F)}). Each pose is a function of F, including video frame selection, SVG state, blur, cursor and particles. No wall-clock animation, unseeded randomness or autonomous video playback. `window.ready` requires loaded fonts and decoded assets. Missing assets and shot gaps are failures. Wait for per-frame asset decoding before screenshots.

Keep engine/core.js generic. Put film-specific helpers in shots/_shared.js. Bundle the actual reference fonts with their licenses; measure widths after they load. Read references/quality.md for stable baselines, temporal blur, native SVG animation, mounting UI components and CTA alignment. Preserve the reference's sharp holds and crisp whips; do not blur every frame.

## Phase 2 — build and inspect

Implement contiguous shot groups. If parallel agents are available and authorized, use up to four builders, each writing only shots/<group>.js; supply prompts/BUILDER_BRIEF_TEMPLATE.md, its SPEC sections, CSV tracks and core API. Otherwise build sequentially with the same boundaries. Shared helpers have one owner.

Render no more than 15 diagnostic frames per call. Inspect reference-left/render-right for each shot's first and last frame, keyframes and two frames into transitions. Iterate on measured errors. Record MATCHES only after inspection and quantitative checks; otherwise CLOSE, ROUGH or NOT CHECKED. Audio must follow the chosen supplied/licensed/replacement policy. Record source and license information; never claim rights were verified without evidence. Optional TTS/transcription providers are user-configured, not included dependencies.

## Phase 3 — integrate and deliver

Validate shot coverage, render all frames, then `verify FILM`. A clean full render refuses stale frames unless --replace-frames was explicitly selected. Encode with the reference's rational FPS; audio is padded/trimmed to the exact video length. Generate `sync FILM` and inspect contact sheets at each second and both sides of group seams. Scan old-brand hues using explicit measured bands and documented photo exclusions. Separate intentional palette changes from actual leftovers.

Report cuts (zero frame offset), geometry error (at most 1% of frame dimensions for strict mode), cursor/camera/typing timing and every unresolved difference. Software count checks do not certify a visual match. Deliver FILM.mp4, out/side-by-side.mp4, SPEC.md, measure/, source, SOURCES.md, SCRIPT.md if narrated, and `frame range | element | difference in pixels/frames | cause`. Never promise perfect reconstruction from a low-resolution or ambiguous reference.
