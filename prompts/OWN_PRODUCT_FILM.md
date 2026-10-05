> Archived toolkit reference. For portable commands and current policy, read [toolkit adaptations](../references/toolkit-adaptations.md) and SKILL.md.

# Your own product film

A launch piece for your own product, no reference video needed. Paste the block below into Claude Code from the kit folder and answer its questions.

```text
TASK: a [LENGTH]-second video for my product, built in a film folder called [FILM] next to example-monkey/. No reference video: the structure comes from my answers.
ASK ME FIRST for anything still in brackets:
Promoting: [WHAT THE PRODUCT IS]. Who cares: [WHO IS WATCHING]. Feeling: [2 OR 3 FEELINGS]. Message: [ONE SENTENCE YOU COULD SHOW HAPPENING]. Look: [3 TO 5 STYLE WORDS]. Size: [1920x1080, 1080x1080 or 1080x1920]. Brand: my logo at [PATH], my font [FONT], my colours [HEX LIST, or derive from my screenshots]. Product: the screenshots I pasted or pointed you to (and a screen recording if I have one). Music: [TRACK URL, or find one with a free commercial licence]. Voiceover: [none, my own recordings, or a TTS service].

STEP 1, MOMENTS: propose a table of 4 to 6 moments (problem, turn, product, proof, promise is the default shape) with a start and end time each, adding up to the length, and one sentence per moment saying what you see. Moments with words get enough time to read them out loud twice. Wait for my go.
STEP 2, PRODUCT: rebuild my product's main screens from the screenshots as HTML in [FILM]/shots/ui.js, each card, row, button and number its own element, colours sampled from the pixels. Show me a still of each rebuild next to its screenshot with every difference in px. Wait for my go.
STEP 3, SHOTS: for each moment, write an eight-line shot brief (SUBJECT, LAYOUT, TYPE, COLOUR, MOTION, TIMING, REFERENCE, CONSTRAINTS) and show it to me. Then build it as a SHOT block with its own frame range in the one page, [FILM]/page.html, copied from engine/page.html. Render stills of its first, middle and last frame (outside the sandbox), describe each in one sentence, and wait for my notes. Apply one note at a time and tell me if anything else changed.
STEP 4, MUSIC: measure the track's BPM and drop, stretch it to an exact BPM, put the drop on the first frame of the product moment, and move every cut to 0 to 2 frames before a beat. Sound effects made in code: whooshes peaking on cuts, clicks on presses. Voiceover lines placed at the start of their moments, music down 18 dB under the voice. Master to -14 LUFS, true peak at or below -1 dBTP. Record the track's URL and licence in [FILM]/audio/SOURCES.md.
STEP 5, FINISH: full render, encode to [FILM].mp4 with ../engine/encode.py, then a contact sheet with one still per second. Tell me what you checked and what you could not check.

RULES (from playbook/CRAFT.md): every entrance eases out at 12 to 19% of the remaining distance per frame; every shot enters already moving and leaves on an accelerating move or a blur ramp; no crossfades (blur-dissolve or whip instead); blur follows speed and direction; groups enter staggered 2 frames apart; pops overshoot once by about 2.5%; nothing still for more than 1.5 s; readable text sharp and still for at least 8 frames; at most 7 words on screen; one small colour world with one accent; no fake UI or grey placeholder cards; measure text only after fonts load.
BUILD: everything is drawn from the frame number (no timers, no CSS transitions, no Math.random). Read TASTE.md first if it exists, and turn every note I give into a TASTE.md rule.
```
