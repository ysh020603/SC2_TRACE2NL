# ZvP_O06 Economy / Expansion / Ground

## Skill Identity

- Skill ID: ZvP_O06
- Matchup: Zerg vs Protoss
- Opening Family: economy / expansion / ground opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg opening that prioritizes economy and expansion while building a ground-oriented army. The strategy focuses on developing a strong economy and tech base, with moderate production and a flexible transition path.

Develop a strong economy and expansion lead while maintaining a ground army core, then adapt to the opponent's tech or air transitions.

This is a strategic template, not a fixed build order. Adapt based on live scouting and opponent actions.

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

- **early_game — Early Economy and Expansion Focus:** Prioritize economy and expansion, keep a ground army core, and scout for tech transitions.
- **early_midgame — Develop Economy and Ground Army:** Focus on economy and expansion, maintain a ground army, and scout for tech or air transitions.
- **midgame — Strengthen Ground Army and Tech:** Increase ground army production and tech, adapt to opponent's composition with counter units, and prepare for air transitions.
- **late_midgame — Maintain Army and Tech:** Maintain army production and tech, add upgrades and tech units, and adapt to air transitions with anti-air.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Counter Immortal-heavy ground armies

**When:** Midgame, around 7 minutes, when opponent has a ground army with Immortals and you have heavy defense and tech investment.

**Mistake → correction:** Staying on a small ground army and continuing to tech without increasing production, leaving you vulnerable to being overwhelmed. → Continue teching and increase army production. Add units that counter Immortals, such as Roaches or Hydralisks.

**Why:** Immortals are strong against armored units, so you need a mix of units. Your tech investment will provide upgrades to help in the fight.

**Read for full checks:** `N005`

### L02 — Transition to anti-air against Phoenix/Warp Prism

**When:** Midgame, around 8 minutes, when opponent transitions to an air-based army with Phoenixes and Warp Prisms, and you have a heavy ground defense.

**Mistake → correction:** Staying on a ground-only army and continuing to strengthen ground forces, leaving you vulnerable to air harassment. → Add anti-air units such as Hydralisks or Mutalisks. Consider building Spore Crawlers for defense.

**Why:** The opponent's air army requires anti-air capabilities. Your strong economy can support a tech switch to counter.

**Read for full checks:** `N007`

### L03 — Maintain flexibility against unknown tech

**When:** Early game, around 3 minutes, with a heavy economy and expansion, while opponent's tech is unknown but heavy.

**Mistake → correction:** Overcommitting to a specific tech path before knowing the opponent's plan, risking a poor matchup. → Continue expanding and teching. Maintain a ground army for safety and scout for tech choices.

**Why:** A strong economy and tech lead will give you an advantage in the mid-game. Ground army provides defense against early pressure.

**Read for full checks:** `N008`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
