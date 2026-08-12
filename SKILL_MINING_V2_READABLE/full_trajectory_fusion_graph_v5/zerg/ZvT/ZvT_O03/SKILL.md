# ZvT_O03 Economy / Technology / Expansion

## Skill Identity

- Skill ID: ZvT_O03
- Matchup: Zerg vs Terran
- Opening Family: economy / technology / expansion opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg opening that prioritizes economy and technology while expanding, aiming for a strong midgame position. The opponent is Terran, and the opening is flexible, allowing adaptation based on scouting.

Develop a robust economy and technology base while expanding, maintaining flexibility to respond to Terran's actions.

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

- **early_game — Economy and Expansion Focus:** Prioritize economy and expansion, maintain defense, continue tech, and re-evaluate when enemy intentions become clearer.
- **early_midgame — Ground Development and Tech:** Develop economy and tech, strengthen ground army, maintain expansion and production, and adapt to enemy transitions.
- **midgame — Defensive Ground and Tech:** Maintain ground army, continue tech, defend against harassment, and adjust to enemy movements.
- **late_midgame — Ground Strength and Tech:** Maintain ground strength, continue economy and tech, prepare anti-air if needed, and monitor for air transitions.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid overextending against a heavy ground Terran

**When:** Early-midgame, around 240-360 game time, with a solid economy and expansion, and enemy intelligence indicating a Terran ground posture with heavy production and technology, possibly Marines and Reapers.

**Mistake → correction:** Tempting to strengthen your ground army and increase production, economy, and expansion aggressively, but this can lead to engaging Siege Tanks head-on without proper tech or positioning, or over-expanding without sufficient army to defend. → Continue developing your economy and technology while strengthening your ground army. Maintain your expansion and production.

**Why:** A strong economy and technology base will allow you to outproduce the Terran in the midgame. Ground army strength is important to defend against potential pressure.

**Read for full checks:** `N001`

### L02 — Avoid overcommitting to army when enemy is unknown

**When:** Early game, around 180-240 game time, with a heavy economy and expansion, and enemy intelligence uncertain with no clear combat units observed, but production and technology appear heavy.

**Mistake → correction:** Tempting to strengthen ground army and increase production, economy, and expansion, but this can overcommit to army production early, slowing your economy, and neglect scouting for early pressure or all-ins. → Focus on economy and expansion while maintaining a defensive posture. Continue developing your technology.

**Why:** A strong economy early will pay off later. Since the opponent's intentions are unclear, it's safe to focus on macro.

**Read for full checks:** `N005`

### L03 — Avoid neglecting army while teching against multi-pronged pressure

**When:** Midgame, around 420 game time, with a heavy economy and investing in technology, and enemy intelligence showing a Terran ground posture with Marines, Reapers, Hellions, and Medivacs, indicating potential multi-pronged pressure.

**Mistake → correction:** Tempting to continue investing in technology and increase economy and expansion, but this can neglect army production while teching, or over-expand if an imminent attack is sensed. → Continue investing in technology while maintaining a defensive ground army. Be prepared for drops or harassment.

**Why:** Technology will give you access to stronger units and upgrades. A defensive posture is needed to handle potential multi-pronged attacks.

**Read for full checks:** `N006`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
