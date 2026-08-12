# TvT_O06 Technology / Economy / Production

## Skill Identity

- Skill ID: TvT_O06
- Matchup: Terran vs Terran
- Opening Family: technology / economy / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Terran mirror opening that emphasizes heavy technology and economy investment while maintaining a moderate production base. The early game is characterized by a ground-oriented posture with possible early pressure from Reapers or Marines. The strategic focus is on developing a strong macro foundation and tech advantage, with flexibility to adapt to opponent moves.

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
- For Terran, use completed parents before scaling capacity, and order parent before add-on or dependent work; persistent bank plus low army favors executable unit throughput.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Ground Macro with Heavy Tech:** Prioritize economy and tech, maintain production, and keep defense solid.
- **early_midgame — Ground Army with Siege Tanks:** Focus on defensive ground strength, economy, and tech; expand cautiously.
- **midgame — Ground Army with Air Transition:** Balance ground and air, expand, and keep tech advancing.
- **late_midgame — Versatile Ground Army:** Keep a strong ground core, expand, and adapt to opponent's tech.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Siege Tank Support

**When:** Early midgame (~5 min) with both players ground-oriented, heavy economy and tech, opponent shows Marine cues, you have Siege Tanks and Marines.

**Mistake → correction:** Pushing without Siege Tank support or into a fortified position. → Continue strengthening your ground army, particularly with Siege Tanks for defensive positioning. Increase economy and maintain production and tech.

**Why:** Siege Tanks provide strong defensive and positional advantages in TvT. Maintaining a heavy economy and tech allows transition to advanced units if needed.

**Read for full checks:** `N003`

### L02 — Avoid Tank Pushes

**When:** Midgame (~7 min) with opponent ground posture with Marines, you have Marines and Marauders.

**Mistake → correction:** Attacking into Siege Tanks without proper positioning or support. → Maintain your ground army and continue increasing economy. Keep production and tech steady.

**Why:** A balanced Marine/Marauder composition is strong in TvT. Maintaining economy and tech allows adaptation to opponent's composition.

**Read for full checks:** `N007`

### L03 — Avoid Siege Stalemate

**When:** Late midgame (~10 min) with opponent ground posture with Marines, you have Siege Tanks, Marines, Marauders, and Hellions.

**Mistake → correction:** Getting into a siege war without breaking their defenses; failing to use mobility to force engagements. → Maintain your ground army and continue increasing economy. Keep production and tech steady.

**Why:** Your army composition is strong and versatile. Maintaining economy and tech ensures sustainability and response to opponent moves.

**Read for full checks:** `N008`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
