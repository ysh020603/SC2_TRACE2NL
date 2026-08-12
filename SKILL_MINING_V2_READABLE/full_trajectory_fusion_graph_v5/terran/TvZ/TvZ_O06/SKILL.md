# TvZ_O06 Technology / Economy / Expansion

## Skill Identity

- Skill ID: TvZ_O06
- Matchup: Terran vs Zerg
- Opening Family: technology / economy / expansion opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Terran opening that prioritizes heavy technology investment and economic expansion while maintaining a ground-oriented army. The early game focuses on building a strong infrastructure and tech base, with production ramping up through the midgame. The approach is flexible, allowing adaptation based on scouting information.

Develop a technology / economy / expansion posture while preserving flexibility for live observation-driven adaptation.

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

- **early_game — Early Ground Macro with Heavy Tech:** Develop economy and tech, strengthen ground army, maintain defenses, expand cautiously.
- **early_midgame — Midgame Ground Strength and Expansion:** Strengthen ground army, expand, maintain production and tech, add Siege Tanks if needed.
- **midgame — Midgame Tech and Army Consolidation:** Strengthen ground army, increase tech, maintain production, expand if safe, keep defenses.
- **late_midgame — Late-Midgame Stabilization and Anti-Air:** Stabilize defenses, strengthen ground army, add anti-air, continue economy and tech.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid overextending economy without defense

**When:** Early-midgame (around 240-300s) with own heavy production and tech, ground army. Opponent still ground macro with moderate production and light tech.

**Mistake → correction:** Overextending your economy without sufficient army to defend, or neglecting scouting for tech switches or all-ins. → Continue strengthening your ground army and expanding. Maintain production and tech progression. Consider adding Siege Tanks or other tech units to your composition.

**Why:** Your heavy production and tech give you a potential army quality advantage. Expanding further will secure your economy for the long game.

**Read for full checks:** `N002`

### L02 — Avoid falling behind in tech or upgrades

**When:** Midgame (around 420-480s) with own heavy ground army, heavy production and tech. Opponent has heavy production and tech, still ground-oriented.

**Mistake → correction:** Falling behind in tech or army upgrades, or over-committing to a single composition without scouting for tech switches. → Continue to strengthen your ground army and increase tech. Maintain production and consider adding more expansions if needed. Keep defenses strong.

**Why:** With both players having heavy economies, tech and army quality become decisive. Your Siege Tanks provide a strong defensive and offensive tool.

**Read for full checks:** `N003`

### L03 — Avoid overextending without scouting for all-ins

**When:** Early game (around 180s) with own heavy production and tech, ground army. Opponent similar to N001 but with lighter defense.

**Mistake → correction:** Overextending your economy without sufficient army to defend, or neglecting scouting for potential all-ins. → Maintain your production and tech, but consider applying light pressure to exploit the opponent's light defense. Continue expanding.

**Why:** Your heavy production can allow you to field a larger army quickly. Pressuring the opponent can disrupt their macro while you continue to develop.

**Read for full checks:** `N004`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
