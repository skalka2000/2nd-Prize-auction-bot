
# Import the auctioneer, to run your auctions
from auctioneer import Auctioneer

# Import some bots to play with
# We have given you some basic bots to start with in the bots folder
# You can also add your own bots to test against
from bots import flat_bot_10
from bots import random_bot
from bots import flat_bot_20
from bots import flat_bot_50
from bots import flat_bot_100
from bots import exact_value_2
from bots import exact_value_3
from bots import exact_value_4
from bots import my_budgets 
from bots import all_budgets
from bots import random_choice_bot
from bots import personal_budget
from bots import score_budget
from bots import score_budget_3
from bots import score_budget_4
from bots import u1925912
from bots import true_value
from bots import remaining_budget
from bots import true_value_late
import random

#random.seed(20)
all_bots=[true_value,
	  true_value_late, 
	  flat_bot_20, 
	  flat_bot_50, 
	  flat_bot_100,
	  exact_value_2, 
	  exact_value_3,
	  exact_value_4,
	  random_choice_bot]
#the random room
#room1=[1925912, random_choice_bot, random_bot, random_bot]
#the true value 1v1
#room1=[1925912,true_value]
#remaining budget 1v1
#room1=[1925912,remaining_budget]
#exact value 2 1v1
#room1=[1925912,exact_value_2]
#exact value 3 1v2
#room1=[1925912,exact_value_3,exact_value_4]



#initialize 5 random rooms with different sizes:
#5 bots room:
#room1=[1925912,exact_value_3,exact_value_4,all_bots[random.randint(0,9)],all_bots[random.randint(0,9)]]
#6 bots room:
#room1=[1925912, exact_value_3,exact_value_4,all_bots[random.randint(0,8)],all_bots[random.randint(0,8)],all_bots[random.randint(0,9)]]
#7 bots room:
#room1=[1925912,exact_value_3,exact_value_4,all_bots[random.randint(0,8)],all_bots[random.randint(0,8)],all_bots[random.randint(0,8)],all_bots[random.randint(0,8)]]
#8 bots room
#room1=[1925912,exact_value_3,exact_value_4,all_bots[random.randint(0,8)],all_bots[random.randint(0,8)],all_bots[random.randint(0,8)],all_bots[random.randint(0,8)],all_bots[random.randint(0,8)]]
#9 bots room
room1=[u1925912,exact_value_3,exact_value_4,all_bots[random.randint(0,8)],all_bots[random.randint(0,8)],all_bots[random.randint(0,8)],all_bots[random.randint(0,8)],all_bots[random.randint(0,8)],all_bots[random.randint(0,8)]]
#the hard room
#room1=[1925912, true_value, flat_bot_50,exact_value_3, flat_bot_100, flat_bot_20, exact_value_4, true_value_late]
#the idiot room
#room1=[1925912,flat_bot_50, exact_value_3 , exact_value_3, exact_value_2, exact_value_2, random_choice_bot, random_choice_bot]
def run_basic_auction():

	# Setup a room of bots to play against each other, imported above from the bots folder
	room = room1
	# Setup the auction
	my_auction = Auctioneer(room=room,slowdown=0)
	# Play the auction
	my_auction.run_auction()


def run_lots_of_auctions():
	"""
	An example if you want to run alot of auctions at once
	"""
	# A large room with a few bots of the same type
	room = room1
	
	win_count = 0
	run_count = 20
	for i in range(run_count):
		# Setup the auction
		# slowdown = 0 makes it fast
		my_auction = Auctioneer(room=room, slowdown=0)
		# run_auction() returns a list of winners, sometimes there are more than one winner if there is a tie
		winners = my_auction.run_auction()
		# Check if the bot's name, "my_bot", was a winner 
		if "1925912" in winners:
			win_count +=1
	print("My bot won {} of {} games".format(win_count, run_count))	


if __name__=="__main__":
	#run_basic_auction()
	run_lots_of_auctions()