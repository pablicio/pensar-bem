import math

from sigmoide import sigmoide

for z in [0.5, 1, 2, 3]:
    print(z, math.isclose(sigmoide(-z), 1 - sigmoide(z)))
