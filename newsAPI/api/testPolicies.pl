:- dynamic nice_movie/0, friend_offer/0, long_time/0, it_rains/0, take_car/0.
rule(r1, go_resto, []):- friend_offer.
rule(r2, stay_home, []):- nice_movie.
rule(p1, prefer(r2, r1), []).
rule(p2, prefer(r1, r2), []):- long_time.
rule(c1, prefer(p2,p1), []).
rule(c2, prefer(p1,p2), []):- it_rains.
rule(c3, prefer(c2,c1), []).
rule(c4, prefer(c1,c2), []):- take_car.
rule(c5, prefer(c4,c3), []).
complement(go_resto, stay_home).
complement(stay_home, go_resto).