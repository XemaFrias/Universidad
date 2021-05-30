
#!/usr/bin/env python3
from sys import argv
import time
import copy

MAP = [] #This is a tuple after parsing
SCHOOLS = {}
FLOYD_SCHOOLS={}
BUS_SIZE = 0
statistics_stops = 0
statistic_expansions = 0
statistics_cost = 0
statistics_endtime = 0
output_array = []
FLOYD_matrix =[]
heu =""

class Node:
    def __init__(self, pos, stp, std, parent,action=""): # Atributes for Node. pos, stp and stp conform the state of the model
        self.pos = pos
        self.stp = stp
        self.std = std
        self.parent = parent
        self.f = 0
        self.g = 0
        self.children = []
        self.action = action              ####Really useful for final printing

    def GenerateChildrenNodes(self): # Function that cheks which actions are possible for the current state and generates new nodes in consecuence
        actual_stop = self.pos.strip('P')
        if self.pos in self.stp:  #If the bus is in a stop whith students, function of pick student is invoked
            self.pickUpStudent()
        if self.pos in SCHOOLS and SCHOOLS[self.pos] in self.std: # If the bus is in a stop whith a school and a student going to that school is in the bus, function of deliver student is invoked
            self.deliverStudent()
        self.move(actual_stop) #We don't need any condition for trying to move the bus
        return self.children

    def pickUpStudent(self):
        for x in list(self.stp[self.pos].items()):
            aux_dic = dict(self.stp[self.pos])
            copy_stp = dict(self.stp) #STP of the children
            copy_std = dict(self.std) #STD of the children
            if x[0] in copy_stp[self.pos] and self.elementsInSTD() < BUS_SIZE:
                aux=str(x)
                number_student = x[1] - 1
                #Remove the students from the stop that were picked up in STP
                if number_student == 0:
                    aux_dic.pop(x[0])
                    if len(aux_dic) == 0:
                        copy_stp.pop(self.pos)
                    else:
                        copy_stp[self.pos] = dict(aux_dic)
                else:
                    aux_dic[x[0]] = number_student
                    copy_stp[self.pos] = dict(aux_dic)
                #Add the students that were picked up in STD
                if x[0] not in copy_std:
                    copy_std[x[0]] = 1
                else:
                    copy_std[x[0]] += 1
                new_child = Node(self.pos, copy_stp, copy_std, self,"(S: 1 "+aux[2:4]+")")
                new_child.g = self.g
                new_child.f = new_child.g + new_child.heuristic()
                self.children.append(new_child)

    def deliverStudent(self):
        copy_std = dict(self.std)
        pos = SCHOOLS[self.pos]
        aux = pos
        if pos in copy_std: # Removing a student from the bus
            if copy_std[pos] == 1:
                copy_std.pop(pos)
            else:
                copy_std[pos] -= 1
        new_child = Node(self.pos, self.stp, copy_std, self,"(B: 1 "+aux+")") # After leaving the student, the new node with the state without the student is generated
        new_child.g = self.g
        new_child.f = new_child.g + new_child.heuristic()
        self.children.append(new_child) # Append child node to children list of parent node

    def move(self,actual_stop):
        for index, x in enumerate(MAP[int(actual_stop)-1]): # For each stop connected
            if x!= 1000000000000000000000: #representation of infinitum (not connection between stops)
                new_pos = 'P' + str(index+1)
                new_child = Node(new_pos, self.stp, self.std, self,"")
                new_child.g = self.g + x
                new_child.f =new_child.g + new_child.heuristic()
                self.children.append(new_child)

    def heuristic(self):
        global heu #Look for heuristc user has gave us
        total = 0
        if(heu == 'pickD'):
            actual_stop=int(self.pos.strip('P'))-1 #We have to look positions in the matrix such that P5 will be in position 4
            for x in self.stp: #For each of the possible stops with students
                school_stop=int(x.strip('P'))-1
                actual_stop=int(self.pos.strip('P'))-1
                total+=FLOYD_matrix[actual_stop][school_stop] #How far is the bus from them
        if(heu == 'busD'):
            actual_stop=int(self.pos.strip('P'))-1
            for x in self.std: #For the students that we have on the bus
                school_stop=int(FLOYD_SCHOOLS[x].strip('P'))-1
                if school_stop != actual_stop:
                    total+=FLOYD_matrix[actual_stop][school_stop] #How far are they from their school
        if(heu == 'lowB'): #combination of the 2 previous
            actual_stop=int(self.pos.strip('P'))-1
            for x in self.stp:
                school_stop=int(x.strip('P'))-1
                actual_stop=int(self.pos.strip('P'))-1
                total+=FLOYD_matrix[actual_stop][school_stop]
            for x in self.std:
                school_stop=int(FLOYD_SCHOOLS[x].strip('P'))-1
                total+=FLOYD_matrix[actual_stop][school_stop]
        return total

    def elementsInSTD(self): # Count number of students in the bus
        count = 0
        for x in self.std:
            count += int(self.std[x])
        return count

    def toString(self): #Store the node in the solution array
        global statistics_stops
        global output_array
        output_array.append(str(self.pos)+" "+ self.action)
        statistics_stops +=1 #we have to keep count how many states does the final solution have

    def printPath(self): #recursive funtion to print all states that lead to solution state
        self.toString()
        if self.parent != 0:
            self.parent.printPath()

class Solver():
    def __init__(self, start):
        self.start = start

    def Solver(self):
        startNode = Node(self.start.pos, self.start.stp, self.start.std, self.start.parent)
        startNode.f = startNode.heuristic()
        openSet = [startNode] #initialize the open list
        closeSet = []
        success = False
        global statistic_expansions
        global statistics_cost
        global statistics_endtime
        while len(openSet) != 0 and not success:
            statistic_expansions+=1
            best = openSet[0].f
            best_g = openSet[0].g
            new_node = openSet[0]
            for x in openSet:
                if x.f < best:
                    best = x.f
                    best_g = x.g
                    new_node = x
                if x.f == best:
                    if x.f - x.g < best - best_g: ##Bigger g means the heuristic is smaller
                        best = x.f
                        best_g = x.g
                        new_node = x

            if new_node.pos == self.start.pos and len(new_node.stp) == 0 and len(new_node.std) == 0: #if the state equals our final state
                success = True
                statistics_endtime = time.time() #We have found solution so we stop the time
                statistics_cost = new_node.g
                print('Solution found!')  #Give user Feedback to let him know
                new_node.printPath()
                break
            else:
                new_children = new_node.GenerateChildrenNodes() # Invoke function to generate children of the node that is being evaluated
                openSet.remove(new_node) #Remove chosen node from the open list and move it to the close one
                closeSet.append(new_node)
                for x in list(new_children): #Check if any of the newly generated nodes is useful
                    for y in list(openSet):
                        if x.pos == y.pos and x.stp == y.stp and x.std == y.std:
                            if x.f < y.f: #If we find 2 nodes with the same characteristics but the new one has less cost, we get rid of the old one
                                openSet.remove(y)
                            else:
                                new_children.remove(x)
                                break
                for x in list(new_children):
                    for y in list(closeSet):
                        if x.pos == y.pos and x.stp == y.stp and x.std == y.std:
                            new_children.remove(x) #This nodes are already in the close one so we know they are the best option, so we ignore new ones
                            break
                for x in new_children: #The nodes that haven't been removed can be potential candidates
                    openSet.append(x)
        return success

def matrix_parser(file):
    stops = file.readline().split("P")  # Read the first line dividing whenerver a P is found. This will give us the stops
    stops = len(stops) - 1
    last = 0
    costs_matrix = []
    for x in range(stops): # Create the cost matrix knowing its dimensions
        var = file.readline().strip('\n').split(' ') # Removing special characters, reading line by line until all stops are read
        var.pop(0)
        while "" in var:
            var.remove('')
        for i, y in enumerate(var):
            if var[i] == '--':
                var[i] = 1000000000000000000000
            else:
                var[i] = int(var[i]) #We cast the numbers as integers
        costs_matrix.append((var))
    return (costs_matrix)

def parse_schools(file):
    schools_array = file.readline().strip('\n').split('; ') #We haven't close the file so we can continue reading
    for x in schools_array:
        var = x.split(': ')
        SCHOOLS[var[1]]=var[0]
        FLOYD_SCHOOLS[var[0]]=var[1] #Inverse of the previous dictionary that will be used in the floyd matrix generation

def parse_students(file):
    auxstudents = file.readline().strip('\n').split('; ')
    students_dic = {}
    for x in auxstudents: #Aux students stores each of the stops  separately
        var = x.split(': ')
        var2 = var[1].split(', ') #We need to continue spliting in case there are children that go to different schools
        aux_dic = {}
        for y in var2:
            var3 = y.split(' ')
            aux_dic[var3[1]] = int(var3[0])
        students_dic[var[0]] = aux_dic
    return students_dic

def parse_bus(file):
    auxbus = file.readline().strip('B: ').split(' ')
    return auxbus[0],int(auxbus[1])

def init_Floyd_matrix(): #Creates a matrix that gives cost of the shortest path between nodes of the graph
  global FLOYD_matrix
  FLOYD_matrix= copy.deepcopy(MAP) #Generate a copy of the problems graph
  vertices=len(MAP)
  for k in range(vertices): #implementation of Floyd-Warshall
      for i in range(vertices):
          for j in range(vertices):
              FLOYD_matrix[i][j] = min(FLOYD_matrix[i][j], FLOYD_matrix[i][k] + FLOYD_matrix[k][j])
  count=0
  for x in FLOYD_matrix:
      x[count]=0
      count+=1


if __name__ == "__main__":
    # Arguments are assigned to correspondet variables
    input = argv[1]
    if len(argv) == 3:
        heu = argv[2]
    f = open(input) #store the memory direction of the specified file
    MAP = matrix_parser(f)
    parse_schools(f)
    STP = parse_students(f)
    bus_pos, BUS_SIZE = parse_bus(f)
    f.close()
    if heu != "": #Floyd is only useful if we are going to use an heuristic
        init_Floyd_matrix()
    #Intial node is created
    start = Node(bus_pos, STP, {}, 0,"")
    statistics_starttime = time.time()#Start the time as we start to look at the problem
    a_star = Solver(start)
    var = a_star.Solver()
    if(not var): #If solver didnt succed, inform the user
        print("Impossible to solve")
    else:
        filestr = input + ".statistics"
        f = open(filestr,"w+")
        statistics_totaltime = (statistics_endtime - statistics_starttime )
        f.write("Overall time: " + str(statistics_totaltime)+"\n")
        f.write("Overall cost: " + str(statistics_cost)+"\n")
        f.write("# Stops: " + str(statistics_stops)+"\n")
        f.write("# Expansions: " + str(statistic_expansions)+"\n")
        f.close()
        filestr = input + ".output"
        f = open(filestr,"w+")
        output_array.pop(0) #We already know that last state is bus.stop, so we do this for making easier our lives
        for i in reversed(output_array):
            f.write(i +" \u2192  ") #unicode for arrow
        f.write(bus_pos+"\n")
        f.close()
