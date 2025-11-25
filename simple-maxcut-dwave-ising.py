import numpy as np
import dimod

# define matrix J and external field h
J = {(0,1):1,(0,2):1,(1,2):1,(1,3):1,(2,4):1,(3,4):1}
h = {}
# define the model as Ising Hamiltonian from {h,J}
model = dimod.BinaryQuadraticModel(h, J, 0.0, dimod.SPIN)
print("The model that we are going to solve is")
print(model)
print()

from dwave.system import DWaveSampler, EmbeddingComposite, FixedEmbeddingComposite

# now use the Advantage2 D-Wave computer to solve it 
sampler = EmbeddingComposite(DWaveSampler(solver='Advantage2_system1.8'))
sampler_name = sampler.properties['child_properties']['chip_id']
response = sampler.sample(model, num_reads=1000)
print("The solution obtained by D-Wave's quantum annealer",sampler_name,"is")
print(response)

