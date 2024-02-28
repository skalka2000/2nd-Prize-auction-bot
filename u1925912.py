
import random
import math

class Bot(object):

    def __init__(self):
        self.name = "1925912" # Put your id number her. String or integer will both work
        # Add your own variables here, if you want to. 

    def get_bid(self, current_round, bots, artists_and_values, round_limit,
            starting_budget, painting_order, my_bot_details, current_painting, winner_ids, amounts_paid):
        
        """Strategy for value type games. 

        Parameters:
        current_round(int):             The current round of the auction game
        bots(dict):                     A dictionary holding the details of all of the bots in the auction
                                        Includes what paintings the other bots have won and their remaining budgets
        artists_and_values(dict):        A dictionary of the artist names and the painting value to the score (for value games)
        round_limit(int):                Total number of rounds in the game
        starting_budget(int):            How much budget each bot started with
        painting_order(list str):        A list of the full painting order
        my_bot_details(dict):            Your bot details. Same as in the bots dict, but just your bot. 
                                        Includes your current paintings, current score and current budget
        current_painting(str):            The artist of the current painting that is being bid on
        winner_ids(list str):            List of which bots have won the rounds so far, in round order
        amounts_paid(list int):            List of amounts paid for paintings in the rounds played so far 

        Returns:
        int:Your bid. Return your bid for this round. 
        """

        # WRITE YOUR STRATEGY HERE - MOST VALUABLE PAINTINGS WON WINS
        

        # Here is an example of how to get the current painting's value
        current_painting_value = artists_and_values[current_painting]

        # get the number of bots
        num_bots=len(bots)
        #convert the list containing the order of artists sold
        #to lists with paintings values
        painting_order_value=[]
        left_paintings_values=[]
        sold_paintings_values=[]
        i1=0
        for artist in painting_order:
            painting_order_value.append(artists_and_values[artist])
            if i1>=current_round:
                left_paintings_values.append(artists_and_values[artist])
            else:
                sold_paintings_values.append(artists_and_values[artist])
            i1 += 1
        #sum the paintings values
        total_paintings_value=sum(painting_order_value)
        total_left_paintings_value=sum(left_paintings_values)
        total_sold_paintings_value=sum(sold_paintings_values)
        #calculate the predicted budget spent or left at each round
        #this is based on the assumpton that the budget should is allocated uniformly 
        #across all painting value units
        #for Van Gogh (12) I will predict to spend 6 times more than on Picasso (2)
        predicted_personal_budget_spent=starting_budget*(total_sold_paintings_value/(total_left_paintings_value+total_sold_paintings_value))
        predicted_personal_budget_left=starting_budget-predicted_personal_budget_spent
        #calculate the total remaining budget for all bots 
        total_remaining_budget=0
        for bot in bots:
            total_remaining_budget += bot['budget']
        #calculate my remaining budget
        my_budget = my_bot_details["budget"]

        #other_bots_remaining_budget=total_remaining_budget-my_budget
        #total_spent_budget=num_bots*starting_budget-total_remaining_budget
        ##if ratio_remaining_budget is lower than 1: it means people have spent more than predicted
        ##therefore overbidding
        ##if higher than 1 underbidding
        ##define ratio to make the of 1 painting value equal to 1 dollar:
        #ratio_remaining_budget = total_remaining_budget/(predicted_personal_budget_left*(num_bots-1))

        #define total budget in the game across all bots
        total_budget = starting_budget*num_bots
        #suppose that all the money is spent in 200 rounds
        #this is how much money (on average) a single unit of painitng value will be worth 
        unit_worth = total_budget/total_paintings_value
        #define budget_ratio and score_ratio
        for bot in bots:
            #budget ratio would be the ratio between the remaining budget of the bot
            #to the budget that the bot is predcited to have at this stage of the auction
            #if the ratio is bigger than 1 it means that the particular bot
            #has relatively more budget to spend than the running prediction suggests
            #and has therefore already spent less money than it would be predicted of it
            #there is a threshold set at 3 and is usually crossed
            #while half of the auctions have already passed and no money has been spent by a bot
            #this is done to account for the bots, who bid lowly 
            bot['budget_ratio'] = min(bot['budget']/(predicted_personal_budget_left+0.01),3)
            #division by zero error adjustment, when zero budget has been spent by a bot:
            #make the score_ratio equal to the ratio between the predicted total budget left
            #and actual remaining total budget left.
            #if this ratio is greater than 1, it means other bots have been over-bidding so far
            # and therefore not bidding in previous rounds should mean that the bot is winning by comparisoon  
            #this is accounted for the very late bidders who are not likely to end with a high score
            #even if they started winning good portion of the total remaining budget
            if (starting_budget-bot['budget'])==0:
                bot['score_ratio']=min(predicted_personal_budget_left*num_bots/(total_remaining_budget+0.01),
                total_left_paintings_value*unit_worth/(total_remaining_budget+0.01))
            #score_ratio is calculated by obtaining the ratio between the obtained score 
            # and the money spent, adjusted by the unit worth defined earlier
            #the higher it is, the better's bot performance so far:
            # the more score it gained out of all the money spent so far
            # the score is adjusted to account for bots who bid late on:
            # they may buy the paintings for a relatively good price
            #but they are not likely to get a high score at the end of the game
            #because there are not many paintings left to buy
            else:
                bot['score_ratio']=min(bot['score']*unit_worth/(starting_budget-bot['budget']),
                                       (bot['score']+total_left_paintings_value*bot['budget']/(total_remaining_budget+0.01))*unit_worth      /starting_budget)
                

        #we update my_bot_details dictionary in the same way

        my_bot_details['budget_ratio'] = min(my_bot_details['budget']/(predicted_personal_budget_left+0.01),2)
        if (starting_budget-my_bot_details['budget'])==0:
            my_bot_details['score_ratio']=min(predicted_personal_budget_left*num_bots/(total_remaining_budget+0.01),
                total_left_paintings_value*unit_worth/(total_remaining_budget+0.01))
        else:
            my_bot_details['score_ratio']= min(my_bot_details['score']*unit_worth/(starting_budget-my_bot_details['budget']),
                                               (my_bot_details['score']+total_left_paintings_value*my_bot_details['budget']/(total_remaining_budget+0.01))*unit_worth      /starting_budget)


        #calculate the scores_budget_ratio 
        #if budget_ratio is low it means a particular bot will not spend much money in the remaining rounds
        #that is because it has already spent too much money in the previous rounds
        #if the scores_ratio is low it means a particular bot is likely to be performing badly
        #they have either under-bid or over-bid in the previous rounds. 
        #budget_ratio and score_ratio^k are multiplied together. Score_ratio is taken to the power of k
        #to better detect the bots performing badly. The root rs is taken from the score_budget_ratio
        # of well-perforiming bots to make sure we do not overestimate their significance 
        scores_budget_ratio=0
        k=3
        rs=0.25
        for bot in bots:
            if bot['budget_ratio']*bot['score_ratio']**k<1:
                scores_budget_ratio+=bot['budget_ratio']*bot['score_ratio']**k
            else:
                scores_budget_ratio+=(bot['budget_ratio']*bot['score_ratio']**k)**rs
        #we should not care about my score_budget_ratio as we do not want our potentially lower score_ratio
        #to result in a lower bid (on the contrary!)
        if my_bot_details['budget_ratio']*my_bot_details['score_ratio']**k>1:
             scores_budget_ratio=scores_budget_ratio-(my_bot_details['budget_ratio']*my_bot_details['score_ratio']**k)**rs
        else:
            scores_budget_ratio=scores_budget_ratio-(my_bot_details['budget_ratio']*my_bot_details['score_ratio']**k)
        if 1>scores_budget_ratio>my_bot_details['budget_ratio']*my_bot_details['score_ratio']**k:
            scores_budget_ratio=num_bots-1

        #prints the particular things from the bot dictionary every 20 rounds
        if (current_round+1)%20==0:
            for bot in bots:
                print('name:',bot['bot_name'],
                      ', score:',bot['score'],
                        ', budget:', round(bot['budget'],2),
                        ', score_ratio:',round(bot['score_ratio'],2),
                        ', budget_ratio:',round(bot['budget_ratio'],2))
        #calculate the bid of my bot
        #aim for the true value
        bid1=round((scores_budget_ratio+1)*my_budget*current_painting_value/total_left_paintings_value,0)
        print(bid1)
        #determine the bid that my bot would place if the current painting was of value 12 (Van Gogh) 
        bid2=round((scores_budget_ratio+1)*my_budget*12/total_left_paintings_value,0)
        #make sure the bot does not spend all its money in the first rounds
        #we want to make sure bidding is more uniformly distributed across all rounds
        #to see what the tendency of the bots is before we spend most of our money
        if current_round<50:
            if (my_budget-bid2)<0.9*predicted_personal_budget_left:
                bid1=round(bid1*0.7,0)
        elif current_round<100:
            if (my_budget-bid2)<0.8*predicted_personal_budget_left:
                bid1=round(bid1*0.8,0)
        else:
            if (my_budget-bid2)<0.7*predicted_personal_budget_left:
                bid1=round(bid1*0.95,0)
        bid=min(bid1,my_budget)
        print(bid)
        return bid

