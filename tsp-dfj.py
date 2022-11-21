from docplex.mp.model import Model
import cplex
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain, combinations


from functools import reduce
from itertools import combinations, product

def solve_tsp():

    m = Model(name='tsp', log_output = False)

    nb_villes = 5


    #constraints to ensure passing exactly once by each vertex


    N = 5
    c =  [
    [99, 7, 8, 5, 3],
    [ 7,99, 2, 9,10],
    [ 8, 2,99, 6, 9],
    [ 5, 9, 6,99, 4],
    [ 3,10, 9, 4,99]
    ]
    # Variables
    x = m.binary_var_dict((i, j) for i in range(1, N+1) for j in range(1, N+1))
    print(x)

    nodes = list(range(N))
    p = reduce(lambda x, y: x+y, [list(combinations(nodes, i)) for i in range(2, N)])
    print(p)

    number_of_sets = 2^N - 2

    for k in range(1, number_of_sets+1):
        if len(p[k-1])<=N-1 and len(p[k-1])>=2:
            m.add_constraint(m.sum([x[i+1, j+1] for i in p[k-1] for j in p[k-1]])<=len(p[k])-1)
            

    m.add_constraint(m.sum([x[i, j] for j in range(1, N+1) for i in range(1, N+1)]) == 1)

# constraint #2: salesperson leaving a node i

    m.add_constraint(m.sum([x[i, j] for i in range(1, N+1) for j in range(1, N+1)]) == 1)


    number_of_sets = 2^N - 2

    for k in range(1, number_of_sets+1):
        if len(p[k-1])<=N-1 and len(p[k-1])>=2:
            m.add_constraint(m.sum([x[i+1, j+1] for i in p[k-1] for j in p[k-1]])<=len(p[k])-1)
            
    card = (2**nb_villes)

    def powerset(iterable):
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(2, len(s)))

    subtours = list(powerset(range(nb_villes)))

    # The first element of the list is the empty set and the last element is the full set, hence we remove them.
    subtours = subtours[1:(len(subtours)-1)]

    print(subtours)

    #subtours = [k for k in range_set for i in range(nb_villes) if (k/(2**(i-1))) % 2 == 1]


    '''
    for s in subtours:
        m.add_constraint(m.sum(A[(i,j)] for i,j in arcs if i!=j)<= len(s)-1)
    '''

    #solution = m.solve(log_output=False)
    
    #print(m.get_solve_status())
    #solution.display()

    
    #subtours = 
    #print(subtours)
    #constraint for subtours
    # m.add_constraint()

    m.minimize(sum([c[i-1][j-1]*x[i, j] for i in range(1, N+1) for j in range(1, N+1)]))

    m.print_information()
    sol = m.solve()
    m.print_solution()

solve_tsp()