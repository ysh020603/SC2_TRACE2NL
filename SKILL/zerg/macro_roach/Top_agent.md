# Summary

## Applicability
This skill is designed for Zerg against Terran.
Base family: `macro_roach` / archetype `macro_roach`.

## Core Objective
Play macro roach as Zerg vs Terran, adapting the next 60–120s macro queue to observable enemy style tags.

## Default Opening Policy
- 0-180s: Hatch-first economy into Spawning Pool and gas.
- 180-360s: Roach Warren; Roaches + Queens; natural expand secure.
- Lair only after Roach baseline unless air scouting demands it.

## Phase Identification
- Opening: roughly 0–210s from game time, incomplete core production/tech.
- Response: 210–420s once enemy intelligence shows expand/tech/army bias.
- Transition: after core composition exists; scale economy or shift tech.
- Infer phase only from game time, Completed, Under Construction, Active Queues, and unit structure.

## Observable Opponent Responses
1. If Opponent is expanding quickly with lower immediate pressure.
   - Avoid over-investing in static defense.
   - Match economy: take or secure your next expansion if supply and production allow.
   - Do not all-in with incomplete production.
   - Evidence: n=9626, wr=0.4479534593808435, grade=A
2. If Opponent has multiple production structures.
   - Increase your own production or tighten tech that enables higher army quality.
   - Evidence: n=7429, wr=0.5275272580428052, grade=A
3. If Opponent invests in early static defense.
   - Favor efficient tech/units that beat static lines; keep expanding if safe.
   - Do not mirror unnecessary static defense.
   - Evidence: n=4678, wr=0.5156049593843522, grade=A
4. If Opponent commits Factory ground or Roach-style composition.
   - Adjust composition toward suitable counters (Immortals/Tanks/Roach-Hydra as fits).
   - Evidence: n=4328, wr=0.4410813308687615, grade=A
5. If Opponent shows one-base high production pressure.
   - Prioritize unit production and static/tech defense prerequisites over third base.
   - Delay greedy tech that does not help immediate survival.
   - Do not queue a greedy third base this decision window.
   - Evidence: n=2905, wr=0.5376936316695353, grade=A

## Composition Transition
- After core composition is online, scale economy or add the next tech tier only with visible prerequisites.

## Economy And Production Scaling
- Expand when mineral bank is high and production is saturated.
- If resources bank while army is small, add production before luxury tech.
- Stop further expand under clear one-base pressure tags.

## Abandon Conditions
- If chosen tech has no supporting units/buildings after a full decision cycle, replace unstarted luxury tech in the next queue.
- If enemy composition hard-counters the current tech path and anti-counter tech is available, pivot next 60–120s.

## Invariants
- Never issue attack, scout, spell, or positioning commands.
- Do not repeat actions already Under Construction or in Active Queues.
- Keep worker production unless supply-blocked or under lethal pressure.
- Use exact canonical macro unit/building names only.
