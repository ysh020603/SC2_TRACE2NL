# TvP_O04 Expansion / Economy / Technology

## Skill Identity

- Skill ID: TvP_O04
- Matchup: Terran vs Protoss
- Opening Family: expansion / economy / technology opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Terran opening that prioritizes a heavy economy and technology investment while maintaining a flexible, ground-leaning army posture. The early game focuses on establishing a strong economic base and teching up, with production ramping up as the game progresses. The approach is adaptable, allowing for adjustments based on scouting information about the Protoss opponent's composition and strategy.

Develop a expansion / economy / technology posture while preserving flexibility for live observation-driven adaptation.

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

- **early_game — Early Game Tech and Economy Focus:** Prioritize economy and tech, keep light defense, scout with Reaper, adapt to enemy info.
- **early_midgame — Early Midgame Ground Development:** Strengthen ground, expand, maintain defense, adapt to scouting.
- **midgame — Midgame Ground Army with Air Support:** Strengthen ground, tech up, maintain air, expand, watch for air transitions.
- **late_midgame — Late Midgame Ground Army with Siege Tanks:** Strengthen ground, tech up, maintain expansion, watch for air transitions.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground: Don't Overextend Economy

**When:** Early-midgame, both sides ground-oriented with heavy production and tech, around 300 seconds.

**Mistake → correction:** Continuing to expand and tech without reinforcing your army, assuming the enemy is passive. → Strengthen your ground army and increase technology investment. Consider adding air units for flexibility. Maintain expansion and production.

**Why:** The opponent is ground-oriented, so a strong ground army is essential. Air units provide flexibility against potential air transitions.

**Read for full checks:** `N002`

### L02 — Early Game: Don't Overcommit to Tech

**When:** Early game, both sides unknown compositions, heavy economy and tech investment, around 180 seconds.

**Mistake → correction:** Over-committing to tech at the expense of army production and neglecting scouting. → Focus on developing economy and technology while maintaining a light defensive posture. Use your Reaper for scouting to gather information.

**Why:** This sets up a strong midgame, and scouting helps you adapt to the opponent's choices.

**Read for full checks:** `N003`

### L03 — Ground vs Air: Don't Ignore Anti-Air

**When:** Early-midgame, opponent air-oriented with Phoenixes and Oracles, you have ground army with Siege Tanks and Marines, around 360 seconds.

**Mistake → correction:** Neglecting your ground army entirely or over-investing in anti-air without a clear threat. → Add anti-air units such as Marines, Thors, or Vikings to counter the opponent's air presence. Maintain your ground army and continue expanding.

**Why:** The opponent's air units can be a threat, so you need a response. Adding anti-air units helps defend against harass and potential air attacks.

**Read for full checks:** `N006`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
