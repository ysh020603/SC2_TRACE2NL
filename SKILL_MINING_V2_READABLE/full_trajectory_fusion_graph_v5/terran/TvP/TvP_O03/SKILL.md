# TvP_O03 Technology / Economy / Production

## Skill Identity

- Skill ID: TvP_O03
- Matchup: Terran vs Protoss
- Opening Family: technology / economy / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Terran opening that emphasizes heavy economy and technology investment while keeping production moderate, aiming for a flexible transition into either a ground or air-oriented midgame based on scouting.

Develop a technology / economy / production posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

## Strategic Characteristics

- Economy: heavy
- Production: moderate
- Technology: heavy
- Army direction: ground-leaning

## Strategic Priorities

- Preserve the opening's strategic identity without reproducing a fixed sequence.
- Check current Completed, Under Construction, Active Queues, resources, supply, and prerequisites before choosing exact macro actions.
- Match any adaptation against partial Enemy Intelligence and current Threat Flags.
- Re-evaluate economy, production, technology, and army trade-offs at every decision.

## V5 Human-Trajectory / Runtime Bridge

- The phase policy below supplies the strategic target distilled from aggregate trajectory states; it is not an action sequence.
- The live router supplies exactly one current execution bottleneck. Resolve it without replacing the phase target with a generic macro rule.
- For Terran, use completed parents before scaling capacity, and order parent before add-on or dependent work; persistent bank plus low army favors executable unit throughput.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Early Tech/Eco Development:** Prioritize economy and tech, expand, and keep production moderate; scout with Reaper if available.
- **early_midgame — Early-Midgame Ground Macro:** Maintain ground army strength, keep expanding, and continue tech; adapt if opponent shows air or Colossus.
- **midgame — Midgame Ground Army with Siege Tanks:** Strengthen ground army, keep economy and production; add Siege Tanks or transition to air based on scouting.
- **late_midgame — Late-Midgame Ground Army with Anti-Air:** Maintain ground army, add Vikings for Colossus, and keep economy and production; adapt to late-game tech.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid overcommitting to a single attack

**When:** Midgame with a ground-oriented army, heavy production and technology, and moderate defense.

**Mistake → correction:** Committing to a single attack without sufficient army strength, risking a counterattack while the opponent is also building up. → Continue strengthening your ground army and maintain economy and production. Consider adding more Siege Tanks or transitioning to air if the opponent goes for Colossus or air units.

**Why:** Siege Tanks provide strong defensive and offensive capabilities against ground armies. Maintaining a heavy economy allows you to tech switch if needed.

**Read for full checks:** `N003`

### L02 — Avoid engaging without proper positioning

**When:** Midgame with a ground-oriented army, heavy production and technology, and moderate defense.

**Mistake → correction:** Engaging in a straight-up fight without proper positioning, as the opponent's army is powerful. → Continue strengthening your ground army and maintain economy and production. Consider adding more Siege Tanks or transitioning to air if the opponent goes for Colossus or air units.

**Why:** Siege Tanks provide strong defensive and offensive capabilities against ground armies. Maintaining a heavy economy allows you to tech switch if needed.

**Read for full checks:** `N005`

### L03 — Avoid neglecting ground defense during air transition

**When:** Midgame with a ground-oriented army transitioning to air, with moderate air presence and Banshees.

**Mistake → correction:** Neglecting ground defense while focusing on air, as the opponent could still push with a strong ground army. → Increase your air presence and strengthen your air army. Continue developing your economy and technology to support the transition.

**Why:** Transitioning to air can give you an advantage if the opponent is heavily ground-based. Banshees can harass and provide mobility.

**Read for full checks:** `N006`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
