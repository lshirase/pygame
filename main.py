import backgrounds
import pygame
from pygame.locals import *
from pygame.mixer import *
from backgrounds import *
import os

BOARD_WIDTH = 12 
BOARD_HEIGHT = 20
BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 400
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT 
TILE_WIDTH = SCREEN_WIDTH / BOARD_WIDTH
TILE_HEIGHT = SCREEN_HEIGHT / BOARD_HEIGHT
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT


TILE_COLOR_LIST = [(255, 204, 255), (253, 209, 254), (252, 215, 253), (251, 221, 253), (250, 226, 252), (249, 232, 252), (248, 238, 251), (247, 243, 251
), (246, 249, 250)]


LEVEL_SPEED = ( 80, 80, 75, 75, 70, 70, 65, 60, 55, 50,
				45, 40, 35, 30, 32 )

				
WIN_LEVEL = 15

current_speed = 50 # Current tile speed in milliseconds
board = []
direction = 1
current_x = 0
current_y = BOARD_HEIGHT - 1
current_width = 3
current_level = 0
current_color = 0
current_colorcount = 9


	

INTRO = 0
PLAYING = 1
LOSE = 2
WIN = 3

game = INTRO

images = ( pygame.image.load(os.path.join('backgrounds', 'first.png')), pygame.image.load(os.path.join('backgrounds', 'main.png')), pygame.image.load(os.path.join('backgrounds', 'lose.png')), pygame.image.load(os.path.join('backgrounds', 'youwon.png')))


play = True

def main():
	global game, current_x, current_y, current_speed, play, current_width, current_level, current_color, current_colorcount, goodsound
	pygame.init()
	pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
	screen = pygame.display.set_mode( SCREEN_SIZE )

	
	reset_game()


	while(play):
		update_movement()
		update_board_info()
		update_screen(screen)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				play = False
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					key_hit()
				if event.key == K_F1: # Yes, this is a cheat.
					current_x -= 1
					if (current_x < 0): current_x = 0
					current_width += 1
					if (current_width >= BOARD_WIDTH): current_width = BOARD_WIDTH - 1

def reset_game():
	global game, current_x, current_y, current_speed, play, current_width, current_level

	clear_board()
	
	play = True
	
	game = INTRO
	
	current_x = 0
	current_y = BOARD_HEIGHT - 1
	current_level = 0
	current_speed = LEVEL_SPEED[current_level]
	current_width = 3


def key_hit():
	global play, game, current_x, current_y, current_width, current_speed, current_level
	goodsound = pygame.mixer.Sound(os.path.join('sounds', 'good.ogg'))
	tempwidth = current_width
	if game == PLAYING:
		if current_y < BOARD_HEIGHT - 1:
			for x in range(current_x, current_x + current_width):
				if board[x][current_y + 1] == 0: # If they're standing on a block that did not work
					current_width -= 1 # Then next time, give them one less block
					board[x][current_y] = 0 # Also, get rid of this block that isn't standing on solid ground.
		##plays a good sound if player doesn't lose a block
		if current_width == tempwidth:
			goodsound.play()
		current_y -= 1
		current_level += 1
		game_status()
	elif game == INTRO:
		game = PLAYING
	elif game == LOSE:
		reset_game()
		game = INTRO
	else:
		play = False

def game_status():
	global game, current_width, current_level, current_speed, play, TILE_COLOR
	
	if current_width == 0:
		game = LOSE
	# elif current_level == WIN_LEVEL:
	# 	game = WIN
	else:
		current_speed = LEVEL_SPEED[current_level]


last_time = 0
def update_movement():
	global game, last_time, current_x, current_y, current_width, current_speed, direction

	if game == PLAYING:
		current_time = pygame.time.get_ticks()
		if (last_time + current_speed <= current_time):
			new_x = current_x + direction
			if (new_x < 0) or (new_x + current_width > BOARD_WIDTH):
				direction = -direction
			
			current_x += direction
			
			last_time = current_time
		
def update_screen(screen):
	global game

	screen.blit(images[game], (0,0,SCREEN_WIDTH,SCREEN_HEIGHT), (0,0,SCREEN_WIDTH,SCREEN_HEIGHT))

	if game == PLAYING:
		if current_y < SCREEN_HEIGHT - 3:
			screen.blit(images[game], (0,0,SCREEN_WIDTH,SCREEN_HEIGHT - 10), (0,0,SCREEN_WIDTH,SCREEN_HEIGHT - 10))
		draw_board(screen)
		
		# pygame.draw.rect(screen, col, (4 * TILE_WIDTH, BOARD_HEIGHT -3 * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
		# pygame.draw.rect(screen, (0, 0, 0), (4 * TILE_WIDTH, BOARD_HEIGHT -3 * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 2)

	elif game == INTRO:
		pass
	elif game == LOSE:
		pass
	elif game == WIN:
		pass
	
	pygame.display.flip()
	
def update_board_info():
	clear_row(current_y)
	fill_current_row()
	
def draw_board(screen):
	for x in range(BOARD_WIDTH):
		for y in range(BOARD_HEIGHT):
			if board[x][y] == 1:
				draw_tile(screen, x, y)
			
def draw_tile(screen, x, y):
	global current_color, current_colorcount
	col = (255,0,0)

	if current_color == 0 and current_colorcount == 9:
		col = TILE_COLOR_LIST[current_color] 
		current_color = current_color + 1
		current_colorcount = current_colorcount - 1

	elif current_color < 8 and current_colorcount > 0:
		col = TILE_COLOR_LIST[current_color]
		current_color = current_color + 1
		current_colorcount = current_colorcount - 1

	elif current_color == 8 and current_colorcount == 0:
		col = TILE_COLOR_LIST[current_color]
		current_color = current_color - 1
		current_colorcount = current_colorcount + 1
	elif current_color > 0 and current_colorcount < 8:
		col = TILE_COLOR_LIST[current_color]
		current_color = current_color - 1
		current_colorcount = current_colorcount + 1

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
	global current_x, current_y, current_width
	for x in range(current_x, current_x + current_width):
		board[x][current_y] = 1


main()
pygame.quit()
quit()		