# ZvT_O05 Expansion / Economy / Production

## Skill Identity

- Skill ID: ZvT_O05
- Matchup: Zerg vs Terran
- Opening Family: expansion / economy / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg opening that prioritizes economy and expansion while maintaining a flexible ground-oriented posture. Early game focuses on queens and zerglings, with technology investment ramping up through the midgame. The opponent is expected to follow a ground-heavy Terran composition, but the plan remains adaptable to observed enemy tech choices.

Develop a strong economy and production base while preserving flexibility to respond to the opponent's tech and army composition. Aim to reach a midgame with a solid ground army and the option to transition into air if needed.

This is a strategic template, not a fixed build order. Adapt based on live scouting and enemy intelligence.

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

- **early_game — Early Game Foundation:** Establish economy and defense, produce queens, tech towards midgame.
- **early_midgame — Early-Midgame Expansion:** Expand and increase production, invest in tech, maintain ground army.
- **midgame — Midgame Tech Investment:** Increase tech and production, expand, strengthen ground army with counter units.
- **late_midgame — Late-Midgame Army Strengthening:** Strengthen ground army, increase tech, maintain economy and production.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid over-expanding without defense

**When:** Early-midgame, when you have a ground-oriented posture with moderate production and light tech, and the opponent is also ground-oriented with heavy production and tech.

**Mistake → correction:** Focusing solely on expanding and teching up while neglecting army production and defense, leaving you vulnerable to enemy aggression. → Increase your expansion and production while investing in technology, but ensure you maintain a defensive force to protect your bases.

**Why:** A strong economy and tech base will allow you to transition into a powerful midgame army, but only if you survive the early-midgame pressure.

**Read for full checks:** `N011`

### L02 — Avoid passivity in early game

**When:** Early game, when you have a ground-oriented posture with moderate production and light tech, and the opponent is ground-oriented with moderate production and heavy tech.

**Mistake → correction:** Being too passive and focusing only on economy and expansion, allowing the Terran to dictate the pace and apply pressure without resistance. → Maintain your economy and expansion rate while producing queens for defense. Continue teching towards a midgame composition.

**Why:** A strong economy allows you to outproduce the opponent in the midgame. Queens provide cost-effective defense against early pressure and creep spread.

**Read for full checks:** `N001`

### L03 — Avoid over-investing in tech at the expense of army

**When:** Early-midgame, when you have a ground-oriented posture with moderate production and heavy tech, and the opponent is ground-oriented with heavy production and tech.

**Mistake → correction:** Over-investing in technology and upgrades while neglecting army size and scouting, leaving you unprepared for an enemy attack. → Increase your technology and production to match the opponent. Continue expanding and strengthening your ground army.

**Why:** Investing in technology now allows you to unlock key units like Hydralisks or Roaches, which are essential against a Terran ground army, but you must also maintain a sufficient army to defend.

**Read for full checks:** `N003`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
