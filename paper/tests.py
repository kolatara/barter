import numpy as np
import random
from munkres import *
from operator import add

def weight_of (a, match):
    sum = 0
    for (i, j) in match:
            if a[i][j] == 1:
                sum += 1
    return sum

# max_matching
#
# INPUT:
# a - 2d array representing the preference matrix
#
# OUTPUT: An array of tuples, eaching containing two indices that were matched

def max_matching (a):
        m = Munkres()
        maxsize = np.amax(a)
        cost_matrix = make_cost_matrix(np.copy(a), lambda cost: maxsize - cost)
        return m.compute(cost_matrix)

# budget_match
#
# INPUT:
# m - a 2d array representing the preference matrix of people to items
# b - an integer representing the payoff budget, such that payoff < b
#
# OUTPUT: 
#
# ALGORITHM:
# 1. For each i from 0 to B, create i ghost houses and i ghost people such 
#    that all old people have 0-weight edges to the i ghost houses and the
#    old houses have 0-weight edges to the i ghost people. Delete all negative
#    weight edges in the graph.
# 2. Run maximum-weight perfect matching on this graph, G_i. In the final
#    matching we will include all matchings of old people to houses. The
#    old people matched to ghosts are in P_u, and the old houses matched to
#    ghosts are in H_u. Match P_u and H_u to each other in the *original*
#    graph containing negative weight edges. The resulting matching will be
#    included in the final matching.
# 3. Let W_i be the weight of the final matching from G_i (sum the weight of
#    all included edges). Return the matching with the maximum W_i.

def budget_match (m, network_size, b):
        print m
        max_w = -1
        max_match = []
        max_i = -1
        B = b if b <= network_size else network_size + 1
        no_edge = -1 * (network_size + B)
        for i in range(B):
                G_i = np.append(np.copy(m), np.zeros((i, network_size), int), 
                                axis=0)
                G_i = np.c_[G_i, np.zeros((network_size + i, i), int)]
                G_i[G_i == -1] = no_edge
                for j in range(network_size, network_size + i):
                        for k in range(network_size, network_size + i):
                                G_i[j][k] = no_edge
                P_u = []
                H_u = []
                final_match = []
                m_m = max_matching(G_i)
                r_n = range(0, network_size)
                r_i = range(network_size, network_size + i)
                for match in m_m:
                        if match[0] in r_n and match[1] in r_i:
                                P_u.append(match[0])
                        if match[1] in r_n and match[0] in r_i:
                                H_u.append(match[1])
                        if match[0] in r_n and match[1] in r_n:
                                final_match.append(match)
                ghost_G_i = np.copy(m)[P_u][:, H_u]
                ghost_match = max_matching(ghost_G_i) if i > 0 else []
                for (a, b) in ghost_match:
                        final_match.append((P_u[a], H_u[b]))
                w_i = weight_of(m, final_match)
                if w_i > max_w:
                        max_w = w_i
                        max_match = final_match
                        max_i = i
        print "MAX WEIGHT:"
        print weight_of(m, max_match)
        print "MATCHING:"
        print max_match
        print "MAX I:"
        print max_i
# generate_matrices
#
# INPUT:
# network_size - an integer representing the number of people trading
# k - an integer representing the number of game days left in the season
# p_demand - an array of size k representing the probability that a given game
#            will be demanded on the market
# p_supply - an array of size k representing the probability that a given game
#            will be supplied on the market
#
# OUTPUT: one matrix of form (network_size * network_size) representing market

def generate_bucket_matrix (network_size, k, p_demand = None, p_supply = None):
        supply = np.random.choice(k, network_size, p = p_demand)
        demand = []
        for i in supply:
                a = np.empty([0], dtype=int)
                while not(a.size):
                        a = np.random.choice(k, random.randrange(1, k+1), 
                                        False, p_supply)
                        a = a[a != i]
                demand.append(a)
        matrix = np.ones((network_size, network_size), int) * -1
        np.fill_diagonal(matrix, 0)
        for i, desired in enumerate(demand):
                for j, available in enumerate(supply):
                        if available in desired:
                                matrix[i][j] = 1
        return matrix

NETWORK_SIZE = 50

m = generate_bucket_matrix(NETWORK_SIZE, NETWORK_SIZE)
b_m = (np.random.binomial(1, 0.5, (NETWORK_SIZE, NETWORK_SIZE)))
b_m[b_m == 0] = -1
np.fill_diagonal(b_m, 0)
r_m = np.random.randint(-1, 1, (NETWORK_SIZE, NETWORK_SIZE))
test = np.append([[0, 1, -1, -1], [-1, 0, -1, 1], [-1, -1, 0, 1]], [[-1, -1, 1, 0]], axis=0)

budget_match(m, NETWORK_SIZE, 10)
