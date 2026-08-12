# ZvZ_O01 Economy / Expansion / Ground

## Skill Identity

- Skill ID: ZvZ_O01
- Matchup: Zerg vs Zerg
- Opening Family: economy / expansion / ground opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

This opening focuses on a heavy economy and expansion posture with a ground-oriented army. Production is moderate early, with technology investment light or uncertain. The goal is to develop a strong macro foundation while maintaining flexibility to adapt to opponent actions.

Develop a economy / expansion / ground posture while preserving flexibility for live observation-driven adaptation.

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

- **early_game — Early Ground Economy:** Develop ground forces and economy while keeping defense ready; adapt to pressure or tech shifts.
- **early_midgame — Early-Mid Ground Development:** Maintain ground strength and economy; watch for tech or air transitions.
- **midgame — Midgame Ground Macro:** Sustain ground macro; adapt to air threats or pressure as needed.
- **late_midgame — Late-Midgame Ground Defense:** Bolster defenses against air while continuing ground development; adapt to opponent's commitment.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid Premature Tech

**When:** Early-midgame, both sides ground, heavy economy, moderate production, light tech. Zergling and Queen cues visible.

**Mistake → correction:** Investing in unnecessary technology that delays army production. → Continue strengthening ground, maintain economy, production, tech, and expansion.

**Why:** Maintaining a balanced ground macro approach keeps you competitive while allowing adaptation to opponent's tech or army choices.

**Read for full checks:** `N002`

### L02 — Don't Ignore Air Threat

**When:** Midgame, opponent ground with heavy air presence, heavy economy, heavy production, moderate tech. Zergling, Mutalisk, Queen, Overseer cues.

**Mistake → correction:** Staying purely ground when opponent has a significant air force. → Increase defense, economy, continue production and tech, strengthen ground.

**Why:** With opponent having air presence, you need to bolster defenses and possibly tech to anti-air while maintaining economy.

**Read for full checks:** `N008`

### L03 — Don't Neglect Ground Defense

**When:** Midgame, opponent ground with light air, heavy economy, heavy production, heavy tech. Zergling, Roach, Queen cues.

**Mistake → correction:** Neglecting ground defense while teching to air. → Increase air, economy, continue tech, maintain production, strengthen air.

**Why:** If you have air presence and opponent is ground-heavy, transitioning to air can give you a strategic advantage.

**Read for full checks:** `N009`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
