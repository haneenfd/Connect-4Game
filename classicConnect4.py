import math
import random
import numpy as np
import pygame 
import sys

ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2

SQUARE_SIZE=100
BLUE=(0,0, 255)
BLACK=(0,0,0)
RED=(255,24,24)
YELLOW = (255,255,0)


RADIUS = int(SQUARE_SIZE/2-5)

# Create the game board as a 2D array
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Check if the column is valid (not full)
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

#get row where piece will go 
def get_row_location(board,col):
    for i in range (ROW_COUNT):
        if board[i][col]==0:
            return i
        
def print_board(board):
    print(np.flip(board, 0))

# Drop the piece on the board
def drop_piece(board,col,piece):
    row=get_row_location(board,col)
    board[row][col]=piece

# Check if a player has won the game
def check_win(board,piece):
     # Check horizontal locations for win 
     for i in range(ROW_COUNT):
         for j in range(COLUMN_COUNT-3):
             if board[i][j]==piece and board[i][j+1]==piece and board[i][j+2]==piece and board[i][j+3]==piece:
                 return True
# check for vertical locations 
     for i in range (COLUMN_COUNT):
        for j in range (ROW_COUNT-3):
            if board[j][i]==piece and board[j+1][i]==piece and board[j+2][i]==piece and board[j+3][i]==piece:
                return True
#check for +ve diagonl locations
     for i in range(ROW_COUNT-3):
         for j in range (COLUMN_COUNT-3):
             if board[i][j]==piece and board[i+1][j+1]==piece and board[i+2][j+2]==piece and board[i+3][j+3]==piece:
                 return True
# check for -ve diagonl locations (************)
     for i in range(ROW_COUNT-3):
         for j in range(3,COLUMN_COUNT):
             if board[i][j] ==piece and board[i+1][j-1] == piece and board[i+2][j-2] == piece and board[i+3][j-3] == piece:
                 return True


def draw(screen):
    pygame.draw.rect(screen, BLUE, (0, SQUARE_SIZE, SQUARE_SIZE*COLUMN_COUNT, SQUARE_SIZE*ROW_COUNT)) 
    for i in reversed(range(ROW_COUNT)):
        for j in range(COLUMN_COUNT):
            x = j*SQUARE_SIZE + SQUARE_SIZE/2
            y = i*SQUARE_SIZE+SQUARE_SIZE + SQUARE_SIZE/2
            if board[ROW_COUNT-i-1][j]==0:
                pygame.draw.circle(screen, BLACK, (x, y), RADIUS)
            elif board[ROW_COUNT-i-1][j]==1:
                pygame.draw.circle(screen, RED, (x, y), RADIUS)
            elif board[ROW_COUNT-i-1][j]==2:
                pygame.draw.circle(screen, YELLOW, (x, y), RADIUS)

def get_valid_locations(board):
    arr=[]
    for i in range(COLUMN_COUNT):
        if is_valid_location(board, i):
            arr.append(i)
    return arr

def is_terminal_node(board):  #if win or no valid locations
    return check_win(board,AI_PIECE) or check_win(board,PLAYER_PIECE) or len(get_valid_locations(board))==0

def min_max(board,depth,maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        #return static evaluation of node
        if is_terminal: 
            if check_win(board,AI_PIECE):
                return (None, 100000000000000)
            elif check_win(board,PLAYER_PIECE):
                return (None, -10000000000000)
            else:
                return(None,0)
        else:
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        maxVal = -math.inf
        column = random.choice(valid_locations)
        for i in valid_locations:
            b_copy = board.copy()
            drop_piece(b_copy,i,AI_PIECE)
            val=min_max(b_copy,depth-1,False)[1]
            if val>maxVal:
                maxVal=val
                column=i
        return (column,maxVal)
    else:
        minVal = math.inf
        column = random.choice(valid_locations)
        for i in valid_locations:
            b_copy = board.copy()
            drop_piece(b_copy,i,PLAYER_PIECE)
            val=min_max(b_copy,depth-1,True)[1]
            if val<minVal:
                minVal=val
                column=i
        return (column,minVal)

#heuristic function
def score_position(board, piece):
    score=0

    # score horizontal position
    for i in range(ROW_COUNT):
        for j in range (COLUMN_COUNT-3):
            window = [board[i][j+c] for c in range(4)]
            score += evaluate_window(window, piece)
    #score vertical position
    for i in range (COLUMN_COUNT):
        for j in range (ROW_COUNT-3):
            window = [board[j+c][i] for c in range(4)]
            score+=evaluate_window(window,piece)
    #score +ve diagonal
    for i in range (ROW_COUNT-3):
        for j in range (COLUMN_COUNT-3):
            window = [board[i+c][j+c] for c in range(4)]
            score+=evaluate_window(window,piece)
    #score for -ve diagonal 
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r-3-i][c+i] for i in range(0)]
            score += evaluate_window(window, piece)
    return score
			
		

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2
                
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score 

    
pygame.init()

pygame.font.init()
font = pygame.font.SysFont("monospace", 75)

height = SQUARE_SIZE * (ROW_COUNT+1)
width = SQUARE_SIZE * (COLUMN_COUNT)
size=(width, height)
screen = pygame.display.set_mode(size)
board= create_board()
print(board)

turn=PLAYER
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            screen.fill((0, 0, 0))
            x = event.pos[0]
            if turn==0:
                pygame.draw.circle(screen, RED, (x, SQUARE_SIZE/2), RADIUS)
            elif turn==1:
                pygame.draw.circle(screen, YELLOW, (x, SQUARE_SIZE/2), RADIUS)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
            if turn==PLAYER:
                x=event.pos[0]
                col= math.floor((x/SQUARE_SIZE))
                print(col)
                if is_valid_location(board,col):
                    drop_piece(board,col,PLAYER_PIECE)
                    print_board(board)
                    turn+=1
                    turn%=2
                    draw(screen)
                    pygame.display.flip()
                    if check_win(board,PLAYER_PIECE):
                        label = font.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over=True
          
    
    if turn == AI and not game_over:
        col, minimax_score = min_max(board, 3,True)
        if is_valid_location(board, col):
            drop_piece(board,col,AI_PIECE)
            print_board(board)
            if check_win(board,AI_PIECE):
                label = font.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40,10))
                game_over=True
            turn+=1
            turn%=2
    
    draw(screen)
    pygame.display.flip()
    if game_over == True:
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()