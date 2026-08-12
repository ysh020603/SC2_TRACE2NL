# TvT_O04 Expansion / Economy / Technology

## Skill Identity

- Skill ID: TvT_O04
- Matchup: Terran vs Terran
- Opening Family: expansion / economy / technology opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Terran mirror opening that prioritizes economy and technology development, with a flexible ground-oriented posture. Early game focuses on heavy economy and technology investment, transitioning to a strong ground army with Siege Tanks and Marines in the midgame.

Develop a strong economy and technology base while maintaining flexibility to adapt to opponent's composition, aiming for a midgame ground army with Siege Tank support.

This is a strategic template, not a fixed build order. Adapt based on live scouting and opponent's actions.

## Strategic Characteristics

- Economy: heavy
- Production: moderate
- Technology: heavy
- Army direction: ground-leaning

## Strategic Priorities

- Preserve the opening's strategic identity without reproducing a fixed sequence.
- Check current Completed, Under Construction, Active Queues, resources, supply, and prerequisites before choosing exact macro actions.
- Match any adaptation against partial Enemy Intelligence and current Threat Flags.
- Re-evaluate economy, production, technology, and army trade-offs at every decision.

## V5 Human-Trajectory / Runtime Bridge

- The phase policy below supplies the strategic target distilled from aggregate trajectory states; it is not an action sequence.
- The live router supplies exactly one current execution bottleneck. Resolve it without replacing the phase target with a generic macro rule.
- For Terran, use completed parents before scaling capacity, and order parent before add-on or dependent work; persistent bank plus low army favors executable unit throughput.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Economy and Technology Focus with Scouting:** Prioritize economy and tech, scout for opponent's plan, maintain defensive readiness.
- **early_midgame — Ground Development with Defensive Readiness:** Develop economy and tech, strengthen ground army, maintain defense against possible pressure.
- **midgame — Siege Tank Transition with Air Flexibility:** Add air units for defense, continue ground strength, maintain economy.
- **late_midgame — Sustained Pressure with Air and Economy:** Strengthen ground, increase air, maintain economy for sustained fight.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Midgame Ground vs. Air Flexibility

**When:** At around 540 seconds, both players have transitioned to a midgame ground army with Siege Tanks, Marines, and supporting units. The opponent shows moderate air presence.

**Mistake → correction:** Tempting to focus solely on strengthening your ground army and continuing production, economy, and technology without adding air units, leaving you vulnerable to drops or air harassment. → Increase your air presence to counter potential drops or air threats, continue strengthening your ground army, and maintain your economy.

**Why:** With both players having similar ground compositions, adding air units provides flexibility and counters potential medivac drops or air harassment.

**Read for full checks:** `N002`

### L02 — Late Midgame Sustained Pressure

**When:** At around 600 seconds, both players have a heavy ground army with Siege Tanks and Marines, and a moderate air presence. The opponent has a heavy defense.

**Mistake → correction:** Tempting to overcommit to ground forces and neglect air upgrades or economy, potentially losing a prolonged engagement due to lack of air support or resource exhaustion. → Continue strengthening your ground army, increase your air presence, and maintain your economy to support a long fight.

**Why:** With both players having strong ground armies, adding air units and maintaining a robust economy gives you an edge in the late game.

**Read for full checks:** `N005`

### L03 — Early Midgame Economy and Defense

**When:** At around 300 seconds, both players have a heavy economy and technology investment, with a ground-oriented army. The opponent shows possible pressure with Reapers and Hellions.

**Mistake → correction:** Tempting to over-extend or attack into a fortified position, or to neglect defensive readiness while focusing on economy and technology. → Continue developing your economy and technology, strengthen your ground army, and maintain defensive readiness.

**Why:** Both players are in a similar economic and technological state. Maintaining a strong economy and technology lead while building a versatile ground army positions you well for the midgame.

**Read for full checks:** `N001`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
