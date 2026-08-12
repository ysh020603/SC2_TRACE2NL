# PvP_O02 Technology / Economy / Production

## Skill Identity

- Skill ID: PvP_O02
- Matchup: Protoss vs Protoss
- Opening Family: technology / economy / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Protoss versus Protoss opening that emphasizes technology and economy development while keeping production flexible. Early game is marked by uncertainty in both armies, with a gradual shift toward heavier ground compositions and tech as the game progresses.

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

- **early_game — Early Game Development with Safety Checks:** Develop economy and tech with flexible production, maintaining safety checks.
- **early_midgame — Early Midgame Development with Safety Checks:** Continue economy and tech development, with flexible production and ground defense if needed.
- **midgame — Midgame Development with Safety Checks:** Develop economy and tech with defensive posture, adapting army composition to opponent's cues.
- **late_midgame — Late Midgame Development with Safety Checks:** Continue economy and tech development with defensive posture, preparing for potential large-scale engagement.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground Defense Priority

**When:** Early midgame, opponent has ground posture with Zealots, heavy economy, moderate production. You have moderate economy and heavy tech.

**Mistake → correction:** Overcommitting to air units or neglecting scouting, assuming the opponent lacks anti-air. → Strengthen your ground army and continue developing economy and technology. Maintain a defensive posture while preparing for a potential ground engagement.

**Why:** The opponent's ground posture suggests a Zealot-heavy army. Ground forces and tech advantage counter their composition.

**Read for full checks:** `N006`

### L02 — Balanced Ground and Tech

**When:** Late midgame, both you and opponent have ground posture with Zealots, Stalkers, Immortals. Both economies and production are heavy.

**Mistake → correction:** Neglecting air defense or overextending economy without adequate defense. → Continue to strengthen your ground army and develop economy and technology. Maintain a defensive posture while preparing for a potential large-scale engagement.

**Why:** Both sides have similar ground compositions. Continuing economy and tech development gives an advantage in upgrades or army size.

**Read for full checks:** `N008`

### L03 — Macro Defense with Unknown Composition

**When:** Early midgame, opponent has heavy economy and expansion, moderate production. You have moderate economy and heavy tech, with heavy expansion.

**Mistake → correction:** Overextending economy without adequate defense or neglecting scouting due to unknown composition. → Strengthen your ground army and continue to develop economy and technology. Maintain a defensive posture while preparing for a potential ground engagement.

**Why:** The opponent's heavy economy suggests a macro-oriented game. Ground forces and tech advantage counter their eventual army.

**Read for full checks:** `N009`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
