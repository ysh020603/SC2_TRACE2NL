# ZvP_O07 Economy / Production / Expansion

## Skill Identity

- Skill ID: ZvP_O07
- Matchup: Zerg vs Protoss
- Opening Family: economy / production / expansion opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg opening that prioritizes economy, production, and expansion while maintaining a ground-oriented army. The strategy is flexible and adapts to opponent observations.

Develop a strong economy and production base while preserving flexibility to respond to Protoss tech choices.

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

- **early_game — Early Economy Focus with Defensive Production:** Prioritize economy and expansion, but begin production and army buildup; stay defensive.
- **early_midgame — Ground Development with Tech and Economy Expansion:** Develop economy and production, strengthen ground army, maintain expansion, watch for pressure.
- **midgame — Ground Army Strengthening with Tech and Economy:** Strengthen ground army, continue economy and tech, maintain defense.
- **late_midgame — Ground Army Consolidation with Tech and Economy:** Maintain economy, production, tech, strengthen ground army, keep defense.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid over-expanding without army support

**When:** Early game, around 180 seconds, when you have a heavy economy and expansion but light production and tech, and opponent's posture is unknown.

**Mistake → correction:** Continuing to expand and strengthen ground army without first building up production and scouting, leaving you vulnerable to early aggression. → Focus on economy and expansion, but start building up production and army. Maintain a defensive posture.

**Why:** Your economy is strong, so you can afford to expand and tech. The opponent's unknown posture means you should be cautious.

**Read for full checks:** `N002`

### L02 — Avoid blind teching without scouting

**When:** Early midgame, around 240 seconds, when you have a heavy economy and expansion but light production and tech, and opponent's posture is unknown.

**Mistake → correction:** Increasing economy and tech without scouting, potentially leaving you unprepared for the opponent's strategy and neglecting army production. → Increase your economy and tech, while maintaining your production and expansion. Keep a defensive posture.

**Why:** Your economy is strong, so you can invest in tech. The opponent's unknown posture means you should be cautious.

**Read for full checks:** `N004`

### L03 — Avoid neglecting ground defense against air-heavy opponent

**When:** Midgame, around 540 seconds, when you have a heavy economy, production, expansion, and tech, and opponent has an air posture with heavy production and tech.

**Mistake → correction:** Continuing to strengthen ground army and expand without adding anti-air, leaving you vulnerable to the opponent's air units. → Increase your economy, production, and expansion, while continuing to develop your ground army. Consider adding anti-air.

**Why:** The opponent's air threat requires a response, so you need to prepare anti-air while maintaining your economy.

**Read for full checks:** `N008`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
