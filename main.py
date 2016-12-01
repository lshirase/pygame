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


TILE_COlOR_LIST_ONE= [(247, 202, 201), (237,209,210), (226,215,219), (216,222,228), (206,229,237), (195,235,246), (185,242,255)]


TILE_SPEED = ( 85, 85, 80, 80, 75, 75, 70, 70, 65, 63, 60, 55, 52, 50, 45, 40, 35, 30, 29, 28)

				
WIN_LEVEL = 20

INTRO = 0
PLAYING = 1
LOSE = 2
WIN = 3



images = ( pygame.image.load(os.path.join('backgrounds', 'first.png')), pygame.image.load(os.path.join('backgrounds', 'main.png')), pygame.image.load(os.path.join('backgrounds', 'lose.png')), pygame.image.load(os.path.join('backgrounds', 'youwon.png')))



class Game(object):
	def __init__(self):
		self.last_time = 0
		self.current_speed = 50 
		self.board = []
		self.direction = 1
		self.x_position = 0
		self.y_position = BOARD_HEIGHT - 1
		self.old_y = self.y_position
		self.block_width = 3
		self.current_level = 0
		self.col = (247, 202, 201)
		self.prevcol = 0
		self.colorreverse = False
		self.play = True
		self.game_status= INTRO

	def main(self):

		pygame.init()
		pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
		self.screen = pygame.display.set_mode( SCREEN_SIZE )
		pygame.mixer.music.load(os.path.join('sounds', 'soundtrack.ogg'))
		pygame.mixer.music.play(-1)

		
		self.reset_game()


		while(self.play):
			
			self.movement()
			self.update_board_info()
			self.update_screen(self.screen)
			
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_SPACE:
						self.key_hit()
					##bug checking, makes it easier to check win state
					if event.key == K_RETURN: 
						self.x_position -= 1
						if (self.x_position < 0): 
							self.x_position = 0
						self.block_width += 1
						if (self.block_width >= BOARD_WIDTH): 
							self.block_width = BOARD_WIDTH - 1




	def movement(self):

		if self.game_status== PLAYING:
			current_time = pygame.time.get_ticks()
			if (self.last_time + self.current_speed <= current_time):
				new_x = self.x_position + self.direction
				if (new_x < 0) or (new_x + self.block_width > BOARD_WIDTH):
					self.direction = -self.direction
				
				self.x_position += self.direction
				
				self.last_time = current_time

	def update_board_info(self):
		self.clear_row(self.y_position)
		self.fill_current_row()

	def clear_row(self,y):
		for x in range(BOARD_WIDTH):
			self.board[x][y] = 0

	def fill_current_row(self):
		self.x_position, self.y_position, self.block_width
		for x in range(self.x_position, self.x_position + self.block_width):
			self.board[x][self.y_position] = 1

	def update_screen(self,screen):


		self.screen.blit(images[self.game_status], (0,0,SCREEN_WIDTH,SCREEN_HEIGHT), (0,0,SCREEN_WIDTH,SCREEN_HEIGHT))

		if self.game_status== PLAYING:
			if self.y_position < SCREEN_HEIGHT - 3:
				self.screen.blit(images[self.game_status], (0,0,SCREEN_WIDTH,SCREEN_HEIGHT - 15), (0,0,SCREEN_WIDTH,SCREEN_HEIGHT - 15))

			self.draw_board(self.screen)
			

		elif self.game_status== INTRO:
			pass
		elif self.game_status== LOSE:
			pass
		elif self.game_status== WIN:
			pass
		
		pygame.display.flip()

	def draw_board(self,screen):
		for x in range(BOARD_WIDTH):
			for y in range(BOARD_HEIGHT):
				if self.board[x][y] == 1:
					self.draw_tile(self.screen, x, y)


				
	def draw_tile(self,screen, x, y):

		if self.colorreverse == False:
			try:
				self.col = TILE_COlOR_LIST_ONE[self.prevcol + 1]
			except:
				self.colorreverse == True
				self.col = TILE_COlOR_LIST_ONE[self.prevcol - 1]

		else:
			try:
				self.col = TILE_COlOR_LIST_ONE[self.prevcol - 1]
			except:
				self.colorreverse == False
				self.col = TILE_COlOR_LIST_ONE[self.prevcol + 1]

		if y == BOARD_HEIGHT - 1:
			self.col = TILE_COlOR_LIST_ONE[0]
		elif y == BOARD_HEIGHT - 2:
			self.col = TILE_COlOR_LIST_ONE[1]
		elif y == BOARD_HEIGHT - 3:
			self.col = TILE_COlOR_LIST_ONE[2]
		elif y == BOARD_HEIGHT - 4:
			self.col = TILE_COlOR_LIST_ONE[3]
		elif y == BOARD_HEIGHT - 5:
			self.col = TILE_COlOR_LIST_ONE[4]
		elif y == BOARD_HEIGHT - 6:
			self.col = TILE_COlOR_LIST_ONE[5]
		elif y == BOARD_HEIGHT - 7:
			self.col = TILE_COlOR_LIST_ONE[6]
		elif y == BOARD_HEIGHT - 8:
			self.col = TILE_COlOR_LIST_ONE[5]
		elif y == BOARD_HEIGHT - 9:
			self.col = TILE_COlOR_LIST_ONE[4]
		elif y == BOARD_HEIGHT - 10:
			self.col = TILE_COlOR_LIST_ONE[3]
		elif y == BOARD_HEIGHT - 11:
			self.col = TILE_COlOR_LIST_ONE[2]
		elif y == BOARD_HEIGHT - 12:
			self.col = TILE_COlOR_LIST_ONE[1]
		elif y == BOARD_HEIGHT - 13:
			self.col = TILE_COlOR_LIST_ONE[0]


		pygame.draw.rect(self.screen, self.col, (x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
		pygame.draw.rect(self.screen, (0, 0, 0), (x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 2)
		

	def reset_game(self):

		self.clear_board()
		
		self.play = True
		
		self.game_status= INTRO
		
		self.x_position = 0
		self.y_position = BOARD_HEIGHT - 1
		self.current_level = 0
		self.current_speed = TILE_SPEED[self.current_level]
		self.block_width = 3


	def key_hit(self):

		goodsound = pygame.mixer.Sound(os.path.join('sounds', 'good.ogg'))
		badsound = pygame.mixer.Sound(os.path.join('sounds', 'bad.ogg'))
		losesound = pygame.mixer.Sound(os.path.join('sounds', 'lose.ogg'))
		tempwidth = self.block_width
		if self.game_status== PLAYING:
			if self.y_position < BOARD_HEIGHT - 1:
				for x in range(self.x_position, self.x_position + self.block_width):
					if self.board[x][self.y_position + 1] == 0: # If they're standing on a block that did not work
						self.block_width -= 1 # Then next time, give them one less block
						self.board[x][self.y_position] = 0 # Also, get rid of this block that isn't standing on solid ground.
			##plays a good sound if player doesn't lose a block
			if self.block_width == tempwidth:
				goodsound.play()
			##plays a bad sound if player loses a block
			else:
				badsound.play()
			self.y_position -= 1
			self.current_level += 1
			self.win_lose()
			if self.game_status== LOSE:
				losesound.play()
		elif self.game_status== INTRO:
			self.game_status= PLAYING
		elif self.game_status== LOSE:
			self.reset_game()
			self.game_status= INTRO
		else:
			self.play = False



	def win_lose(self):

		
		if self.block_width == 0:
			self.game_status= LOSE
		elif self.current_level == WIN_LEVEL:
		 	self.game_status= WIN
		else:
			self.current_speed = TILE_SPEED[self.current_level]



	def clear_board(self):
		
		self.board = []
		for x in range(BOARD_WIDTH):
			self.board.append([])
			for y in range (BOARD_HEIGHT):
				self.board[x].append(0)




if __name__ == '__main__':
    game = Game()
    game.main()

pygame.quit()
quit()		
