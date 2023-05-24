:- dynamic all_time/0, at_work/0, not_at_work/0, weekend/0.
neg(at_work):- not_at_work.
rule(r1, entertainment, []):- neg(at_work).
rule(r2, technology, []):- neg(at_work).
rule(r3, gaming, []):- neg(at_work).
rule(r4, entertainment, []):- all_time.
rule(r5, technology, []):- at_work.
rule(r6, gaming, []):- weekend.
rule(p1, prefer(r4, r1), []).
rule(p2, prefer(r5, r2), []).
rule(p3, prefer(r6, r3), []).
complement(entertainment, technology).
complement(entertainment, gaming).
complement(technology, entertainment).
complement(technology, gaming).
complement(gaming, entertainment).
complement(gaming, technology).
