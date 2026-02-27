import random

BOARD_HEIGHT = 50
BOARD_WIDTH = 100
            
def neighbor_bonus(board, i):
    # defining bonuses so they don't stack up infinitely
    river_bonus = 1
    mountain_bonus = 1
    
    if i > 0:
        if board[i-1] == "~":
            river_bonus *= 2
        elif board[i-1] == "&":
            mountain_bonus *= 4.5
    if i >= BOARD_WIDTH:
        if board[i-BOARD_WIDTH] == "~":
            river_bonus *= 2.5
        elif board[i-BOARD_WIDTH] == "&":
            mountain_bonus *= 3
        
    return river_bonus, mountain_bonus
    
def generate_map():
    # plain tile | river tile | mountain tile
    features = ("_", "~", "&")
            
    board_tmp = [] # less mess than with strings
    board = "" # to write to file
    board_length = BOARD_HEIGHT * BOARD_WIDTH
            
    for i in range(board_length):
        # defining here so they don't stack up infinitely
        weights = [0.78, 0.12, 0.1] # all add up to 1 for simplicity
        
        # calculate the bonuses
        bonuses = neighbor_bonus(board_tmp, i)
        
        weights[1] *= bonuses[0]
        weights[2] *= bonuses[1]
                    
        # draw random tile
        board_tmp.append(random.choices(features, weights)[0])
        
    # convert to string and arrange into board shape
    for i in range(0, board_length, BOARD_WIDTH):
        board += "".join(board_tmp[i:i+BOARD_WIDTH]) + "\n"
        
    try: 
        with open("map.txt", "w") as file:
            file.write(board)
    except ValueError:
        print("Wrong file type!")
    print(weights)
    
def main():
    generate_map()
    
if __name__ == "__main__":
    main()