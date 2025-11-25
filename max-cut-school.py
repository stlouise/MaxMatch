import numpy as np
import dimod

J= { (0,1):2.0, (0,2):2, (1,3):2, \
(2,3):2.0, (2,4):2.0, \
(3,4):2.0}
h= { 0:-2.0, 1:-2.0, 2:-3.0, 3:-3.0, 4:-2.0 }
model = dimod.BinaryQuadraticModel(h, J, 0.0, dimod.BINARY)

sampler = dimod.SimulatedAnnealingSampler()
response = sampler.sample(model, num_reads=100)
print("The solution with simulated annealing is")
summaryres= response.aggregate()
print()
for i in summaryres.record:
	print(i)
