import time
import copy
import heapq
import linecache
import timeit

spentTime = 0

currentUserPizza = -1

class UniGraph : 
    
    def __init__(self, edges = [], vertexNo = 0, looseEdgesData = [], studentsData = {}, deliveryPriority = [], pizzerias = [], startNode = 0) :
        self.edges = edges
        self.vertexNo = vertexNo
        self.looseEdgesData = looseEdgesData
        self.studentsData = studentsData
        self.deliveryPriority = deliveryPriority
        self.pizzerias = pizzerias
        self.startNode = startNode

    def __eq__(self, other) : 
        return (self.edges, self.vertexNo, self.looseEdgesData, self.studentsData, self.deliveryPriority, self.pizzerias, self.startNode) == \
        (other.edges, other.vertexNo, other.looseEdgesData, other.studentsData, other.deliveryPriority, other.pizzerias, other.startNode)

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
                currentUserPizza = i

    def pizzaIsBoughtForStudent(self, node) : # check delivery priority here ??
        if(node == currentUserPizza) :
            self.studentsData[node][1]=True
            return True
        return False


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

        newState1.path.append(currentNode)
        newState1.steps+=1
        return [newState1]


        # if((currentNode in self.graph.studentsData.keys()) and (currentNode not in self.studentsRecieved)) : #if cuurent node is student and has not recieved pizza yet check pizza delivery and priority
        #     priorityIsOk = True
        #     studentPizzaIsBought = False
        #     if(self.graph.studentsData[currentNode][0] in self.pizzasTaken) :
        #         studentPizzaIsBought = True

        #     if(studentPizzaIsBought) :
        #         for i in range(self.graph.vertexNo) :
        #             if(currentNode in self.graph.deliveryPriority[i]) :
        #                 if(i not in self.studentsRecieved) :
        #                     priorityIsOk = False

        #     if(priorityIsOk and studentPizzaIsBought) : # we can deliver pizza to student
        #         newState.studentsRecieved.add(currentNode)
        #         newState.pizzasTaken.clear()
        
        # else : # its a pizzeria
        #     if(currentNode in self.graph.pizzerias) :

        #         pizzaAlreadyDelivered = False
        #         for m in self.graph.studentsData.keys() :
        #             if(self.graph.studentsData[m][0] == currentNode) :
        #                 if(m in self.studentsRecieved) :
        #                     pizzaAlreadyDelivered = True

        #         if(currentNode not in newState.pizzasTaken and (pizzaAlreadyDelivered==False)) :
        #             newState.pizzasTaken.append(currentNode)
        

        # newState.path.append(currentNode+1)
        # newState.steps+=1
        # return newState
        
    def getNewNPDStates(self) :
        newStates = []
        v = self.graph.startNode
        
        #check loose edges here !

        for node in self.graph.edges[v] :
            s = self.createNewNPDState(node)
            for stateItem in s :
                newStates.append(stateItem)
            #newStates.append(self.createNewNPDState(node)) 

        return newStates   


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
        #         print("appended", s.graph.startNode)
        # print("--")        

    return None, None, visit_states


uniGraph_ = UniGraph()
uniGraph_.retrieveGraphData("E:\\university\\semester 8\\AI\\CA1\\AI-CA1\\code\\tests\\Test1.txt")


initial_state = NPDState(graph=uniGraph_, path=[uniGraph_.startNode+1])
# NPD(uniGraph=uniGraph_, pathTraversed = [uniGraph_.startNode+1])

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
