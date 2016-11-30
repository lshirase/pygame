import backgrounds
import pygame
from pygame.locals import *
from pygame.mixer import *
from backgrounds import *
import os

##SONG CREDIT - EDU TEODORO - 420 (MACINTOSH PLUS) - SEGA GENESIS REMIX
##LINK TO SONG - https://soundcloud.com/edu-teodoro/420-macintosh-plus-sega-genesis-remix

BOARD_WIDTH = 12 
BOARD_HEIGHT = 20
BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 400
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT 
TILE_WIDTH = 20
TILE_HEIGHT = 20
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT


TILE_COLOR_LIST_ONE= [(247, 202, 201), (237,209,210), (226,215,219), (216,222,228), (206,229,237), (195,235,246), (185,242,255)]


TILE_SPEED = ( 85, 85, 80, 80, 75, 75, 70, 70, 65, 63, 60, 55, 52, 50, 45, 40, 35, 30, 29, 28)

				
WIN_LEVEL = 20

current_speed = 50 # Current tile speed in milliseconds
board = []
direction = 1
x_position = 0
y_position = BOARD_HEIGHT - 1
old_y = y_position
block_width = 3
current_level = 0
col = (247, 202, 201)
prevcol = 0
counter = 0
colorreverse = False



	

INTRO = 0
PLAYING = 1
LOSE = 2
WIN = 3

game_status= INTRO

images = ( pygame.image.load(os.path.join('backgrounds', 'first.png')), pygame.image.load(os.path.join('backgrounds', 'main.png')), pygame.image.load(os.path.join('backgrounds', 'lose.png')), pygame.image.load(os.path.join('backgrounds', 'youwon.png')))


play = True

def main():
	global game_status, x_position, y_position, current_speed, play, block_width, current_level, current_color, current_colorcount, goodsound
	pygame.init()
	pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
	screen = pygame.display.set_mode( SCREEN_SIZE )
	pygame.mixer.music.load(os.path.join('sounds', 'soundtrack.ogg'))
	pygame.mixer.music.play(-1)

	
	reset_game()


	while(play):
		update_movement()
		update_board_info()
		update_screen(screen)
		
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					key_hit()
				##bug checking, makes it easier to check win state
				if event.key == K_RETURN: 
					x_position -= 1
					if (x_position < 0): 
						x_position = 0
					block_width += 1
					if (block_width >= BOARD_WIDTH): 
						block_width = BOARD_WIDTH - 1

def reset_game():
	global game_status, x_position, y_position, current_speed, play, block_width, current_level

	clear_board()
	
	play = True
	
	game_status= INTRO
	
	x_position = 0
	y_position = BOARD_HEIGHT - 1
	current_level = 0
	current_speed = TILE_SPEED[current_level]
	block_width = 3


def key_hit():
	global play, game_status, x_position, y_position, block_width, current_speed, current_level
	goodsound = pygame.mixer.Sound(os.path.join('sounds', 'good.ogg'))
	badsound = pygame.mixer.Sound(os.path.join('sounds', 'bad.ogg'))
	losesound = pygame.mixer.Sound(os.path.join('sounds', 'lose.ogg'))
	tempwidth = block_width
	if game_status== PLAYING:
		if y_position < BOARD_HEIGHT - 1:
			for x in range(x_position, x_position + block_width):
				if board[x][y_position + 1] == 0: # If they're standing on a block that did not work
					block_width -= 1 # Then next time, give them one less block
					board[x][y_position] = 0 # Also, get rid of this block that isn't standing on solid ground.
		##plays a good sound if player doesn't lose a block
		if block_width == tempwidth:
			goodsound.play()
		##plays a bad sound if player loses a block
		else:
			badsound.play()
		y_position -= 1
		current_level += 1
		win_lose()
		if game_status== LOSE:
			losesound.play()
	elif game_status== INTRO:
		game_status= PLAYING
	elif game_status== LOSE:
		reset_game()
		game_status= INTRO
	else:
		play = False

def update_movement():
	global game_status, last_time, x_position, y_position, block_width, current_speed, direction

	if game_status== PLAYING:
		current_time = pygame.time.get_ticks()
		if (last_time + current_speed <= current_time):
			new_x = x_position + direction
			if (new_x < 0) or (new_x + block_width > BOARD_WIDTH):
				direction = -direction
			
			x_position += direction
			
			last_time = current_time

def win_lose():
	global game_status, block_width, current_level, current_speed, play, TILE_COLOR
	
	if block_width == 0:
		game_status= LOSE
	elif current_level == WIN_LEVEL:
	 	game_status= WIN
	else:
		current_speed = TILE_SPEED[current_level]


last_time = 0

		
def update_screen(screen):
	global game

	screen.blit(images[game_status], (0,0,SCREEN_WIDTH,SCREEN_HEIGHT), (0,0,SCREEN_WIDTH,SCREEN_HEIGHT))

	if game_status== PLAYING:
		if y_position < SCREEN_HEIGHT - 3:
			screen.blit(images[game_status], (0,0,SCREEN_WIDTH,SCREEN_HEIGHT - 10), (0,0,SCREEN_WIDTH,SCREEN_HEIGHT - 10))
		draw_board(screen)
		
		# pygame.draw.rect(screen, col, (4 * TILE_WIDTH, BOARD_HEIGHT -3 * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
		# pygame.draw.rect(screen, (0, 0, 0), (4 * TILE_WIDTH, BOARD_HEIGHT -3 * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 2)

	elif game_status== INTRO:
		pass
	elif game_status== LOSE:
		pass
	elif game_status== WIN:
		pass
	
	pygame.display.flip()
	
def update_board_info():
	clear_row(y_position)
	fill_current_row()
	
def draw_board(screen):
	global counter, colorreverse
	for x in range(BOARD_WIDTH):
		for y in range(BOARD_HEIGHT):
			if board[x][y] == 1:
				draw_tile(screen, x, y)


			
def draw_tile(screen, x, y):
	global colorreverse, counter, prevcol
	if colorreverse == False:
		try:
			col = TILE_COLOR_LIST_ONE[prevcol + 1]
		except:
			colorreverse == True
			col = TILE_COLOR_LIST_ONE[prevcol - 1]

	else:
		try:
			col = TILE_COLOR_LIST_ONE[prevcol - 1]
		except:
			colorreverse == False
			col = TILE_COLOR_LIST_ONE[prevcol + 1]





	# counttemp = counter % 3
	# if colorreverse == False:
	# 	if counttemp == 6:
	# 		col = TILE_COLOR_LIST_ONE[counttemp]
	# 		colorreverse = True
	# 	else:
	# 		col = TILE_COLOR_LIST_ONE[counttemp]
	# elif colorreverse == True:
	# 	if counttemp == 0:
	# 		col = TILE_COLOR_LIST_ONE[counttemp]
	# 		colorreverse = False
	# 	else:
	# 		col = TILE_COLOR_LIST_ONE[counttemp]

	# if colorreverse == False:
	# 	counter = counter + 1
	# else:
	# 	counter = counter - 1


	if y == BOARD_HEIGHT - 1:
		col = TILE_COLOR_LIST_ONE[0]
	elif y == BOARD_HEIGHT - 2:
		col = TILE_COLOR_LIST_ONE[1]
	elif y == BOARD_HEIGHT - 3:
		col = TILE_COLOR_LIST_ONE[2]
	elif y == BOARD_HEIGHT - 4:
		col = TILE_COLOR_LIST_ONE[3]
	elif y == BOARD_HEIGHT - 5:
		col = TILE_COLOR_LIST_ONE[4]
	elif y == BOARD_HEIGHT - 6:
		col = TILE_COLOR_LIST_ONE[5]
	elif y == BOARD_HEIGHT - 7:
		col = TILE_COLOR_LIST_ONE[6]
	elif y == BOARD_HEIGHT - 8:
		col = TILE_COLOR_LIST_ONE[5]
	elif y == BOARD_HEIGHT - 9:
		col = TILE_COLOR_LIST_ONE[4]
	elif y == BOARD_HEIGHT - 10:
		col = TILE_COLOR_LIST_ONE[3]
	elif y == BOARD_HEIGHT - 11:
		col = TILE_COLOR_LIST_ONE[2]
	elif y == BOARD_HEIGHT - 12:
		col = TILE_COLOR_LIST_ONE[1]
	elif y == BOARD_HEIGHT - 13:
		col = TILE_COLOR_LIST_ONE[0]


	# if current_color == 0 and current_colorcount == 9:
	# 	col = TILE_COLOR_LIST_ONE[current_color] 
	# 	current_color = current_color + 1
	# 	current_colorcount = current_colorcount - 1

	# elif current_color < 8 and current_colorcount > 0:
	# 	col = TILE_COLOR_LIST_ONE[current_color]
	# 	current_color = current_color + 1
	# 	current_colorcount = current_colorcount - 1

	# elif current_color == 8 and current_colorcount == 0:
	# 	col = TILE_COLOR_LIST_ONE[current_color]
	# 	current_color = current_color - 1
	# 	current_colorcount = current_colorcount + 1
	# elif current_color > 0 and current_colorcount < 8:
	# 	col = TILE_COLOR_LIST_ONE[current_color]
	# 	current_color = current_color - 1
	# 	current_colorcount = current_colorcount + 1

	pygame.draw.rect(screen, col, (x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
	pygame.draw.rect(screen, (0, 0, 0), (x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 2)

def clear_board():
	global board
	
	board = []
	for x in range(BOARD_WIDTH):
		board.append([])
		for y in range (BOARD_HEIGHT):
			board[x].append(0)

def clear_row(y):
	for x in range(BOARD_WIDTH):
		board[x][y] = 0

def fill_current_row():
	global x_position, y_position, block_width
	for x in range(x_position, x_position + block_width):
		board[x][y_position] = 1


main()
pygame.quit()
quit()		