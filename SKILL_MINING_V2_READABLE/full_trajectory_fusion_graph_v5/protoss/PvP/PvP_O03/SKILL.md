# PvP_O03 Technology / Defense / Economy

## Skill Identity

- Skill ID: PvP_O03
- Matchup: Protoss vs Protoss
- Opening Family: technology / defense / economy opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Protoss versus Protoss opening that prioritizes heavy technology investment, a solid defensive posture, and a growing economy. The early game is characterized by moderate production and an unknown army composition, with the flexibility to transition into either a ground or air-oriented midgame depending on scouting information.

Develop a technology / defense / economy posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

## Strategic Characteristics

- Economy: moderate
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

- **early_game — Early Game Stabilization:** Focus on economy and tech, keep defense up, build a flexible ground core, and be ready to adapt to air if needed.
- **early_midgame — Early-Midgame Ground Commitment:** Build up ground forces, keep economy and tech growing, maintain defense, and watch for air transitions.
- **midgame — Midgame Air Transition:** Build up air forces, keep economy strong, maintain defense, and be ready to adapt if opponent counters.
- **late_midgame — Late-Midgame Air Integration:** Add air units to your ground army, keep economy and defense up, and stay flexible.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground: Avoid Overcommitting Without Anti-Air

**When:** Midgame (7-9 minutes), opponent shows ground posture (Zealots, Stalkers), your army is ground-oriented with Zealots and Immortals.

**Mistake → correction:** Tempting to blindly strengthen ground forces and continue production without considering anti-air, risking vulnerability to an air transition. → Continue strengthening ground army and economy, but maintain defensive posture and consider adding tech like High Templar for spell support.

**Why:** Ground army with Immortals is strong vs enemy ground, especially armored units. Solid economy enables further tech and expansion.

**Read for full checks:** `N004`

### L02 — Ground vs Ground with Oracles: Avoid Ignoring Spell Support

**When:** Late-midgame (10-12 minutes), opponent shows ground posture (Zealots, Stalkers, Immortals, Oracles), your army is ground-oriented with Zealots.

**Mistake → correction:** Tempting to continue pure ground production without adding spell casters, missing opportunities to counter enemy composition. → Continue strengthening ground army and economy, but add tech like High Templar for spell support and maintain defensive posture.

**Why:** Zealots alone can be countered; High Templar provide spell support and improve composition. Economy allows further tech and expansion.

**Read for full checks:** `N007`

### L03 — Air vs Air: Avoid Neglecting Ground Defense

**When:** Late-midgame (10-12 minutes), opponent shows air posture (Zealots, Stalkers, Void Rays, Oracles), your army is air-oriented with Void Rays.

**Mistake → correction:** Tempting to overcommit to air units without ensuring ground defense, risking vulnerability to ground transitions. → Continue strengthening air army and economy, but maintain defensive posture and consider adding tech like Tempests for late-game.

**Why:** Air army with Void Rays is powerful vs air-oriented opponent. Strong economy enables further tech and expansion.

**Read for full checks:** `N009`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
