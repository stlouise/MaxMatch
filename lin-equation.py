import numpy as np
import dimod


# We will start with a simple case for linear equation: (x1-x2+1=0)^(2x1-x2-1=0)
# Ising form
J= { (0,1):5.0, (0,2):-1.5, (0,3):-3.0, \
(1,2):-3.0, (1,3):-6.0, \
(2,3):2.0}
h= { 0:2.0, 1:4.0, 2:-1.5, 3:-3.0 }
# QUBO form
#J= { (0,1):20.0, (0,2):-6.0, (0,3):-12.0, \
#(1,2):-12.0, (1,3):-24.0, \
#(2,3):8.0}
#h= { 0:3.0, 1:16.0, 2:2.0, 3:8.0 }

# More complicated A=[[2,1,-1],[1,2,-1],[1,1,1]] and B= [[0],[-2],[-9]] with 3 qubits/variable
# QUBO form
#J= { (0,1):24.0, (0,2):48.0, (0,3):10.0, (0,4):20.0, (0,5):40.0, (0,6):-4.0, (0,7):-8.0, (0,8):-16.0,\
#(1,2):96.0, (1,3):20.0, (1,4):40.0, (1,5):80.0, (1,6):-8.0, (1,7):-16.0, (1,8):-32.0,\
#(2,3):40.0, (2,4):80.0, (2,5):160.0, (2,6):-16.0, (2,7):-32.0, (2,8):-64.0,\
#(3,4):24.0, (3,5):48.0, (3,6):-4.0, (3,7):-8.0, (3,8):-16.0,\
#(4,5):96.0, (4,6):-8.0, (4,7):-16.0, (4,8):-32.0,\
#(5,6):-16.0, (5,7):-32.0, (5,8):-64.0,\
#(6,7):12.0, (6,8):24.0,\
#(7,8):48.0,\
#}
#h= { 0:-16.0, 1:-20.0, 2:8.0, 3:-20.0, 4:-28.0, 5:-8.0, 6:-11.0, 7:-16.0, 8:-8.0 }
# Ising form
#J= { (0,1):6.0, (0,2):12.0, (0,3):2.5, (0,4):5.0, (0,5):10.0, (0,6):-1.0, (0,7):-2.0, (0,8):-4.0,\
#(1,2):24.0, (1,3):5.0, (1,4):10.0, (1,5):20.0, (1,6):-2.0, (1,7):-4.0, (1,8):-8.0,\
#(2,3):10.0, (2,4):20.0, (2,5):40.0, (2,6):-4.0, (2,7):-8.0, (2,8):-16.0,\
#(3,4):6.0, (3,5):12.0, (3,6):-1.0, (3,7):-2.0, (3,8):-4.0,\
#(4,5):24.0, (4,6):-2.0, (4,7):-4.0, (4,8):-8.0,\
#(5,6):-4.0, (5,7):-8.0, (5,8):-16.0,\
#(6,7):3.0, (6,8):6.0,\
#(7,8):12.0\
#}
#h= { 0:20.5, 1:41., 2:82., 3:18.5, 4:37., 5:74., 6:-10.5, 7:-21., 8:-42. }

model = dimod.BinaryQuadraticModel(h, J, 0.0, dimod.SPIN)
#model = dimod.BinaryQuadraticModel(h, J, 0.0, dimod.BINARY)

print("The model that we are going to solve is")
print(model)
print()

# We can solve it exactly


#from dimod.reference.samplers import ExactSolver
#sampler = ExactSolver()
#solution = sampler.sample(model)
#print("The exact solution is")
#print(solution)
#print()


# Or with *simulated annealing* (a heuristic method used in classical computers)


sampler = dimod.SimulatedAnnealingSampler()
response = sampler.sample(model, num_reads=10)
print("The solution with simulated annealing is")
print(response)
print()


# And, of course, with D-Wave's quantum computer 


from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
#sampler = EmbeddingComposite(DWaveSampler(solver='Advantage_system6.1'))
sampler = EmbeddingComposite(DWaveSampler(solver='Advantage2_prototype1.1'))
sampler_name = sampler.properties['child_properties']['chip_id']
response = sampler.sample(model, num_reads=1000)
print("The solution obtained by D-Wave's quantum annealer",sampler_name,"is")
print(response)
print()

print()
print()
print()

