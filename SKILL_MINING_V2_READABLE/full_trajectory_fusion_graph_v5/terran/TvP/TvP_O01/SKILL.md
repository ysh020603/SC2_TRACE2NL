# TvP_O01 Technology / Economy / Production

## Skill Identity

- Skill ID: TvP_O01
- Matchup: Terran vs Protoss
- Opening Family: technology / economy / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A macro-oriented opening that prioritizes heavy technology and economy development while maintaining moderate production. The strategic template emphasizes flexible adaptation based on live observation rather than a fixed build order.

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

- **early_game — Early Tech/Economy Development:** Focus on economy and tech, keep production steady, build ground forces for safety.
- **early_midgame — Ground Macro with Heavy Tech:** Strengthen ground forces, expand economy, keep tech advancing, and maintain defensive readiness.
- **midgame — Ground Defense vs Colossus:** Boost defense against Colossus, keep ground army strong, and adapt tech to counter threats.
- **late_midgame — Ground with Air Support:** Add air units for support, keep ground forces strong, and continue tech and defense.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid premature army commitment

**When:** Early game, around 180 seconds, with unknown enemy posture and heavy tech investment.

**Mistake → correction:** Committing to a large army before knowing the opponent's plan, or over-expanding without defense. → Focus on developing economy and tech while maintaining production. Strengthen ground army as a baseline.

**Why:** Early game is about establishing a strong economy and tech base. A ground-oriented army provides flexibility against unknown enemy tech.

**Read for full checks:** `N002`

### L02 — Balance expansion with defense

**When:** Early-midgame, around 240 seconds, with ground-oriented posture and heavy production.

**Mistake → correction:** Neglecting defense while expanding, or committing to a single tech path without information. → Continue strengthening ground army and increase production. Maintain expansion and tech progression.

**Why:** Heavy production allows a strong ground army. Continuing to expand and tech gives a long-term advantage.

**Read for full checks:** `N003`

### L03 — Maintain defense while developing

**When:** Early-midgame, around 360 seconds, with ground-oriented posture and enemy ground cues.

**Mistake → correction:** Continuing to expand and tech without reinforcing the army, assuming the enemy is passive. → Maintain defensive posture while continuing to develop ground army. Increase economy and tech.

**Why:** Siege Tanks provide strong defensive capabilities against ground pushes. Maintaining defense while expanding gives a safe economy.

**Read for full checks:** `N005`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
