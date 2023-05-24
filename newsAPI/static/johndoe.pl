:- dynamic all_time/0, at_work/0, not_at_work/0, weekend/0.
neg(at_work):- not_at_work.
rule(r1, fitness, []):- neg(at_work).
rule(r2, culture, []):- neg(at_work).
rule(r3, science, []):- neg(at_work).
rule(r4, fitness, []):- weekend.
rule(r5, culture, []):- at_work.
rule(r6, science, []):- weekend.
rule(p1, prefer(r4, r1), []).
rule(p2, prefer(r5, r2), []).
rule(p3, prefer(r6, r3), []).
complement(fitness, culture).
complement(fitness, science).
complement(culture, fitness).
complement(culture, science).
complement(science, fitness).
complement(science, culture).
