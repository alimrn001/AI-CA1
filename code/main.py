import time
import copy
import heapq
import linecache

spentTime = 0

class uniGraph : 
    #looseEdges = []
    def __init__(self, edges = [], vertexNo = 0, looseEdgesData = [], studentsData = {}, currentNode = 0) :
        self.edges = edges
        self.vertexNo = vertexNo
        self.looseEdgesData = looseEdgesData
        self.studentsData = studentsData
        self.currentNode = currentNode

    def __eq__(self, other) : 
        return (self.edges, self.vertexNo, self.looseEdgesData, self.studentsData, self.currentNode) == \
        (other.edges, other.vertexNo, other.looseEdgesData, other.studentsData, other.currentNode)

    def initializeEdges(self, n) :
        #n is vertex no.
        self.edges = [ [] for i in range(n)]
        self.looseEdgesData = [ [0]*n for j in range(n)] # fill all elements to 0

    def addEdge(self, u, v) :
        #considering vertexes starting from 1
        self.edges[u-1].append(v-1)
        self.edges[v-1].append(u-1)

    def retrieveGraphData(self, fileName) :
        fileData = open(fileName)
        n, m = map(int, fileData.readline().split())
        self.initializeEdges(n);
        for i in range(m) : 
            u, v = map(int, fileData.readline().split())
            self.addEdge(u, v)
        self.vertexNo = n

        h = int(fileData.readline())
        for j in range(h) :
            edgeNo, edgeTime = map(int, fileData.readline().split())
            src, dst = map(int, linecache.getline(fileName, edgeNo+1).split())
            self.looseEdgesData[src-1][dst-1] = edgeTime
            self.looseEdgesData[dst-1][src-1] = edgeTime

    def showLooseEdges(self) :
        print("loose edges are : ")
        for i in range(self.vertexNo) :
            for j in range(self.vertexNo) :
                if(self.looseEdgesData[i][j] != 0) :
                    print("(", i+1, "->", j+1, ") : ", self.looseEdgesData[i][j])
                    #print("(", j+1, "->", i+1, ") : ", self.looseEdgesData[i][j])
                    #print("-------------------")

    def showGraphData(self) :
        for i in range(len(self.edges)) :
            print("node", (i+1),  "connects to :", end=" ")
            for j in range(len(self.edges[i])) :
                print(self.edges[i][j]+1, end=" ")
            print("\n")
        self.showLooseEdges()


start = time.time()
uniGraph_ = uniGraph()
uniGraph_.retrieveGraphData("tests\\Test1.txt")
end = time.time()
elapsedTime = end-start
print('total time taken :', elapsedTime, 'seconds')

# uniGraph_.initializeEdges(5)
# uniGraph_.addEdge(1, 2)
# uniGraph_.addEdge(2, 3)
# uniGraph_.addEdge(3, 4)
# uniGraph_.addEdge(3, 5)

uniGraph_.showGraphData()