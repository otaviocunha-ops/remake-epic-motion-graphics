# Sources — pyramids sting audio

## Music
- **Track:** "Rising Forest" by Diego Nava (Mixkit ID 471, genre House, 1:39)
- **File:** https://assets.mixkit.co/music/471/471.mp3 → `src/mixkit-rising-forest-471.mp3`
  (sha256 `4c2ebb1c5e7e9271eceb11ea13c7dbea64f207daefcc6cc12040b5f32f0cff1a`, downloaded 2026-09-27)
- **Listed on:** https://mixkit.co/free-stock-music/tag/corporate/. The page's own schema.org record for this track says
  `"copyrightNotice":"Mixkit Stock Music Free License"`, `"license":"https://mixkit.co/license/#musicFree"`, `"isAccessibleForFree":true`
- **License:** Mixkit Stock Music Free License, https://mixkit.co/license/#musicFree. It allows free use in commercial and personal
  video projects with no attribution required. (This is the same license the x3d and lordy remakes used.) The track may not be
  redistributed on its own as a music file.
- **Edit:** one continuous 12.075 s excerpt, source 44.0–56.1 s. It is time-stretched by ×0.999936 (124.008 → 124.000 BPM)
  with ffmpeg `atempo`, and there are no splices. See `build_music.py`.

## Reference
- `../ref/audio.wav` was used **only to measure timing**. The beat grid, drop and cut times come from `../AUDIO.md` and `../BEATS.md`.
  None of its audio is in `music.wav` or `mix.wav`.

## SFX
- All sound effects are synthesized in numpy by `sfx.py` with fixed seeds, and nothing is downloaded. The helpers are copied
  from `../../x3d/audio/sfx.py`.
