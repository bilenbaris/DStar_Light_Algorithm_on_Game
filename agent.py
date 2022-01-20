import time

class Agent:

    """
        initialize some member variables
    """
    def __init__(self):
        self.player_row = 0
        self.player_col = 0
        self.level_matrix = None
        self.elapsed_solve_time = 0

        """
            please use these variables for statistics
        """
        self.expanded_node_count = 0
        self.generated_node_count = 0
        self.maximum_node_in_memory_count = 0

        #  not implemented, not necessary
        self.real_distance_matrix = []
        self.manhattan_distance_matrix = []
    
    
    def count_apples_in_level_matrix(self, level_matrix):
        apple_count = sum(row.count("A") for row in level_matrix)
        return apple_count
        
    
    def print_level_matrix(self, level_matrix):
        print("")
        for row in level_matrix:
            print(row)
        print("")



    


    """
        level_matrix is list of lists (like 2d array)
    that contains whether a particular cell is
    -A (apple)
    -F (floor)
    -P (player)
    -W (wall)

    level_matrix[0][0] is top left corner
    level_matrix[height-1][0] is bottom left corner
    level_matrix[height-1][width-1] is bottom right corner

        player_row and player_column are current position
    of the player, eg:
    level_matrix[player_row][player_column] supposed to be P
      
        returns a character list, list of moves
    that needs to be played in order to solve
    given level
    valid letters are R, U, L, D corresponds to:
    Right, Up, Left, Down
    an example return value:
    L = ["U", "U", "U", "L", "R", "R"]...
    """
    def solve(self, level_matrix, player_row, player_column):
        self.player_row = player_row
        self.player_col = player_column
        self.level_matrix = level_matrix

      
