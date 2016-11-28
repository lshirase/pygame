'''Game main module.

Last Day Game Entry, by Clint Herron
'''

import data
import pygame
from pygame.locals import *
from data import *
import os

BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = 12, 20
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 240, 400
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = SCREEN_WIDTH / BOARD_WIDTH, SCREEN_HEIGHT / BOARD_HEIGHT

TILE_COLOR = (255, 204, 255)
TILE_COLOR_ALT = (204, 204, 255)

LEVEL_SPEED = ( 80, 80, 75, 75, 70, 70, 65, 60, 55, 50,
				45, 40, 35, 30, 32 )
MAX_WIDTH = (3, 3, 3, 3, 2, 2, 2, 2, 1, 1,
				1, 1, 1, 1, 1)
				
COLOR_CHANGE_Y = 10 # The block below which are displayed in the alternate color
WIN_LEVEL = 15

current_speed = 50 # Current tile speed in milliseconds
board = []
current_direction = 1
current_x, current_y, current_width = 0, BOARD_HEIGHT - 1, 3
current_level = 0

INTRO = 0
PLAYING = 1
LOSE = 2
WIN = 3

game_state = INTRO

bg_images = ( pygame.image.load(os.path.join('data', 'intro.png')), pygame.image.load(os.path.join('data', 'game.png')), pygame.image.load(os.path.join('data', 'lose.png')), pygame.image.load(os.path.join('data', 'win.png')))

keep_running = True

def main():
	global game_state, current_x, current_y, current_speed, keep_running, current_width, current_level
	
	pygame.init()
	screen = pygame.display.set_mode( SCREEN_SIZE )	
	
	reset_game()

	while(keep_running):
		update_movement()
		update_board_info()
		update_screen(screen)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				keep_running = False
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					key_hit()
				if event.key == K_F1: # Yes, this is a cheat.
					current_x -= 1
					if (current_x < 0): current_x = 0
					current_width += 1
					if (current_width >= BOARD_WIDTH): current_width = BOARD_WIDTH - 1

def reset_game():
	global game_state, current_x, current_y, current_speed, keep_running, current_width, current_level

	clear_board()
	
	keep_running = True
	
	game_state = INTRO
	
	current_x = 0
	current_y = BOARD_HEIGHT - 1
	current_level = 0
	current_speed = LEVEL_SPEED[current_level]
	current_width = MAX_WIDTH[current_level]

def key_hit():
	global keep_running, game_state, current_x, current_y, current_width, current_speed, current_level
	
	if game_state == PLAYING:
		if current_y < BOARD_HEIGHT - 1:
			for x in range(current_x, current_x + current_width):
				if board[x][current_y + 1] == 0: # If they're standing on a block that did not work
					current_width -= 1 # Then next time, give them one less block
					board[x][current_y] = 0 # Also, get rid of this block that isn't standing on solid ground.
		current_y -= 1
		current_level += 1
		check_win_lose()
	elif game_state == INTRO:
		game_state = PLAYING
	elif game_state == LOSE:
		reset_game()
		game_state = INTRO
	else:
		keep_running = False

def check_win_lose():
	global game_state, current_width, current_level, current_speed, keep_running, TILE_COLOR
	
	if current_width == 0:
		game_state = LOSE
	elif current_level == WIN_LEVEL:
		game_state = WIN
	else:
		current_speed = LEVEL_SPEED[current_level]
		if current_width > MAX_WIDTH[current_level]:
			current_width = MAX_WIDTH[current_level]

last_time = 0
def update_movement():
	global game_state, last_time, current_x, current_y, current_width, current_speed, current_direction

	if game_state == PLAYING:
		current_time = pygame.time.get_ticks()
		if (last_time + current_speed <= current_time):
			new_x = current_x + current_direction
			if (new_x < 0) or (new_x + current_width > BOARD_WIDTH):
				current_direction = -current_direction
			
			current_x += current_direction
			
			last_time = current_time
		
def update_screen(screen):
	global game_state

	screen.blit(bg_images[game_state], (0,0,SCREEN_WIDTH,SCREEN_HEIGHT), (0,0,SCREEN_WIDTH,SCREEN_HEIGHT))

	if game_state == PLAYING:
		draw_board(screen)
	elif game_state == INTRO:
		pass
	elif game_state == LOSE:
		pass
	elif game_state == WIN:
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
	col = TILE_COLOR
	if (y < COLOR_CHANGE_Y):
		col = TILE_COLOR_ALT
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