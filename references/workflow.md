# Measurement and acceptance

Ranges are zero-based and inclusive. Record rational FPS, total frames, duration, source hash, source timestamps and extraction command. The probe and extraction must agree; a file without declared nb_frames is counted by ffprobe. Never silently change resolution, frame rate, rotation or aspect ratio. The CLI rejects variable frame spacing and rotation metadata; normalize deliberately and keep both the original and mapped reference.

For each major element, use a threshold against sampled background, seeded flood fill or settled-frame template matching. Record the method, seed/crop, confidence and occlusion handling. Keep raw samples. A smoothed curve may remove detector noise only after it has been checked against reference pixels; never smooth away an intentional impact or overshoot. Use exact cut anchors and declared hold frames.

SPEC.md: geometry/FPS/count/duration; shot table; per-shot measurements; repeated-component inventory; text and typing timing; font cap height/weight/tracking; color sample frame/pixel; cursor glyph/tip/click curve; camera; blur; audio onset/beat phase/BPM/drop/stops/loudness; narration words and timestamps; estimates; swap-induced deviations. Analyze ambiguous audio onsets with waveform/spectrogram and ears; BPM autocorrelation is an estimate until confirmed. The toolkit does not contain speech recognition or a TTS service.

Compare positions against width/height separately. For 1920×1080, 1% is 19.2 px horizontally and 10.8 px vertically; it is not a universal 19.2 px tolerance. Cut/typing/cursor frame tolerances are zero unless the accepted contract says otherwise. Compare whole pose, not just attractive stills. All rows need evidence and status; missing evidence is NOT CHECKED.

Adaptation requests (speech bubbles instead of cards, new mascot motion, animated logo, new UI sequence) override strict visual identity only for those elements. Put them in the exception table, never hide them in an accuracy score.

Audio: keep the reference as analysis material. Choose supplied audio, licensed commercial replacement, original synthesis or silence according to the user. Set narration slots to reference line starts and measure any time stretch (target ≤8% where requested), duck under voice, measure integrated loudness/true peak. FFmpeg encode padding does not certify a -14 LUFS/-1 dBTP mix; use FFmpeg loudnorm two-pass or a measured equivalent. Preserve source terms in SOURCES.md.
