## Matthew Conroy 2017
##
##
## A simulation of the game No Thanks!
## see https://en.wikipedia.org/wiki/No_Thanks!_(game)
##
##
import itertools,random

class Player:

	def __init__(self, tokens, cards):
		self.tokens = tokens
		self.cards = cards

class GameState: # I don't actually use this class!!!

	def __init__(self, tokens, card): ## the current state of the game is the number of tokens on the
		self.tokens = tokens          ## current card, and which card is current
		self.card = card

numberOfPlayers = 4 ## the number of players
numberOfGames = 1000000
alpha = 17   ## fixed alpha values for all players in order for testing advanced strategy
total_c = []

token_thresh = [2]
card_thresh = range(34,35)

for t in card_thresh: 
	for l in token_thresh: 
		conf = []
		for k in range(10): 
			wins=[] # array to keep track of how many times each player wins
			for i in range(numberOfPlayers):
				wins.append(0)

			for game in range(numberOfGames): ## main game loop
				save = set()
				### prepare the deck for a game
				# generate the deck
				deck = list(range(3,36))
				# shuffle the cards
				random.shuffle(deck)
				#remove 9 cards
				deck = deck[:-9]


				### initialize players array
				# Each player needs two things: an integer indicating how many
				# tokens they have, and a list of the cards they have

				players=[]
				for i in range(numberOfPlayers):
					players.append(1)

				# initialize each player with 11 tokens and an empty list of cards

				for i in range (numberOfPlayers):
					players[i] = Player(11,[])


				#### start playing

				currentPlayer = game % numberOfPlayers ## start with a different player each time
				cardIndex = 0 # start at one end of the deck of cards
				currentTokens = 0 # initially there are no tokens on the current card
				while(cardIndex<24):
					currentCard = deck[cardIndex]
					## currentPlayer either adds a token, or takes the card
					if (currentPlayer in [0]):
						cardThresh=alpha
						# this next conditional statement is the strategy for this/these players:
						# pick up the card if (1) it is adjacent to a card the player already has, or
						# (2) currentCard-currentTokens<cardThresh, so the number of tokens offsets the points of the cards sufficiently, or
						# (3) the player has no tokens

						# additional strategy: 	if the card is large enough and cost nothing to pick, 
						# 						then don't pick until there are at least x tokens on that card
												# TODO: use constant
												# TODO: test this, 先找currentTokens的最best的值，再固定第二个，找cardThresh2的best值

						# if ((currentCard+1 in players[currentPlayer].cards or currentCard-1 in players[currentPlayer].cards) \
						# 	and currentCard>=cardThresh2 and currentTokens < 0.2*currentCard and players[currentPlayer].tokens!=0 ): 
						if ((currentCard+1 in players[currentPlayer].cards or currentCard-1 in players[currentPlayer].cards) \
							and currentCard>=t and currentTokens < 1 and players[currentPlayer].tokens!=0 ): 
							# if the card is large enough, and there are fewer than 3 tokens on that card, and the player has remaining tokens 
							## currentPlayer adds a token to the card
							currentTokens = currentTokens + 1
							players[currentPlayer].tokens=players[currentPlayer].tokens-1
							save.add(currentCard)
						elif ((currentCard+1 in players[currentPlayer].cards) or (currentCard-1 in players[currentPlayer].cards) \
							or (currentCard-currentTokens<cardThresh) or (players[currentPlayer].tokens==0)):
							## currentPlayer takes the card and the tokens, if any
							players[currentPlayer].tokens = players[currentPlayer].tokens+currentTokens
							players[currentPlayer].cards.append(currentCard)
							cardIndex=cardIndex+1 ## get ready to turn over the next card
							currentTokens=0
						else:
							## currentPlayer adds a token to the card
							currentTokens = currentTokens + 1
							players[currentPlayer].tokens=players[currentPlayer].tokens-1

					if (currentPlayer in [1,2,3]):
						cardThresh=alpha
						# this next conditional statement is the strategy for this/these players:
						# pick up the card if (1) is a adjacent to a card the player already has, or
						# (2) currentCard-currentTokens<cardThresh, so the number of tokens offsets the points of the cards sufficiently, or
						# (3) the player has no tokens
						if ( (currentCard+1 in players[currentPlayer].cards) or (currentCard-1 in players[currentPlayer].cards) or
						(currentCard-currentTokens<cardThresh) or (players[currentPlayer].tokens==0)):
						## currentPlayer takes the card and the tokens, if any
							players[currentPlayer].tokens = players[currentPlayer].tokens+currentTokens
							players[currentPlayer].cards.append(currentCard)
							cardIndex=cardIndex+1 ## get ready to turn over the next card
							currentTokens=0
						else:## currentPlayer adds a token to the card
							currentTokens = currentTokens + 1
							players[currentPlayer].tokens=players[currentPlayer].tokens-1

					# next players turn
					currentPlayer = (currentPlayer+1) % numberOfPlayers

				## game is over!
				c = 0
				save = list(save)
				for i in save: 
					if i in players[0].cards: 
						c += 1
				if len(save) != 0: 
					total_c.append(c/len(save))
				## calculate the players' scores

				# initialize score array
				scores=[]
				for i in range(numberOfPlayers):
					scores.append(1)

				minScore = 0 # clear minScore
				for i in range(numberOfPlayers):
					# calculate player i's score, find minimum score
					scores[i] = -players[i].tokens # start by subtracting the tokens
					players[i].cards.sort() # put the cards list in increasing order
					for j in range(len(players[i].cards)):
						# the lowest cards count, and all other cards count only if they are not one more
						# than the previous cards in the list
						if( (j==0)  or (players[i].cards[j-1]!=players[i].cards[j]-1)):
							scores[i] = scores[i]+players[i].cards[j]
					if ((scores[i]<minScore) or (i==0)):
						minScore = scores[i]
				numWithMinScore=0
				for i in range(numberOfPlayers):
					# count number of players with minimum score
					if (scores[i]==minScore):
						numWithMinScore += 1
				# if a tie, each tying player gets an equal fraction of the win (i.e., if two tie, they each get 0.5, etc.)
				for i in range(numberOfPlayers):
					if (scores[i]==minScore):
						wins[i] += 1./numWithMinScore

				# print out current estimated win probability for player zero every so often
				# if ((game % 10000==0) and (game>0)):
				# 	print(f'Current total game: {game}, player 0 wins: ', wins[0]*1./game)
					#print game
					#for jj in range(numberOfPlayers):
					#	print jj," ",wins[jj]*1./game
			conf.append(wins[0]*1./numberOfGames)
		## output winning wins for all the players
		print(f'threshold of current card: {t}')
		print(f'threshold of current Tokens: {l}')
		print('Min and Max: ', [min(conf), max(conf)])
		# print('Percentage of getting the declined card in the end', sum(total_c)/len(total_c))