k = 8.987e9

force :: (Integral q1, Integral q2, Integral dist) => q1 -> q2 -> dist -> Int
force q1 q2 dist = (k * q1 * q2) / (dist^2)

dist :: (Integral )