# ZvZ_O04 Economy / Defense / Ground

## Skill Identity

- Skill ID: ZvZ_O04
- Matchup: Zerg vs Zerg
- Opening Family: economy / defense / ground opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg versus Zerg opening that emphasizes a heavy economy and a defensive ground posture, with moderate production and light technology investment in the early game. The plan is to develop safely while keeping options open for adaptation based on scouting.

Develop a strong economy and a solid ground defense while maintaining flexibility to transition into either a ground or air composition depending on the opponent's actions.

This is a strategic template, not a fixed build order. Adapt based on live scouting and enemy intelligence.

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

- **early_game — Early Ground Macro with Heavy Economy:** Prioritize economy and ground defense, maintain production, and adapt to scouting.
- **early_midgame — Early Midgame Economy and Ground:** Focus on economy and ground strength, maintain expansion, and stay alert for enemy aggression.
- **midgame — Midgame Ground Sustain:** Sustain ground army and economy, consider tech transitions, and maintain defense.
- **late_midgame — Late Midgame Ground Power:** Maintain ground strength, consider upgrades or tech, and keep economy stable.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground: Avoid Economy Complacency

**When:** Midgame, both players have heavy economies and heavy production. Opponent shows moderate tech and ground posture.

**Mistake → correction:** Tempting to just keep producing ground units and expanding economy without considering tech transitions or scouting for tech switches. → Continue to strengthen your ground army, maintain your economy and production, and keep your defense up. Consider adding tech when safe.

**Why:** With both players on heavy economies, the one who transitions more efficiently to a better composition will gain an advantage. Maintaining a strong ground army prevents being caught off guard.

**Read for full checks:** `N002`

### L02 — Late Midgame Ground: Avoid Tech Overcommitment

**When:** Late midgame, both players have heavy economies and heavy production. Opponent shows moderate tech and ground posture with Roach cues.

**Mistake → correction:** Tempting to over-invest in technology without sufficient army, or neglect scouting for tech switches. → Maintain your ground army and economy, continue to strengthen your ground forces, and consider adding upgrades or tech to gain an edge.

**Why:** With heavy tech, you can transition to a more powerful composition like Roach or Hydralisk. Maintaining a strong ground army keeps you safe while you tech up.

**Read for full checks:** `N004`

### L03 — Midgame vs Heavy Tech: Avoid Tech Race

**When:** Midgame, you have a heavy economy and heavy production, but the opponent shows heavy tech and a ground posture with Roach cues.

**Mistake → correction:** Tempting to over-invest in technology without sufficient army, or neglect scouting for tech switches. → Increase your defense and economy, continue your production and tech, and strengthen your ground army. Stabilize and prepare for a potential engagement.

**Why:** The opponent has heavy tech, so you need to ensure your army composition can handle theirs. Increasing defense and economy gives you the resources to tech up and outproduce them.

**Read for full checks:** `N005`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
