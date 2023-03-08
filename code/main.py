import time
import copy
import heapq

spentTime = 0

class uniGraph : 
    #looseEdges = []
    def __init__(self, edges = [], vertexNo = 0, looseEdges = {}, studentsData = {}, currentNode = 0) :
        self.edges = edges
        self.vertexNo = vertexNo
        self.looseEdges = looseEdges
        self.studentsData = studentsData
        self.currentNode = currentNode

    def __eq__(self, other) : 
        return (self.edges, self.vertexNo, self.looseEdges, self.studentsData, self.currentNode) == \
        (other.edges, other.vertexNo, other.looseEdges, other.studentsData, other.currentNode)

    def initializeEdges(self, n) :
        #n is vertex no.
        self.edges = [ [] for i in range(n)]

    def addEdge(self, u, v) :
        #considering vertexes starting from 1
        self.edges[u-1].append(v-1)
        self.edges[v-1].append(u-1)

    def showGraphData(self) :
        for i in range(len(self.edges)) :
            print("node", (i+1),  "connects to :", end=" ")
            for j in range(len(self.edges[i])) :
                print(self.edges[i][j]+1, end=" ")
            print("\n")


uniGraph_ = uniGraph()
uniGraph_.initializeEdges(5)
uniGraph_.addEdge(1, 2)
uniGraph_.addEdge(2, 3)
uniGraph_.addEdge(3, 4)
uniGraph_.addEdge(3, 5)

uniGraph_.showGraphData()