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

class Block(object):
	def __init__(self):
		self.x_position = 0
		self.y_position = BOARD_HEIGHT - 1
		self.col = (247, 202, 201)
		self.block_width = 3


class Scoreboard(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.rows = 20
		self.font = pygame.font.SysFont("Helvetica", 16)
        
	def update(self):
		self.text = "rows left %d" % (self.rows)
		self.image = self.font.render(self.text, 1, (185,242,255))
		self.rect = self.image.get_rect()


class Game(object):
	def __init__(self):
		self.last_time = 0
		self.current_speed = 50 
		self.board = []
		self.direction = 1
		self.current_level = 0
		self.play = True
		self.game_status= INTRO



	def main(self):

		pygame.init()
		pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
		self.screen = pygame.display.set_mode( SCREEN_SIZE )
		pygame.mixer.music.load(os.path.join('sounds', 'soundtrack.ogg'))
		pygame.mixer.music.play(-1)
		block = Block()
		self.reset_game(block)
		scoreboard = Scoreboard()
		scoreSprite = pygame.sprite.Group(scoreboard)
		

		while(self.play):


			
			self.movement(block)
			self.update_board_info(block)
			self.update_screen(self.screen,scoreSprite,block)
			scoreSprite.update()
			scoreSprite.draw(self.screen)



			
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_SPACE:
						self.key_hit(scoreboard, scoreSprite, block)
						pygame.display.flip()


					##bug checking, makes it easier to check win state
					if event.key == K_RETURN: 
						block.x_position -= 1
						if (block.x_position < 0): 
							block.x_position = 0
						block.block_width += 1
						if (block.block_width >= BOARD_WIDTH): 
							block.block_width = BOARD_WIDTH - 1

			







	def movement(self,block):

		if self.game_status== PLAYING:
			current_time = pygame.time.get_ticks()
			if (self.last_time + self.current_speed <= current_time):
				new_x = block.x_position + self.direction
				if (new_x < 0) or (new_x + block.block_width > BOARD_WIDTH):
					self.direction = -self.direction
				
				block.x_position += self.direction
				
				self.last_time = current_time

	def update_board_info(self,block):
		self.clear_row(block)
		self.fill_current_row(block)


	def clear_row(self,block):
		for x in range(BOARD_WIDTH):
			self.board[x][block.y_position] = 0

	def fill_current_row(self,block):

		for x in range(block.x_position, block.x_position + block.block_width):
			self.board[x][block.y_position] = 1

	def update_screen(self,screen,scoreSprite,block):


		self.screen.blit(images[self.game_status], (0,0,SCREEN_WIDTH,SCREEN_HEIGHT), (0,0,SCREEN_WIDTH,SCREEN_HEIGHT))

		if self.game_status== PLAYING:
			if block.y_position < SCREEN_HEIGHT - 3:
				self.screen.blit(images[self.game_status], (0,0,SCREEN_WIDTH,SCREEN_HEIGHT - 15), (0,0,SCREEN_WIDTH,SCREEN_HEIGHT - 15))
				
			scoreSprite.draw(self.screen)
			self.draw_board(self.screen,block)
	





			

		elif self.game_status== INTRO:
			pass
		elif self.game_status== LOSE:
			pass
		elif self.game_status== WIN:
			pass
		
		pygame.display.flip()

	def draw_board(self,screen,block):
		for x in range(BOARD_WIDTH):
			for y in range(BOARD_HEIGHT):
				if self.board[x][y] == 1:
					self.draw_tile(self.screen, x, y,block)






				
	def draw_tile(self,screen, x, y,block):

		# if self.colorreverse == False:
		# 	try:
		# 		block.col = TILE_COlOR_LIST_ONE[self.prevcol + 1]
		# 	except:
		# 		self.colorreverse == True
		# 		self.col = TILE_COlOR_LIST_ONE[self.prevcol - 1]

		# else:
		# 	try:
		# 		self.col = TILE_COlOR_LIST_ONE[self.prevcol - 1]
		# 	except:
		# 		self.colorreverse == False
		# 		self.col = TILE_COlOR_LIST_ONE[self.prevcol + 1]

		if y == BOARD_HEIGHT - 1:
			block.col = TILE_COlOR_LIST_ONE[0]
		elif y == BOARD_HEIGHT - 2:
			block.col = TILE_COlOR_LIST_ONE[1]
		elif y == BOARD_HEIGHT - 3:
			block.col = TILE_COlOR_LIST_ONE[2]
		elif y == BOARD_HEIGHT - 4:
			block.col = TILE_COlOR_LIST_ONE[3]
		elif y == BOARD_HEIGHT - 5:
			block.col = TILE_COlOR_LIST_ONE[4]
		elif y == BOARD_HEIGHT - 6:
			block.col = TILE_COlOR_LIST_ONE[5]
		elif y == BOARD_HEIGHT - 7:
			block.col = TILE_COlOR_LIST_ONE[6]
		elif y == BOARD_HEIGHT - 8:
			block.col = TILE_COlOR_LIST_ONE[5]
		elif y == BOARD_HEIGHT - 9:
			block.col = TILE_COlOR_LIST_ONE[4]
		elif y == BOARD_HEIGHT - 10:
			block.col = TILE_COlOR_LIST_ONE[3]
		elif y == BOARD_HEIGHT - 11:
			block.col = TILE_COlOR_LIST_ONE[2]
		elif y == BOARD_HEIGHT - 12:
			block.col = TILE_COlOR_LIST_ONE[1]
		elif y == BOARD_HEIGHT - 13:
			block.col = TILE_COlOR_LIST_ONE[0]


		pygame.draw.rect(self.screen, block.col, (x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
		pygame.draw.rect(self.screen, (0, 0, 0), (x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 2)


	def reset_game(self,block):

		self.clear_board()
		
		self.play = True
		
		self.game_status= INTRO
		
		block.x_position = 0
		block.y_position = BOARD_HEIGHT - 1
		self.current_level = 0
		self.current_speed = TILE_SPEED[self.current_level]
		block.block_width = 3


	def key_hit(self,scoreboard, scoreSprite, block):

		goodsound = pygame.mixer.Sound(os.path.join('sounds', 'good.ogg'))
		badsound = pygame.mixer.Sound(os.path.join('sounds', 'bad.ogg'))
		losesound = pygame.mixer.Sound(os.path.join('sounds', 'lose.ogg'))
		tempwidth = block.block_width
		if self.game_status== PLAYING:
			if block.y_position < BOARD_HEIGHT - 1:
				for x in range(block.x_position, block.x_position + block.block_width):
					if self.board[x][block.y_position + 1] == 0: # If they're standing on a block that did not work
						block.block_width -= 1 # Then next time, give them one less block
						self.board[x][block.y_position] = 0 # Also, get rid of this block that isn't standing on solid ground.
			##plays a good sound if player doesn't lose a block
			if block.block_width == tempwidth:
				goodsound.play()
			##plays a bad sound if player loses a block
			else:
				badsound.play()
			block.y_position -= 1
			scoreboard.rows -=1
			self.current_level += 1
			self.win_lose(block)
			if self.game_status== LOSE:
				losesound.play()
				scoreboard.rows = WIN_LEVEL
		elif self.game_status== INTRO:
			self.game_status= PLAYING
		elif self.game_status== LOSE:
			self.reset_game(block)
			self.game_status= INTRO
		else:
			self.play = False




	def win_lose(self,block):

		
		if block.block_width == 0:
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
