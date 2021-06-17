import sys,os, pygame
import pickle
from network import Network
pygame.init()

screen = pygame.display.set_mode((542, 500))
background = pygame.image.load('bg.jpg').convert()
background= pygame.transform.scale(background,(520,400))

blueball = pygame.image.load("slot3.gif").convert()
redball= pygame.image.load("red2").convert()
bluerect=blueball.get_rect()
redrect=redball.get_rect()

victory_sound= pygame.mixer.Sound("success.wav")


class Ball(pygame.sprite.Sprite):
	def __init__(self,image,rect,c):
		pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
		self.x=0
		self.pos=-1
		self.c=c
		self.y=30
		self.image=image
		self.rect=rect
		
	def update(self):
		xpos,ypos= pygame.mouse.get_pos()
		if (xpos<105):
			self.x=60
			self.pos=0
		elif (xpos<175):
			self.x=130
			self.pos=1
		elif (xpos<245):
			self.x=200
			self.pos=2
		elif (xpos<315):
			self.x=270
			self.pos=3
		elif (xpos<385):
			self.x=340
			self.pos=4
		elif (xpos<455):
			self.x=410
			self.pos=5
		else:
			self.x=480
			self.pos=6
		if((self.c%2)==1):
			self.rect.midtop = self.x,self.y-24
		else:
			self.rect.midtop = self.x,self.y
			
	def drop(self,game,bleuball,redball):
		x_val=self.x-31
		y_val=((5-game.count[self.pos])*65)+100
		game.count[self.pos]=game.count[self.pos]+1
		objects=game.objects
		
		if(game.count[self.pos]<7) :
		
			if((game.turn)%2==1):
				x_val=x_val-19
				y_val=y_val-25
				
			for position in range (100,y_val,65):
				screen.blit(background, (12, 95))
				for x in range(6):
					for y in range(7):
						pygame.draw.circle(screen, (175,238,238), ((y*70)+60,(x*65)+132), 27, 0)
				for positions in objects:
					if(positions[2]==0):
						screen.blit(blueball,(positions[0],positions[1]))
					else:
						screen.blit(redball,(positions[0],positions[1]))
				screen.blit(self.image,(x_val,position))
				pygame.display.update()
				pygame.time.delay(80)
				
			if(game.turn==0):
				game.grid[game.count[self.pos]-1][self.pos]=0
			else:
				game.grid[game.count[self.pos]-1][self.pos]=1
			game.objects.append((x_val,y_val,game.turn%2))
			game.win=game.check(self.pos)
			game.turn=(game.turn+1)%2
			return game
			
			
def display_message(message):
		font = pygame.font.Font(None, 36)
		text = font.render(message, 1, (10, 10, 10))
		textpos = text.get_rect(centerx=background.get_width()/2)
		screen.blit(text, textpos)


def draw_background(game,player,allsprites):

	screen.fill((175,238,238))
	screen.blit(background, (12, 95))
		     
	for x in range(6):
		for y in range(7):
			pygame.draw.circle(screen, (175,238,238), ((y*70)+60,(x*65)+132), 27, 0)
	
	if not(game.ready):
		display_message("Waiting for player 2...")
	
	else:
		for positions in game.objects:
				if(positions[2]==0):
					screen.blit(blueball,(positions[0],positions[1]))
				else:
					screen.blit(redball,(positions[0],positions[1]))
		allsprites.draw(screen)
		if(game.turn==0):
			display_message("Player 1(blue) goes now")
		else:
			display_message("Player 2(red) goes now")
		if game.win == False :
			allsprites.update()
	pygame.display.update()
	
	
		

				
def main():
	run=True
	n=Network()
	game=n.getgame()
	
	if not game:
		print("Not connected")
	else:
		player=game.player
		print("You are player: ", game.player+1)
		
		if(player==0):
			ball=Ball(blueball,bluerect,0)
		else:
			ball=Ball(redball,redrect,1)
	
		while run:
			try:
				game=n.send(game)
			except:
				run=False
				print("Couldn't load game")
			allsprites = pygame.sprite.RenderPlain((ball))
			draw_background(game,player,allsprites)
			if game.win ==True:
				message="won the game!"
				if (game.turn==0):
					message = "Red "+message
					game.redscore=game.redscore+1
				else :
					message = "Blue " +message
					game.bluescore=game.bluescore+1
				victory_sound.play()
				for i in range(0,3000):
					pygame.draw.rect(screen,(175,238,238),(90,0,400,26))
					display_message(message)
					pygame.display.update()

				message="Blue: "+str(game.bluescore)+",  Red: "+str(game.redscore)
				for i in range(0,4000):
					screen.fill((175,238,238))
					display_message(message)
					pygame.display.update()
				game.message="reset"
				game=n.send(game)
				
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					pygame.quit()
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN and game.win == False and game.ready== True:
					if game.turn==player :
						game=ball.drop(game,blueball,redball)
						game.message="drop"
					else:
						font = pygame.font.Font(None, 36)
						text = font.render("Opponent makes a move now...", 1, (10, 10, 10))
						textpos = text.get_rect(centerx=background.get_width()/2)
						for i in range(0,6000):
							pygame.draw.rect(screen,(175,238,238),(90,0,400,26))
							screen.blit(text, textpos)
							pygame.display.update()
					game=n.send(game)
            
def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        screen.fill((175,238,238))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        screen.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()		
		
		
while True:
    menu_screen()
