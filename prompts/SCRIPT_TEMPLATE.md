> Archived toolkit reference. For portable commands and current policy, read [toolkit adaptations](../references/toolkit-adaptations.md) and SKILL.md.

# Script template

Purpose: write a narration script with every line locked to a fixed start time.
Requires: for a remake, the reference narration with word timestamps; for an original film, the storyboard timings.

Save the block below as `SCRIPT.md` in the film folder.

Rules:
1. Each line starts at the reference line's start time. The new words may be shorter or longer; the start time stays fixed, so the picture stays in sync. If a new line runs more than 8% longer than its slot, rewrite it shorter. Do not stretch the voice.
2. Write the truth rules before any line: what the product does, and what the film must never claim. Check every line against them.

```markdown
# [FILM NAME]: script ([remake of REF / original], [DURATION] s @ [FPS] fps)

## Product truth (source: [SITE / DOCS PAGE], checked [DATE])
[2–4 sentences: what the product does, for whom, how people use it, what it costs. Only facts with a source.]

## Direction
[1–3 sentences from the client: what to base the film on, what may be shown as "coming soon", what to change vs the reference.]

## Hard truth rules
- Never say or show [SOMETHING THE PRODUCT DOES NOT DO].
- No invented stats. Replace any number in the reference with a real, sourced one, or drop it.
- [Any legal/brand rule: no competitor names, nominative use of other platforms' logos only, etc.]

## Lines
Each line starts at the reference line's start time. On-screen captions follow the NEW words, laid out where the reference caption sits.

| # | start s | ref end s | Reference words | NEW narration | NEW on-screen text (*italics* = accent words) |
|---|---|---|---|---|---|
| 1 | 0.00 | 0.60 | Hm. | Hm. | (none) |
| 2 | 1.08 | 1.60 | Okay. | Okay. | (none) |
| 3 | 3.04 | 5.86 | [ref line] | [new line, similar length] | "[caption line 1]" / "*[accent words]*" |
| 4 | 9.74 | 10.90 | Be honest. | Be honest. | "Be honest" |
| … | | | | | |
| N | [t] | [t] | Try [OLD BRAND] now. | Try [NEW BRAND] free. | button "Try free" |

## Visual swaps (keep the reference's layout, size, motion and timing)
- [Reference surface, time range] → [new surface]. e.g. "Platform A feed (0–9 s) → Platform B home feed, same card positions".
- [Reference form/input] → [equivalent input].
- [Reference data table] → [new table: which columns, which sample rows].
- [Old logo / shards / wordmark] → [new mark as a mask / shards of it / new wordmark].
- Palette: [how colours map, e.g. "every warm colour becomes the blue family via PALETTE_SWAP; draw with the ref's colours and let it convert"].

## Voice
- TTS service + voice: [NAME, premade voice]. Key read from an env var, never printed.
- Pace target: [words per minute measured on the reference].
- Per-line generation with word timestamps → captions reveal on those timestamps.
```

## Steps

1. Get the reference words and timings from a speech-to-text service that returns word timestamps. Copy them into the first four columns unchanged.
2. Write the new narration line by line, with the reference line's length beside it. Count syllables, not words.
3. Keep the reference's rhythm words ("Hm.", "Okay.") when they fit. They carry the timing.
4. In the on-screen column, keep the reference's accent pattern (which words get the colour or the weight). Move the accent to the new key idea.
5. Read the finished table aloud against the muted reference video. Shorten any line that does not fit its slot.

## Check

- Every line has a start time equal to a reference line's start time.
- No line runs more than 8% past its slot.
- Every line passes the hard truth rules.
