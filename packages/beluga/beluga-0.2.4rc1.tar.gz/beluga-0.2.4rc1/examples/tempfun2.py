from beluga.liepack.domain.liealgebras import so
from beluga.liepack import Commutator

g = so(3)

basis = g.basis()

x = basis[0]
y = basis[1]
z = basis[2]

adx = Commutator(x)

print(adx(y) == z) # This is true since [x,y] = z
print(adx(z) == -y) # This is true since [x,z] = -y
print(adx(y, anticommutator=-1) == z) # This is false since the result isn't even in so(3)
print(adx(y) == z) # This is true since [x,y] = z but it's also not affected by the line above
print(Commutator().map(x,y) == z) # This is true, and similar to using bvpsol().solve(guess)