# ZvP_O03 Economy / Expansion / Upgrade

## Skill Identity

- Skill ID: ZvP_O03
- Matchup: Zerg vs Protoss
- Opening Family: economy / expansion / upgrade opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg opening focused on heavy economy and expansion while maintaining a ground-oriented army. The build is flexible, allowing adaptation to Protoss tech choices.

Develop a strong economy and expansion lead while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

## Strategic Characteristics

- Economy: heavy
- Production: moderate
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
- For Zerg, production capacity is bases plus larva/inject throughput; Overlords and Drones consume the same larva as army, so do not translate facility-count rules from other races.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Early Game Ground Macro with Heavy Economy:** Prioritize economy and expansion while keeping a modest ground force for safety.
- **early_midgame — Early-Midgame Ground Macro with Heavy Economy:** Balance economy growth with ground army strength, adapting to opponent cues.
- **midgame — Midgame Ground Macro with Heavy Tech:** Maintain strong economy and tech while reinforcing ground army, with anti-air readiness.
- **late_midgame — Late-Midgame Ground Macro with Heavy Tech:** Continue economic and tech growth while reinforcing ground forces.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Keep pace with opponent's tech while maintaining ground strength

**When:** Midgame, around 480 seconds, when you have a ground army with Zerglings and Queens, heavy production but moderate technology, and the opponent shows a ground posture with Stalkers, Sentries, and Warp Prisms.

**Mistake → correction:** Focusing solely on strengthening your ground army and continuing economy without advancing your technology, risking falling behind in tech and being vulnerable to warp prism harass. → Maintain your current production and economy, and continue developing your technology. Keep your ground army strong.

**Why:** The opponent's heavy tech and production require you to keep pace. Maintaining a solid economy and production will allow you to tech up without falling behind.

**Read for full checks:** `N004`

### L02 — Balance economy, tech, and ground strength in late midgame

**When:** Late midgame, around 600-720 seconds, when you have a ground army with Zerglings, Roaches, and Queens, heavy production and technology, and the opponent shows a ground posture with Zealots, Stalkers, and Sentries.

**Mistake → correction:** Neglecting economy or upgrades, or overcommitting to a single attack if the opponent is defending well, while only focusing on strengthening ground forces. → Increase your economy and technology, continue expanding and producing. Strengthen your ground army further.

**Why:** The opponent's composition is strong on the ground, so you need to maintain a powerful ground force and tech to counter their upgrades.

**Read for full checks:** `N005`

### L03 — Prepare anti-air while maintaining ground and economy

**When:** Midgame, around 420 seconds, when you have a ground army with Zerglings, Roaches, and Queens, moderate production but heavy technology, and the opponent shows an air posture with Void Rays and Oracles.

**Mistake → correction:** Ignoring the air threat and overcommitting to ground units without anti-air support, while focusing on strengthening ground and increasing economy. → Increase your economy and technology, continue expanding and producing. Strengthen your ground army and prepare for air threats.

**Why:** The opponent's air composition requires you to tech into anti-air units while maintaining a strong economy.

**Read for full checks:** `N010`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
