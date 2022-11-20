from docplex.mp.model import Model
import cplex
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain, combinations

def solve_tsp():

    m = Model(name='tsp', log_output = False)

    nb_villes = 5

    sommets = [i for i in range(nb_villes)]
    arcs = [(i,j) for i in sommets for j in sommets if i!=j]

    #Generate random coordinates

    rnd = np.random
    rnd.seed(1)

    X = (rnd.rand(nb_villes)*100).round()
    Y = (rnd.rand(nb_villes)*100).round()


    plt.figure(figsize=(10,10))
    plt.scatter(X,Y,color='purple')
    s=[]

    for n in range(len(X)):
        s_temp=[]
        s_temp.append("%.1f" %X[n])
        s_temp.append("%.1f" %Y[n])
        s.append(s_temp)

    plt.xlabel("Distance X")
    plt.ylabel("Distance Y")
    plt.title("Dispertion des sommets - TSP")

    for n in range(len(X)):
        plt.annotate(str(s[n]), xy=(X[n],Y[n] ), xytext=(X[n]-4,Y[n]-4), 
                    color='green')
        
    for n in range(len(X)):
        plt.annotate(str(n), xy=(X[n],Y[n] ), xytext=(X[n]+0.5,Y[n]+1),
                    color='red')

    #plt.show()

    distances={(i, j): np.hypot(X[i] - X[j], Y[i] - Y[j]) for i,j in arcs}

    m = Model('tsp')

    A=m.binary_var_dict(arcs,name='A')
    S=m.continuous_var_dict(sommets,name='S')

    m.minimize(m.sum(distances[i]*A[i] for i in arcs))

    #constraints to ensure passing exactly once by each vertex

    for s in sommets:
        m.add_constraint(m.sum(A[(i,j)] for i,j in arcs if i==s)==1)

    for s in sommets:
        m.add_constraint(m.sum(A[(i,j)] for i,j in arcs if j==s)==1)


    card = (2**nb_villes)

    def powerset(iterable):
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)))

    subtours = list(powerset(range(nb_villes)))

    # The first element of the list is the empty set and the last element is the full set, hence we remove them.
    subtours = subtours[1:(len(subtours)-1)]

    print(subtours)

    #subtours = [k for k in range_set for i in range(nb_villes) if (k/(2**(i-1))) % 2 == 1]


    for s in subtours:
        m.add_constraint(m.sum(A[(i,j)] for i,j in arcs if i!=j)<= len(s)-1)

    solution = m.solve(log_output=False)
    
    print(m.get_solve_status())
    #solution.display()

    
    #subtours = 
    #print(subtours)
    #constraint for subtours
    # m.add_constraint()

solve_tsp()