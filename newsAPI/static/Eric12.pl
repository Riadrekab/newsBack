:- dynamic all_time/0, at_work/0, not_at_work/0, weekend/0.
neg(at_work):- not_at_work.
rule(r1, careers, []):- neg(at_work).
rule(r2, sports, []):- neg(at_work).
rule(r3, careers, []):- at_work.
rule(r4, sports, []):- weekend.
rule(p1, prefer(r3, r1), []).
rule(p2, prefer(r4, r2), []).
complement(careers, sports).
complement(sports, careers).
