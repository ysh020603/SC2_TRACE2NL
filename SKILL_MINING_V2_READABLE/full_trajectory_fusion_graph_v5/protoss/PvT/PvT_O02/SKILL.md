# PvT_O02 Technology / Economy / Production

## Skill Identity

- Skill ID: PvT_O02
- Matchup: Protoss vs Terran
- Opening Family: technology / economy / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A flexible Protoss opening that prioritizes technology and economy while keeping production options open. Early game is characterized by light or uncertain information, with a gradual shift toward a ground-oriented army and heavier production as the game progresses.

Develop a technology / economy / production posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

## Strategic Characteristics

- Economy: light_or_uncertain
- Production: light_or_uncertain
- Technology: moderate
- Army direction: ground-leaning

## Strategic Priorities

- Preserve the opening's strategic identity without reproducing a fixed sequence.
- Check current Completed, Under Construction, Active Queues, resources, supply, and prerequisites before choosing exact macro actions.
- Match any adaptation against partial Enemy Intelligence and current Threat Flags.
- Re-evaluate economy, production, technology, and army trade-offs at every decision.

## V5 Human-Trajectory / Runtime Bridge

- The phase policy below supplies the strategic target distilled from aggregate trajectory states; it is not an action sequence.
- The live router supplies exactly one current execution bottleneck. Resolve it without replacing the phase target with a generic macro rule.
- For Protoss, spend through completed powered compatible producers before adding capacity; preserve opening tempo and never force a new facility solely from a clock threshold.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Early Game Development with Safety Checks:** Develop economy and tech while maintaining defense; if Reaper is seen, prioritize defense and stabilize.
- **early_midgame — Early-Midgame Development with Safety Checks:** Balanced development with safety checks; if ground cues appear, strengthen defense and stabilize before advancing.
- **midgame — Midgame Development with Safety Checks:** Continue balanced growth; if ground cues are present, prioritize defense and ground strength.
- **late_midgame — Late-Midgame Development with Safety Checks:** Maintain balanced development with strong ground defense; if drop threats are present, reinforce defense.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Stabilize before pushing

**When:** Early-midgame, around 240 seconds, with heavy defense and moderate economy, while the opponent shows a ground posture with Marine cues.

**Mistake → correction:** Over-committing to offense before your defense is solid, potentially leaving you vulnerable to a ground attack. → Increase economy and technology. Strengthen ground forces. Increase defense. Maintain expansion. Continue production.

**Why:** The opponent's ground posture suggests a potential ground attack. Stabilizing your defense while developing your economy and tech is prudent.

**Read for full checks:** `N008`

### L02 — Balanced development under uncertainty

**When:** Early-midgame, around 300-360 seconds, with heavy defense and moderate economy, while the opponent's posture is unknown.

**Mistake → correction:** Over-committing to offense before your defense is solid, risking vulnerability when the opponent's intentions are unclear. → Increase economy and technology. Strengthen ground forces. Increase defense. Maintain expansion. Continue production.

**Why:** With limited information, balanced development keeps options open. Strengthening ground forces provides a solid base for any transition.

**Read for full checks:** `N011`

### L03 — Maintain ground defense against drops

**When:** Late-midgame, around 600 seconds, with heavy economy and production, while the opponent shows a ground posture with SiegeTank, Reaper, Thor, and Medivac.

**Mistake → correction:** Neglecting ground defense, leaving you vulnerable to drops or flanking maneuvers. → Increase economy, production, and technology. Strengthen ground forces. Maintain defense and expansion. Continue air development.

**Why:** The opponent's ground posture suggests a potential ground attack. Strengthening ground forces and maintaining defense is prudent while continuing development.

**Read for full checks:** `N010`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
