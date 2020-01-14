#!/usr/bin/python3

import sys
import copy
import queue
import random
from path import Path

class Board:

	default = "  o aa|  o   |xxo   |ppp  q|     q|     q"

	def __init__(self, state = default):
		self.state = state
		self.board = []
		self.matrix()
	
	def matrix(self):
		# creates matrix of initialized board
		board_matrix = [[]]
		for space in self.state:
			if space == '|':
				board_matrix.append([])
			else:
				length = len(board_matrix)
				board_matrix[length-1].append(space)

		self.board = board_matrix
		return self.board
	
	def print(self, states):
		if states == []:
			return

		startcolumn = 0
		endcolumn = 6

		while endcolumn < len(states)+6:
			row = 0

			while row !=  8:
				for state in states[startcolumn:endcolumn]:
					if row == 0: # create top border
						print(' ------ ', end = "")
						print("   ", end = "")

					elif 0 < row < 7:
						print('|', end="")
						for space in state[row-1]:
							print(space, end="")
						if row != 3:
							print('|', end="")
							print("   ", end = "")
						else:
							print("    ", end = "")

					elif row == 7: # create bottom row
						print(' ------ ', end = "")
						print("   ", end = "")

				row+=1
				print()
			print()
			startcolumn = endcolumn
			endcolumn += 6

	def done(self, state):
		if state[2][5] == 'x':
				return True
		return False

	def movement(self,coordinates):
		# returns the way the car moves, either vertical or horizontal
		if coordinates[0][0] == coordinates[1][0]:
			return 'horizontal'
		else:
			return 'vertical'

	def next_for_car(self, car):
		# returns all next states for car
		coordinates = []
		for row in range(6):
			for column in range(6):
				if self.board[row][column] == car:
					coordinates.append([row,column])
		
		board = copy.deepcopy(self.board) # makes deep copy of board (clone)

		states = []
		start = coordinates[0]
		end = coordinates[-1]
		coordinatescopy = copy.deepcopy(coordinates)

		if self.movement(coordinates) == 'horizontal':
			# see if before start is empty otherwise check if after end is empty
			if start[1] != 0: # only look at not first column to see if there's room to move before start coordinate
				while board[start[0]][start[1]-1] == ' ' and start[1] > 0:
					index = 0
					for cord in coordinates:
						board[cord[0]][cord[1]-1] = board[cord[0]][cord[1]]
						board[cord[0]][cord[1]] = ' '
						coordinates[index] = [cord[0],cord[1] - 1]
						index += 1
					
					states.append(copy.deepcopy(board))
					start[1] = start[1]- 1
					
			board = copy.deepcopy(self.board)

			if end[1] != 5:	# see if we can move car to the right if it's not at the end already
				while board[end[0]][end[1]+1] == ' ' and end[1] < 5:
					index = -1
					for cord in reversed(coordinatescopy):
						board[cord[0]][cord[1]+1] = board[cord[0]][cord[1]]
						board[cord[0]][cord[1]] = ' '
						coordinatescopy[index] = [cord[0],cord[1]+1]
						index -= 1

					states.append(copy.deepcopy(board))
					if end[1] == 4:
						break
					else:
						end[1] += 1

		else: # vertical movement
			if start[0] != 0: # only look at not first column to see if there's room to move before start coordinate
				while board[start[0]-1][start[1]] == ' ' and start[0] > 0:
					index = 0
					for cord in coordinates:
						board[cord[0]-1][cord[1]] = board[cord[0]][cord[1]]
						board[cord[0]][cord[1]] = ' '
						coordinates[index] = [cord[0]-1,cord[1]]
						index += 1
					
					states.append(copy.deepcopy(board))
					start[0] = start[0]- 1
			
			board = copy.deepcopy(self.board)
			
			if end[0] != 5:	# see if we can move car to the right if it's not at the end already
				while board[end[0]+1][end[1]] == ' ' and end[0] < 5:
					index = -1
					for cord in reversed(coordinatescopy):
						board[cord[0]+1][cord[1]] = board[cord[0]][cord[1]]
						board[cord[0]][cord[1]] = ' '
						coordinatescopy[index] = [cord[0]+1,cord[1]]
						index -= 1

					states.append(copy.deepcopy(board))
					if end[0] == 4:
						break
					else:
						end[0] += 1
		return states
			

	def next(self):
		board = self.state
		cars = []
		for value in board: # get set of all cars on board
			if value not in cars:
				cars.append(value)
		cars.remove(' ')
		cars.remove('|')
	
		states = []
		for car in cars:
			for state in self.next_for_car(car):
				states.append(state)
	
		return states

	def randomWalk(self, n = 10):

		root = Path(self.board)
		root.add(self.board)
		possibleMoves = self.next()
		counter = 1

		for i in range(n-1):

			if self.done(root.last()):
				self.print(root.get_path())
				print(counter)
				return

			randomMove = random.choice(possibleMoves)
			root.add(randomMove)

			self.board = randomMove
			possibleMoves = self.next()
			counter += 1

		self.print(root.get_path())
		print("Doesn't finish")
		

	def bfs(self):

		q = queue.Queue()
		root = Path(self.board)
		root.add(self.board)
		q.put(root)
		
		visited = []
		counter = 1

		while not q.empty():
			curr = q.get()

			print("_________________________________________________________________")
			self.print(curr.get_path())

			if self.done(curr.state):
				print(counter)
				return

			self.board = curr.state
			for state in self.next():

				if state not in visited:
					
					visited.append(state)

					parent = copy.deepcopy(curr)
					child = Path(state)
					
					child.add(parent.clone(state))
					q.put(child)
			
			counter += 1	

		print("Doesn't finish")


	def heuristic(self, arr): # returns point value for a board based on distance from goal
		points = 0
		index = 0
		xindex = 0
		for value in arr [2]:
		    if value == 'x':
		        xindex = index
		    index+=1

		points = 5 - xindex
		return points

	def lowestF(self,queue): # returns index to lowest f in queue
		index = 0
		lowestF = 10000
		elemToRemove = 0

		for elem in queue:
			if elem.f < lowestF:
				elemToRemove = index
				lowestF = elem.f	
			index+=1

		return elemToRemove

	def astar(self):
		
		root = Path(self.board)
		root.add(self.board)
		root.h = self.heuristic(self.board)
	
		open = [root]
		
		closed = []
		counter = 1

		while open:

			lowestF = self.lowestF(open)
			curr = open.pop(lowestF)

			print("_________________________________________________________________")
			self.print(curr.get_path())

			if self.done(curr.state):
				print(counter)
				return

			self.board = curr.state
			for state in self.next():

				if state not in closed:
					
					closed.append(state)

					parent = copy.deepcopy(curr)
					child = Path(state)

					child.g = curr.g + 1
					child.h = self.heuristic(state)
					child.f = child.g + child.h

					child.add(parent.clone(state))
					open.insert(0,child)	
			counter += 1

		print("Doesn't finish")


if __name__ == "__main__":

	if len(sys.argv) == 3:
		board = Board(sys.argv[2])
		for row in board.matrix():
			if len(row) != 6:
				print("Invalid board size entered. Needs to be 6x6.")
				sys.exit()
	else:
		board = Board()

	if sys.argv[1] == 'print':
		board.print([board.board])
	elif sys.argv[1] == 'done':
		print(board.done(board.board))
	elif sys.argv[1] == 'next':
		board.print(board.next())
	elif sys.argv[1] == 'random':
		board.randomWalk()
	elif sys.argv[1] == 'bfs':
		board.bfs()
	elif sys.argv[1] == 'astar':
		board.astar()
	else:
		print("Invalid command. Please enter command 'print','done','next', 'random', 'bfs', or 'astar'.")