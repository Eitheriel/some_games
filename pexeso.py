import os
import random
import string
import time

class Battlefield():

	def __init__(self,text,lower_limit,higher_limit,default_num):
		self.text=text
		self.lower_l=lower_limit
		self.higher_l=higher_limit
		self.default_n=default_num
		self.coord_x=self.dimension()
		self.coord_y=self.coord_x
		self.stuff=self.board_Stuffing()

	def dimension(self):
		"""Returns integer representing variable value according to the text in input."""
		while True:
				dim=input("Please enter the {}, between {} and {}. Press enter and {} will be set. ".format(self.text,self.lower_l,self.higher_l,self.default_n))
				if dim=="":
					return self.default_n 
				try:
					if int(dim) not in range(self.lower_l,self.higher_l+1,2):
						print("\nYou must enter the proper number.")
						continue
					else:
						return int(dim)
				except ValueError:
					print("\nYou must enter the proper number.")
					continue

	def board_Stuffing(self):
		"""
		Return the list of list.
		In every list is array of numbers representing each cell of battlefield. 
		The count of numbers in every list is influenced by battlefield proportions.
		"""

		superboard=[]
		num1=1
		for i in range(self.coord_y):
			line=[]
			for j in range(self.coord_x):
				line.append(num1)
				num1+=1
			superboard.append(line)
		return superboard

	def board_Frame(self):
		"""
		Return graphical frame of cells of battlefield according to the number of cells.
		"""

		horizontal_wall="-"*4*self.coord_x+"-"
		vertical_wall="|"+self.coord_x*"{:^3}|"
		print(horizontal_wall)
		for i in self.stuff:
			print(vertical_wall.format(*(i)))
			print(horizontal_wall)

class Gameplay():
	"""
	Return list of strings, which represent different symbols on pexeso cards.
	every symbol has a identic double in the list and the order of symbols in the list is shuffled.

	"""

	def __init__(self,win=["",0,0],win_count=0):
		self.x=battle.coord_x
		self.y=self.x
		self.stuff=battle.stuff
		self.win=win
		self.win_count=win_count
		self.riddle=self.riddle()
		self.clear=self.clear1()

	def riddle(self):
		riddle_list=[]
		index1=int((self.x**2)/2)
		string1=list(string.ascii_letters)
		random.shuffle(string1)

		for i in string1[0:index1]:
			riddle_list.extend(("({})".format(i),"({})".format(i))) if i.islower() else riddle_list.extend(("[{}]".format(i),"[{}]".format(i)))
		random.shuffle(riddle_list)
		return riddle_list


	def round(self):
		"""
		Return  a) integer - number of card selected by player,
				b) integers - coordinates of the selected card on the battlefield
		"""

		while True:
			try:
				turn_input=int(input("Please enter the number of the card you want to reveal: "))
				
				coordinate1=int((turn_input-0.5)//self.x)
				coordinate2=(turn_input%self.x)-1 if turn_input%self.x!=0 else self.x-1 
				
				if turn_input not in range (1,(self.x*self.y)+1):
					print("\nYou may enter numbers only in range from 1 to {}.".format(self.x*self.y))
					continue
				if self.stuff[coordinate1][coordinate2]!= turn_input:
					print("\nThis cell is already empty or chosen, try another.")
					continue
				else:
					self.stuff[coordinate1][coordinate2]=self.riddle[turn_input-1]
					return turn_input,coordinate1,coordinate2
			except ValueError:
				print("\nPlease try again.")
				continue

	def reveal(self,player_number,turn_a,turn_b):
		"""
		Return integer 1 or 0 representing a win point.
		This method is also used for 'revealing' symbols on the back of card and evaluating, if player
		found the pair of same symbols. In case he found a pair, the face of both cards remains blank. 
		In other case the numbers of both cards are comming back.

		""" 
		num_imput_1,num_coord_1x,num_coord_1y=turn_a
		num_input_2,num_coord_2x,num_coord_2y=turn_b
		if self.riddle[num_imput_1-1]==self.riddle[num_input_2-1]:
			self.stuff[num_coord_1x][num_coord_1y]=self.stuff[num_coord_2x][num_coord_2y]=" "
			print("Player no. {} gains a point!".format(player_number))
			return 1
		else:
			self.stuff[num_coord_1x][num_coord_1y]=num_imput_1
			self.stuff[num_coord_2x][num_coord_2y]=num_input_2
			return 0

	def win_score(self,player_number,points):
		"""
		Return string and two integers.
		The string carries the name of winner; integers inform about number of poins, that both players achieved.
		"""
		self.win[player_number]+=points
		if self.win[1]>self.win[2]:
			self.win[0]="Player 1"
			return self.win
		elif self.win[1]<self.win[2]:
			self.win[0]="Player 2"
			return self.win
		else:
			self.win[0]="Nobody"
			return self.win

	def half_turn(self,player_number,turn_num):
		"""
		Return  a) integer - number of card selected by player,
				b) integers - coordinates of the selected card on the battlefield
		This method is same as 'round', but contains some graphical editing of what players can see. 
		"""
		print("\nPlayer {}'s {} move:".format(player_number,turn_num))
		battle.board_Frame()
		turn_a=game.round()
		self.clear()
		return turn_a

	def turn(self,player_num):
		"""
		Return integer, which signals, that all pairs of cards has been revealed and game ends.
		Prints informations about final score: who won and how many points each player achieved.
		"""
		turn_a=game.half_turn(player_num,"first")
		turn_b=game.half_turn(player_num,"second")

		print("\nPlayer {}'s second move:".format(player_num))
		battle.board_Frame()
		
		win_point=game.reveal(player_num,turn_a,turn_b)
		self.win_count+=win_point
		win_message=game.win_score(player_num,win_point)
		time.sleep(2)
		self.clear()

		if win_point==1:
			if self.win_count!=(self.x**2)/2: 
				return game.turn(player_num)
			else:
				print("\nPlayer {}'s second move:".format(player_num))
				battle.board_Frame()		
			
			print("\nPlayer 1 has {} point(s).\nPlayer 2 has {} point(s).\n{}\n{} wins!".format(win_message[1],win_message[2],25*"-",win_message[0]))
			return 0

	def clear1(self):
		"""
		Clear the screen.
		"""
		try:
			clear2=lambda: os.system('cls')
			return clear2
		except:
			clear2=lambda: os.system('clear')
			return clear2

	def main(self):
		"""
		Main function of the game. This method repeat itself until all cards are revealed.
		"""
		while True:
			for i in range(1,3): 
				if game.turn(i)==0: return None

battle=Battlefield("size of battlefield (only even numbers)",2,10,8)
game=Gameplay()
game.main()


