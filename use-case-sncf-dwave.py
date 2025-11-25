import numpy as np
import dimod
from dwave.system import DWaveSampler,EmbeddingComposite

def random_set_cover(num_groups,num_trains,lamb1,lamb2):
    '''returns a random instance of the set cover simplification for optimbilan'''
    m = num_groups
    n = num_trains
    L = []
    for i in range(m):
        list_length = np.random.choice([1, 2])
        random_list = np.random.randint(0, n, size=list_length)
        L.append(random_list)
 
    Q = np.zeros((n, n))
 
 
    for iter in L:
        # print(iter)
        # print(f'len iter {len(iter)}')
        if len(iter) == 1:
            Q[int(iter[0])][int(iter[0])] -= lamb1
 
        if len(iter) == 2:
            Q[int(iter[0])][int(iter[0])] -= lamb2
            Q[int(iter[1])][int(iter[1])] -= lamb2
            Q[int(iter[0])][int(iter[1])] += lamb2
 
    for i in range(n):
        Q[i][i] += 1
 
    return Q


sampler = EmbeddingComposite(DWaveSampler(solver='Advantage2_system1.8'))
 
max_trains = 21 # was 27
max_groups = 40 #was 50

trains= max_trains
groups= max_groups

M = random_set_cover(groups, trains, trains + 1, trains + 1)
print("QUBO matrix:", M)
response = sampler.sample_qubo(M, num_reads=500)
myres= response.lowest()
print("Results=")
for re in myres.record:
	print(re[0], "cost=", re[1], "proba(%)=", re[2]/5.0)

#print(response)
