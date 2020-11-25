import random
import time
from IPython.display import clear_output

class Deck():
	def __init__(self):
		self.deck = {"nums" : ["A", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "K", "Q"],
					 "suit" : ['♠', '♣', '♥', '♦']}
		self.used_cards = []

class Hand():
	def __init__(self):
		self.cards = [("A", '♣'), ("A", '♦')]
		self.busted = False
		self.score = 0

	def getScore(self):
		score = 0
		aces = 0
		
		for card in self.cards:
			if isinstance(card[0], int):
				score += card[0]
			elif card[0] in "KQJ":
				score += 10
			else:
				score += 11
				aces += 1
		while score > 21 and aces > 0:
			score -= 10
			aces -= 1
		self.score = score  #This updates the self.score of the player
		return score         #This gives a value that can be printed for the user's sake

	def bust(self):
		if self.score > 21:
			self.busted = True
			print("This hand busted!")
			return True
		return False #This will return a Bool, can be used to break out of the game
		
class Player(Deck):

	def __init__ (self):
		Deck.__init__(self) #Is this right?
		self.hands = [Hand()]
		#I'll need to make self.hand a list of lists to enable multiple hands for splitting
		self.score = 0
		self.curHand = 0
		self.busted = False
	#Create a constructor for the player class that will hold the hand,cards,and tally the score

	def deal(self):
		while len(self.hands[0].cards) < 2:
			card = (random.choice(self.deck["nums"]), random.choice(self.deck["suit"]))
			if card not in self.used_cards:
				self.hands[0].cards.append(card)
				self.used_cards.append(card)
	
	def hitPlayer(self):
		stillNeedsCard = True
		while stillNeedsCard:
			card = (random.choice(self.deck["nums"]), random.choice(self.deck["suit"]))
			if card not in self.used_cards:
				self.hands[self.curHand].cards.append(card)
				print(str(card[0]) + card[1])
				stillNeedsCard = False

	def checkBusted(self):
		if len(self.hands) == 1 and self.hands[0].busted:
			self.busted = True
			# return True
		else:
			self.busted = all([hand.busted for hand in self.hands])
			# return self.busted

	def getScore(self):
		self.score = max([hand.getScore() for hand in self.hands])
		return self.score

				
	# Get total score based on the hand the user/player is given

class Human(Player):

	def __init__(self, name, blackJackBool = False):
		Player.__init__(self)
		self.name = name #I should move this (and the dealer's name) up to Player class
		self.blackJackBool = blackJackBool
		# self.hands = [[('A', '♠'), ('A', '♣')]] #Start with a split for now

	def deal(self, hand_index):
		while len(self.hands[hand_index].cards) < 2:
			card = (random.choice(self.deck["nums"]), random.choice(self.deck["suit"]))
			if card not in self.used_cards:
				self.hands[hand_index].cards.append(card)
				self.used_cards.append(card)
		self.showHandPlayer()
		self.promptSplit(hand_index) #We need to show all hands before prompting to split.
	
	def promptSplit(self, hand_index):
		for hand in range(len(self.hands)): #Should I be using a queue or stack?
			if self.hands[hand_index].cards[0][0] == self.hands[hand_index].cards[1][0]:
				stillNeedsToChoose = True
				while stillNeedsToChoose:
					time.sleep(0.5)
					choice = input("Would you like to split your hand? (y/n)").lower()
					if choice == 'y' or choice == 'n':
						stillNeedsToChoose = False
				if choice == 'y':
					self.split(hand_index) # May need to pass in a hand here

	def split(self, hand_index):
		#Take each card and make each one the first card of a hand, the original hand and a new hand.
		self.hands.append(Hand())
		card_1 = self.hands[hand_index].cards[0]
		card_2 = self.hands[hand_index].cards[1]
		self.hands[hand_index].cards = [card_1]
		self.hands[-1].cards = [card_2] # The last hand in self.hands, in case you're looking at the first of two
		#hands which both need to be split, you don't overwrite a hand.
		self.deal(hand_index)
		self.deal(-1)

	# def getScore(self):
	# 	score = 0
	# 	aces = 0
		
	# 	for card in self.hands[self.curHand]:
	# 		if isinstance(card[0], int):
	# 			score += card[0]
	# 		elif card[0] in "KQJ":
	# 			score += 10
	# 		else:
	# 			score += 11
	# 			aces += 1
	# 	while score > 21 and aces > 0:
	# 		score -= 10
	# 		aces -= 1
	# 	self.score = score  #This updates the self.score of the player
	# 	return score         #This gives a value that can be printed for the user's sake
	
	def blackJack(self):
		if self.getScore() == 21:
			print(f"{self.name} got Blackjack!!!")
			self.blackJackBool = True
			
	def showHandPlayer(self):
		time.sleep(0.5)
		if len(self.hands) == 1:
			print('Here is your hand:')
			for card in self.hands[0].cards:
				print(str(card[0]) + card[1])
		else:
			print('Here are your hands:')
			for hand in range(len(self.hands)):
				time.sleep(1)
				print(f'Hand #{hand + 1}: ')
				for card in self.hands[hand].cards:
					print(str(card[0]) + card[1])
				
				
class Dealer(Player):

	def __init__(self, name):
		Player.__init__(self)
		self.name = "Dealer"
				
	def showHand(self):
		print("Dealer's face-up card:")
		print(str(self.hands[self.curHand].cards[0][0]) + self.hands[self.curHand].cards[0][1])
		
	def showHandEnd(self):
		print("Here is the dealer's hand:")
		for card in self.hands[self.curHand].cards:
			print(str(card[0]) + card[1])
	

class Game(Dealer, Human):

	#Define a constructor that will have a dealer,human,and players(the dealer and the human)
	def __init__(self, name):
		Dealer.__init__(self, name)
		Human.__init__(self, name)
		self.name = name
	
	#Define a method to display a message if the user/player wins
	# def winner(self):
		# if human_player.busts or dealer_player.score > human_player.score:
		#     print(dealer_player.name + ' wins!')
		# elif dealer_player.busts or human_player.score > dealer_player.score:
		#     print(human_player.name + ' wins!')
		# else:
		#     print('This hand was a tie.')
			  
	#Define a method to display a message if the user/player pushes

			  
	#Define a method to display a message if the user/player loses    

	
wanthit = 'y'
def main():
	human_player = Human(input("What is Your Name? "))
	dealer_player = Dealer('Dealer')
	game = Game('Tuesday')
			  
	#Ask the player how many decks they want to use - Then print the number of decks
	human_player.deal(human_player.curHand)
	dealer_player.deal()
	if len(human_player.hands) == 1:
		human_player.showHandPlayer()
	human_player.blackJack() #Make sure game ends
	if not human_player.blackJackBool:
		dealer_player.showHand()
	for _ in range(len(human_player.hands)):
		wanthit = 'y'
		while not human_player.busted and wanthit == 'y' and not human_player.blackJackBool: #Player's hits
			if human_player.curHand >= 1:
				human_player.showHandPlayer()
				print(f'Moving on to hand #{human_player.curHand + 1}!')
			wanthit = input('Would you like to take a hit? (y/n) ')
			if wanthit.lower() == 'y':
				human_player.hitPlayer()
				human_player.getScore()
				human_player.hands[human_player.curHand].bust()
				human_player.checkBusted()

		human_player.curHand += 1
	if dealer_player.getScore() < 17 and not human_player.busted and not human_player.blackJackBool:
		print('Dealer takes a hit!')
		dealer_player.hitPlayer()
		dealer_player.getScore()
		dealer_player.hands[0].bust()
		dealer_player.checkBusted()
	dealer_player.showHandEnd()
	if not human_player.busted:
		print(f'{human_player.name} had a score of {str(human_player.score)}')
	if not dealer_player.busted:
		print(f'{dealer_player.name} had a score of {str(dealer_player.score)}')
	if human_player.busted or (dealer_player.score > human_player.score and not dealer_player.busted):
		print(f'{dealer_player.name} wins!')
	elif dealer_player.busted or (human_player.score > dealer_player.score and not human_player.busted):
		print(f'{human_player.name} wins!')
	else:
		print('This hand was a tie.')

main()