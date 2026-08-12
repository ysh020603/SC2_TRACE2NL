# PvP_O05 Technology / Economy / Expansion

## Skill Identity

- Skill ID: PvP_O05
- Matchup: Protoss vs Protoss
- Opening Family: technology / economy / expansion opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Protoss versus Protoss opening that emphasizes heavy technology investment, a strong economy, and expansion while keeping production moderate early. The strategic template is flexible, allowing adaptation to either a ground or air transition based on live observations.

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
- For Protoss, spend through completed powered compatible producers before adding capacity; preserve opening tempo and never force a new facility solely from a clock threshold.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Tech and Economy Focus:** Prioritize tech and economy, keep production moderate, expand, and avoid early army overcommitment.
- **early_midgame — Ground Development with Heavy Tech:** Focus on ground army strength, keep economy and tech developing, maintain expansion and production.
- **midgame — Midgame Ground Macro with Immortal Support:** Strengthen ground with Immortals, maintain economy and expansion, watch for air transition or timing.
- **late_midgame — Late-Mid Ground Army with Observer and Immortal:** Strengthen ground with Immortals, ensure detection, maintain economy and expansion, watch for air or splash needs.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid neglecting detection or anti-air when both sides are heavy ground

**When:** Midgame, both sides have heavy ground armies and heavy tech. Own army includes Stalkers and Immortals, opponent shows Zealot cues.

**Mistake → correction:** Continuing to strengthen ground and expand without ensuring detection or anti-air, risking a surprise transition to air units like Oracles or Void Rays. → Continue strengthening your ground army, adding more Immortals and supporting units. Keep expanding and increasing your economy.

**Why:** Immortals are strong against Zealot-heavy ground compositions common in PvP. Maintaining a heavy economy allows you to outproduce the opponent.

**Read for full checks:** `N002`

### L02 — Avoid over-investing in army early when opponent is unknown

**When:** Early game, both sides have heavy economy and technology, but no clear army composition yet. No reliable combat-unit cues from the opponent.

**Mistake → correction:** Making a large army investment too early, which may delay your tech and economy. → Focus on developing your economy and technology while maintaining a flexible army composition. Continue expanding and increasing production.

**Why:** In the early game, investing in tech and economy sets up a strong midgame. Keeping options open allows you to react to the opponent's first moves.

**Read for full checks:** `N003`

### L03 — Avoid being too passive when opponent has heavy ground and detection

**When:** Late-midgame, both sides have heavy ground armies and heavy tech. Own army includes Stalkers, Observers, and Immortals, opponent shows Stalker, Sentry, WarpPrism, Observer cues.

**Mistake → correction:** Being too passive, allowing the opponent to build up for a timing attack. → Continue strengthening your ground army, adding more Immortals and ensuring you have detection. Maintain your economy and expansion.

**Why:** Observers provide detection against potential cloaked units, while Immortals are strong against armored ground units. A heavy economy allows you to sustain a large army.

**Read for full checks:** `N005`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
