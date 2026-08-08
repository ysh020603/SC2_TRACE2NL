# Summary

## Applicability
This skill is designed for Zerg against Protoss.
Base family: `roach_hydra` / archetype `roach_hydra`.

## Core Objective
Play roach hydra as Zerg vs Protoss, adapting the next 60–120s macro queue to observable enemy style tags.

## Default Opening Policy
- Open Hatch/Pool/gas into Roach Warren.
- Add Hydralisk Den after Lair or when ground anti-air is required.
- Keep Drone count healthy before mass Hydra.

## Phase Identification
- Opening: roughly 0–210s from game time, incomplete core production/tech.
- Response: 210–420s once enemy intelligence shows expand/tech/army bias.
- Transition: after core composition exists; scale economy or shift tech.
- Infer phase only from game time, Completed, Under Construction, Active Queues, and unit structure.

## Observable Opponent Responses
1. If Opponent shows air tech or high-tech commitment.
   - Add anti-air units/tech appropriate to your race (Vikings/Thors, Stalkers/Void, Hydra/Spore).
   - Keep a ground baseline while tech completes.
   - Do not ignore anti-air while continuing pure ground all-in.
   - Evidence: n=75, wr=0.3733333333333333, grade=C
2. If Opponent invests in early static defense.
   - Favor efficient tech/units that beat static lines; keep expanding if safe.
   - Do not mirror unnecessary static defense.
   - Evidence: n=42, wr=0.4523809523809524, grade=D
3. If Opponent has multiple production structures.
   - Increase your own production or tighten tech that enables higher army quality.
   - Evidence: n=27, wr=0.3703703703703703, grade=D
4. If Opponent looks like standard macro.
   - Follow default opening policy for this decision window.
   - Evidence: n=20, wr=0.4, grade=D
5. If Opponent shows one-base high production pressure.
   - Prioritize unit production and static/tech defense prerequisites over third base.
   - Delay greedy tech that does not help immediate survival.
   - Do not queue a greedy third base this decision window.
   - Evidence: n=17, wr=0.2352941176470588, grade=D

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
