# ZvP_O01 Economy / Expansion / Production

## Skill Identity

- Skill ID: ZvP_O01
- Matchup: Zerg vs Protoss
- Opening Family: economy / expansion / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg opening that prioritizes economy and expansion while maintaining moderate production and light technology. The early game focuses on building a strong economic base with Queens and Zerglings for defense, then transitions into a heavier ground army with tech upgrades as the game progresses.

Develop a robust economy and expansion lead while preserving flexibility to adapt to Protoss tech choices, whether they commit to ground or air.

This is a strategic template, not a fixed build order. Adapt based on live scouting and enemy tech choices.

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

- **early_game — Early Economy and Queen Defense:** Prioritize economy and expansion, maintain Queens for defense, and stay alert for enemy tech.
- **early_midgame — Early-Mid Ground Army and Tech Adaptation:** Balance ground army strength with expansion, adapt to enemy tech, and maintain scouting.
- **midgame — Midgame Ground Army Consolidation and Tech:** Consolidate ground army, adapt to enemy composition, and maintain map presence.
- **late_midgame — Late-Mid Army and Tech Adaptation:** Adapt army composition to enemy, maintain economy, and prepare for decisive engagement.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Anti-Air Defense

**When:** Early-midgame, around 6 minutes, when enemy shows Phoenixes and Oracles.

**Mistake → correction:** Ignoring air threats and continuing pure ground army without anti-air. → Maintain ground army while adding anti-air like Hydralisks or Spore Crawlers. Continue expanding and teching.

**Why:** Phoenix and Oracle can harass workers and pick off units. Anti-air protects economy and army.

**Read for full checks:** `N007`

### L02 — Ground Composition Counter

**When:** Late-midgame, around 10-12 minutes, when enemy has heavy ground army with Observers.

**Mistake → correction:** Being out-teched and not adapting composition to enemy's heavy ground. → Continue strengthening ground army and tech. Add Roaches or Hydralisks for anti-armor. Maintain map control and prepare for decisive battle.

**Why:** With strong economy, you can afford larger army and tech upgrades. Matching enemy composition with counters is key.

**Read for full checks:** `N008`

### L03 — Transition to Air

**When:** Late-midgame, around 10-12 minutes, when enemy has heavy air presence including Phoenixes and Oracles.

**Mistake → correction:** Staying pure ground against heavy air. → Transition to air units like Mutalisks or Corruptors to counter enemy air. Continue expanding and teching. Maintain ground defense.

**Why:** Air units can counter enemy air and provide harassment. Mixed army with anti-air is essential.

**Read for full checks:** `N009`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
