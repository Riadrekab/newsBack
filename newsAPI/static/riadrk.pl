:- dynamic all_time/0, at_work/0, not_at_work/0, weekend/0.
neg(at_work):- not_at_work.
rule(r1, careers, []):- neg(at_work).
rule(r2, sports, []):- neg(at_work).
rule(r3, technology, []):- neg(at_work).
rule(r4, careers, []):- weekend.
rule(r5, sports, []):- at_work.
rule(r6, technology, []):- at_work.
rule(p1, prefer(r4, r1), []).
rule(p2, prefer(r5, r2), []).
rule(p3, prefer(r6, r3), []).
complement(careers, sports).
complement(careers, technology).
complement(sports, careers).
complement(sports, technology).
complement(technology, careers).
complement(technology, sports).
