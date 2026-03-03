import random
    
BOARD_HEIGHT = 50
BOARD_WIDTH = 100
    
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
        
    # list of all neighbour tiles coordinates
    neighbours = [(-1, -1), (0, -1), (1, -1),
                  (-1, 0),           (1, 0),
                  (-1, 1), (0, 1), (1, 1)]
    
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            tile = new_board[y][x]
            if tile == "_":
                continue
            
            isolated = True
            
            # look for same-feature tiles in 1-tile area (including corners)
            for dx, dy in neighbours:
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
            
    except ValueError:
        print("Wrong file type!")

def main():
    regenerate = True
    usr_answer = ""
    while regenerate: # map generation loop
        generate_map()
        usr_answer = input('Would you like to generate the map again?\n(Please enter "Y" to generate again.)\n')
        if usr_answer.lower() != "y":
            regenerate = False
        
if __name__ == "__main__":
    main()