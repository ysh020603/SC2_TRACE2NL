# ZvT_O02 Economy / Expansion / Ground

## Skill Identity

- Skill ID: ZvT_O02
- Matchup: Zerg vs Terran
- Opening Family: economy / expansion / ground opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

This opening focuses on developing a strong economy and expanding while maintaining a ground-oriented army. Early information about the opponent is limited, so the plan emphasizes flexibility and safety checks.

Develop a economy / expansion / ground posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

## Strategic Characteristics

- Economy: light_or_uncertain
- Production: light_or_uncertain
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

- **early_game — Early Game Development:** Develop economy and expand with safety checks, keeping options open.
- **early_midgame — Early-Midgame Development:** Maintain economy and expansion, with a branch to strengthen ground army if opponent shows heavy ground.
- **midgame — Midgame Development:** Maintain economy and expansion, with a branch to strengthen ground army if opponent shows heavy ground.
- **late_midgame — Late-Midgame Development:** Maintain economy and expansion with safety checks.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid head-on engagement with Siege Tanks

**When:** Early-midgame, opponent shows heavy ground production (e.g., Marines) and you have moderate ground forces.

**Mistake → correction:** Committing to a head-on fight against Siege Tanks without proper tech or positioning, or over-expanding without sufficient army to defend. → Strengthen your ground army, increase economy and expansion, and continue technology development.

**Why:** The opponent is investing heavily in ground forces, so matching their strength while growing your economy is prudent.

**Read for full checks:** `N007`

### L02 — Balance tech and army production

**When:** Midgame, opponent has heavy ground production (e.g., Marines) and you have a strong economy but moderate production.

**Mistake → correction:** Neglecting army production while teching, or over-expanding if an attack is imminent. → Strengthen your ground army, increase economy and expansion, and continue technology development.

**Why:** The opponent is investing heavily in ground forces, so you need a strong army to defend while maintaining your economy.

**Read for full checks:** `N008`

### L03 — Develop economy before committing

**When:** Early game, opponent's posture is unknown and your own economy is still developing.

**Mistake → correction:** Overcommitting to army before your economy is stable. → Maintain current development path with safety checks. Focus on economy and expansion while keeping options open.

**Why:** With limited information, it is efficient to build a solid economic foundation before committing to a specific strategy.

**Read for full checks:** `N001`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
