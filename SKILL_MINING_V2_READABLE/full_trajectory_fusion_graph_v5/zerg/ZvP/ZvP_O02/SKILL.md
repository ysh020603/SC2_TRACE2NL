# ZvP_O02 Economy / Expansion / Ground

## Skill Identity

- Skill ID: ZvP_O02
- Matchup: Zerg vs Protoss
- Opening Family: economy / expansion / ground opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg opening that prioritizes economy and expansion while maintaining a flexible ground-oriented posture. Early information is limited, so the plan emphasizes safe development and adaptation based on scouting.

Develop a strong economy and expand while keeping a ground army core, preserving flexibility to respond to Protoss tech or pressure.

This is a strategic template, not a fixed build order. Adjust based on live scouting and enemy actions.

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
- For Zerg, production capacity is bases plus larva/inject throughput; Overlords and Drones consume the same larva as army, so do not translate facility-count rules from other races.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Early Game Heavy Economy:** Maintain economy and scouting, avoid overcommitting, adapt based on enemy tech.
- **early_midgame — Early-Midgame Unknown Posture:** Maintain development, scout, avoid overcommitment, adapt to enemy info.
- **midgame — Midgame Unknown Posture:** Maintain development, scout, avoid overcommitment, adapt to enemy info.
- **late_midgame — Late-Midgame Unknown Posture:** Maintain development, scout, avoid overcommitment, adapt to enemy info.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground: Avoid Straight-Up Fight

**When:** Midgame, enemy scouted as ground-heavy with Zealots, Stalkers, Sentries, possibly Immortals; your army is ground-based with Zerglings, Roaches, Queens.

**Mistake → correction:** Engaging in a straight-up fight without proper army composition, or over-investing in economy at the expense of defense. → Strengthen your ground army, continue teching, and add units that counter the enemy's composition (e.g., Roaches against Zealots/Stalkers).

**Why:** Matching the enemy's ground strength is necessary to hold off potential pushes and maintain map control.

**Read for full checks:** `N004`

### L02 — Unknown Enemy: Avoid Overcommitting Without Scouting

**When:** Early-midgame, enemy shows heavy economy and tech investment with moderate production; your army is ground-based with Zerglings and Queens.

**Mistake → correction:** Over-committing to an attack without knowing the opponent's composition, or neglecting scouting to confirm their greed. → Increase your economy and tech, strengthen your ground army, and keep scouting to identify the enemy's plan.

**Why:** Matching the enemy's economy and tech is important to avoid falling behind, while maintaining a defensive ground army.

**Read for full checks:** `N006`

### L03 — Stalker Ground: Avoid Straight-Up Fight

**When:** Early-midgame, enemy scouted with Stalkers and a heavy ground posture; your army is ground-based with Zerglings and Queens.

**Mistake → correction:** Engaging in a straight-up fight without proper army composition, or over-investing in economy at the expense of defense. → Strengthen your ground army, continue teching, and consider adding units that counter the enemy's composition (e.g., Roaches against Stalkers).

**Why:** Matching the enemy's ground strength is necessary to hold off potential pushes and maintain map control.

**Read for full checks:** `N007`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
