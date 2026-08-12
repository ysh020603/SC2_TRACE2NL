# ZvZ_O02 Economy / Ground / Expansion

## Skill Identity

- Skill ID: ZvZ_O02
- Matchup: Zerg vs Zerg
- Opening Family: economy / ground / expansion opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg versus Zerg opening that emphasizes economy and expansion while keeping ground forces as the primary defensive and offensive arm. The early game is characterized by uncertainty about the opponent's intentions, so the strategy is to develop a solid economic base and a flexible ground army, ready to adapt based on scouting information.

Develop a robust economy and a ground-oriented army while maintaining flexibility to respond to opponent actions. Prioritize expansion and worker production to secure a long-term advantage, but keep enough defensive units to deter early aggression.

This is a strategic template, not a fixed build order. Adapt your actions based on live scouting and opponent behavior.

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

- **early_game — Balanced Development with Scouting:** Develop economy and scouting, stay flexible, avoid overcommitment.
- **early_midgame — Flexible Development with Scouting:** Develop economy and production, keep army flexible, scout for information.
- **midgame — Consolidate and Scout:** Consolidate economy, increase scouting, build defensive army.
- **late_midgame — Prepare for Late Game:** Develop economy and production, increase army, scout for information.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid premature tech investment

**When:** Early-mid game, opponent has ground posture with Zerglings, heavy economy, and you have moderate production and light tech.

**Mistake → correction:** Investing in unnecessary technology that delays army production. → Continue strengthening your ground army and maintain economy. Consider expanding further to secure long-term advantage.

**Why:** Both sides focus on economy and ground forces; the better economy and army composition will prevail.

**Read for full checks:** `N007`

### L02 — Avoid falling behind in economy

**When:** Early game, opponent has ground posture with Queen, your economy is moderate, and you have light tech.

**Mistake → correction:** Making unnecessary units that could be drones, falling behind economically. → Maintain a balanced approach: develop economy while strengthening ground army. Focus on scouting to gain information.

**Why:** Opponent focuses on economy; you need to keep up economically while building a defensive army to deter attacks. Balanced approach adapts to opponent's actions.

**Read for full checks:** `N006`

### L03 — Avoid unnecessary aggression

**When:** Early-mid game, opponent has ground posture with Zerglings, heavy economy, and you have moderate production and light tech.

**Mistake → correction:** Engaging in unnecessary aggression that costs drones, neglecting scouting for tech switches or all-ins. → Continue strengthening ground army and maintain economy. Consider expanding further to secure long-term advantage.

**Why:** Both sides focus on economy and ground forces; the better economy and army composition will prevail.

**Read for full checks:** `N007`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
