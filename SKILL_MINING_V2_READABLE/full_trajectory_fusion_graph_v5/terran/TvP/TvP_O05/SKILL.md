# TvP_O05 Technology / Economy / Upgrade

## Skill Identity

- Skill ID: TvP_O05
- Matchup: Terran vs Protoss
- Opening Family: technology / economy / upgrade opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Terran opening that emphasizes heavy technology and economy development while maintaining a flexible ground-oriented posture. The opening is designed to support a strong mid-game transition with upgrades and production, while keeping options open for adaptation based on scouting.

Develop a technology / economy / upgrade posture while preserving flexibility for live observation-driven adaptation.

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

- **early_game — Early Game Heavy Economy and Technology Development:** Prioritize economy and tech, keep ground army flexible, and scout for opponent's tech direction.
- **early_midgame — Early-Mid Ground Macro with Heavy Economy:** Focus on ground army and economy, expand, and keep tech developing; watch for air transition.
- **midgame — Mid-Game Ground Macro with Heavy Economy:** Maintain ground army and economy, keep tech and defense, and stay alert for air threats.
- **late_midgame — Late-Mid Ground Defense and Development:** Boost defense, keep ground army strong, and maintain economy and tech; watch for air.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid over-committing to a single attack without scouting

**When:** Early-midgame, around 4 minutes, both sides have heavy economy and production, opponent likely ground with Zealots/Stalkers, you have Marines/Marauders.

**Mistake → correction:** Over-committing to a single attack without scouting, neglecting anti-air, or over-investing in ground without flexibility. → Continue strengthening your ground army while increasing economy and expansions. Maintain current defense and technology development.

**Why:** Both sides are in a macro-oriented phase. Maintaining a strong economy and production allows you to out-scale the opponent if they commit to a ground composition.

**Read for full checks:** `N001`

### L02 — Avoid over-extending economy without sufficient army

**When:** Early game, around 3 minutes, you have ground army of Marines/Marauders, heavy economy, opponent posture unknown but heavy economy.

**Mistake → correction:** Over-extending your economy without sufficient army, or neglecting scouting to identify opponent's tech path. → Increase your production and continue developing your ground army. Maintain your economy and technology development.

**Why:** With a ground army already established, it is efficient to continue producing units and expanding your economy to support a strong mid-game.

**Read for full checks:** `N004`

### L03 — Avoid neglecting anti-air against air transition

**When:** Early-midgame, around 5 minutes, opponent has transitioned to air with Oracles/Zealots, you have ground army with Marines/Marauders.

**Mistake → correction:** Neglecting your ground army in favor of anti-air, or being caught off guard by Oracle harassment. → Maintain your ground army while considering adding anti-air capabilities. Continue developing your economy and technology.

**Why:** The opponent's air presence requires you to prepare for potential Oracle harassment or a transition to a more air-heavy composition.

**Read for full checks:** `N006`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
