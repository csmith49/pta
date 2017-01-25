from terms import *

print("<==== Testing positions ====>")
print("Instance creation: {p}".format(p=Position(1, 2, 3)))
p = Position()
print("Recognizing empty position: p = {p}, empty? = {empty}".format(p=p, empty=p.is_root()))
p1 = Position(1, 2)
p2 = Position(1, 2, 3)
p3 = Position(1, 3)
print("{x} <= {y} <= {z}? {check}".format(x=p1, y=p2, z=p3, check=(p1 < p2 and p2 < p3)))

print("<==== Testing Terms ====>")
t1 = Term(1)
t2 = Term('f', 1, 2)
print(t1)
print(t2)
