# ZvT_O04 Economy / Upgrade / Expansion

## Skill Identity

- Skill ID: ZvT_O04
- Matchup: Zerg vs Terran
- Opening Family: economy / upgrade / expansion opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg opening focused on heavy economy, upgrades, and expansion while maintaining a ground-oriented army. The strategy emphasizes macro development with safety checks, adapting to Terran ground compositions.

Develop a strong economy and tech base while expanding, keeping flexibility to respond to Terran pressure or transitions.

This is a strategic template, not a fixed build order. Adapt based on live observations.

## Strategic Characteristics

- Economy: heavy
- Production: moderate
- Technology: light_or_uncertain
- Army direction: ground-leaning

## Strategic Priorities

- Preserve the opening's strategic identity without reproducing a fixed sequence.
- Check current Completed, Under Construction, Active Queues, resources, supply, and prerequisites before choosing exact macro actions.
- Match any adaptation against partial Enemy Intelligence and current Threat Flags.
- Re-evaluate economy, production, technology, and army trade-offs at every decision.

## V5 Human-Trajectory / Runtime Bridge

- The phase policy below supplies the strategic target distilled from aggregate trajectory states; it is not an action sequence.
- The live router supplies exactly one current execution bottleneck. Resolve it without replacing the phase target with a generic macro rule.
- For Zerg, production capacity is bases plus larva/inject throughput; Overlords and Drones consume the same larva as army, so do not translate facility-count rules from other races.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Early Game Development:** Develop economy and expansion, strengthen ground, continue tech with safety checks.
- **early_midgame — Early-Midgame Ground Focus:** Strengthen ground, maintain economy, continue tech with safety checks.
- **midgame — Midgame Ground Defense:** Maintain ground, continue economy, increase tech.
- **late_midgame — Late-Midgame Ground and Air:** Maintain ground, continue economy, increase tech, consider air.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Balance economy and safety in early game

**When:** Early game, opponent posture unknown, own ground-oriented with Queens.

**Mistake → correction:** Overcommitting to army before economy is stable. → Maintain economy and expansion, strengthen ground, continue tech, develop with safety checks.

**Why:** Establish a solid economic and tech foundation while staying safe against early pressure.

**Read for full checks:** `N001`

### L02 — Tech up to counter Terran ground threats

**When:** Early-midgame, opponent ground with Marines, Reapers, Hellions, own ground with Zerglings, Queens, moderate tech.

**Mistake → correction:** Falling behind in army strength while teching. → Continue economy, increase tech, strengthen ground.

**Why:** Tech up to handle Terran ground threats.

**Read for full checks:** `N008`

### L03 — Use Mutalisks for harassment and map control

**When:** Midgame, opponent ground with Marines, Ghosts, Hellions, Medivacs, own ground with Zerglings, Mutalisks, Queens, Overseers.

**Mistake → correction:** Overcommitting to air without ground support. → Increase air, strengthen air, continue economy, increase upgrades.

**Why:** Use Mutalisks for harassment and map control.

**Read for full checks:** `N011`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
