# Prevent the failures that make a remake look cheap

## Text
Load and bundle fonts first. Set window.FONT_LOADS to the actual font specifications (for example ["700 64px BrandSans"]) so the page explicitly loads them before width tables are built. Measure the settled full phrase once. Reserve fixed word boxes and use a shared typographic baseline (flex align-items:baseline or explicit font metrics); do not center each word's ink independently. Lock the settled group center and line height. Animate transforms, not changing font size/line breaking. Rounding each trajectory frame causes stepping; retain subpixel coordinates. Holds must be stationary. Re-render the same frame after seeking elsewhere and require identical pixels on the same runtime.

## Motion blur
Measure the reference blur direction and extent. For real temporal blur, evaluate the deterministic scene at fractional shutter samples around F and average their pixels in linear-light space; clamp or segment at cuts so unrelated shots never bleed together. Use an explicit shutter and 5–9 samples initially, then validate against the reference. Directional SVG/CSS filters are approximations and must be labeled as such. Blur follows velocity; text settles sharp. Never stack arbitrary ghosts over a stationary title. The bundled renderer outputs single samples; a temporal compositor is an optional film helper, not claimed as built in.

## Native animated SVG and logos
Inspect the actual SVG viewBox, path bounds, animation definitions and transparent canvas. Remove an unwanted backing rectangle only when requested; do not redraw a supplied mascot as a spinning ellipse. Reuse its eyes, squash/stretch and expressions. For SMIL, pauseAnimations() and setCurrentTime(F/FPS); for CSS/WAAPI, pause every animation and set currentTime explicitly. Rebuilt DOM nodes must be sought again each frame. Do not let CSS play by wall clock. No outer rotateY unless present in the reference or requested. SVG loaded as img cannot expose its internal animation clock: inline it or pre-render a sought frame sequence.

Animate the actual logo paths with measured path lengths, stroke reveal then fill, a mask reveal, or its native animation. Keep the wordmark's real proportions and final bounding box. Treat a whole-logo scale as a separate measured motion, not as a substitute for logo animation.

## UI, video and composition
Reuse real app components/styles in an isolated film copy when supplied; never modify the user's product merely to make a promo. Mount the shell, panels, controls, timeline and preview on explicit frame keys. Use decoded local video frame sequences; index by the media time map, independent of playback. Keep panels in a measured grid with safe margins and a stable title zone. Final poses should be readable and coherent rather than tiny scattered screenshots. Speech bubbles need consistent padding, tails and hierarchy, no accidental overlaps.

CTA: align logo, phrase and button on one center axis; use measured width and shared baseline. Keep cursor tip separate from its visual bounds. A 3D cursor may use a real mesh or extruded SVG with consistent perspective/light/shadow; do not mislabel a flat drawing as a real 3D model. Seek click/press/release at specified frames. Inspect the final settled frame and the click transition.
