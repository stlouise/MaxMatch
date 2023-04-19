import numpy as np
import dimod

J= { (0,1):2.0, (0,2):2, (1,3):2, \
(2,3):2.0, (2,4):2.0, \
(3,4):2.0}
h= { 0:-2.0, 1:-2.0, 2:-3.0, 3:-3.0, 4:-2.0 }
model = dimod.BinaryQuadraticModel(h, J, 0.0, dimod.BINARY)

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

sampler = EmbeddingComposite(DWaveSampler(solver='Advantage2_prototype1.1'))
sampler_name = sampler.properties['child_properties']['chip_id']
response = sampler.sample(model, num_reads=1000)
print("The solution obtained by D-Wave's quantum annealer",sampler_name,"is")
print(response)
