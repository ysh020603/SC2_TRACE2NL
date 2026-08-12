# TvT_O07 Technology/Economy/Production

## Skill Identity

- Skill ID: TvT_O07
- Matchup: Terran vs Terran
- Opening Family: Technology/Economy/Production
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Terran mirror opening that emphasizes heavy technology and economy investment while maintaining moderate production. The early game is characterized by an unknown army posture, with a focus on developing infrastructure and teching up. As the game progresses, the posture becomes ground-oriented with heavy production and technology, and the strategic goal is to build a strong economy and tech base while remaining flexible to adapt to the opponent's actions.

Develop a technology/economy/production posture while preserving flexibility for live observation-driven adaptation.

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

- **early_game — Tech-Focused Economy with Ground Baseline:** Prioritize economy and tech, keep ground defense, avoid early army overcommitment.
- **early_midgame — Ground Macro with Heavy Production and Tech:** Balance economy, tech, and ground army; keep defenses solid, adapt to enemy moves.
- **midgame — Defensive Ground Siege with Economy Focus:** Hold position with siege tanks, keep economy growing, prepare for potential air threats.
- **late_midgame — Ground Strength with Air Support:** Keep ground army strong, add anti-air, stay defensive, adapt to enemy air commitment.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid premature army investment

**When:** Early game, around 180 seconds, when both players have unknown army postures but heavy technology investment, and your production is moderate while the opponent's is heavy.

**Mistake → correction:** Committing to a large army before knowing the enemy's plan, which can leave you vulnerable to tech switches or economic deficits. → Focus on increasing your economy and expansion while continuing technology development. Strengthen ground forces as a baseline and maintain a defensive posture.

**Why:** With the opponent's army unknown, building a solid economy and tech base allows flexibility to adapt to whatever the opponent reveals.

**Read for full checks:** `N002`

### L02 — Avoid passivity and unsieged engagements

**When:** Midgame, around 420-540 seconds, when both players have ground-oriented macro postures with heavy production and technology, and the opponent shows siege tanks and marines.

**Mistake → correction:** Being too passive, allowing the opponent to gain an economic advantage, or engaging without proper siege setup. → Increase defensive capabilities while continuing to strengthen ground forces. Maintain economy and expansion, and consider adding siege tanks to your composition.

**Why:** With both sides having heavy ground armies, a defensive posture with siege tanks helps hold position while teching and expanding, outlasting the opponent in a macro game.

**Read for full checks:** `N003`

### L03 — Avoid neglecting air defense

**When:** Late midgame, around 600 seconds, when both players have ground-oriented macro postures with heavy production and technology, and the opponent has medivacs while your air presence is light.

**Mistake → correction:** Neglecting air defense, leaving you vulnerable to Medivac drops and healing. → Continue strengthening ground forces while adding air support or anti-air capabilities to counter medivacs. Maintain defensive posture and economy.

**Why:** The opponent's medivacs provide mobility and healing, so adding air units or anti-air helps deal with drops and sustain in engagements.

**Read for full checks:** `N004`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
