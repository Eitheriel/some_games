class Battlefield():

	def dimension(self,text,x,y,num):
		"""Returns integer representing variable value according to the text in input."""
		while True:
				dim=input("Please enter the {}, between {} and {}. Press enter and {} will be set. ".format(text,x,y,num))
				if dim=="":
					return num 
				try:
					if int(dim) not in range(x,y+1):
						print("\nYou must enter the proper number.")
						continue
					else:
						return int(dim)
				except ValueError:
					print("\nYou must enter the proper number.")
					continue

	def adjust_line(self,x,y):
		"""
		Returns integer representing the length of line of the same symbols, which is needed for winning the game.
		The returning number is adjusted according to the size of battlefield to ensure of win possibility.
		"""

		if x==3 or y==3: return 3
		if x==4 or y==4: return 4
		if x>=5 or y>=5: return battle.dimension("length of line",3,5,3)



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

	def board_Frame(self,x,stuffing):
		"""
		Return graphical frame of cells of battlefield according to the number of cells.
		"""

		horizontal_wall="-"*4*x+"-"
		vertical_wall="|"+x*"{:^3}|"
		print(horizontal_wall)
		for i in stuffing:
			print(vertical_wall.format(*(i)))
			print(horizontal_wall)


class Player(Battlefield):

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


class Gameplay():

	def turn1(self,stuff1,x,y,symbol):
		"""
		Replace the order number of cell with the specific symbol of player. 
		Returns coordinates of number the player want to replace for his/her symbol.
		It also controls, if the chosen cell is already taken.
		"""

		while True:
			try:
				turn_input=int(input("Please enter the number of the cell you want to put your symbol: "))
				
				coordinate1=int((turn_input-0.5)//x)
				coordinate2=(turn_input%x)-1 if turn_input%x!=0 else x-1 
				
				if turn_input not in range (1,(x*y)+1):
					print("\nYou may enter numbers only in range from 1 to {}.".format(x*y))
					continue
				if stuff1[coordinate1][coordinate2]!= turn_input:
					print("\nThis cell is already taken, try another.")
					continue
				else:
					stuff1[coordinate1][coordinate2]=symbol
					return coordinate1,coordinate2
					break
			except ValueError:
				print("\nPlease try again.")
				continue

	def winwin(self,line1,stuff,x_coord,y_coord):
		"""
		Controls, if player created the line of same symbols of the given length on the battlefield. If yes, it returns True.

		First for loop determines the direction of checked win line (both diagonal, vertical and horizontal).
		Second loop determines the number of checks of win line in certain direction.
		Third loop checks, if there is proper count of symbols in the line in the certain direction.
		"""
		for const1,const2 in ((1,1),(1,-1),(1,0),(0,1)):
			for i in range(1,line1+1):
				try_set=set()
				for j in range(-line1+i,0+i):
					if y_coord+j*const2<0 or x_coord+j*const1<0:
						try_set=set()
						break
					else:
						try:
							try_set.add(stuff[x_coord+j*const1][y_coord+j*const2])
							if len(try_set)>1:
								try_set=set()
								break
						except IndexError:
							try_set=set()
							break
				if len(try_set)==1:
					return True

print("""
Welcome in Tic Tac Toe game!
============================
In this game you can set a lot of options, but if you want 
to play classical Tic Tac Toe, just 'enter' everything.

Have fun!
""")

battle=Battlefield()
x=battle.dimension("number of columns",3,20,3)
y=battle.dimension("number of rows",3,20,3)
line=battle.adjust_line(x,y)
stuff=battle.board_Stuffing(x,y)

player_info=Player()
num_of_players=player_info.dimension("number of players",2,3,2)
list_of_players=player_info.symbol(num_of_players,"X","O","#")

play=Gameplay()

print("\nLet's start a game!\n===================\n")
battle.board_Frame(x,stuff) # Create the overview of battlefield.

count=0
end=True
while end:
	for i,j in list_of_players.items():
		print("\nPlayer '{}':".format(j))
		coo_x,coo_y=play.turn1(stuff,x,y,j)
		battle.board_Frame(x,stuff)
		if play.winwin(line,stuff,int(coo_x),int(coo_y)):
			print("Player {} win! Congratulation!".format(j))
			end=False
			break
		count+=1
		if count==x*y: #Counter terminates the game in case, when all cells are filled.
			print("It's a draw.")
			end=False
			break





