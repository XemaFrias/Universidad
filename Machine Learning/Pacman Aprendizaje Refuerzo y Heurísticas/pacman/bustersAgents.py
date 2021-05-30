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
		self.distanceCal= 0

	def registerInitialState(self, gameState):
		"Initializes beliefs and inference modules"
		import __main__
		self.distanceCal= Distancer(gameState.data.layout)
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
	"""
	  Q-Learning Agent

	  Functions you should fill in:
		- update

	  Instance variables you have access to
		- self.epsilon (exploration prob)
		- self.alpha (learning rate)
		- self.discount (discount rate)
	"""
	def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True):
		inferenceType = util.lookup(inference, globals())
		self.inferenceModules = [inferenceType(a) for a in ghostAgents]
		self.observeEnable = observeEnable
		self.elapseTimeEnable = elapseTimeEnable
		self.table_file = open("qtable.txt", "r+")
		self.q_table = self.readQtable()
		self.alpha = 0	    #alpha    - learning rate
		self.epsilon = 0    #epsilon  - exploration rate
		self.gamma = 0      #gamma    - discount factor

		self.actions = {"North":0, "South":1, "West":2, "East":3}
		self.ghostDir = 0    #estado[0], la direccion en la que te acercas al fantasma mas cercano
		self.foodDir = 4     #estado[1], la direccion en la que te acercas a la comida mas cercana. 4 significa que no quedan
		self.ghostDistance = 9999             #variable: guarda la distancia al fantasma mas cercano
		self.foodDistance = 9999              #variable: guarda la distancia a la comida mas cercana
		self.estados = [(0,0),(0,0)]      #array de estadoAnterior y estadoActual
		self.scores = [0,0]                   #array de scoreAnterior y scoreActual
		self.counter = False                  #booleano, True si ya ha pasado un tick desde el inicio de la ejecucion
		self.distanceReward = [0,20]          #array de variables: guardan la distancia a lo mas cercano en el anterior y el actual
		self.dinamic = [0,0,0,0]              #variable: guarda la distancia al fantasma mas cercano si te movieras 1 en cada direccion
		self.actionsArray = ["North","North"] #variable: guarda la accion tomada en el anterior y en el actual
		self.legalActions = []                #array de acciones: guarda las acciones legales en el actual

	def readQtable(self):
		table = self.table_file.readlines()
		q_table = []

		for i, line in enumerate(table):
			row = line.split()
			row = [float(x) for x in row]
			q_table.append(row)

		return q_table

	def writeQtable(self):
		"Write qtable to disc"
		self.table_file.seek(0)
		self.table_file.truncate()

		for line in self.q_table:
			for item in line:
				self.table_file.write(str(item)+" ")
			self.table_file.write("\n")

	def __del__(self):
		"Destructor. Invokation at the end of each episode"
		self.writeQtable()
		self.table_file.close()

	def computePosition(self, state):
		return state[0]*5+state[1]

	def getQValue(self, state, action):
		position = self.computePosition(state)
		action_column = self.actions[action]

		return self.q_table[position][action_column]

	def computeValueFromQValues(self, state):
		if len(self.legalActions)==0:
			return 0
		return max(self.q_table[self.computePosition(state)])

	def computeActionFromQValues(self, state):
		best_actions = [self.legalActions[0]]
		best_value = self.getQValue(state, self.legalActions[0])
		for action in self.legalActions:
			value = self.getQValue(state, action)
			if value == best_value:
				best_actions.append(action)
			if value > best_value:
				best_actions = [action]
				best_value = value
		return random.choice(best_actions)

	def findMinDistance(self, pacmanPos, ghostPos, ghostDis, action, dir):
		"Show the new possible position of Pacman"
		dx, dy =  Actions._directions[action]
		x, y = pacmanPos
		x += dx
		y += dy
		newPosPacman=(x,y)
		"Calculate distances in new position"
		distances=[]
		for t in ghostPos:
			dist = self.distanceCal.getDistance(newPosPacman, t)
			distances.append(dist)
		self.dinamic[dir]=min(distances)
		print self.dinamic[dir]

	def calculateDir(self, pacmanPos, ghostPos, ghostDis):
		self.dinamic = [9999,9999,9999,9999]
		if 'North'in self.legalActions:
			print("Distancias si Norte")
			self.findMinDistance(pacmanPos, ghostPos, ghostDis, Directions.NORTH, 0)
		if 'South'in self.legalActions:
			print("Distancias si Sur")
			self.findMinDistance(pacmanPos, ghostPos, ghostDis, Directions.SOUTH, 1)
		if 'East'in self.legalActions:
			print("Distancias si Este")
			self.findMinDistance(pacmanPos, ghostPos, ghostDis, Directions.EAST, 3)
		if 'West'in self.legalActions:
			print("Distancias si Oeste")
			self.findMinDistance(pacmanPos, ghostPos, ghostDis, Directions.WEST, 2)
		print "self.dinamic", self.dinamic
		self.ghostDistance=min(self.dinamic)
		index=0
		for x in self.dinamic:
			if x==self.ghostDistance:
				self.ghostDir=index
			index+=1
		print "self.ghostDir", self.ghostDir

	def huntFood(self, pacmanPos, foodPos, action, dir):
		dx, dy = Actions._directions[action]
		x, y = pacmanPos
		x += dx
		y += dy
		newPosPacman = (x,y)
		distance = self.distanceCal.getDistance(newPosPacman, foodPos)
		if distance<self.foodDistance:
			self.foodDistance=distance
			self.foodDir=dir

	def foodDirect(self, pacmanPos, foodPos):
		self.foodDistance=99
		if foodPos is not None:
			if 'North'in self.legalActions:
				self.huntFood(pacmanPos, foodPos, Directions.NORTH, 0)
			if 'South'in self.legalActions:
				self.huntFood(pacmanPos, foodPos, Directions.SOUTH, 1)
			if 'East'in self.legalActions:
				self.huntFood(pacmanPos, foodPos, Directions.EAST, 3)
			if 'West'in self.legalActions:
				self.huntFood(pacmanPos, foodPos, Directions.WEST, 2)
		else:
			self.foodDir=4
		print "distancia Comida", self.foodDistance

	def getAction(self, gameState):
		print "--------------Nuevo tick-----------------"
		#Actualizamos los arrays de control para dejar hueco a la seccion de ahora
		self.estados[0] = self.estados[1]
		self.scores[0] = self.scores[1]
		self.distanceReward[0] = self.distanceReward[1]
		self.actionsArray[0] = self.actionsArray[1]

		#No nos interesa el Stop asi que lo eliminamos
		self.legalActions = gameState.getLegalActions()
		self.legalActions.remove('Stop')

		self.scores[1]= gameState.getScore()

		#Calculamos los atributos del estado
		pacmanPos = gameState.getPacmanPosition()
		foodPos = gameState.getNearestFood()
		ghostPos = gameState.getGhostPositions()
		ghostDis = gameState.getNoisyGhostDistances()

		index=0
		while index < len(ghostDis):
			if ghostDis[index] is None:
				ghostDis.pop(index) #Eliminamos del array de distancias a los fantasmas los que hayan sido comidos
				ghostPos.pop(index) #Tambien del array de posiciones
			else:
				index +=1
		self.calculateDir(pacmanPos, ghostPos, ghostDis)
		self.foodDirect(pacmanPos, foodPos)

		#Elegimos como medir el refuerzo, o la distancia a la comida mas cercana o al fanastama mas cercano
		if foodPos is None:                     #Si no queda comida, el refuerzo se aplica si te acercas al fantasma mas cercano
			print "No hay Comida"
			self.distanceReward[1] = min(ghostDis)
		else:
			print "Comida mas Cerca"
			self.distanceReward[1]=self.foodDistance

		#Se construye el nuevo estado actual
		estado=(self.ghostDir, self.foodDir)
		self.estados[1] = estado
		print "estado: ", self.estados[1]

		#Moneda decide en funcion de epsilon comportamiento guiado o aleatorio
		flip = util.flipCoin(self.epsilon)
		if flip == False:
			action = self.getPolicy(self.estados[1])
			print "Accion pensada: ", action
		else:
			action = random.choice(self.legalActions)
			print "Accion random: ", action
		self.actionsArray[1]=action

		#Calculamos el refuerzo
		reward = self.scores[1]-self.scores[0]
		if reward <0:
			reward=0
		elif reward==199 and estado[1] !=4:
			reward =0	
		if reward==0:
			reward=5*(self.distanceReward[0]-self.distanceReward[1]) #Si es positiva es que nos hemos acercado al objetivo
			if reward<0:
				reward=reward*2
	

		#La primera vez que ejecutamos el loop no tenemos datos para definir estado siguiente por lo que esperamos 1
		if self.counter:
			self.update(self.estados[0], self.actionsArray[0], self.estados[1], reward)
		else:
			self.counter = True
		return action

	def update(self, state, action, nextState, reward):
		position = self.computePosition(state)
		action_column = self.actions[action]
		q = self.getQValue(state, action)
		print "position: ", position

		self.q_table[position][action_column] = (1-self.alpha) * q + self.alpha * (reward + self.gamma * self.getValue(nextState))

	def getPolicy(self, state):
		return self.computeActionFromQValues(state)

	def getValue(self, state):
		return self.computeValueFromQValues(state)
