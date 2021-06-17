class Player():
	def __init__(self,gameId):
		self.objects=[]
		self.grid=[[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1]]
		self.count=[0,0,0,0,0,0,0]
		self.bluescore=0
		self.redscore=0
		self.turn=0
		self.player=0
		self.message=""
		self.gameId=gameId
		self.ready=False
		self.win=False
		self.reset=False
			
	def check(self,pos):
		player = self.grid[self.count[pos]-1][pos]
		maxCol=7
		maxRow=6
		colNum=pos
		rowNum=self.count[pos]-1
		for i in range (0,maxRow):
		    for j in range (0,maxCol-3):
		    	if (self.grid[i][j] == player and self.grid[i][j+1] == player and self.grid[i][j+2] == player and self.grid[i][j+3] == player):
		            return True
		for i in range (0,maxRow-3):
		    for j in range (0,maxCol):
		        if (self.grid[i][j]== player and self.grid[i+1][j] == player and self.grid[i+2][j] == player and self.grid[i+3][j]==player):
		            return True      
		for i in range (3,maxRow):
		    for j in range (0,maxCol-3):
		        if (self.grid[i][j] == player and self.grid[i-1][j+1] == player and self.grid[i-2][j+2] == player and self.grid[i-3][j+3] == player):
		            return True
		for i in range (3,maxRow):
		    for j in range (3,maxCol):
		        if (self.grid[i][j] == player and self.grid[i-1][j-1] == player and self.grid[i-2][j-2] == player and self.grid[i-3][j-3] == player):
		            return True
		return False

	
			
	def resetgame(self):
		self.grid=[[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1]]
		self.count=[0,0,0,0,0,0,0]
		self.objects=[]
		if((self.redscore+self.bluescore)%2==0) :
			self.turn=0
		else:
			self.turn=1
		self.win=False
		self.message="get"
		self.reset=False

