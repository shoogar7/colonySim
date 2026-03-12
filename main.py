import random
import time
    
BOARD_HEIGHT = 50
BOARD_WIDTH = 100

# list of all neighbour tiles coordinates
NEIGHBOURS = [(-1, -1), (0, -1), (1, -1),
                (-1, 0),           (1, 0),
                (-1, 1), (0, 1), (1, 1)]
    
def update_map(new_board):
    lines = ""
 
    for y in range(BOARD_HEIGHT):
        lines += "".join(new_board[y]) + "\n"
        
    try: 
        with open("map.txt", "w") as file:
            file.writelines(lines)
            # print("Updated the board!")
            return new_board
            
    except ValueError:
        print("Wrong file type!")
    
def neighbor_bonus(board, y, x):
    # defining bonuses so they don't stack up infinitely
    river_bonus = 1
    mountain_bonus = 1
    
    # check previous tile
    if x > 0: 
        if board[y][x-1] == "~":
            river_bonus *= 2
        elif board[y][x-1] == "&":
            mountain_bonus *= 4.5
    # check tile above
    if y > 0:
        if board[y-1][x] == "~":
            river_bonus *= 2.5
        elif board[y-1][x] == "&":
            mountain_bonus *= 3
        
    return river_bonus, mountain_bonus
    
# turn all single-tile features into plain ("_") tile
def feature_cleanup(board):
    new_board = [row[:] for row in board] # make deepcopy of board to not affect original
    
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            tile = new_board[y][x]
            if tile == "_":
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
                new_board[y][x] = "_"
                
    return new_board        
    
def generate_map():
    # plain tile | river tile | mountain tile
    features = ("_", "~", "&")
            
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
    except ValueError:
        print("Wrong file type!")
   
def estimate_distance(current_node, target_node):
    return ((target_node[0]-current_node[0])**2 + (target_node[1]-current_node[1])**2)**0.5
   
# Work in progress
def find_path(board, start, stop):
    # get the tiles of start and stop
    start_tile = board[start[1]][start[0]] # O on board
    stop_tile = board[stop[1]][stop[0]] # Q on board
        
    # start and stop tiles have to be on plain ("_") tile
    if start_tile not in "O_":
        # pick another tile
        pass
    else:
        if start_tile != "O":
            # mark it on board 
            board[start[1]][start[0]] = "O"
            board = update_map(board)
        if stop_tile not in "Q_":
            # pick another tile
            pass
        else:
            if stop_tile != "Q":
                # mark it on board 
                board[stop[1]][stop[0]] = "Q"
                board = update_map(board)
                                        
            unvisited = {}
            tile_path = {}
            # make a dict of tiles with distance from start and a dict of path for every tile
            for y in range(BOARD_HEIGHT):
                for x in range(BOARD_WIDTH):
                    unvisited[f"{x}_{y}"] = float('inf')
                    tile_path[f"{x}_{y}"] = []
                             
            # make start tile distance 0 (because it's start)   
            unvisited[f"{start[0]}_{start[1]}"] = 0
                        
            # pick the tile with smallest distance
            current_node = min(unvisited, key=unvisited.get)
            
            path = []
            dead_ends = []
            unvisited["a_b"] = float('inf') # default tile for comparison
            tile = " "
            current_tile = [0, 0]
                        
            # while current node isn't the stop tile
            while unvisited:
                # print(tile_path[current_node])
                time.sleep(0.1)
                if unvisited[current_node] == float('inf'):
                    print("Only unreachable nodes remain!")
                    break
                                                 
                closest_neighbor = "a_b" # could change it to None someday

                # get the coordinates
                current_tile[0] = int(current_node.split("_")[0])
                current_tile[1] = int(current_node.split("_")[1])

                for dx, dy in NEIGHBOURS:
                    nx, ny = current_tile[0]+dx, current_tile[1]+dy # apply neighbour tile coordinate differences
                    # assign distance for tiles, don't change mountain because it's not meant to be traversable
                    if 0 <= nx < BOARD_WIDTH and 0 <= ny < BOARD_HEIGHT and f"{nx}_{ny}" in unvisited:
                        if board[ny][nx] == "~":
                            unvisited[f"{nx}_{ny}"] = 2
                        elif board[ny][nx] == "_":
                            unvisited[f"{nx}_{ny}"] = 1
                        elif board[ny][nx] == "Q": # end tile
                            unvisited[f"{nx}_{ny}"] = 0
                            
                        unvisited[f"{nx}_{ny}"] += estimate_distance((nx, ny), stop)
                                                    
                        # pick the neighbor with shortest path
                        closest_neighbor = {True: f"{nx}_{ny}", False: closest_neighbor}[unvisited[closest_neighbor] > unvisited[f"{nx}_{ny}"]]

                board[current_tile[1]][current_tile[0]] = tile
                board = update_map(board)
                        
                if current_node in unvisited:
                    path.append(current_node)
                
                # if no neighbors left, trace back
                if closest_neighbor == "a_b":
                    dead_ends.append(path.pop())
                    closest_neighbor = path.pop()
                    while closest_neighbor in dead_ends: # trace back more
                        closest_neighbor = path.pop()
                        # print(closest_neighbor)
                    unvisited[closest_neighbor] = 0
                
                tile_path[closest_neighbor].append(current_node)
                
                # if end goal reached - stop
                if current_node == f"{stop[0]}_{stop[1]}":
                    break
                
                # remove visited tile from unvisited
                del unvisited[current_node]
                
                # move to the next tile
                current_node = closest_neighbor  
                
                # mark the path on board
                tile = board[current_tile[1]][current_tile[0]]
                board[current_tile[1]][current_tile[0]] = "."
                board = update_map(board)   
                
            if not unvisited: # empty dict is equal to False
                print("All tiles visited!")
                print("But no way found :(")
                return None
                        
            return tile_path[f"{stop[0]}_{stop[1]}"]
           
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
        print("Wrong file type!")
        
    
    print(find_path(board, (14,2), (83,46)))

def main():
    test()
    
    # Working correctly, leave it commented for now to not disturb while implementing other functionalities and testing
    # regenerate = True
    # usr_answer = ""
    # while regenerate: # map generation loop
    #     board = generate_map()
    #     usr_answer = input('Would you like to generate the map again?\n(Please enter "Y" to generate again.)\n')
    #     if usr_answer.lower() != "y":
    #         regenerate = False
    
    # if not regenerate:
    #     find_path(board)
    
if __name__ == "__main__":
    main()