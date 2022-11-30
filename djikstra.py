from queue import PriorityQueue
from math import sqrt, inf
import pprint

class Edge():
    def __init__(self, cost, to_node, from_node):
        self.cost = cost
        self.to_node = to_node
        self.from_node = from_node
    
    def __str__(self):
        return "(" + str(self.cost) + "," + str(self.to_node) + "," + str(self.from_node) + ")"

class Djikstra():

    def  __init__(self, n):

        self.width = n
        self.height = n 
        size = self.width * self.height
        
        self.adj_matrix = [[inf for i in range(size + 1)] for j in range(size + 1)]
        self.grid = self.fill_grid()
        

        self.front = PriorityQueue()
        self.visited = []

    def fill_grid(self):

        grid = [[0 for i in range(self.width)] for j in range(self.height)]
        index = 1

        for i in range(self.height):
            for j in range(self.width):
                grid[i][j] = index
                index = index + 1
                
        return grid

    def fill_adj_matrix(self):
        
        # Loop through grid 
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):

                # x and y are 1 index 
                x = column + 1
                y = row + 1
                from_node = self.coord_to_index(x,y)

                neighbours = self.neighbours(x, y)

                # Go through each neighbour and add to adj matrix
                for n_coord in neighbours:
                    dist = sqrt((n_coord[0] - x)**2 + (n_coord[1] - y)**2)
                    to_node = self.coord_to_index(n_coord[0], n_coord[1])

                    self.adj_matrix[to_node][from_node] = dist     
 
    def coord_to_index(self, x, y):
        return (y * self.height) - (self.width - x)

    def index_to_coord(self, index):
        y = -(index // -self.height) 

        x = index % self.width
        if x == 0:
            x += self.width

        return [x,y]

    def is_in_grid(self, x, y, i, j):
        return (x + i - 1 > 0) and (y + j - 1 > 0) and (x + i - 1 <= self.width) and (y + j - 1 <= self.height) and not(i == 1 and j == 1)

    def neighbours(self, x, y):
        
        neighbours = []

        # Go through every permuation of -1/0/1 , -1/0/1
        for i in range(3):
            for j in range(3):

                # Check if its in the grid constraint and that the node itself isnt a neighbour
                if self.is_in_grid(x,y,i,j):  
                    neighbours.append([x + i - 1, y + j - 1])

        return neighbours

    def set_obstacle(self, index):
        for i in range(len(self.adj_matrix)):
            self.adj_matrix[index][i] = inf
            self.adj_matrix[i][index] = inf

    def check_visited(self, i):
        for visit_node in self.visited:
            if visit_node[1] == i:
                return True

        return False

    def get_visited(self, i):
        
        for node in self.visited:
            if node[1] == i:
                return node

    def check_front(self, i):
        for visit_node in self.front.queue:
            if visit_node[1][1] == i:
                return True

        return False


    def get_front(self, i):
        #return False
        for visit_node in self.front.queue:
            if visit_node[1][1] == i:
                return visit_node
                
    
    def djikstra(self, source, dest):
        self.adj_matrix[source][source] = 0

        # Adding the initial node 
        source_edge = (0, source, None) 

        self.front.put((source_edge[0], source_edge))

        while not self.front.empty():


            # Getting the lowest cost node 
            lowest_cost_node = self.front.get()
            self.visited.append(lowest_cost_node[1])

            print("low",lowest_cost_node)


            # Getting the lowest cost to_node
            lowest_cost_to_node = lowest_cost_node[1][1]   
            print("vis", self.visited)


            # Stop when we hit goal 
            if lowest_cost_node[1][1] == dest:
                print(self.visited)
                break

            # Get niighbours
            for i in range(len(self.adj_matrix[lowest_cost_to_node])):
                
                if self.adj_matrix[lowest_cost_to_node][i] != inf and self.adj_matrix[lowest_cost_to_node][i] != 0:
            
                    # check if visited
                    if self.check_visited(i) ==  False:

                        # Check if the visited node is in front 
                        if self.check_front(i) == True:

                            visited_node = self.get_front(i)
                            cost = self.adj_matrix[lowest_cost_to_node][i] + lowest_cost_node[1][0]
                            check_node = (cost, i, lowest_cost_to_node)

                            # Replace if the cost of edge in front is higher than the current edge we are checking
                            if cost < visited_node[0]:
                                self.front.queue.remove(visited_node)
                                self.queue.put((cost, check_node))

                        else:
                            cost = self.adj_matrix[lowest_cost_to_node][i] + lowest_cost_node[1][0]
                            add_edge = (cost, i, lowest_cost_to_node)
                            self.front.put((cost, add_edge))
                                
        


            

        
a = Djikstra(6)

pp = pprint.PrettyPrinter()
#
a.fill_adj_matrix()
a.set_obstacle(6)
a.set_obstacle(4)
a.set_obstacle(9)
a.djikstra(24,3)


