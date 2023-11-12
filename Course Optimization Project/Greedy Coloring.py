import numpy as np

matrix = np.load("/Users/kunwoosmac/Desktop/adjacent matrix.npy");
G=matrix
print(G)

# inisiate the name of node.
node = [100, 202, 232, 302, 305, 311, 312, 313, 315, 320, 350, 365, 370, 373, 410, 411, 414, 419, 443, 470, 476, 485]
t_={}
for i in range(len(G)):
    
    t_[node[i]] = i
# print(t_)

# count degree of all node.
degree =[]
for i in range(len(G)):
    
    degree.append(sum(G[i]))
# print(degree)

a_or_c = ['a','a','a','a','a','a','a','a','a','a','a','c','c','c','a','a','a','a','a','c','c','a']

print(len(a_or_c))
# inisiate the posible color
colorDict = {}
for i in range(len(G)):
    if a_or_c[i] == 'a':
        colorDict[node[i]]=['Auditorium 1', 'Auditorium 2', 'Auditorium 3']
    elif a_or_c[i] == 'c':
        colorDict[node[i]]=['Classroom 1', 'Classroom 2', 'Classroom 3', 'Classroom 4', 'Classroom 5']

# sort the node depends on the degree
sortedNode=[]
indeks = []

# use selection sort
for i in range(len(degree)): #0~21
    _max = 0 
    j = 0
    for j in range(len(degree)): ##0~21
        if j not in indeks:
            if degree[j] > _max:# _max=2
                _max = degree[j]
                idx = j
    indeks.append(idx)
    sortedNode.append(node[idx])

# The main process
theSolution={}
for n in sortedNode:
    
    setTheColor = colorDict[n]
    theSolution[n] = setTheColor[0]
    adjacentNode = G[t_[n]]
    for j in range(len(adjacentNode)):
        if adjacentNode[j]==1 and (setTheColor[0] in colorDict[node[j]]):
            colorDict[node[j]].remove(setTheColor[0])

for t,w in sorted(theSolution.items()):
    print("MMAE",t," = ",w)
