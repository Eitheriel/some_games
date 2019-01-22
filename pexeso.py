import os
import random
import string
import time

class Battlefield():

	def dimension(self,text,x,y,num):
		"""Returns integer representing variable value according to the text in input."""
		while True:
				dim=input("Please enter the {}, between {} and {}. Press enter and {} will be set. ".format(text,x,y,num))
				if dim=="":
					return num 
				try:
					if int(dim) not in range(x,y+1,2):
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

class Gameplay():
	"""
	Return list of strings, which represent different symbols on pexeso cards.
	every symbol has a identic double in the list and the order of symbols in the list is shuffled.

	"""

	def __init__(self,win,win_count):
		self.win=win
		self.win_count=win_count

	def riddle(self,x):
		riddle_list=[]
		index1=int((x**2)/2)
		string1=list(string.ascii_letters)
		random.shuffle(string1)

		for i in string1[0:index1]:
			riddle_list.extend(("({})".format(i),"({})".format(i))) if i.islower() else riddle_list.extend(("[{}]".format(i),"[{}]".format(i)))
		random.shuffle(riddle_list)
		return riddle_list


	def round(self,stuff1,riddle1,x):
		"""
		Return  a) integer - number of card selected by player,
				b) integers - coordinates of the selected card on the battlefield
		"""

		while True:
			try:
				turn_input=int(input("Please enter the number of the card you want to reveal: "))
				
				coordinate1=int((turn_input-0.5)//x)
				coordinate2=(turn_input%x)-1 if turn_input%x!=0 else x-1 
				
				if turn_input not in range (1,(x*y)+1):
					print("\nYou may enter numbers only in range from 1 to {}.".format(x*y))
					continue
				if stuff1[coordinate1][coordinate2]!= turn_input:
					print("\nThis cell is already empty or chosen, try another.")
					continue
				else:
					stuff1[coordinate1][coordinate2]=riddle1[turn_input-1]
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
		if riddle[num_imput_1-1]==riddle[num_input_2-1]:
			stuff[num_coord_1x][num_coord_1y]=stuff[num_coord_2x][num_coord_2y]=" "
			print("Player no. {} gains a point!".format(player_number))
			return 1
		else:
			stuff[num_coord_1x][num_coord_1y]=num_imput_1
			stuff[num_coord_2x][num_coord_2y]=num_input_2
			return 0

	def win_score(self,player_number,win,points):
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
		battle.board_Frame(x,stuff)
		turn_a=game.round(stuff,riddle,x)
		clear()
		return turn_a

	def turn(self,i,win_count):
		"""
		Return integer, which signals, that all pairs of cards has been revealed and game ends.
		Prints informations about final score: who won and how many points each player achieved.
		"""
		turn_a=game.half_turn(i,"first")
		turn_b=game.half_turn(i,"second")

		print("\nPlayer {}'s second move:".format(i))
		battle.board_Frame(x,stuff)
		
		win_point=game.reveal(i,turn_a,turn_b)
		self.win_count+=win_point
		win_message=game.win_score(i,self.win,win_point)
		time.sleep(2)
		clear()

		if win_point==1 and self.win_count!=(x**2)/2: return game.turn(i,self.win_count)
		elif win_point==1 and self.win_count==(x**2)/2:
			print("\nPlayer {}'s second move:".format(i))
			battle.board_Frame(x,stuff)		
			
			print("\nPlayer 1 has {} point(s).\nPlayer 2 has {} point(s).\n{}\n{} wins!".format(win_message[1],win_message[2],25*"-",win_message[0]))
			return 0


	def clear1(self):
		try:
			clear2=lambda: os.system('cls')
			return clear2
		except:
			clear2=lambda: os.system('clear')
			return clear2


	def main(self):
		"""
		Main function of the game. Recursive function repeat itself until all cards are revealed.
		"""
		while True:
			for i in range(1,3): 
				if game.turn(i,self.win_count)==0: return None
		# return game.main()


battle=Battlefield()
x=y=battle.dimension("size of battlefield (only even numbers)",2,10,8)
stuff=battle.board_Stuffing(x,y)
# clear=game.clear()

game=Gameplay(["",0,0],0)
riddle=game.riddle(x)
clear=game.clear1()
# clear=lambda: os.system('cls')
# clear()

# win=["",0,0]
# win_count=0
game.main()


