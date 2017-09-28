# each item to be packed is represented as a set of triples (size,value,name)
def itemSize(item): return item[0]
def itemValue(item): return item[1]
def itemName(item): return item[2]

# example used in lecture
exampleItems = [(3,3,'A'),
        (4,1,'B'),
        (8,3,'C'),
        (10,4,'D'),
        (15,3,'E'),
        (20,6,'F')]
        
exampleSizeLimit = 32

def pack(items,sizeLimit):
    P = {}
    for nItems in range(len(items)+1):
        for lim in range(sizeLimit+1):
            if nItems == 0:
                P[nItems,lim] = 0
            elif itemSize(items[nItems-1]) > lim:
                P[nItems,lim] = P[nItems-1,lim]
            else:
                P[nItems,lim] = max(P[nItems-1,lim],
                    P[nItems-1,lim-itemSize(items[nItems-1])] +
                    itemValue(items[nItems-1]))
    
    L = []      
    nItems = len(items)
    lim = sizeLimit
    while nItems > 0:
        if P[nItems,lim] == P[nItems-1,lim]:
            nItems -= 1
        else:
            nItems -= 1
            L.append(itemName(items[nItems]))
            lim -= itemSize(items[nItems])

    L.reverse()
    return L
