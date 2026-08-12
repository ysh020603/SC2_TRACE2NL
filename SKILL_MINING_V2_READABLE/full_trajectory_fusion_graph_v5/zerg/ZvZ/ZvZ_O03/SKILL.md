# ZvZ_O03 Economy / Technology / Expansion

## Skill Identity

- Skill ID: ZvZ_O03
- Matchup: Zerg vs Zerg
- Opening Family: economy / technology / expansion opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg versus Zerg opening that prioritizes a heavy economy, technology, and expansion posture while maintaining a ground-oriented army. The approach is flexible, with a focus on developing infrastructure and tech before committing to aggressive actions.

Develop a strong economy and technology base while expanding, keeping ground army strength sufficient to deter or respond to pressure, and preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order. Adapt based on live scouting and enemy intelligence.

## Strategic Characteristics

- Economy: heavy
- Production: moderate
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
- For Zerg, production capacity is bases plus larva/inject throughput; Overlords and Drones consume the same larva as army, so do not translate facility-count rules from other races.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Early Economy and Tech Focus with Defense Preparation:** Prioritize economy and tech, keep production and expansion steady, and maintain a defensive buffer against potential early pressure.
- **early_midgame — Balanced Ground Macro Development:** Balance economy, tech, and ground army; keep production and expansion steady while staying alert to pressure.
- **midgame — Midgame Ground Army Strengthening with Stability:** Focus on ground army durability with Roaches, sustain economy and tech, and keep defense robust to handle pressure.
- **late_midgame — Late-Midgame Heavy Macro and Tech Scaling:** Scale economy and tech with upgrades, keep ground army strong, and stay flexible to adapt to tech switches.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Early Economy vs. Defense

**When:** Early game, around 180 seconds, with both sides expanding and minimal army (Queen only), opponent shows Zergling and Queen.

**Mistake → correction:** Over-committing to economy and tech while neglecting defense, assuming the opponent is passive. → Focus on economy and tech development while preparing to defend. Maintain production and expansion, but be ready to build defensive units if pressure comes.

**Why:** Early game is about establishing a strong economy and tech lead. Investing now will pay off, but you must be prepared to defend against early Zergling pressure.

**Read for full checks:** `N003`

### L02 — Balanced Macro in Early-Midgame

**When:** Early-midgame, around 300 seconds, with both sides in a ground-oriented macro posture, heavy economy and expansion, moderate production/tech, enemy shows Zergling and Queen.

**Mistake → correction:** Neglecting army production entirely, leaving yourself vulnerable to a sudden attack. → Continue developing your economy and tech while strengthening your ground army. Maintain current production and expansion pace, but keep safety checks in mind.

**Why:** The situation is symmetric and stable; investing in economy and tech now will pay off later. Maintaining a ground army deters potential aggression without overcommitting.

**Read for full checks:** `N001`

### L03 — Scaling with Upgrades in Late-Midgame

**When:** Late-midgame, around 600-720 seconds, with both sides having heavy economy, defense, production, and tech. Your army is ground-based with Zergling and Queen, opponent shows Zergling, Roach, Queen.

**Mistake → correction:** Over-investing in technology without sufficient army, and neglecting scouting for tech switches. → Increase your economy and tech further, and consider upgrades. Maintain your ground army and production, but be ready to adapt if the opponent tech switches.

**Why:** With a heavy economy and tech, you can afford to invest in upgrades and a larger army. Maintaining a strong ground presence keeps you safe while you scale.

**Read for full checks:** `N004`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
