import numpy as np
import dimod


# We will start with a simple case for linear equation: (x1-x2+1=0)^(2x1-x2-1=0)

J = {(0,1):5,(0,2):-3/2,(0,3):-3,(1,2):-3,(1,3):-6,(2,3):2}

h = {0:5/2,1:4,2:-3/2,3:-3}
model = dimod.BinaryQuadraticModel(h, J, 0.0, dimod.SPIN)

print("The model that we are going to solve is")
print(model)
print()

# We can solve it exactly


from dimod.reference.samplers import ExactSolver
sampler = ExactSolver()
solution = sampler.sample(model)
print("The exact solution is")
print(solution)
print()


# Or with *simulated annealing* (a heuristic method used in classical computers)


sampler = dimod.SimulatedAnnealingSampler()
response = sampler.sample(model, num_reads=10)
print("The solution with simulated annealing is")
print(response)
print()


# And, of course, with D-Wave's quantum computer 


from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = EmbeddingComposite(DWaveSampler(solver='Advantage_system5.3'))
sampler_name = sampler.properties['child_properties']['chip_id']
response = sampler.sample(model, num_reads=1000)
print("The solution obtained by D-Wave's quantum annealer",sampler_name,"is")
print(response)
print()

print()
print()
print()


