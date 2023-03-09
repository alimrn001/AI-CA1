import time
import copy
import heapq
import linecache
import timeit

spentTime = 0

class UniGraph : 
    
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
            self.studentsData[p-1] = [q-1, False] ## p-1 , q-1 ???

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

    def getPizzaFromNode(self, node) : # check delivery priority here ?
        for i in self.studentsData.keys() :
            if(self.studentsData[i][0]==node) :
                self.studentsData[i][1] = True

    def pizzaIsBoughtForStudent(self, node) : # check delivery priority here ??
        if(node in self.studentsData.keys()) :
            return self.studentsData[node][1] 
        return False

class NPD : 

    def __init__(self, uniGraph, studentsMet = set(), pathTraversed = [], totalStepsTaken = 0, timeSpentOnLooseEdges = 0) :
        self.uniGraph = uniGraph
        self.studentsMet = studentsMet
        self.pathTraversed = pathTraversed
        self.totalStepsTaken = totalStepsTaken
        self.timeSpentOnLooseEdges = timeSpentOnLooseEdges

    def __eq__(self, other) :
        if other == None :
            return False
        return (self.timeSpentOnLooseEdges, self.uniGraph.startNode, self.uniGraph.studentsData, self.studentsMet) ==\
               (other.timeSpentOnLooseEdges, other.uniGraph.startNode, other.uniGraph.studentsData, other.studentsMet)

    def __lt__(self, other) :
        return self.totalStepsTaken < other.totalStepsTaken

    def goalReached(self) :
        if(len(self.studentsMet) != len(self.uniGraph.studentsData.keys())) :
            return False
        if(self.uniGraph.startNode not in self.uniGraph.studentsData.keys()) :
            return False
        return True

    def createNPDNewDelivery(self, currentNode) :
        newDeliveryGraph = copy.deepcopy(self.uniGraph)
        newDeliveryGraph.startNode = currentNode
        newDeliveryGraph.getPizzaFromNode(currentNode)
        newDeliveryGraphStudentsMet = copy.deepcopy(self.studentsMet)

        if(newDeliveryGraph.pizzaIsBoughtForStudent(currentNode)) : # check delivery priority here ??
            newDeliveryGraphStudentsMet.add(currentNode)

        NPDNewPathTraversed = copy.deepcopy(self.pathTraversed)
        NPDNewPathTraversed.append(currentNode+1)
        
        return NPD(uniGraph = newDeliveryGraph, studentsMet = newDeliveryGraphStudentsMet,\
                    pathTraversed = NPDNewPathTraversed, timeSpentOnLooseEdges=self.timeSpentOnLooseEdges,\
                    totalStepsTaken = self.totalStepsTaken+1)

    def getNewNPDDelivery(self) :
        newDeliveries =[] 
        v = self.uniGraph.startNode

        if v in self.uniGraph.looseEdgesData : ## possible bug here !!!!!!!
            for i in range(self.uniGraph.vertexNo) :
                if(self.uniGraph.looseEdgesData[i][v] > self.timeSpentOnLooseEdges) :
                    newDelivery = copy.deepcopy(self)
                    newDelivery.totalStepsTaken += 1
                    newDelivery.timeSpentOnLooseEdges += 1
                    return [newDelivery]

                self.timeSpentOnLooseEdges = 0

        for n in self.uniGraph.edges[v] :
            newDeliveries.append(self.createNPDNewDelivery(n)) 

        return newDeliveries   



def BFS(init_state) :
    frontier, visited, visit_states = [], [], 0
    frontier.append(copy.deepcopy(init_state))

    while  len(frontier) > 0 :

        # for frt in frontier :
        #     print(" frt start node :", frt.uniGraph.startNode)

        # print("---")

        current_state = frontier.pop(0)
        visit_states += 1
        #print("current state :", current_state.uniGraph.startNode)

        if current_state.goalReached() :
            path, cost_of_path = current_state.pathTraversed, current_state.totalStepsTaken
            return path, cost_of_path, visit_states

        visited.append(current_state)  

        # for vst in visited :
        #     print("start node", vst.uniGraph.startNode)
        # print("----")

        new_states = current_state.getNewNPDDelivery()
        # print("new state :")
        # for st in new_states :
        #     print("start node", st.uniGraph.startNode)
        
        
        for s in new_states :
            if (s not in visited) and (s not in frontier)  :
                frontier.append(s)
                print("appended", s.uniGraph.startNode)
        print("--")        

    return None, None, visit_states






# def set_morids(input_file_name):
#         input_file = open(input_file_name)
#         s = int(input_file.readline())
#         dis = {}
#         for i in range(s):
#             line = list(map(int, input_file.readline().split()))
#             dis[line[0]-1] = list(map(lambda x : x-1 , line[2:]))
#             for j in range(len(dis[line[0]-1])):
#                 dis[line[0]-1][j] = [dis[line[0]-1][j], False]
#         morids = dis
#         return morids

# x = set_morids("testx.txt")
# print(x)


uniGraph_ = UniGraph()
uniGraph_.retrieveGraphData("E:\\university\\semester 8\\AI\\CA1\\AI-CA1\\code\\testx.txt")


initial_state = NPD(uniGraph=uniGraph_, pathTraversed = [uniGraph_.startNode+1])

ExecutionTimeList = []
for i in range(3) :
    start = time.time()
    ###### CHOOSE ALGORITHM ######

    path, cost_of_path, visit_states = BFS(initial_state)
    # path, cost_of_path, visit_states = IDS(initial_state)
    # path, cost_of_path, visit_states = Astar(initial_state)
    # path, cost_of_path, visit_states = Astar(initial_state, alpha=1.6)
    # path, cost_of_path, visit_states = Astar(initial_state, alpha=7)

    end = time.time()
    ExecutionTimeList.append(end - start)

print(f"Path : {path}\nCost Of Path : {cost_of_path}\
        \nExecution Time : {sum(ExecutionTimeList)/3}\nSeen States : {visit_states}")








# start = timeit.default_timer()
# uniGraph_ = UniGraph()
# uniGraph_.retrieveGraphData("tests/Test3.txt")
# end = timeit.default_timer()
# elapsedTime = end-start
# elapsedTime = elapsedTime*1000
# print('total time taken :', elapsedTime, 'miliseconds')


# uniGraph_.showGraphData()