# TvT_O01 Economy / Technology / Production

## Skill Identity

- Skill ID: TvT_O01
- Matchup: Terran vs Terran
- Opening Family: economy / technology / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Terran mirror opening that emphasizes heavy economy, production, and technology investment while maintaining a flexible ground-oriented posture. Early game focuses on establishing a strong macro foundation with light harassment potential.

Develop a robust economy and technology base while preserving flexibility to adapt to opponent actions and transition into a strong midgame ground army.

This is a strategic template, not a fixed build order. Adapt based on live observations and opponent behavior.

## Strategic Characteristics

- Economy: heavy
- Production: heavy
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

- **early_game — Macro Foundation with Scouting:** Prioritize economy and tech; scout for opponent's tech choices; maintain defensive ground posture.
- **early_midgame — Ground Development with Siege Tank Transition:** Develop ground forces, scout for tech, transition to Siege Tanks if needed; maintain economy and production.
- **midgame — Balanced Ground Army with Air Support:** Maintain balanced army, expand and tech, add air for support and scouting.
- **late_midgame — Defensive Strengthening with Tech Diversification:** Fortify defenses, expand, diversify tech to counter opponent's mix, ensure detection.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid greedy expansion without scouting

**When:** Early-midgame, around 5 minutes, when the opponent shows a ground posture with Siege Tanks and Marauders, and you have Marines and a heavy economy.

**Mistake → correction:** Expanding too greedily without proper scouting, risking being caught off guard by an enemy push. → Transition into a Siege Tank-based army to counter the opponent's ground composition, while continuing to expand and tech.

**Why:** Siege Tanks provide strong defensive and offensive capabilities against ground armies, especially in TvT.

**Read for full checks:** `N004`

### L02 — Avoid neglecting anti-air defenses

**When:** Late-midgame, around 10 minutes, when the opponent shows a ground posture with Siege Tanks, Reapers, Banshees, and Ravens, and you have a ground army with Siege Tanks, Marines, Reapers, and Hellions.

**Mistake → correction:** Neglecting anti-air defenses, leaving you vulnerable to Banshees and Ravens. → Diversify your tech to counter the opponent's mix, adding air defense and detection. Continue expanding and teching.

**Why:** The opponent's mix of air and ground units requires a balanced response. Heavy economy allows for tech diversification.

**Read for full checks:** `N010`

### L03 — Avoid neglecting upgrades or falling behind in army supply

**When:** Midgame, around 8 minutes, when both players have a moderate air presence and heavy ground armies, with you having Siege Tanks, Marines, Marauders, and Medivacs, and the opponent showing similar units.

**Mistake → correction:** Neglecting upgrades or falling behind in army supply, as the opponent may attempt a timing attack with Siege Tanks. → Maintain your balanced army composition and continue expanding. Consider adding air units for scouting and drop potential.

**Why:** A balanced army is versatile and can adapt to various opponent compositions. Heavy economy supports continued production.

**Read for full checks:** `N005`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
