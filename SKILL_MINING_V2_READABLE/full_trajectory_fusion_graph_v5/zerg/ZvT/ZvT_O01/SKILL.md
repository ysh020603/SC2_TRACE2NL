# ZvT_O01 Economy / Expansion / Ground

## Skill Identity

- Skill ID: ZvT_O01
- Matchup: Zerg vs Terran
- Opening Family: economy / expansion / ground opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg opening focused on heavy economy and expansion while maintaining a ground-oriented army. The opponent is Terran, and early intelligence suggests a ground posture with possible early pressure. The strategy emphasizes macro development with safety checks.

Develop a strong economy and expand while building a ground-based army, maintaining flexibility to adapt to opponent's tech or air transitions.

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

- **early_game — Early Ground Macro with Expansion:** Prioritize economy and expansions while building Zerglings and Queens; maintain scouting to detect early aggression.
- **early_midgame — Early Midgame Ground Tech Transition:** Balance tech upgrades with army production; expand cautiously and keep scouting for tech switches.
- **midgame — Midgame Ground vs Ground with Hydralisks:** Maintain a strong ground army with Hydralisks, continue expanding, and tech towards upgrades while scouting.
- **late_midgame — Late Midgame Ground vs Ground:** Prepare for large engagements by maintaining economy and tech, while keeping a strong ground army and scouting.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Balanced Macro with Ground Focus

**When:** Early game, opponent ground posture (Marine/Reaper), own Zergling/Queen, moderate production and light tech.

**Mistake → correction:** Being too passive and letting the Terran dictate the pace, neglecting army production while expanding. → Strengthen ground army, increase economy, maintain expansions and production, continue tech.

**Why:** Maintaining a balanced macro approach supports a strong midgame.

**Read for full checks:** `N002`

### L02 — Late Midgame Preparation

**When:** Late midgame, opponent ground posture (SiegeTank/Marine/Reaper/Hellion), own Zergling/Queen, heavy production and tech.

**Mistake → correction:** Being passive and letting the Terran dictate the pace, neglecting upgrades. → Strengthen ground army, increase economy, continue expansions and production, increase tech.

**Why:** In late midgame, you need to prepare for large engagements; maintaining economy while teching is crucial.

**Read for full checks:** `N005`

### L03 — Transition to Midgame

**When:** Early midgame, opponent ground posture (Marine/Reaper/Hellion), own Zergling/Queen, moderate tech.

**Mistake → correction:** Over-investing in tech at the expense of army size, neglecting scouting to anticipate the attack. → Strengthen ground, increase economy, continue expansions and production, increase tech.

**Why:** As you transition to midgame, you need to start teching to counter opponent's composition; maintaining economy is key.

**Read for full checks:** `N007`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
