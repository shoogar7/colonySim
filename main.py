import random
import time
    
DEBUG = False

BOARD_HEIGHT = 50
BOARD_WIDTH = 100
PLAIN = "_"
RIVER = "~"
MOUNTAIN = "&"

# list of all neighbour tiles coordinates
NEIGHBOURS = [(-1, -1), (0, -1), (1, -1),
                (-1, 0),           (1, 0),
                (-1, 1), (0, 1), (1, 1)]

CORNER_NEIGHBOURS = [(-1, -1), (1, -1),
                     (-1, 1), (1, 1)]
    
def update_map(new_board):
    lines = ""
 
    for y in range(BOARD_HEIGHT):
        lines += "".join(new_board[y]) + "\n"
        
    try: 
        with open("map.txt", "w") as file:
            file.writelines(lines)
            return new_board
            
    except FileNotFoundError:
        print("Wrong file!")
    
def neighbor_bonus(board, y, x):
    # defining bonuses so they don't stack up infinitely
    river_bonus = 1
    mountain_bonus = 1
    
    # check previous tile
    if x > 0: 
        if board[y][x-1] == RIVER:
            river_bonus *= 2
        elif board[y][x-1] == MOUNTAIN:
            mountain_bonus *= 4.5
    # check tile above
    if y > 0:
        if board[y-1][x] == RIVER:
            river_bonus *= 2.5
        elif board[y-1][x] == MOUNTAIN:
            mountain_bonus *= 3
        
    return river_bonus, mountain_bonus
    
# turn all single-tile features into PLAIN
def feature_cleanup(board):
    new_board = [row[:] for row in board] # make deepcopy of board to not affect original
    
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            tile = new_board[y][x]
            if tile == PLAIN:
                continue
            
            isolated = True
            
            # look for same-feature tiles in 1-tile area (including corners)
            for dx, dy in NEIGHBOURS:
                nx, ny = x+dx, y+dy # apply neighbour tile coordinate differences
                if 0 <= nx < BOARD_WIDTH and 0 <= ny < BOARD_HEIGHT:
                    if new_board[ny][nx] == tile:
                        isolated = False
                        break
                    
            if isolated:
                new_board[y][x] = PLAIN
                
    return new_board        
    
def generate_map():
    features = (PLAIN, RIVER, MOUNTAIN)
            
    # initializing 2d array
    board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)] 
    
    lines = "" # to write to file
            
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            # defining here so they don't stack up infinitely
            weights = [0.78, 0.12, 0.1] # all add up to 1 for simplicity
            
            # calculate the bonuses
            bonuses = neighbor_bonus(board, y, x)
                
            weights[1] *= bonuses[0]
            weights[2] *= bonuses[1]
                        
            # draw random feature
            board[y][x] = random.choices(features, weights)[0]
        
    board = feature_cleanup(board)
    
    for y in range(BOARD_HEIGHT):
        lines += "".join(board[y]) + "\n"
                
    try: 
        with open("map.txt", "w") as file:
            file.write(lines)
            
        return board
    except FileNotFoundError:
        print("Wrong file!")
   
# returns euclidean distance from current to target node
def estimate_distance(current_node, target_node):
    return ((target_node[0]-current_node[0])**2 + (target_node[1]-current_node[1])**2)**0.5
   
def reconstruct_path(previous, current):
    total_path = [current]
    while current in previous:
        current = previous[current]
        total_path.append(current)
    return total_path[::-1]

def goal_reachable(board, tile):
    reachable = False
    for dx, dy in NEIGHBOURS:
        nx, ny = tile[0] + dx, tile[1] + dy # get the real, neighbor coordinates
        if board[ny][nx] != MOUNTAIN:
            reachable = True
            break
    return reachable        
   
def find_path(board, start, goal):
    if not goal_reachable(board, goal):
        return None
    
    # the heuristic is estimate_distance()
    open_nodes = [start] # (x, y): considerable elements for path
    previous = {} # (x, y): distance - but for the previous node on our path
        
    cost_from_start = {} # (x, y): distance; cheapest path from start to n
    total_cost = {} # (x, y): distance; cheapest path from start to goal through n
    
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            cost_from_start[(x, y)] = float('inf') 
            total_cost[(x, y)] = float('inf')
    
    cost_from_start[start] = 0 
    total_cost[start] = estimate_distance(start, goal)
    
    while open_nodes:
        # pick the tile with current known shortest distance to goal from start
        current = min(open_nodes, key = lambda tile: total_cost[tile])
       
        if current == goal: 
            return reconstruct_path(previous, current)
        
        open_nodes.remove(current) 
                
        for dx, dy in NEIGHBOURS:
            nx, ny = current[0] + dx, current[1] + dy # get the real, neighbor coordinates
            
            if (dx, dy) in CORNER_NEIGHBOURS:
                feature_cost = 1.4 # corners take a little longer to traverse
            else:
                feature_cost = 1 # 
            
            if 0 <= nx < BOARD_WIDTH and 0 <= ny < BOARD_HEIGHT: # if it exists
                if board[ny][nx] == MOUNTAIN:
                    feature_cost += float('inf') # mountains are untraversable
                elif board[ny][nx] == RIVER:
                    feature_cost += 1 # it takes longer to cross rivers
                    
                potential_cost_from_start = cost_from_start[current] + feature_cost 
                if potential_cost_from_start < cost_from_start[(nx, ny)]:
                    previous[(nx, ny)] = current # move on to the neighbor node
                    cost_from_start[(nx, ny)] = potential_cost_from_start 
                    total_cost[(nx, ny)] = potential_cost_from_start + estimate_distance((nx, ny), goal)
                    
                    if (nx, ny) not in open_nodes:
                        open_nodes.append((nx, ny))
    return None
   
def visualize_path(main_board, real_route):
    if not real_route:
        print("Error: no path found!")
        return None
    
    board = [row[:] for row in main_board] # named main_board to use 'board' freely
    route = real_route.copy()
    current_node = route.pop(0)
    
    tile = board[current_node[1]][current_node[0]] # save tile for later
    board[current_node[1]][current_node[0]] = "O"
    
    goal = route[-1]
    board[goal[1]][goal[0]] = "Q" # mark goal on board
    
    board = update_map(board)
    
    while route:
        time.sleep(0.1)
        previous_node = current_node
        board[previous_node[1]][previous_node[0]] = tile
        
        current_node = route.pop(0)
        tile = board[current_node[1]][current_node[0]] # save tile for later
        board[current_node[1]][current_node[0]] = "O"
        
        board = update_map(board)       
           
# Temporary testing helper while developing functionalities                  
def test():
    board = generate_map()
    
    board = []
    line = []
    try: 
        with open("map.txt", "r") as file:
            for row in file:
                for tile in row[:BOARD_WIDTH]:
                    # to make sure it's a list and not a string (can't assign specific tiles to string later)
                    line.append(tile)
                board.append(line)
                line = []
                            
    except ValueError:
        print("Wrong file!")
    
    visualize_path( board, find_path(board, (1, 47), (92, 3)) )

def main():
    regenerate = True
    usr_answer = ""
    while regenerate: # map generation loop
        board = generate_map()
        usr_answer = input('Would you like to generate the map again?\n(Please enter "Y" to generate again.)\n')
        if usr_answer.lower() != "y":
            regenerate = False
    
    if not regenerate:
        visualize_path( board, find_path(board, (1, 47), (92, 3)) )
    
if __name__ == "__main__":
    if DEBUG:
        test()
    else:
        main()