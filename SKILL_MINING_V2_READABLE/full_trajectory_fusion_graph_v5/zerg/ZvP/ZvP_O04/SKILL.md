# ZvP_O04 Expansion / Economy / Production

## Skill Identity

- Skill ID: ZvP_O04
- Matchup: Zerg vs Protoss
- Opening Family: expansion / economy / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg opening focused on early economy and expansion, with moderate production and light technology investment. The strategy aims to build a strong economic foundation while maintaining flexibility to adapt to Protoss tech choices.

Develop a expansion / economy / production posture while preserving flexibility for live observation-driven adaptation.

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

- **early_game — Early Economy and Ground Foundation:** Prioritize economy and ground army development, maintain production, and adapt technology based on scouting.
- **early_midgame — Early-Midgame Ground Reinforcement:** Reinforce ground forces, expand economy, and maintain production while scouting for tech adaptation.
- **midgame — Midgame Ground vs Ground:** Strengthen ground forces, add detection, and mix in counters to handle multiple threats.
- **late_midgame — Late-Midgame Air Transition:** Balance air and ground strength, add Corruptors for Void Ray counter, and sustain economy.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Detection and Composition vs Dark Templar

**When:** Midgame around 480 seconds, with both players having ground armies. Opponent shows Stalkers, Dark Templars, Warp Prisms, and Observers.

**Mistake → correction:** Neglecting detection and overcommitting to a single unit type, leaving your army vulnerable to Dark Templar harassment and lacking counters to Stalkers. → Continue strengthening your ground army and maintain economy. Add detection (e.g., Overseers) and mix in units that counter Stalkers and Dark Templars (e.g., Banelings).

**Why:** Dark Templars require detection to be fought effectively; a mixed composition with detection prevents devastating losses and handles multiple threats.

**Read for full checks:** `N003`

### L02 — Scouting and Tech Adaptation

**When:** Early-midgame around 300 seconds, with the opponent having a ground posture but no combat units observed. You have Zerglings and Queens.

**Mistake → correction:** Overcommitting to a single unit composition and neglecting scouting, leaving you unprepared for the opponent's heavy tech investment. → Continue developing your ground army and economy. Maintain production and consider increasing technology to match the opponent's heavy investment.

**Why:** The opponent's heavy tech suggests they may be teching to a specific unit; a strong economy and ground army allow you to adapt to whatever they produce.

**Read for full checks:** `N005`

### L03 — Countering Immortals and Warp Prism Drops

**When:** Midgame around 420 seconds, with the opponent having a ground army including Warp Prisms and Immortals. You have a ground army with Zerglings and Queens.

**Mistake → correction:** Relying solely on Roaches, which are countered by Immortals, and neglecting detection against Warp Prism drops. → Increase your production and expansion to support a larger army. Consider adding Roaches or Hydralisks to counter the Immortals and Warp Prisms.

**Why:** Immortals are strong against armored units; adding Roaches and Hydralisks provides effective counters and helps defend against drops.

**Read for full checks:** `N008`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
