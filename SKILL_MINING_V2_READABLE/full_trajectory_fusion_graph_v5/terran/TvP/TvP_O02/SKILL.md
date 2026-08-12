# TvP_O02 Technology / Economy / Production

## Skill Identity

- Skill ID: TvP_O02
- Matchup: Terran vs Protoss
- Opening Family: technology / economy / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

This opening focuses on developing a technology and economy foundation while keeping production flexible. Early game is characterized by light or uncertain production and technology, with the option to transition into a heavier ground-oriented composition as the game progresses.

Develop a technology / economy / production posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

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

- **early_game — Early Game Development with Safety Checks:** Develop economy and technology with flexible production, maintaining safety checks.
- **early_midgame — Early-Mid Game Development Continuation:** Continue balanced development with safety checks, avoiding unnecessary risks.
- **midgame — Midgame Development with Safety Checks:** Continue balanced development with safety checks, avoiding unnecessary risks.
- **late_midgame — Late-Midgame Development with Safety Checks:** Continue balanced development with safety checks, avoiding unnecessary risks.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Match Opponent's Economy

**When:** Early game when opponent has heavy economy and technology, moderate production, and your own economy is moderate with heavy technology.

**Mistake → correction:** Focusing on technology and economy while neglecting army production, leaving you vulnerable to an attack. → Increase your economy and production to match the opponent's heavy economy, while continuing technology development.

**Why:** The opponent's heavy economy and technology indicate a macro-oriented game; matching their economy and production keeps you competitive.

**Read for full checks:** `N006`

### L02 — Counter Ground Composition

**When:** Late-midgame when both sides have ground posture, opponent has Zealots and Stalkers with heavy economy, production, and technology, and your ground forces include Marines, Reapers, and Widow Mines.

**Mistake → correction:** Neglecting upgrades or tech that could give the opponent an advantage in the ground engagement. → Strengthen your ground forces further, considering adding Siege Tanks or Marauders to counter Zealots and Stalkers.

**Why:** The opponent's ground army is strong; Siege Tanks provide area denial and Marauders are effective against Zealots.

**Read for full checks:** `N007`

### L03 — Adapt to Sentry Threats

**When:** Early-midgame when opponent has ground posture with Zealots and Sentries, heavy economy, production, and technology, and your ground forces include Marines.

**Mistake → correction:** Over-committing to a single unit composition that could be countered by Sentry abilities. → Strengthen your ground forces, considering adding Marauders to counter Zealots and Sentries.

**Why:** The opponent's ground army is strong; Marauders are effective against Zealots and can help break Sentry force fields.

**Read for full checks:** `N008`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
