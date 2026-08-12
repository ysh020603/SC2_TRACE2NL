# TvZ_O02 Technology / Economy / Production

## Skill Identity

- Skill ID: TvZ_O02
- Matchup: Terran vs Zerg
- Opening Family: technology / economy / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

This opening emphasizes developing a technology and economy foundation while keeping production flexible. Early game is characterized by uncertainty in both own and opponent postures, with a focus on safe development and scouting. As the game progresses, the path can branch into a heavier ground-oriented composition if the opponent shows a ground macro posture.

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

- **early_game — Safe Development with Ground Contingency:** Develop safely with steady production, economy, and technology; if ground cues appear, pivot to ground army strength and economy growth.
- **early_midgame — Steady Development with Ground Adaptation:** Continue safe development; if ground cues appear, strengthen ground forces and economy while maintaining production.
- **midgame — Safe Development with Ground Confrontation Readiness:** Maintain steady development; if heavy ground confrontation emerges, bolster ground army and economy while continuing tech.
- **late_midgame — Safe Development with Ground Defense Emphasis:** Continue safe development; if heavy ground confrontation, strengthen ground defense, economy, and expansion while maintaining production.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground: Defend and Expand

**When:** Late midgame, both sides have heavy ground-oriented postures. Opponent shows Zergling, Roach, Queen. Own army includes Siege Tank, Marine, Reaper, Marauder.

**Mistake → correction:** Overextending with ground forces without proper support, neglecting upgrades or production. → Strengthen ground army, increase defense, economy, and expansion. Continue production and technology.

**Why:** With both sides committed to ground, maintaining a strong defensive position while expanding economy supports a larger army. Siege tanks and marines provide a solid core.

**Read for full checks:** `N006`

### L02 — Early Ground Threat: Flexible Response

**When:** Early game, opponent shows a ground posture with Zergling. Own economy is moderate with heavy expansion.

**Mistake → correction:** Over-teching without sufficient army production, allowing opponent's Zerglings to punish greed. → Strengthen ground army, increase economy, increase expansion, continue production and technology.

**Why:** The opponent's ground posture suggests a potential ground-based army. Maintaining flexible development allows you to respond appropriately without overcommitting.

**Read for full checks:** `N010`

### L03 — Midgame Ground Clash: Solid Core

**When:** Midgame, both sides have heavy ground-oriented postures. Opponent shows Zergling, Hydralisk, Roach, Queen. Own army includes Marine.

**Mistake → correction:** Overextending without proper support, neglecting upgrades or production. → Strengthen ground army, increase economy, continue production and technology.

**Why:** With both sides committed to ground, maintaining a strong army composition is important. Marines provide a solid core, but consider adding supporting units like Marauders or Siege Tanks.

**Read for full checks:** `N012`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
