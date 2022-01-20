import time
import random
from copy import deepcopy
from agent import Agent


#  use whichever data structure you like, or create a custom one
import queue
import heapq
from collections import deque


"""
  you may use the following Node class
  modify it if needed, or create your own
"""
class Node():
    
    def __init__(self, parent_node, level_matrix, current, g, rhs, h_value, key_value):
        self.parent_node = parent_node
        self.level_matrix = level_matrix
        self.current_pos = current
        self.g = g
        self.rhs = rhs
        self.h = h_value
        self.key_value = key_value      

class PriorityQueue: 
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]


class DStarLiteAgent(Agent):

    def __init__(self):
        super().__init__()
        
        
        self.initialized = False
        
        
        #  g cost in A*, 2d array of size [height][width] 
        #    IMPORTANT NOTE!!!
        #please fill values inside this array
        #as you perform the A* search!
        self.g_values = []
        
        #  rhs cost in D*, 2d array of size [height][width]
        #SAME AS G, FILL THESE VALUES IN YOUR CODE
        self.rhs_values = []

        
        #  a large enough value for initializing g values at the start
        self.INFINITY_COST = 2**10

        self.start_pos = []
        self.apple_pos = []
        self.last = []
        self.k_m = 0

        self.queue = []
        self.direction = [[0,1],[0,-1],[1,0],[-1,0]]   #RIGHT, LEFT, DOWN ,UP 

    
    #  finds apple's position in the given level matrix
    #return a tuple of (row, column)
    def find_apple_position(self, level_matrix):
        for r in range(len(level_matrix)):
            for c in range(len(level_matrix[0])):
                if (level_matrix[r][c] == "A"):
                    return (r, c)
        
        return (-1, -1)
        
    
    #  calculates manhattan distance between player and apple
    #this function assumes there is only a single apple in the level
    def heuristic(self, player_row, player_column, apple_row, apple_column):
        return abs(player_row - apple_row) + abs(player_column - apple_column)
    
    ###--- Function for generating a key value for sorting ---###
    def getKeyValue(self,Node):
        return Node.key_value
    
    ###--- Function for sorts the queue list and returns to top element of the list ---###
    def topQueue(self):
        self.queue.sort(key = self.getKeyValue)
        return self.queue[0]

    ###--- Function to create a node ---###
    def nodeCreate(self, parrent_node,current_pos):
        h = self.heuristic(current_pos[0],current_pos[1],self.start_pos[0],self.start_pos[1])       
        return Node(parrent_node, self.level_matrix, current_pos, self.g_values[current_pos[0]][current_pos[1]], self.rhs_values[current_pos[0]][current_pos[1]], h, 0)

    ###--- Function to calculate key tuple ---###
    def CalculateKey(self,current_pos,k_m):
        return (min(self.g_values[current_pos[0]][current_pos[1]], self.rhs_values[current_pos[0]][current_pos[1]]) 
                + self.heuristic(self.start_pos[0],self.start_pos[1], current_pos[0],current_pos[1]) + k_m,
                min(self.g_values[current_pos[0]][current_pos[1]], self.rhs_values[current_pos[0]][current_pos[1]]))
        
    def Initialize(self):

        ###--- Initializing g and rhs matrix ---###
        rows, cols = (len(self.level_matrix), len(self.level_matrix[0]))
        self.g_values = [ [self.INFINITY_COST]*rows for i in range(cols) ]
        self.rhs_values = [ [self.INFINITY_COST]*rows for i in range(cols) ]

        ###--- Initialize rhs value of apple ---### 
        self.rhs_values[self.apple_pos[0]][self.apple_pos[1]] = 0

        ###--- Creating node ---###
        h = self.heuristic(self.start_pos[0],self.start_pos[1],self.apple_pos[0],self.apple_pos[1])
        g = self.g_values[self.apple_pos[0]][self.apple_pos[1]]
        rhs = self.rhs_values[self.apple_pos[0]][self.apple_pos[1]]

        new_node = Node(None,self.level_matrix, self.apple_pos, g, rhs, h, None)
        new_node.key_value = self.CalculateKey(new_node.current_pos, self.k_m)

        ###--- Starting queue ---###
        self.queue.append(new_node)

    def UpdateVertex(self, Node):

        pos = Node.current_pos   
        ###--- Pass if the vertex is a wall ---###  
        if self.level_matrix[pos[0]][pos[1]] == "W":
            return
        
        ###--- Updating nodes rhs values other than apple node ---###
        if(pos != self.apple_pos): 
            min_rhs = self.INFINITY_COST
            ###--- Calculating min rhs value by comparing neigboring indices ---###
            for i in self.direction:
                if self.level_matrix[pos[0] + i[0]][pos[1] + i[1]] != "W":
                    min_rhs = min(min_rhs, (self.g_values[pos[0] + i[0]][pos[1] + i[1]] + 1))
            ###--- Appending min rhs to the node ---###
            Node.rhs = min_rhs
            self.rhs_values[pos[0]][pos[1]] = min_rhs
        
        ###--- If node is already in queue dequeue it ---###
        node_in_queue = []  
        for node in self.queue:
            if pos == node.current_pos:
                node_in_queue.append(node)
        if node_in_queue != []: 
            self.queue.remove(node_in_queue[0])
        ###--- Update nodes key tupples and requeue the node ---###
        if(self.g_values[pos[0]][pos[1]] != self.rhs_values[pos[0]][pos[1]] and self.level_matrix[pos[0]][pos[1]] != "W"):
            Node.key_value = self.CalculateKey(pos,self.k_m)
            self.queue.append(Node)


    def ComputeShortestPath(self):
        ###--- While starting pos is not reached ---###
        while((self.topQueue().key_value < self.CalculateKey(self.start_pos, self.k_m)) or self.g_values[self.start_pos[0]][self.start_pos[1]] != self.rhs_values[self.start_pos[0]][self.start_pos[1]]):
            head_node = self.queue.pop(0)
            k_old = head_node.key_value

            ###--- If key value is changed recalculate key tupple and requeue the node ---###
            if k_old < self.CalculateKey(head_node.current_pos,self.k_m):
                head_node.key_value = self.CalculateKey(head_node.current_pos,self.k_m)
                self.queue.append(head_node)
            ###--- Updating g value and searching and expanding to neighbors ---### 
            elif head_node.g > head_node.rhs:
                head_node.g = head_node.rhs
                self.g_values[head_node.current_pos[0]][head_node.current_pos[1]] = head_node.rhs
                for i in self.direction:
                    new_pos = [(head_node.current_pos[0] + i[0]),(head_node.current_pos[1] + i[1])]
                    self.UpdateVertex(self.nodeCreate(head_node,new_pos))
            ###--- Update the g value of changed node and requeue the node ---###
            else:
                head_node.g = self.INFINITY_COST
                self.g_values[head_node.current_pos[0]][head_node.current_pos[1]] = self.INFINITY_COST
                for i in self.direction:
                    self.UpdateVertex(self.nodeCreate(head_node, [head_node.current_pos[0] + i[0],head_node.current_pos[1] + i[1]]))

    ###--- Function for generating a move sequence ---###
    def get_road(self):
        pos = self.start_pos
        g = self.g_values[pos[0]][pos[1]]
        road = []
        
        while pos != self.apple_pos:
            for i in self.direction:
                if g > self.g_values[pos[0] + i[0]][pos[1] + i[1]]:
                    if i == [0,-1]:
                        road.append("L")
                    elif i == [0,1]:
                        road.append("R")
                    elif i == [-1,0]:
                        road.append("U")
                    elif i==[1,0]:
                        road.append("D")
                    g = self.g_values[pos[0] + i[0]][pos[1] + i[1]]
                    pos = [pos[0] + i[0],pos[1] + i[1]]
                    break
        return road

    def solve(self, level_matrix, player_row, player_column, changed_row, changed_column):
        super().solve(level_matrix, player_row, player_column)
        move_sequence = []

        """
            YOUR CODE STARTS HERE
            fill move_sequence list with directions chars
        """

        initial_level_matrix = [list(row) for row in level_matrix] #deepcopy(level_matrix)
        self.print_level_matrix(initial_level_matrix)

        self.start_pos = [player_row,player_column]   #to simplfy
        self.apple_pos = list(self.find_apple_position(initial_level_matrix))
        

        if (not self.initialized):
            #  first time calling D*lite agent solve()
            self.last = self.start_pos
            self.Initialize()
            self.ComputeShortestPath()                
            move_sequence = self.get_road()

            self.initialized = True
        else:
            #  initialization phase is already performed
            #  this means solve() is called once again because there is
            #a change detected in the map
            print("Solve called again because a new obstacle appeared at position:(", changed_row, ",", changed_column, ")")
            ###--- Update k_m value with respect to new information ---###
            self.k_m = self.k_m + self.heuristic(self.last[0],self.last[1],self.start_pos[0],self.start_pos[1])
            self.last = self.start_pos

            ###--- Update edge costs ---###
            self.g_values[changed_row][changed_column]= self.INFINITY_COST
            self.rhs_values[changed_row][changed_column]= self.INFINITY_COST

            self.g_values[self.start_pos[0]][self.start_pos[1]]= self.INFINITY_COST

            ###--- Reevaluating map ---###
            self.UpdateVertex(self.nodeCreate(None,self.start_pos))
            self.ComputeShortestPath() 
            move_sequence = self.get_road()        
        
        """
            YOUR CODE ENDS HERE
            return move_sequence
        """
        return move_sequence
    
    
    
    def on_encounter_obstacle(self):
        pass
