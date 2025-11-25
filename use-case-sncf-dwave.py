import numpy as np
import dimod
from dwave.system import DWaveSampler,EmbeddingComposite
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import traceback
 
 
 
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
 
liste_proba = []
temps_qpu = []
 

for trains in range(1,max_trains,3):
    print(f'trains {trains}')
    liste_proba.append([])
    temps_qpu.append([])
    for groups in range(1,max_groups,5):
        # liste_proba[(trains-1)//3].append([])
        # temps_qpu[(trains-1)//3].append([])
        print(f'groups {groups}')
        liste_moyenne = []
        liste_proba_provisoire = []
        for i in range(5):
 
            try:
                M = random_set_cover(groups, trains, trains + 1, trains + 1)
                response = sampler.sample_qubo(M, num_reads=500)
                energies = response.record['energy']
                occurrences = response.record['num_occurrences']
                best_energy = min(energies)
                best_energy_occurrences = occurrences[energies == best_energy].sum()
                proba = best_energy_occurrences / 500
                liste_proba_provisoire.append(proba)
                temps_utilisation_qpu = response.info['timing']['qpu_access_time']
                liste_moyenne.append(temps_utilisation_qpu)
            except Exception as e:
                print('problème')
                traceback.print_exc()
                break
        print('oui')
        moyenne = sum(liste_moyenne) / len(liste_moyenne)
        liste_proba[(trains-1)//3].append(sum(liste_proba_provisoire) / len(liste_proba_provisoire))
        temps_qpu[(trains-1)//3].append(moyenne)
 
 
 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
print(liste_proba)
for i, proba in enumerate(liste_proba):
    print(proba)
    print(range(len(proba)))
    print([i]*len(proba))
 
# Plot the lines in 3D
for i, proba in enumerate(liste_proba):
    ax.plot(range(len(proba)), [i] * len(proba), proba, label=f'Curve proba {i + 1}')
 
 
 
 
# Set labels for each axis
ax.set_xlabel('Groups')
ax.set_ylabel('Trains')
ax.set_zlabel('Proba')
 
 
 
x_ticks = range(0, len(proba) * 5, 5)  # Assuming 5 is your step size
ax.set_xticks(x_ticks)
ax.set_xticklabels(range(0, 50, 10))  # Adjust labels based on your actual data range
# Add a legend to distinguish curves
ax.legend()
 
# Show the plot
plt.savefig('3d_plot_proba.png')
 
# Close the plot (optional)
plt.close()
 
 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
 
 
for i, temps in enumerate(temps_qpu):
    ax.plot(range(len(temps)), [i] * len(temps), temps, label=f'Curve temps{i + 1}')
 
 
# Set labels for each axis
ax.set_xlabel('Groups')
ax.set_ylabel('Trains')
ax.set_zlabel('QPU access time')
 
# Add a legend to distinguish curves
ax.legend()
 
# Show the plot
plt.savefig('3d_plot_time.png')
 
# Close the plot (optional)
plt.close()
