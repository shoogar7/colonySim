import random

def generate_map():
    # features = {"_": 0.7, "~": 0.2, "&": 0.1}
    
    # plain tile | river tile | mountain tile
    features = ("_", "~", "&")
    weights = [0.8, 0.15, 0.05]
    
    # don't generate dictionaries
    # do all in one line then divide for visuals
    
    BOARD_HEIGHT = 50
    BOARD_WIDTH = 100
    
    board_tmp = ""
    board = ""
    board_length = BOARD_HEIGHT * BOARD_WIDTH
    
    for i in range(board_length):
        multiplier = 1
        if i > 0:
            if board_tmp[i-1] in "~&":
                multiplier *= 1.05
        if i >= BOARD_WIDTH:
            if board_tmp[i-BOARD_WIDTH] in "~&":
                multiplier *= 1.05
            
        # apply the multipliers if occured
        weights[1] *= multiplier 
        weights[2] *= multiplier
        
        # generating board
        board_tmp += random.choices(features, weights)[0]
            
    for i in range(0, board_length, BOARD_WIDTH):
        board += board_tmp[i:i+BOARD_WIDTH] + "\n"
        
    try: 
        with open("map.txt", "w") as file:
            file.write(board)
    except ValueError:
        print("Wrong file type!")
    
def main():
    generate_map()
    
if "__name__" == "__main()__":
    main()