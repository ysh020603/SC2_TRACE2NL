# ZvP_O05 Economy / Expansion / Defense

## Skill Identity

- Skill ID: ZvP_O05
- Matchup: Zerg vs Protoss
- Opening Family: economy / expansion / defense opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg opening focused on economy, expansion, and defense, with a ground-leaning army and moderate production. Technology investment is light or uncertain early, but can develop later.

Develop a strong economy and defensive posture while maintaining flexibility to adapt to Protoss tech choices.

This is a strategic template, not a fixed build order.

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

- **early_game — Early Game Queen Focus:** Prioritize economy and expansions, maintain ground forces, and keep scouting for opponent's tech.
- **early_midgame — Early Midgame Ground Development:** Focus on economy and ground army, increase production and expansions, and scout for opponent's tech.
- **midgame — Midgame Ground Defense with Anti-Air Consideration:** Maintain ground army, keep economy stable, and prepare anti-air if needed.
- **late_midgame — Late Midgame Infestor Tech:** Maintain ground army, continue economy, and consider upgrades while scouting for air transitions.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid tech overcommitment without scouting

**When:** Early midgame, own ground army with Zerglings, opponent unknown but heavy tech.

**Mistake → correction:** Over-committing to a specific tech path or army composition without more information, neglecting scouting or defensive positioning. → Continue developing economy and ground forces, increase production and expansions.

**Why:** Maintain economic lead while preparing for potential tech switches.

**Read for full checks:** `N001`

### L02 — Avoid neglecting scouting and over-investing in tech

**When:** Early game, own Queen, opponent unknown but heavy tech.

**Mistake → correction:** Neglecting scouting and over-investing in tech before confirming the opponent's plan. → Increase economy and expansions, continue ground development.

**Why:** Queens provide defense and creep spread, supporting a macro-oriented start.

**Read for full checks:** `N002`

### L03 — Avoid over-committing to Infestors without scouting for air

**When:** Late midgame, own Zergling/Infestor/Queen/Overseer, opponent ground with Zealots/Stalkers.

**Mistake → correction:** Over-committing to Infestors if the opponent transitions to air, and neglecting scouting to detect tech switches. → Maintain ground army, continue economy, consider upgrades.

**Why:** Infestors provide strong spellcasting against ground-based Protoss armies.

**Read for full checks:** `N005`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
