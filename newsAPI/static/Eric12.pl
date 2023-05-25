:- dynamic all_time/0, at_work/0, not_at_work/0, weekend/0.
neg(at_work):- not_at_work.
rule(r1, sports, []):- neg(at_work).
rule(r2, technology, []):- neg(at_work).
rule(r3, sports, []):- weekend.
rule(r4, technology, []):- at_work.
rule(p1, prefer(r3, r1), []).
rule(p2, prefer(r4, r2), []).
complement(sports, technology).
complement(technology, sports).
