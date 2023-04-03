from email.mime import image
import numpy as np
import pygame
import sys
import random
import math
from button import Button






gameoption = True

SQUARESIZE = 100

ROW_COUNT = 6
COLUMN_COUNT = 7

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

screen = pygame.display.set_mode(size)

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

RADIUS = int(SQUARESIZE/2 - 5)


pygame.init()

myfont = pygame.font.SysFont("monospace", 75)

#pygame.init()

screen = pygame.display.set_mode((size))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

#pygame.display.update()
b = True

def colors():
	global b
	if b:
		b = False
		return [(204, 0, 102),(255, 255, 255),(153, 51, 255),(0, 230, 230)]
	else :
		b = True
		return [(0,0,255), (0,0,0), (255,0,0), (255,255,0)]
    


BLUE,BLACK,RED,YELLOW = colors()

def options():
	


    SCREEN = pygame.display.set_mode(size)


    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TITLE = get_font(45).render("SETTINGS", True, "Black")
        OPTIONS_RECT = OPTIONS_TITLE.get_rect(center=(350, 80))
        SCREEN.blit(OPTIONS_TITLE, OPTIONS_RECT)

        

        OPTIONS_WHITE = Button(image=None, pos=(480, 260), 
                            text_input="WHITE", font=get_font(45), base_color="Black", hovering_color="Green")


        OPTIONS_DARK = Button(image=None, pos=(180, 260), 
                            text_input="DARK", font=get_font(45), base_color="Black", hovering_color="Green")

        OPTIONS_SAVE = Button(image=None, pos=(220, 560), 
                            text_input="SAVE", font=get_font(45), base_color="Black", hovering_color="Green")

        OPTIONS_BACK = Button(image=None, pos=(460, 560), 
                            text_input="BACK", font=get_font(45), base_color="Black", hovering_color="Green")



        OPTIONS_DARK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_DARK.update(SCREEN)

        OPTIONS_WHITE.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_WHITE.update(SCREEN)
        
        OPTIONS_SAVE.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_SAVE.update(SCREEN)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_SAVE.checkForInput(OPTIONS_MOUSE_POS):
                    
                    main_menu()


        
        pygame.display.update()


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value



def gameover(b):
	SCREEN = pygame.display.set_mode(size)
	
	if b == 1:
		
		while True:
			OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

			SCREEN.fill("white")

			OPTIONS_TEXT = get_font(45).render("Player 1 Won", True, "Black")
			OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(340, 260))
			SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

			OPTIONS_RESTART = Button(image=None,pos=(340,440),
			text_input="RESTART",font=get_font(75), base_color="orange", hovering_color="red")

			OPTIONS_BACK = Button(image=None, pos=(340, 560), 
								text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

			OPTIONS_RESTART.changeColor(OPTIONS_MOUSE_POS)
			OPTIONS_RESTART.update(SCREEN)

			OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
			OPTIONS_BACK.update(SCREEN)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
						main_menu()
					if OPTIONS_RESTART.checkForInput(OPTIONS_MOUSE_POS):
						if gameoption:
							main()
						else :
							ai()
				
			pygame.display.update()
		
	else :
		while True:
			OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
			SCREEN.fill("black")

			OPTIONS_TEXT = get_font(45).render("Player 2 Won", True, "white")
			OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(340, 260))
			SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

			OPTIONS_RESTART = Button(image=None,pos=(340,440),
			text_input="RESTART",font=get_font(75), base_color="blue", hovering_color="red")

			OPTIONS_BACK = Button(image=None, pos=(340, 560), 
								text_input="BACK", font=get_font(75), base_color="yellow", hovering_color="red")

			OPTIONS_RESTART.changeColor(OPTIONS_MOUSE_POS)
			OPTIONS_RESTART.update(SCREEN)

			OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
			OPTIONS_BACK.update(SCREEN)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
						main_menu()
					if OPTIONS_RESTART.checkForInput(OPTIONS_MOUSE_POS):
						if gameoption:
							main()
						else :
							ai()
				
				
			pygame.display.update()


def main():
	game_over = False
	turn = 0
	player = 0
	
	board = create_board()
	print_board(board)
	draw_board(board)
	while not game_over:



		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
				posx = event.pos[0]
				if turn == 0:
					pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
				else: 
					pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
			pygame.display.update()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
				#print(event.pos)
				# Ask for Player 1 Input
				if turn == 0:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))

					if is_valid_location(board, col):
						row = get_next_open_row(board, col)
						drop_piece(board, row, col, 1)

						if winning_move(board, 1):
							label = myfont.render("Player 1 wins!!", 1, RED)
							screen.blit(label, (40,10))
							game_over = True
							player = 1


				# # Ask for Player 2 Input
				else:				
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))

					if is_valid_location(board, col):
						row = get_next_open_row(board, col)
						drop_piece(board, row, col, 2)

						if winning_move(board, 2):
							label = myfont.render("Player 2 wins!!", 1, YELLOW)
							screen.blit(label, (40,10))
							game_over = True
							player = 2

				print_board(board)
				draw_board(board)

				turn += 1
				turn = turn % 2

				if game_over:
					gameover(player)

def ai():
	board = create_board()
	print_board(board)
	game_over = False

	

	SQUARESIZE = 100

	width = COLUMN_COUNT * SQUARESIZE
	height = (ROW_COUNT+1) * SQUARESIZE

	size = (width, height)

	RADIUS = int(SQUARESIZE/2 - 5)

	screen = pygame.display.set_mode(size)
	draw_board(board)
	pygame.display.update()

	myfont = pygame.font.SysFont("monospace", 75)

	turn = random.randint(PLAYER, AI)

	while not game_over:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
				posx = event.pos[0]
				if turn == PLAYER:
					pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

			pygame.display.update()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
				#print(event.pos)
				# Ask for Player 1 Input
				if turn == PLAYER:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))

					if is_valid_location(board, col):
						row = get_next_open_row(board, col)
						drop_piece(board, row, col, PLAYER_PIECE)

						if winning_move(board, PLAYER_PIECE):
							label = myfont.render("Player 1 wins!!", 1, RED)
							screen.blit(label, (40,10))
							game_over = True

						turn += 1
						turn = turn % 2

						print_board(board)
						draw_board(board)


		# # Ask for Player 2 Input
		if turn == AI and not game_over:				

			#col = random.randint(0, COLUMN_COUNT-1)
			#col = pick_best_move(board, AI_PIECE)
			col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

			if is_valid_location(board, col):
				#pygame.time.wait(500)
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, AI_PIECE)

				if winning_move(board, AI_PIECE):
					label = myfont.render("Player 2 wins!!", 1, YELLOW)
					screen.blit(label, (40,10))
					game_over = True

				print_board(board)
				draw_board(board)

				turn += 1
				turn = turn % 2

		if game_over:
			pygame.time.wait(3000)

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(340, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(340, 250), 
                            text_input="FRIEND", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
							
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(340, 400), 
                            text_input="AI", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(340, 550), 
                            text_input="QUIT", font=get_font(45), base_color="#d7fcd4", hovering_color="White")

        SETTING_BUTTON = Button(image=pygame.image.load("assets/sun.png"),pos=(670,30),
						text_input="",font=get_font(60),base_color="#d7fcd4",hovering_color="Red")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, SETTING_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
				
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ai()
                if SETTING_BUTTON.checkForInput(MENU_MOUSE_POS):
                    global b,BLUE,BLACK,RED,YELLOW 
                    BLUE,BLACK,RED,YELLOW = colors()
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()		
		
main_menu()

