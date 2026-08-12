# PvZ_O01 Technology / Economy / Upgrade

## Skill Identity

- Skill ID: PvZ_O01
- Matchup: Protoss vs Zerg
- Opening Family: technology / economy / upgrade opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Protoss opening that emphasizes heavy technology and economy development while maintaining moderate production. The early game is flexible, with the option to transition into either a ground or air-oriented army based on scouting and game flow. The focus is on establishing a strong economic and technological foundation before committing to a specific army composition.

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
- For Protoss, spend through completed powered compatible producers before adding capacity; preserve opening tempo and never force a new facility solely from a clock threshold.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Flexible Tech-Economy Foundation:** Prioritize economy and tech, keep ground baseline, increase production, expand cautiously, adapt to scouting.
- **early_midgame — Ground Army Development with Tech Lead:** Strengthen ground, increase production, expand, adapt to enemy tech with air branch if needed.
- **midgame — Ground Army Consolidation with Tech Options:** Consolidate ground, add tech units, use Warp Prism, adapt to enemy air with air branch.
- **late_midgame — Late-Midgame Ground Army with Tech Transition:** Strengthen ground, add Colossi/High Templar, use Void Rays for support, maintain economy.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid neglecting army while teching

**When:** Early game around 3 minutes, with heavy economy and technology investment, but army composition not yet defined. Opponent likely on ground macro with Zergling/Queen presence.

**Mistake → correction:** Focusing solely on economy and technology while ignoring production and army composition, leaving you vulnerable to early Zergling pressure. → Continue developing economy and technology, but maintain a flexible army composition. Strengthen ground forces as a baseline, and adapt based on scouting information.

**Why:** This opening prioritizes a strong economic and technological foundation. By not committing to a specific army composition early, you retain flexibility to respond to the opponent's strategy. Strengthening ground forces provides a safe baseline against early pressure.

**Read for full checks:** `N001`

### L02 — Avoid overcommitting to one unit type

**When:** Late-midgame around 10-12 minutes, with a strong ground army and heavy economy/technology. Opponent remains on ground posture with Zerglings, Queens, and Overseers.

**Mistake → correction:** Overcommitting to a single unit type, such as only Immortals and Void Rays, which can be countered if the opponent tech switches to air or mass ground units. → Continue strengthening your ground army and maintain your economic and technological advantage. Consider adding Colossi or High Templar for additional splash damage and spellcasting. Use your Void Rays to harass and provide air support.

**Why:** The opponent's army is still ground-heavy, and your Immortals and Void Rays provide good damage against armored units. Your heavy economy allows you to tech into Colossi or High Templar for a powerful late-game composition.

**Read for full checks:** `N004`

### L03 — Avoid over-committing before scouting

**When:** Early game around 3 minutes, with heavy economy and technology, but no clear army composition. Opponent has a ground posture with no reliable combat-unit cues.

**Mistake → correction:** Over-committing to a specific army composition before scouting the opponent's tech path, or neglecting defense while focusing on economy. → Continue developing economy and technology while maintaining a flexible army composition. Increase production to prepare for the midgame, and consider expanding further to secure your economy.

**Why:** With a heavy economy and technology, you can afford to invest in a strong midgame army. By not committing to a specific composition early, you retain flexibility to counter the opponent's strategy.

**Read for full checks:** `N005`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
