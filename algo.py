import numpy as np
from munkres import *
import knapsack
import networkx as nx

# Pack using 
# M U M' : cycle-weight = sum of benefit edges, cost - sum of costs of edges
# Compute max-weight matching M'
# Create 0-weight matching M
# Create Benefit Matrix


def get_cost_benefit (cycles, matrix):
    ben_cost = []
    for c in cycles:
        benefit = 0
        cost = 0
        for idx, i in enumerate(c):
            if idx+1 == len(c): 
                j = c[0]
            else: j = c[idx+1]
            if matrix[i][j] > 0:
                benefit = benefit + matrix[i][j]
            else: cost = cost + (-1 * matrix[i][j])
        ben_cost.append((cost, benefit, c))
    return ben_cost

def max_matching (matrix):
    maxsize = np.amax(matrix)
    cost_matrix = make_cost_matrix(matrix, lambda cost: maxsize - cost)
    m = Munkres()
    indexes = m.compute(cost_matrix)
    return indexes

def diag_zero (a, n):
    for i in range(0, n):                       
        a[i][i] = 0 
    return a

def  main ():
    n = 5
    budget = 5
    print ("Size: " + str(n) + ", Budget: " + str(budget))
    benefit_matrix = diag_zero(np.random.randint(-50, 50, (n, n)), n)
    print "The Benefit Matrix: "
    print benefit_matrix
    #zero_match = [(i,i) for i in range(0, n)]
    max_match = max_matching(benefit_matrix)
    print "\n Max-weight Matching:"
    print (max_match)
    #Add zero_match + max_match if wanted
    cycles = list(nx.simple_cycles(nx.DiGraph(max_match)))
    print "\n All cycles in Max-match:"
    print list(cycles)
    packing_m = get_cost_benefit(cycles, benefit_matrix)
    print "\n Benefit - Cost - Cycle:"
    print packing_m
    final_cycles = knapsack.pack(packing_m, budget)
    print "\n Knapsack-packed cycles:"
    print final_cycles
    for i in range(n):
            if not(any(i in c for c in final_cycles)):
                final_cycles.append([i])
    print "\n Final cycles:"
    print final_cycles
main()
