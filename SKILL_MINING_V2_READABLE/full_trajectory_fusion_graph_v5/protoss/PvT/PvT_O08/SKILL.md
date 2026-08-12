# PvT_O08 Technology / Economy / Production

## Skill Identity

- Skill ID: PvT_O08
- Matchup: Protoss vs Terran
- Opening Family: technology / economy / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Protoss opening that emphasizes heavy technology and economy while maintaining a moderate production base, aiming for a flexible ground-oriented midgame.

Develop a technology / economy / production posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

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
- For Protoss, spend through completed powered compatible producers before adding capacity; preserve opening tempo and never force a new facility solely from a clock threshold.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Tech/Economy Foundation with Ground Flexibility:** Develop tech/economy, strengthen ground, maintain defense, keep scouting.
- **early_midgame — Ground Reinforcement with Utility Additions:** Strengthen ground, increase production/tech, maintain economy/defense, add utility units.
- **midgame — Ground Army Consolidation with Splash and Utility:** Strengthen ground, use Sentries/Immortals, maintain economy/expansion, keep scouting.
- **late_midgame — Ground Army Consolidation with Air Transition Readiness:** Maintain ground, increase production/tech, consider Phoenixes, watch for air transitions.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Air Transition

**When:** Late midgame (~10 min) with own ground army including Zealots, Stalkers, Sentries, and Immortals; opponent shows ground posture with Siege Tanks, Marines, Reapers, Hellions, heavy production and tech.

**Mistake → correction:** Being too passive and neglecting air defense if opponent transitions to air. → Maintain and strengthen your ground army, continue increasing production and tech. Consider adding Phoenixes for map control and to handle any air transitions.

**Why:** Immortals counter Siege Tanks, Sentries provide shields, and Phoenixes offer mobility and scouting. This composition is robust against ground pushes.

**Read for full checks:** `N003`

### L02 — Splash vs Marine-heavy

**When:** Midgame (~9 min) with own ground army including Zealots, Stalkers, Sentries, and Immortals; opponent shows ground posture with Marines and Marauders, heavy production and tech.

**Mistake → correction:** Being caught without splash against Marine-heavy armies and neglecting scouting for tech switches. → Continue strengthening your ground army, increase production and tech. Use Sentries for force fields and Immortals for tanky units. Maintain economy and expansion.

**Why:** Marauders are strong against armored, but Immortals and Stalkers can handle them. Sentries provide utility.

**Read for full checks:** `N004`

### L03 — Economy vs Defense

**When:** Early-midgame (~5-6 min) with own ground army including Zealots and Stalkers, heavy production and tech; opponent shows ground posture with Siege Tanks and Marines, heavy economy and production.

**Mistake → correction:** Over-extending your economy without proper defense, as Reaper harassment can punish that. → Continue strengthening your ground army and increasing production and tech. Maintain economy growth and keep defense up. Consider adding Sentries or Immortals for utility.

**Why:** Siege Tanks require careful engagement; a mix of Stalkers for mobility and Zealots for tanking, plus Sentry shields, can handle ground pushes.

**Read for full checks:** `N002`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
