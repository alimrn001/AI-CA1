import time
import copy
import heapq
import linecache
import timeit

spentTime = 0

class uniGraph : 
    #looseEdges = []
    def __init__(self, edges = [], vertexNo = 0, looseEdgesData = [], studentsData = {}, deliveryPriority = [], startNode = 0) :
        self.edges = edges
        self.vertexNo = vertexNo
        self.looseEdgesData = looseEdgesData
        self.studentsData = studentsData
        self.deliveryPriority = deliveryPriority
        self.startNode = startNode

    def __eq__(self, other) : 
        return (self.edges, self.vertexNo, self.looseEdgesData, self.studentsData, self.deliveryPriority, self.startNode) == \
        (other.edges, other.vertexNo, other.looseEdgesData, other.studentsData, other.deliveryPriority, other.startNode)

    def initializeEdges(self, n) :
        #n is vertex no.
        self.edges = [ [] for i in range(n)]
        self.looseEdgesData = [ [0]*n for j in range(n)] # fill all elements to 0
        self.deliveryPriority = [ [] for k in range(n)]

    def addEdge(self, u, v) :
        #considering vertexes starting from 1
        self.edges[u-1].append(v-1)
        self.edges[v-1].append(u-1)

    def edgeIsLoose(self, src, dst) :
        if(self.looseEdgesData[src-1][dst-1]==0) :
            return False
        return True

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

        self.startNode = int(fileData.readline()) - 1
        s = int(fileData.readline())
        for k in range(s) :
            p, q = map(int, fileData.readline().split())
            self.studentsData[p] = q ## p-1 , q-1 ???

        t = int(fileData.readline())
        for l in range(t) :
            a, b = map(int, fileData.readline().split())
            self.deliveryPriority[a-1].append(b-1) ## a-1 , b-1 ???

    def showLooseEdges(self) :
        print("loose edges are : ")
        for i in range(self.vertexNo) :
            for j in range(self.vertexNo) :
                if(self.looseEdgesData[i][j] != 0) :
                    print("(", i+1, "->", j+1, ") : ", self.looseEdgesData[i][j])
                    #print("(", j+1, "->", i+1, ") : ", self.looseEdgesData[i][j])
                    #print("-------------------")

    def showDeliveryPriority(self) :
        for i in range(self.vertexNo) :
                if(len(self.deliveryPriority[i])!= 0) :
                    print("node :", i+1, "->", end=" ")
                    for j in range(len(self.deliveryPriority[i])) :
                        print(self.deliveryPriority[i][j]+1, end=" ")
                    print("\n")

    def showGraphData(self) :
        for i in range(len(self.edges)) :
            print("node", (i+1),  "connects to :", end=" ")
            for j in range(len(self.edges[i])) :
                print(self.edges[i][j]+1, end=" ")
            print("\n")
        
        self.showLooseEdges()
        print("\nStudents data : ")
        print(self.studentsData)
        print("\nDelivery priority : ")
        self.showDeliveryPriority()


start = timeit.default_timer()
uniGraph_ = uniGraph()
uniGraph_.retrieveGraphData("tests\\Test3.txt")
end = timeit.default_timer()
elapsedTime = end-start
elapsedTime = elapsedTime*1000
print('total time taken :', elapsedTime, 'miliseconds')


uniGraph_.showGraphData()