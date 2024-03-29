import time
import copy
import heapq
import linecache
import timeit

BFSAlgorithm = 1
IDSAlgorithm = 2
ASTARAlgorithm = 3
ASTARAlgorithmWeighted = 4

class UniGraph : 
    
    def __init__(self, edges = [], vertexNo = 0, looseEdgesData = [], looseEdgesCrossStatus = [], studentsData = {}, deliveryPriority = [], pizzerias = [], startNode = 0) :
        self.edges = edges
        self.vertexNo = vertexNo
        self.looseEdgesData = looseEdgesData
        self.looseEdgesCrossStatus = looseEdgesCrossStatus
        self.studentsData = studentsData
        self.deliveryPriority = deliveryPriority
        self.pizzerias = pizzerias
        self.startNode = startNode

    def __eq__(self, other) : 
        return (self.edges, self.vertexNo, self.looseEdgesData, self.looseEdgesCrossStatus, self.studentsData, self.deliveryPriority, self.pizzerias, self.startNode) == \
        (other.edges, other.vertexNo, other.looseEdgesData, self.looseEdgesCrossStatus, other.studentsData, other.deliveryPriority, other.pizzerias, other.startNode)

    def initializeEdges(self, n) :
        #n is vertex no.
        self.edges = [ [] for i in range(n)]
        self.looseEdgesData = [ [0]*n for j in range(n)] # fill all elements to 0
        self.looseEdgesCrossStatus = [ [-1]*n for j in range(n)] # fill all elements to -1
        self.deliveryPriority = [ [] for k in range(n)]

    def addEdge(self, u, v) :
        #considering vertexes starting from 1
        self.edges[u-1].append(v-1)
        self.edges[v-1].append(u-1)

    def edgeIsLoose(self, src, dst) :
        if(self.looseEdgesData[src][dst]==0) :
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
            self.looseEdgesCrossStatus[src-1][dst-1] = 0
            self.looseEdgesCrossStatus[dst-1][src-1] = 0

        self.startNode = int(fileData.readline()) - 1
        s = int(fileData.readline())
        for k in range(s) :
            p, q = map(int, fileData.readline().split())
            self.studentsData[p-1] = [q-1, False] ## p-1 , q-1 ???
            self.pizzerias.append(q-1)

        t = int(fileData.readline())
        for l in range(t) :
            a, b = map(int, fileData.readline().split())
            std1, pizz1 = map(int, linecache.getline(fileName, a+m+1+h+1+1+1).split())
            std2, pizz2 = map(int, linecache.getline(fileName, b+m+1+h+1+1+1).split())
            self.deliveryPriority[std1-1].append(std2-1) ## a-1 , b-1 ???

    def showLooseEdges(self) :
        print("loose edges are : ")
        for i in range(self.vertexNo) :
            for j in range(self.vertexNo) :
                if(self.looseEdgesData[i][j] != 0) :
                    print("(", i+1, "->", j+1, ") : ", self.looseEdgesData[i][j])
                    #print("(", j+1, "->", i+1, ") : ", self.looseEdgesData[i][j])
                    #print("-------------------")

    def looseEdgeIsCrossed(self, src, dst) :
        if(self.looseEdgesCrossStatus[src][dst] == 1) :
            return True
        return False

    def crossLooseEdge(self, src, dst) :
        self.looseEdgesCrossStatus[src][dst] = 1
        self.looseEdgesCrossStatus[dst][src] = 1

    def getLooseEdgeTime(self, src, dst) :
        return self.looseEdgesData[src][dst]

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


class NPDState :

    def __init__(self, graph, studentsRecieved = set(), path = [], pizzaTaken = -1, steps = 0, looseEdgeSpentTime = 0) :
        self.graph = graph
        self.studentsRecieved = studentsRecieved
        self.path = path
        self.pizzaTaken = pizzaTaken
        self.steps = steps
        self.looseEdgeSpentTime = looseEdgeSpentTime

    def __eq__(self, other) :
        if(other == None) :
            return False
        return (self.graph.startNode, self.studentsRecieved, self.pizzaTaken, self.looseEdgeSpentTime) == \
               (other.graph.startNode, other.studentsRecieved, other.pizzaTaken, other.looseEdgeSpentTime) #check tha last one and also graph.studentsData

    def __lt__(self, other) :
        return self.steps < other.steps

    def isGoal(self) :
        if(len(self.studentsRecieved) != len(self.graph.studentsData.keys())) : # not all students have recieved pizza
            return False
        if(self.graph.startNode not in self.graph.studentsData.keys()) : # our current node is not a student
            return False
        return True # all students have recieved pizza and our current node is a student which is the last student recieving pizza

    def createNewNPDState(self, currentNode) :

        newState1 = copy.deepcopy(self)
        newState1.graph.startNode = currentNode

        if(currentNode in self.graph.pizzerias) : #current node is pizza and you're not currently carrying another pizza
            if(self.pizzaTaken == -1) :
                pizzaAlreadyDelivered = False
                for m in self.graph.studentsData.keys() :
                    if(self.graph.studentsData[m][0] == currentNode) :
                        if(m in self.studentsRecieved) :
                            pizzaAlreadyDelivered = True

                newState2 = copy.deepcopy(newState1)
                newState1.pizzaTaken = currentNode
                newState1.path.append(currentNode+1)
                newState2.path.append(currentNode+1)
                newState1.steps+=1
                newState2.steps+=1
                return [newState1, newState2]

            else :
                newState1.path.append(currentNode+1)
                newState1.steps+=1
                return[newState1]

        elif(currentNode in self.graph.studentsData.keys() and (currentNode not in self.studentsRecieved)) :
            priorityIsOk = True
            studentPizzaIsBought = False
            if(self.graph.studentsData[currentNode][0] == self.pizzaTaken) :
                studentPizzaIsBought= True
            
            if(studentPizzaIsBought) :
                for i in range(self.graph.vertexNo) :
                    if(currentNode in self.graph.deliveryPriority[i]) :
                        if(i not in self.studentsRecieved) :
                            priorityIsOk = False
            
            if(priorityIsOk and studentPizzaIsBought) :
                newState1.studentsRecieved.add(currentNode)
                newState1.pizzaTaken = -1
                newState1.path.append(currentNode+1)
                newState1.steps += 1
                return [newState1]  

            newState1.path.append(currentNode+1)
            newState1.steps += 1
            return [newState1]

        newState1.path.append(currentNode+1)
        newState1.steps+=1
        return [newState1]

    def getNewNPDStates(self) :
        newStates = []
        v = self.graph.startNode
        stateLooseEdgesStatus = []

        # for n in self.graph.edges[v] :
        #     s = self.createNewNPDState(n)
        #     for stateItem in s :
        #         newStates.append(stateItem)

        # return newStates

        for n in self.graph.edges[v] :
            createNewStateAsNormal = True

            if(self.graph.edgeIsLoose(n, v)) :

                if(self.graph.looseEdgeIsCrossed(n, v)==False) :
                    createNewStateAsNormal=False
                    states = self.createNewNPDState(n)
                    for st in states :
                        st.graph.crossLooseEdge(n, v)
                        newStates.append(st)

                else :
                    if(self.graph.looseEdgesData[n][v] > self.looseEdgeSpentTime) :
                        createNewStateAsNormal = False
                        newState = copy.deepcopy(self)
                        newState.steps+=1
                        newState.path.append(v+1)
                        newState.looseEdgeSpentTime += 1
                        newStates.append(newState)
                    else :
                        createNewStateAsNormal = False
                        states2 = self.createNewNPDState(n)
                        for st2 in states2 :
                            st2.looseEdgeSpentTime=0
                            newStates.append(st2)

            if(createNewStateAsNormal == True) :
                s = self.createNewNPDState(n)
                for stateItem in s :
                    newStates.append(stateItem)
        
        return newStates   

    def heuristic(self) :
        pizzasNotDelivered = 0
        for i in self.graph.studentsData.keys() :
            if(i not in self.studentsRecieved) :
                pizzasNotDelivered += 1

        return pizzasNotDelivered


def BFS(init_state) :
    frontier, visited, visit_states = [], [], 0
    frontier.append(copy.deepcopy(init_state))

    while  len(frontier) > 0 :

        current_state = frontier.pop(0)
        visit_states += 1

        if current_state.isGoal() :
            path, cost_of_path = current_state.path, current_state.steps
            return path, cost_of_path, visit_states

        visited.append(current_state)  
        new_states = current_state.getNewNPDStates()

        for s in new_states :
            if (s not in visited) and (s not in frontier)  :
                frontier.append(s)
               
    return None, None, visit_states


def DFS(init_state, depth) :
    stack, visited, visit_states_num = [], [], 0
    stack.append(copy.deepcopy(init_state))

    while len(stack) > 0  :
        cur_state = stack.pop()

        if cur_state.isGoal() :
            return cur_state.path, cur_state.steps, visit_states_num, True
            
        if (cur_state.steps >= depth ) or ((cur_state, cur_state.steps) in visited):
            continue

        visit_states_num += 1
        visited.append((cur_state, cur_state.steps))

        new_states = cur_state.getNewNPDStates()

        for s in new_states :
            if ( (s, s.steps) not in visited ) :
                stack.append(s)

    return None, None, visit_states_num, False


def IDS(init_state) :
    depth, total_visit_state = 1, 0
    while True :
        path, cost_of_path,visitStates, goalReached= DFS(copy.deepcopy(init_state), depth)
        total_visit_state += visitStates
        if goalReached :
            break
        depth += 1
    
    return path, cost_of_path, total_visit_state


def ASTAR(init_state, heuristicWeight=1) :
    frontier, front_list, visited, visited_state = [ [init_state.heuristic()*heuristicWeight, init_state] ], [init_state], [], 0

    while len(frontier) > 0 :
        (h, cur_state) = heapq.heappop(frontier)

        if cur_state.isGoal() :
            return cur_state.path, cur_state.steps, visited_state

        visited.append(cur_state)
        visited_state += 1
        new_states = cur_state.getNewNPDStates()

        for s in new_states :
            if (s not in visited) and (s not in front_list):
                heapq.heappush(frontier, [s.steps + s.heuristic()*heuristicWeight, s] )
                front_list.append(s)

    return cur_state.path, cur_state.steps, visited_state



## execution config start

testFileNo = 0 # from 0 to 5
filePath = "E:\\university\\semester 8\\AI\\CA1\\AI-CA1\\code\\tests\\" + "Test" + str(testFileNo) + ".txt"
numberOfExecutions = 3
selectedAlgorithm = BFSAlgorithm
heuristicWeight1 = 1.5
heuristicWeight2 = 8

uniGraph = UniGraph()
uniGraph.retrieveGraphData(filePath)

## execution config end

initial_state = NPDState(graph=uniGraph, path=[uniGraph.startNode+1])

executionTimes = []
for i in range(numberOfExecutions) :
    
    start = time.time()

    if(selectedAlgorithm == BFSAlgorithm) :
        path, cost_of_path, visit_states = BFS(initial_state)

    elif(selectedAlgorithm == IDSAlgorithm) : 
        path, cost_of_path, visit_states = IDS(initial_state)
    
    elif(selectedAlgorithm == ASTARAlgorithm) :
        path, cost_of_path, visit_states = ASTAR(initial_state)
    
    elif(selectedAlgorithm == ASTARAlgorithmWeighted) :
        path, cost_of_path, visit_states = ASTAR(initial_state, heuristicWeight=heuristicWeight1)
        #path, cost_of_path, visit_states = ASTAR(initial_state, heuristicWeight=heuristicWeight2)

    else :
        print("Wrong configuration!\n")

    end = time.time()
    executionTimes.append(end - start)

print(f"Path : {path}\nCost Of Path : {cost_of_path}\
        \nExecution Time : {sum(executionTimes)/numberOfExecutions}\nSeen States : {visit_states}")
