# Summary

## Applicability
This skill is designed for Zerg against Zerg.
Base family: `mutalisk` / archetype `mutalisk`.

## Core Objective
Play mutalisk as Zerg vs Zerg, adapting the next 60–120s macro queue to observable enemy style tags.

## Default Opening Policy
- Hatch-first into Lair and Spire.
- Secure second gas before Mutalisk mass.
- Keep enough Queens/Spores if enemy air pressure appears first.

## Phase Identification
- Opening: roughly 0–210s from game time, incomplete core production/tech.
- Response: 210–420s once enemy intelligence shows expand/tech/army bias.
- Transition: after core composition exists; scale economy or shift tech.
- Infer phase only from game time, Completed, Under Construction, Active Queues, and unit structure.

## Observable Opponent Responses
1. If Opponent commits Factory ground or Roach-style composition.
   - Adjust composition toward suitable counters (Immortals/Tanks/Roach-Hydra as fits).
   - Evidence: n=153, wr=0.5228758169934641, grade=C
2. If Opponent looks like standard macro.
   - Follow default opening policy for this decision window.
   - Evidence: n=126, wr=0.492063492063492, grade=C
3. If Opponent invests in early static defense.
   - Favor efficient tech/units that beat static lines; keep expanding if safe.
   - Do not mirror unnecessary static defense.
   - Evidence: n=99, wr=0.5151515151515151, grade=C
4. If Opponent is expanding quickly with lower immediate pressure.
   - Avoid over-investing in static defense.
   - Match economy: take or secure your next expansion if supply and production allow.
   - Do not all-in with incomplete production.
   - Evidence: n=13, wr=0.5384615384615384, grade=D
5. If Opponent shows one-base high production pressure.
   - Prioritize unit production and static/tech defense prerequisites over third base.
   - Delay greedy tech that does not help immediate survival.
   - Do not queue a greedy third base this decision window.
   - Evidence: n=9, wr=0.6666666666666666, grade=D

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
