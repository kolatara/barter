import numpy as np
from munkres import *

NETWORK_SIZE = 50
TRIALS = 100

def make_matrix (v, noedge, same, ideal):
        a = np.full((NETWORK_SIZE, NETWORK_SIZE), noedge, dtype=int)
        j, k = 0, 0
        for i, n in enumerate(v):
                if i > n:
                        j, k = n, i
                else: 
                        j, k = i, n
                if k < NETWORK_SIZE - 1:
                        for x in range(j, k+1):
                            a[i][x] = ideal
                else:
                        for x in range(j, k):
                            a[i][x] = ideal
        np.fill_diagonal(a, same)
        return a

def max_matching (a):
        m = Munkres()
        maxsize = np.amax(a)
        cost_matrix = make_cost_matrix(a, lambda cost: maxsize - cost)
        indexes = m.compute(cost_matrix)
        return indexes

def in_match (match, a, n):
        counter = 0
        for (i, j) in match:
                if a[i][j] == n:
                        counter += 1
        return counter

def find_rematch (v):
        s1 = make_matrix (v, -1*NETWORK_SIZE, 0, 1)
        s2 = make_matrix (v, 1, 2, 3)
        max_s1 = max_matching(s1)
        max_s2 = max_matching(s2)
        s1_rematch = in_match(max_s1, s1, 1)
        s2_rematch = in_match(max_s2, s2, 3)
        s2_cost = in_match(max_s2, s2, 1)
        return [s1_rematch, s2_rematch, s2_cost]

def main ():
    data_rand = []
    data_binom = []
    for i in range(0, TRIALS):
        rand_vect  = np.random.randint(NETWORK_SIZE, size=NETWORK_SIZE)
        binom_vect = np.random.binomial(NETWORK_SIZE, 0.5, NETWORK_SIZE) 
        data_rand.append(find_rematch (rand_vect))
        data_binom.append(find_rematch (binom_vect))
    print "Random Distribution:" 
    print "\t - S1 Benefit-improving Rematches:"
    print "\t\t Mean: " + str (np.mean(data_rand, axis=0)[0])
    print "\t\t SD: " + str (np.std(data_rand, axis=0)[0])
    print "\t - S2 Benefit-improving Rematches:"
    print "\t\t Mean: " + str (np.mean(data_rand, axis=0)[1])
    print "\t\t SD: " + str (np.std(data_rand, axis=0)[1])
    print "\t - S2 Benefit-decreasing Rematches:"
    print "\t\t Mean: " + str (np.mean(data_rand, axis=0)[2])
    print "\t\t SD: " + str (np.std(data_rand, axis=0)[2])

    print "Binomial Distribution:" 
    print "\t - S1 Benefit-improving Rematches:"
    print "\t\t Mean: " + str (np.mean(data_binom, axis=0)[0])
    print "\t\t SD: " + str (np.std(data_binom, axis=0)[0])
    print "\t - S2 Benefit-improving Rematches:"
    print "\t\t Mean: " + str (np.mean(data_rand, axis=0)[1])
    print "\t\t SD: " + str (np.std(data_binom, axis=0)[1])
    print "\t - S2 Benefit-decreasing Rematches:"
    print "\t\t Mean: " + str (np.mean(data_binom, axis=0)[2])
    print "\t\t SD: " + str (np.std(data_binom, axis=0)[2])
main()
