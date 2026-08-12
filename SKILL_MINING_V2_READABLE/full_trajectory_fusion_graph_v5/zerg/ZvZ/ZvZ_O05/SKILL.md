# ZvZ_O05 Economy / Ground / Upgrade

## Skill Identity

- Skill ID: ZvZ_O05
- Matchup: Zerg vs Zerg
- Opening Family: economy / ground / upgrade opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg versus Zerg opening that prioritizes a strong economy and ground-based army development, with an emphasis on upgrades and technological progression. The opening is flexible, allowing for adaptation based on scouting information.

Develop a robust economy and a versatile ground army while maintaining the option to transition into air or tech-based compositions as the game evolves.

This is a strategic template, not a fixed build order. Adapt your decisions based on live scouting and enemy intelligence.

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

- **early_game — Early Economy Foundation:** Prioritize drones and expansion, maintain minimal defensive Zerglings and Queens, keep scouting for early threats.
- **early_midgame — Ground Macro Development:** Balance drone and unit production, maintain scouting, keep tech and production steady, prepare to respond to threats.
- **midgame — Ground Army Strengthening:** Add Roaches and upgrades, maintain economy and production, scout for tech switches, adjust if air threat emerges.
- **late_midgame — Ground Consolidation or Air Transition:** Maintain strong economy and production, upgrade units, adapt composition based on scouting, prepare for major engagement.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid premature aggression in a macro mirror

**When:** Early-midgame, both players ground-oriented with light tech and moderate production, strong economy and expansion.

**Mistake → correction:** Launching an unnecessary attack that sacrifices drones or disrupts your economy, or neglecting scouting for tech switches or all-ins. → Continue developing your ground army and economy. Maintain current production and technology levels while keeping an eye on potential threats.

**Why:** Both players are in a similar macro state; continuing to develop economy and ground forces keeps you competitive and ready to respond.

**Read for full checks:** `N001`

### L02 — Match heavy production with robust ground forces

**When:** Midgame, enemy ground posture with heavy production and moderate tech, your army includes Roaches.

**Mistake → correction:** Over-investing in Roaches if the opponent is teching to air, or neglecting expansion and economy. → Strengthen your ground army by adding more Roaches and possibly tech upgrades. Continue to expand your economy and production.

**Why:** Enemy's heavy production suggests a large army; matching production and strengthening ground forces helps defend or counter-attack.

**Read for full checks:** `N002`

### L03 — Prioritize economy over unnecessary units in early game

**When:** Early game, both ground-oriented with moderate production and light tech, your economy moderate and expansion developing.

**Mistake → correction:** Falling behind in economy by making unnecessary units that could be drones. → Focus on expanding your economy and establishing a solid foundation. Continue producing Zerglings and Queens for defense.

**Why:** A strong economy is crucial for long-term success; building a solid foundation allows you to outproduce the enemy in the midgame.

**Read for full checks:** `N003`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
