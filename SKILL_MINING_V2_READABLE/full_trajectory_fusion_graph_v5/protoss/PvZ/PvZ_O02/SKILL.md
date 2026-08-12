# PvZ_O02 Technology / Economy / Production

## Skill Identity

- Skill ID: PvZ_O02
- Matchup: Protoss vs Zerg
- Opening Family: technology / economy / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A flexible Protoss opening that prioritizes technology and economy while keeping production options open. Early game is uncertain, with the potential to transition into a ground-based army or continue teching depending on scouting.

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

- **early_game — Maintain Flexibility with Ground Defense:** Maintain flexibility, prioritize scouting, and if ground cues appear, bolster ground forces and defense while continuing tech and economy.
- **early_midgame — Continue Development with Ground Focus:** Maintain development, adapt to ground cues by strengthening ground forces and continuing production and tech.
- **midgame — Maintain Flexibility with Ground Reinforcement:** Maintain flexibility, reinforce ground forces if ground cues appear, and continue balanced development.
- **late_midgame — Maintain Flexibility with Ground Strength:** Maintain flexibility, strengthen ground forces if ground cues appear, and continue balanced development.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground: Avoid Overcommitting to Tech

**When:** Early-midgame, opponent shows ground posture with Zergling and Queen cues; your own ground posture with Zealot and Stalker cues.

**Mistake → correction:** Tempting to over-invest in technology while neglecting army size, risking falling behind in army strength. → Strengthen ground forces, continue production and technology development, and maintain economy.

**Why:** Both sides ground-oriented, so a strong ground army and tech advantage are key to gaining an edge.

**Read for full checks:** `N007`

### L02 — Ground vs Ground: Avoid Tech Switch Surprise

**When:** Late-midgame, opponent shows ground posture with Queen cues; your own ground posture with Zealot, Stalker, Sentry, and Observer cues.

**Mistake → correction:** Tempting to focus solely on ground army and ignore potential tech switch or large attack, risking being caught off guard. → Strengthen ground forces, continue production and technology development, and maintain economy.

**Why:** Both sides ground-oriented, so a strong ground army and tech advantage are key to gaining an edge.

**Read for full checks:** `N010`

### L03 — Ground vs Ground: Avoid Neglecting Economy

**When:** Midgame, opponent shows ground posture with Queen cues; your own ground posture with Zealot cues.

**Mistake → correction:** Tempting to over-invest in army and tech while neglecting economy, risking being caught off guard by a tech switch or large attack. → Strengthen ground forces, increase production and technology, and maintain economy.

**Why:** Opponent's ground posture suggests potential pressure. Investing in economy and tech while maintaining production provides a solid foundation.

**Read for full checks:** `N011`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
