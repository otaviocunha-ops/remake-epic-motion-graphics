> Archived toolkit reference. For portable commands and current policy, read [toolkit adaptations](../references/toolkit-adaptations.md) and SKILL.md.

# Taste file, feedback log and critic agent

Purpose: keep the client's rules and notes across agent sessions, and review each render with a separate critic agent.
Requires: a film folder; `CRAFT.md` (critic rubric, section 4.2).

An agent keeps no memory between sessions. Three files carry the notes forward:

| File | Content | Writer |
|---|---|---|
| `TASTE.md` | Standing rules: likes, bans and pass criteria, as short trigger → action lines | The agent, from the client's notes. The client approves. |
| `FEEDBACK_LOG.md` | Every note, verbatim, with the date, the version it refers to, and the resulting change | The agent, after every round |
| Critic agent | A second agent that only reviews. It reads `TASTE.md` and the craft rules and judges each render against the reference films. | The client starts it. The builder never grades its own work. |

## Steps

1. Create `TASTE.md` and `FEEDBACK_LOG.md` in the film folder. For several films with one client, place them in the parent folder.
2. Send this as the builder's first message:
   ```text
   Read TASTE.md and FEEDBACK_LOG.md before anything else. After every note I give, append it verbatim to FEEDBACK_LOG.md and turn it into a TASTE.md rule.
   ```
   Result: each note appears in `FEEDBACK_LOG.md` and as a rule in `TASTE.md`.
3. Start the critic agent (section 3) after each render.

## 1. TASTE.md

Rules:
1. Write rules, not adjectives. "Only the hero object is saturated; everything else white/silver/cream" can be checked.
2. One rule per line: when X → do Y, plus its source (date, version).
3. Keep the file under 60 lines.
4. When two rules conflict, the newer rule wins. Delete the older rule. History stays in the feedback log.

Example:

```markdown
# TASTE: [NAME / BRAND]

## Look
- Only the hero object carries the accent colour. Everything else neutral. (2026-03-02, v3 note)
- No purple/indigo, no rainbow gradients.
- Fresh grain every frame; never a looping grain bank.

## Motion
- No static hold longer than 1.5 s except the final logo. Every shot pushes or cuts.
- Glitches only on a real cut, 1 to 2 frames, always with a click.

## Words
- Captions ≤ 7 words, one text layer at a time.
- The brand name appears only at the end.

## Process
- Show 6 stills before any full render.
- Name each render by what changed ("with-bridge"), not by number.
- Never restart an approved direction; build on the approved file.

## Approved references
- [FILM A]: cut rate and type.
- [FILM B]: hero-object lighting.
```

## 2. FEEDBACK_LOG.md

Rules:
1. Append only.
2. Record the client's exact words. A paraphrase drops wording such as "feels weird" or "that's the one".
3. Log approvals as well as complaints. An approved version is the floor; later versions do not drop below it.
4. Log the change made for each note, so each note can be traced to a change.

Example:

```markdown
# Feedback log

## 2026-03-02, render "with-bridge" (55.1 s)
> "the part where the narrator stops feels weird"
Change: added a bridge line between act 2 and act 3; the narrator no longer goes quiet between acts.
Rule added to TASTE.md: "Write a bridge line for every act change."

## 2026-03-03, render "button-macro"
> "that's the one. keep this."
Change: none. Marked as APPROVED. Later versions build on this file.
```

## 3. Critic agent

The builder knows what it intended to draw. The critic sees only the render. Start the critic as a second agent or a fresh Claude Code session with this prompt:

```text
You are a film critic with one job: state what is wrong with this render, with exact fixes.
Read first: TASTE.md, FEEDBACK_LOG.md, playbook/CRAFT.md (the rubric in section 4.2).
Anchor ONLY to these reference films: [PATHS]. Never to "what AI films usually look like".
Input: the 2 fps contact sheet [PATH] and stills [PATHS].
For every beat: KEEP / FIX / CUT, the reference frame it should match (file + time), what is wrong in plain words, and the exact fix (px, frames, dB).
Then: every TASTE.md rule it breaks, and a score out of 10.
Default stance: reject. Do not praise. Mark anything you could not see (motion between sampled frames, audio) as NOT CHECKED.
```

Loop: builder renders → critic reviews → builder applies the fixes → re-render → critic again. Repeat until the critic scores ≥ 9/10 and no taste rule is broken. Then show the render to the client.

Example verdict:

```text
Beat 3 (8 to 17 s, the past): FIX
Ref: film A @ 0:12, counter changes every frame, tabular numerals.
Render: counter steps every 3 frames (f201, f204, f207).
Fix: drive it from the global clock, new value every frame; font-variant-numeric: tabular-nums.

Beat 5 (30 s, hero reveal): KEEP
Beat 7 (end card): FIX
Breaks TASTE "only the hero object carries the accent colour": URL is in the accent colour. Fix: white, 60% opacity.

Score: 7/10. NOT CHECKED: audio sync (contact sheet only).
```

## Check

- `TASTE.md` exists, is under 60 lines, and every rule names its source.
- `FEEDBACK_LOG.md` has one entry per round of notes, including approvals.
- Each critic report has a score, a KEEP / FIX / CUT per beat, and a NOT CHECKED list.
