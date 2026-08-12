# TvT_O02 Economy / Technology / Production

## Skill Identity

- Skill ID: TvT_O02
- Matchup: Terran vs Terran
- Opening Family: economy / technology / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A flexible Terran opening that prioritizes economic and technological development while keeping production options open. Early game is characterized by light or uncertain information, with the potential to transition into a heavy ground-based macro posture.

Develop a robust economy and technology base while maintaining flexibility to adapt to opponent actions. Aim to reach a strong mid-game position with a solid ground army and the option to transition to air if needed.

This is a strategic template, not a fixed build order. Adapt based on live observations and opponent actions.

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
- For Terran, use completed parents before scaling capacity, and order parent before add-on or dependent work; persistent bank plus low army favors executable unit throughput.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Early Game Development:** Develop economy and technology with safety checks; if a Reaper is spotted, strengthen ground forces and increase production.
- **early_midgame — Early-Midgame Development:** Maintain development with safety checks; if opponent shows ground army, consider defensive structures and counter units.
- **midgame — Midgame Development:** Maintain development with safety checks; if opponent has ground army, strengthen ground forces and consider supporting units.
- **late_midgame — Late Midgame Ground Macro:** Maintain development while preparing defense; consider defensive structures or units to counter opponent's composition.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Reaper Harassment Response

**When:** Early game, when you spot a Reaper from the opponent and your own economy is moderate with technology investment.

**Mistake → correction:** Overcommitting to economy and technology while ignoring the Reaper threat, leaving your workers vulnerable to harassment. → Strengthen your ground forces and increase production. Build a defensive structure or a unit to counter Reaper harassment.

**Why:** The Reaper suggests early aggression or a tech switch; defending against it prevents economic damage and prepares you for a counter.

**Read for full checks:** `N004`

### L02 — Midgame Ground Macro Mirror

**When:** Midgame, when both you and the opponent have ground-based armies with Marines and Reapers, and heavy economies.

**Mistake → correction:** Neglecting your economy while building an army, or overcommitting to a single unit composition without adaptability. → Continue strengthening your ground forces and increasing your economy. Consider adding supporting units like Marauders or Siege Tanks.

**Why:** Both players are on a similar ground macro path; strengthening army and economy helps gain an advantage in the midgame.

**Read for full checks:** `N005`

### L03 — Catching Up Against a Strong Ground Army

**When:** Early midgame, when the opponent has a strong ground army with Marines, Reapers, and Marauders, while your own posture is underdeveloped.

**Mistake → correction:** Engaging the opponent's army without a plan, or neglecting your economy while trying to catch up. → Maintain your current development path, but be aware that the opponent is ahead. Consider building a defensive structure or a unit to counter the opponent's composition.

**Why:** The opponent has a strong ground army, so you need to catch up. Maintaining development while preparing a defense is the safest option.

**Read for full checks:** `N007`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
