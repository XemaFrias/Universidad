

# bustersAgents.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference
import busters
from distanceCalculator import Distancer
from game import Actions
from wekaI import Weka

ESTADOS =[]
SCORES=[]

class NullGraphics:
    "Placeholder for graphics"
    def initialize(self, state, isBlue = False):
        pass
    def update(self, state):
        pass
    def pause(self):
        pass
    def draw(self, state):
        pass
    def updateDistributions(self, dist):
        pass
    def finish(self):
        pass

class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """
    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs


class BustersAgent:
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable
        self.weka = Weka()
        self.weka.start_jvm()

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        #for index, inf in enumerate(self.inferenceModules):
        #    if not self.firstMove and self.elapseTimeEnable:
        #        inf.elapseTime(gameState)
        #    self.firstMove = False
        #    if self.observeEnable:
        #        inf.observeState(gameState)
        #    self.ghostBeliefs[index] = inf.getBeliefDistribution()
        #self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP

class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index = 0, inference = "KeyboardInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)

    def printLineData(self, gameState,ending):
        "Pacman"
        pacmanX=gameState.getPacmanPosition()[0]
        pacmanY=gameState.getPacmanPosition()[1]
        actualstate= (str(pacmanX) +", "+ str(pacmanY)+", ")
        "Legal Actions"
        legal = gameState.getLegalActions(0)
        north = 'North' in legal
        south = 'South' in legal
        east = 'East' in legal
        west = 'West' in legal
        stop = 'Stop' in legal
        actualstate +=(str(north) +", "+ str(south)+", "+ str(east) +", "+ str(west)+", "+ str(stop)+", ")
        "Ghosts Coordinates"
        ghostPos = gameState.getGhostPositions()
        for t in ghostPos:
            actualstate +=(str(t[0]) +", " + str(t[1]) + ", ")
        "Living Ghosts"
        actualstate +=(str(sum(gameState.getLivingGhosts())) + ", ")
        "Remaining food"
        actualstate +=(str(gameState.getNumFood()) + ", ")
        "Nearest Food Distance"
        actualstate +=(str(gameState.getDistanceNearestFood()) + ", ")
        "Nearest Food Coordinates"
        foodCoordinates = gameState.getNearestFood()
        if foodCoordinates is not None:
            actualstate +=(str(foodCoordinates[0]) +", " + str(foodCoordinates[1]) + ", ")
        else:
            actualstate +=(str(None) +", " + str(None) + ", ")
        "Chosen Action"
        dir = gameState.data.agentStates[0].getDirection()
        actualstate +=(str(dir) +", ")
        ESTADOS.append(actualstate)
        "Score"
        score = gameState.getScore()
        SCORES.append(str(score))
        if(ending):
            "Crear un archivo de salida arff y guardar la informacion relevante en el"
            f = open("test_samemaps_keyboard.arff","a")
            "Generamos 3 scores extra para los ultimos resultados asumiendo que este se mantienen igual debido al fin del juego. Por eso anadimos 200 del ultimo fantasma"
            score+=200-1
            SCORES.append(str(score))
            SCORES.append(str(score))
            SCORES.append(str(score))
            "Imprimimos todos los resultados"
            for index,x in enumerate(ESTADOS):
                f.write(x + SCORES[index] + ", " +SCORES[index+1] + ", " +SCORES[index+2] + ", " +SCORES[index+3] + "\n")
            f.close()

from distanceCalculator import Distancer
from game import Actions
from game import Directions
import random, sys

'''Random PacMan Agent'''
class RandomPAgent(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food

    ''' Print the layout'''
    def printGrid(self, gameState):
        table = ""
        ##print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def chooseAction(self, gameState):
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        move_random = random.randint(0, 3)
        if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move

class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (according to mazeDistance!).

        To find the mazeDistance between any two positions, use:
          self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
          successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief
        distributions for each of the ghosts that are still alive.  It
        is defined based on (these are implementation details about
        which you need not be concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i+1]]
        return Directions.EAST

class BasicAgentAA(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0

    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food

    ''' Print the layout'''
    def printGrid(self, gameState):
        table = ""
        #print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def printInfo(self, gameState):
        '''print "---------------- TICK ", self.countActions, " --------------------------"
        # Dimensiones del mapa
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print "Width: ", width, " Height: ", height
        # Posicion del Pacman
        print "Pacman position: ", gameState.getPacmanPosition()
        # Acciones legales de pacman en la posicion actual
        print "Legal actions: ", gameState.getLegalPacmanActions()
        # Direccion de pacman
        print "Pacman direction: ", gameState.data.agentStates[0].getDirection()
        # Numero de fantasmas
        print "Number of ghosts: ", gameState.getNumAgents() - 1
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        print "Living ghosts: ", gameState.getLivingGhosts()
        # Posicion de los fantasmas
        print "Ghosts positions: ", gameState.getGhostPositions()
        # Direciones de los fantasmas
        print "Ghosts directions: ", [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        # Distancia de manhattan a los fantasmas
        print "Ghosts distances: ", gameState.data.ghostDistances
        # Puntos de comida restantes
        print "Pac dots: ", gameState.getNumFood()
        # Distancia de manhattan a la comida mas cercada
        print "Distance nearest pac dots: ", gameState.getDistanceNearestFood()
        # Paredes del mapa
        print "Map:  \n", gameState.getWalls()
        # Puntuacion
        print "Score: ", gameState.getScore()'''


    def printLineData(self, gameState,ending):
        "Pacman"
        pacmanX=gameState.getPacmanPosition()[0]
        pacmanY=gameState.getPacmanPosition()[1]
        actualstate= (str(pacmanX) +", "+ str(pacmanY)+", ")
        "Legal Actions"
        legal = gameState.getLegalActions(0)
        north = 'North' in legal
        south = 'South' in legal
        east = 'East' in legal
        west = 'West' in legal
        stop = 'Stop' in legal
        actualstate +=(str(north) +", "+ str(south)+", "+ str(east) +", "+ str(west)+", "+ str(stop)+", ")
        "Ghosts Coordinates"
        ghostPos = gameState.getGhostPositions()
        distance=99999
        dis= Distancer(gameState.data.layout)
        for t in ghostPos:
            candidate=dis.getDistance(gameState.getPacmanPosition(), t)
            if (candidate<distance):
                distance=candidate
                x=t[0]
                y=t[1]
        actualstate +=(str(x) +", " + str(y) + ", ")

        "Living Ghosts"
        if ((sum(gameState.getLivingGhosts())) is not None):
            actualstate +=(str(sum(gameState.getLivingGhosts())) + ", ")
        else: actualstate+=("0, ")
        "Distnace Ghost"
        if min(gameState.data.ghostDistances) is not None:
            actualstate +=(str(min(gameState.data.ghostDistances)) + ", ")
        else: actualstate +=("0, ")
        "Remaining food"
        if (gameState.getNumFood() is not None):
            actualstate +=(str(gameState.getNumFood()) + ", ")
        else: actualstate+=("0, ")
        "Nearest Food Distance"
        if (gameState.getDistanceNearestFood() is not None):
            actualstate +=(str(gameState.getDistanceNearestFood()) + ", ")
        else: actualstate+=("9999, ")
        "Nearest Food Coordinates"
        foodCoordinates = gameState.getNearestFood()
        if foodCoordinates is not None:
            actualstate +=(str(foodCoordinates[0]) +", " + str(foodCoordinates[1]) + ", ")
        else:
            actualstate +=(str(9999) +", " + str(9999) + ", ")
        "Chosen Action"
        dir = gameState.data.agentStates[0].getDirection()
        actualstate +=(str(dir) +", ")
        ESTADOS.append(actualstate)
        "Score"
        score = gameState.getScore()
        SCORES.append(str(score))
        if(ending):
            "Crear un archivo de salida arff y guardar la informacion relevante en el"
            f = open("basicAgentAA.arff","a")
            "Generamos 3 scores extra para los ultimos resultados asumiendo que este se mantienen igual debido al fin del juego. Por eso anadimos 200 del ultimo fantasma"
            score+=200-1
            SCORES.append(str(score))
            SCORES.append(str(score))
            SCORES.append(str(score))
            "Imprimimos todos los resultados"
            for index,x in enumerate(ESTADOS):
                f.write(x + SCORES[index] + ", " +SCORES[index+1] + ", " +SCORES[index+2] + ", " +SCORES[index+3] + "\n")
            f.close()

    def findMinDistance(self, gameState,Distancer,action):
        "Show the new possible position of Pacman"
        dx, dy =  Actions._directions[action]
        x, y = gameState.getPacmanPosition()
        x +=dx
        y +=dy
        newPosPacman=(x,y)
        "Calculate distances in new position"
        distances=[]
        ghostPos = gameState.getGhostPositions()
        "Pop if any ghost has already been eaten"
        ghostDistance =gameState.data.ghostDistances
        index=0
        for z in ghostDistance:
            if z is None:
                ghostPos.pop(index)
                ghostDistance.pop(index)
            index +=1
        "Now we have a clean list"
        for t in ghostPos:
            distance = Distancer.getDistance(newPosPacman, t)
            distances.append(distance)
        if len(distances) >0:
            return min(distances)
        else: return 99999999

    def huntFood(self, gameState,Distancer,action):
        "Show the new possible position of Pacman"
        dx, dy =  Actions._directions[action]
        x, y = gameState.getPacmanPosition()
        x +=dx
        y +=dy
        newPosPacman=(x,y)
        foodCoordinates = gameState.getNearestFood()
        if foodCoordinates is None:
            return 99999999
        else:
            distance = Distancer.getDistance(newPosPacman, foodCoordinates)
            return distance


    def chooseAction(self, gameState):
        
        '''IA Programada'''
        '''

        distanceCalc= Distancer(gameState.data.layout)
        self.countActions = self.countActions + 1
        self.printInfo(gameState)
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        actionChoose= Directions.STOP
        minimumDistance= 999999
        foodCoordinates = gameState.getNearestFood()
        if sum(gameState.getLivingGhosts())==1 and gameState.getNumFood()==1:
            if (Directions.WEST in legal):
                choose = self.huntFood(gameState,distanceCalc,Directions.WEST)
                if (choose<= minimumDistance):
                    actionChoose= Directions.WEST
                    minimumDistance= choose
            if (Directions.EAST in legal):
                choose = self.huntFood(gameState,distanceCalc,Directions.EAST)
                if (choose<= minimumDistance):
                    actionChoose= Directions.EAST
                    minimumDistance= choose
            if (Directions.NORTH in legal):
                choose = self.huntFood(gameState,distanceCalc,Directions.NORTH)
                if (choose<= minimumDistance):
                    actionChoose= Directions.NORTH
                    minimumDistance= choose
            if (Directions.SOUTH in legal):
                choose = self.huntFood(gameState,distanceCalc,Directions.SOUTH)
                if (choose<= minimumDistance):
                    actionChoose= Directions.SOUTH
                    minimumDistance= choose
        elif foodCoordinates is None or (min(gameState.data.ghostDistances)<3 and gameState.getDistanceNearestFood()>4) :
            if (Directions.WEST in legal):
                choose = self.findMinDistance(gameState,distanceCalc,Directions.WEST)
                if (choose<= minimumDistance):
                    actionChoose= Directions.WEST
                    minimumDistance= choose
            if (Directions.EAST in legal):
                choose = self.findMinDistance(gameState,distanceCalc,Directions.EAST)
                if (choose<= minimumDistance):
                    actionChoose= Directions.EAST
                    minimumDistance= choose
            if (Directions.NORTH in legal):
                choose = self.findMinDistance(gameState,distanceCalc,Directions.NORTH)
                if (choose<= minimumDistance):
                    actionChoose= Directions.NORTH
                    minimumDistance= choose
            if (Directions.SOUTH in legal):
                choose = self.findMinDistance(gameState,distanceCalc,Directions.SOUTH)
                if (choose<= minimumDistance):
                    actionChoose= Directions.SOUTH
                    minimumDistance= choose
        else:
            #Similar code but for food
            if (Directions.WEST in legal):
                choose = self.huntFood(gameState,distanceCalc,Directions.WEST)
                if (choose<= minimumDistance):
                    actionChoose= Directions.WEST
                    minimumDistance= choose
            if (Directions.EAST in legal):
                choose = self.huntFood(gameState,distanceCalc,Directions.EAST)
                if (choose<= minimumDistance):
                    actionChoose= Directions.EAST
                    minimumDistance= choose
            if (Directions.NORTH in legal):
                choose = self.huntFood(gameState,distanceCalc,Directions.NORTH)
                if (choose<= minimumDistance):
                    actionChoose= Directions.NORTH
                    minimumDistance= choose
            if (Directions.SOUTH in legal):
                choose = self.huntFood(gameState,distanceCalc,Directions.SOUTH)
                if (choose<= minimumDistance):
                    actionChoose= Directions.SOUTH
                    minimumDistance= choose

        return actionChoose

        '''
        ''' FIN IA PROGRAMADA '''

        ''' WEKA '''

        "Pacman"
        pacmanX=gameState.getPacmanPosition()[0]
        pacmanY=gameState.getPacmanPosition()[1]
        "Legal Actions"
        legal = gameState.getLegalActions(0)
        north = str('North' in legal)
        south = str('South' in legal)
        east = str('East' in legal)
        west = str('West' in legal)
        stop = str('Stop' in legal)
        "Ghosts Coordinates"
        ghostPos = gameState.getGhostPositions()
        "Nearest Food Coordinates"
        foodCoordinates = gameState.getNearestFood()
        if (foodCoordinates is not None):
            foodCoordinates0 = foodCoordinates[0]
            foodCoordinates1 = foodCoordinates[1]
        else:
            foodCoordinates0 = 9999
            foodCoordinates1 = 9999

        x = [pacmanX, pacmanY, north, south, east, west, stop]
        for t in ghostPos:
            x.append(t[0])
            x.append(t[1])
        x.extend([foodCoordinates0, foodCoordinates1])
        a = self.weka.predict("./MODELS/J48.model", x, "./ARFF/test_allmaps.arff")
        #print(x, a)
        if (a in legal):
            return a
        else:
            move = Directions.STOP
            legal = gameState.getLegalActions(0) ##Legal position from the pacman
            move_random = random.randint(0, 3)
            if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
            if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
            if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
            if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
            return move
