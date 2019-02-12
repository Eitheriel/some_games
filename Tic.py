
class Battlefield():

	def dimension(self,text,lower_limit,higher_limit,default_num,stride=1):
		"""Returns integer representing variable value according to the text in input."""
		while True:
				dim=input("Please enter the {}, between {} and {}. Press enter and {} will be set. ".format(text,lower_limit,higher_limit,default_num))
				if dim=="":
					return default_num 
				try:
					if int(dim) not in range(lower_limit,higher_limit+1,stride):
						print("\nYou must enter the proper number.")
						continue
					else:
						return int(dim)
				except ValueError:
					print("\nYou must enter the proper number.")
					continue

	def board_Stuffing(self,x,y):
		"""
		Return the list of list.
		In every list is array of numbers representing each cell of battlefield. 
		The count of numbers in every list is influenced by battlefield proportions.
		"""

		superboard=[]
		num1=1
		for i in range(y):
			line=[]
			for j in range(x):
				line.append(num1)
				num1+=1
			superboard.append(line)
		return superboard

	def board_Frame(self,x,stuff):
		"""
		Return graphical frame of cells of battlefield according to the number of cells.
		"""

		horizontal_wall="-"*4*x+"-"
		vertical_wall="|"+x*"{:^3}|"
		print(horizontal_wall)
		for i in stuff:
			print(vertical_wall.format(*(i)))
			print(horizontal_wall)

	def adjust_Line(self,x,y):
		"""
		Returns integer representing the length of line of the same symbols, which is needed for winning the game.
		The returning number is adjusted according to the size of battlefield to ensure of win possibility.
		"""

		if x==3 or y==3: return 3
		if x==4 or y==4: return 4
		if x>=5 or y>=5: return self.dimension("length of line",3,5,3)

class Gameplay():

	def __init__(self):
		self.x=battle.dimension("number of columns",3,20,3)
		self.y=battle.dimension("number of rows",3,20,3)
		self.line=battle.adjust_Line(self.x,self.y)
		self.num_of_players=battle.dimension("number of players",2,3,2)
		self.list_of_players=self.symbol(self.num_of_players,"X","O","#","@")
		self.stuff=battle.board_Stuffing(self.x,self.y)

	def symbol(self,num_of_players1,*symb):
		"""
		Return dictionary with players as a keys and unique symbols for every player as values.
		The number of players depends on the choice of players.
		"""

		symb1=list(symb)
		list_of_players={}
		for i in range(1,num_of_players1+1):
			while True:
				sym=input("\nChoose your symbol: {}. Press enter and {} will be set. ".format(', '.join(symb1),symb1[0])).upper()
				if sym=="":
					list_of_players["Player"+str(i)]=symb1[0]
					print("Symbol {} has been chosen.".format(symb1[0]))
					symb1.remove(symb1[0])
					break
				if sym in symb1:
					list_of_players["Player"+str(i)]=sym
					print("Symbol {} has been chosen.".format(sym))
					symb1.remove(sym)
					break
				else:
					print("\nPlease choose your symbol.")
					continue
		return list_of_players

	def turn1(self,symbol):
		"""
		Replace the order number of cell with the specific symbol of player. 
		Returns coordinates of number the player want to replace for his/her symbol.
		It also controls, if the chosen cell is already taken.
		"""

		while True:
			try:
				turn_input=int(input("Please enter the number of the cell you want to put your symbol: "))
				
				coordinate1=int((turn_input-0.5)//self.x)
				coordinate2=(turn_input%self.x)-1 if turn_input%self.x!=0 else self.x-1 
				
				if turn_input not in range (1,(self.x*self.y)+1):
					print("\nYou may enter numbers only in range from 1 to {}.".format(self.x*self.y))
					continue
				if self.stuff[coordinate1][coordinate2]!= turn_input:
					print("\nThis cell is already taken, try another.")
					continue
				else:
					self.stuff[coordinate1][coordinate2]=symbol
					return coordinate1,coordinate2
					break
			except ValueError:
				print("\nPlease try again.")
				continue

	def winwin(self,x_coord,y_coord):
		"""
		Controls, if player created the line of same symbols of the given length on the battlefield. If yes, it returns True.

		First for loop determines the direction of checked win line (both diagonal, vertical and horizontal).
		Second loop determines the number of checks of win line in certain direction.
		Third loop checks, if there is proper count of symbols in the line in the certain direction.
		"""
		for const1,const2 in ((1,1),(1,-1),(1,0),(0,1)):
			for i in range(1,self.line+1):
				try_set=set()
				for j in range(-self.line+i,0+i):
					if y_coord+j*const2<0 or x_coord+j*const1<0:
						try_set=set()
						break
					else:
						try:
							try_set.add(self.stuff[x_coord+j*const1][y_coord+j*const2])
							if len(try_set)>1:
								try_set=set()
								break
						except IndexError:
							try_set=set()
							break
				if len(try_set)==1:
					return True

	def main(self):

		print("""
		Welcome in Tic Tac Toe game!
		============================
		In this game you can set a lot of options, but if you want 
		to play classical Tic Tac Toe, just 'enter' everything.

		Have fun!
		""")

		print("\nLet's start a game!\n===================\n")
		battle.board_Frame(self.x,self.stuff)

		count=0
		end=True
		while end:
			for i,j in self.list_of_players.items():
				print("\nPlayer '{}':".format(j))
				coo_x,coo_y=play.turn1(j)
				battle.board_Frame(self.x,self.stuff)
				if play.winwin(int(coo_x),int(coo_y)):
					print("Player {} win! Congratulation!".format(j))
					end=False
					break
				count+=1
				if count==self.x*self.y: #Counter terminates the game in case, when all cells are filled.
					print("It's a draw.")
					end=False
					break		

battle=Battlefield()
play=Gameplay()
play.main()


