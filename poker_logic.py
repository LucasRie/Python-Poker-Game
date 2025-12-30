import random
from config import *

class Cards:
    def __init__(self):
        self.__vals = [x for x in range(2,11)]
        self.__vals.extend(['Jack','Queen','King','Ace'])


        self.__suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']


    def get_values(self):
        return self.__vals
    
    def get_suits(self):
        return self.__suits


class Deck:
    def __init__(self):
        self.cards = Cards()
        self.deck = []


        self.create_deck()
        self.shuffle_deck()


    def create_deck(self):
        #will loop through each value, then looping through each suit for that value and adding it to an array
        [[self.deck.append([value,suit]) for suit in self.cards.get_suits()] for value in self.cards.get_values()]


    def shuffle_deck(self):
        random.shuffle(self.deck)


        self.shuffled = []
        for val,suit in self.deck:
            self.shuffled.append('The %s of %s' % (val, suit))


    def burn_card(self):
        self.shuffled.pop()


    def deal_hole_cards(self, location):
        for i in range(2):
            location.cards.append(self.shuffled.pop())


    def deal_flop(self):
        self.community_cards = []
        for i in range(3):
            self.burn_card()
            self.community_cards.append(self.shuffled.pop())


    def add_community_cards_to_hand_after_flop(self, location):
        for i in range(3):
            location.cards.append(self.community_cards[i])


    def deal_turn_or_river(self):
        self.burn_card()
        self.community_cards.append(self.shuffled.pop())


    def add_community_card_to_hand_after_turn(self, location):
        location.cards.append(self.community_cards[3])


    def add_community_card_to_hand_after_river(self, location):
        location.cards.append(self.community_cards[4])


class GetTypeOfHand:
    def __init__(self):
        pass


    def converting_to_symbol(self, hand):
        hand_as_symbol = []
        for i in hand:
            info_about_card = i.split()
            if info_about_card[1] == '10':
                card = info_about_card[1][:2] + info_about_card[3][:1]
            else:
                card = info_about_card[1][:1] + info_about_card[3][:1]
            hand_as_symbol.append(card)


        return hand_as_symbol


    def get_suit(self, card):
        return card[-1]
    
    def get_value(self,card):
        if card[0] == 'A':
            return 14
        elif card[0] == 'K':
            return 13
        elif card[0] == 'Q':
            return 12
        elif card[0] == 'J':
            return 11
        return int(card[:-1])
    
    def is_flush(self, hand):
        diamonds, hearts, clubs, spades = 0,0,0,0
        for card in hand:
            if card[-1] == 'D':
                diamonds += 1
            elif card[-1] == 'H':
                hearts += 1
            elif card[-1] == 'C':
                clubs += 1
            else:
                spades += 1


        if diamonds >= 5 or hearts >= 5 or clubs >= 5 or spades >= 5:


            # code to determine what is their highest suited card
            card_vals = []
            if diamonds is max([diamonds, hearts, clubs, spades]):
                suit = 'D'
            elif hearts is max([diamonds, hearts, clubs, spades]):
                suit = 'H'
            elif clubs is max([diamonds, hearts, clubs, spades]):
                suit = 'C'
            else:
                suit = 'S'


            for card in hand:
                if card[-1] == suit:
                    card_vals.append(self.get_value(card))
            self.high_value_flush = max(card_vals)


            return True
        else:
            return False


        
    def hand_dist(self,hand):
        # creates a dictionary of the card values, making it easy to compare how many of each value there are
        dist = {value:0 for value in range(1,15)}
        for card in hand:
            dist[self.get_value(card)] += 1


        # the ace can be used as both values 1 or 14 for straights
        dist[1] = dist[14]


        return dist
    
    # returns the value of the high card in a straight if the hand is a straight
    def straight_high_card(self, hand):
        dist = self.hand_dist(hand)
        for value in range (1,11):
            if all([dist[value + k] >= 1 for k in range(5)]):
                return value + 4
        return None
    
    # returns the value of a 'num' of a kind, that is not of value 'but' 
    def card_counter(self, hand, num, but = None):
        dist = self.hand_dist(hand)
        for value in reversed(range(2,15)):
            if value == but:
                continue
            elif dist[value] == num:
                return value
        return None


    def high_card(self, hand, but = None):
        dist = self.hand_dist(hand)
        for value in range(2,15):
            if dist[value] >= 1 and value != but:
                high = value
        
        return high
    
    def get_hand_rank(self, cards):
        hand = self.converting_to_symbol(cards)
        if self.straight_high_card(hand) is not None and self.is_flush(hand):
            return 8 + self.straight_high_card(hand) * 0.01
        
        elif self.card_counter(hand, 4) is not None:
            return 7 + self.card_counter(hand, 4) * 0.01 + self.high_card(hand) * 0.0001
        
        elif self.card_counter(hand, 3) is not None and self.card_counter(hand, 2) is not None:
            return 6 + self.card_counter(hand, 3)*0.01 + self.card_counter(hand, 2)*0.0001
        
        elif self.card_counter(hand, 3) is not None and self.card_counter(hand, 3, self.card_counter(hand, 3)) is not None:
            return 6 + self.card_counter(hand, 3)*0.01 + self.card_counter(hand, 3, self.card_counter(hand, 3))*0.0001
        
        elif self.is_flush(hand):
            return 5 + self.high_value_flush * 0.01
        
        elif self.straight_high_card(hand) is not None:
            return 4 + self.straight_high_card(hand)*0.01
        
        elif self.card_counter(hand, 3) is not None:
            return 3 + self.card_counter(hand, 3)*0.01 + self.high_card(hand)*0.0001
        
        pair1 = self.card_counter(hand, 2)
        if pair1 is not None:
            if self.card_counter(hand, 2, pair1) is not None:
                return 2 + self.card_counter(hand, 2, pair1)*0.0001 + pair1*0.01 + self.high_card(hand)*0.000001
            return 1 + pair1*0.01 + self.high_card(hand)*0.001
        return 0 + self.high_card(hand) * 0.01


class StatsCalc(GetTypeOfHand):
    def __init__(self, hand):
        self.hand = self.converting_to_symbol(hand)
        self.card_count = len(self.hand)


    def get_stats(self):
        if self.card_count == 2:
            return self.calc_deal_stats()
        else:
            return self.calc_flop_turn_river_stats()


    def calc_number_combinations(self, n, r):
        return self.factorial(n) / (self.factorial(r) * self.factorial(n -r))


    def factorial(self, num):
        if num == 1 or num == 0:
            return 1
        elif num < 0:
            return None                 
        else:
            return num * self.factorial(num-1)
        
    def calc_deal_stats(self):
        deal_combinations = self.calc_number_combinations(52,2)


        # algorithm to get a percentage of how many hands the user beats given their current hand
        if self.get_value(self.hand[0]) == self.get_value(self.hand[1]):
            return (deal_combinations - ((14 - self.get_value(self.hand[0])) * self.calc_number_combinations(4,2))) / deal_combinations
        
        elif self.get_value(self.hand[0]) > self.get_value(self.hand[1]):
            remaining_deal_combinations = deal_combinations - (self.calc_number_combinations(13,1) * self.calc_number_combinations(4,2))


            num = 0
            for i in range (1,15-self.get_value(self.hand[0])):
                num += 52 - (i*4)


            return (remaining_deal_combinations - 4 * num) / deal_combinations
        


        else:
            remaining_deal_combinations = deal_combinations - (self.calc_number_combinations(13,1) * self.calc_number_combinations(4,2))


            num = 0
            for i in range (1,15-self.get_value(self.hand[1])):
                num += 52 - (i*4)


            return (remaining_deal_combinations - 4 * num) / deal_combinations
        
    def calc_flop_turn_river_stats(self):
        total_card_combinations = self.calc_number_combinations(52, self.card_count)


        if self.straight_high_card(self.hand) is not None and self.is_flush(self.hand):
            return 1
    
        elif self.card_counter(self.hand, 4) is not None:
            return (total_card_combinations - self.calc_amount_of_straight_flush()) / total_card_combinations
        
        elif self.card_counter(self.hand, 3) is not None and (self.card_counter(self.hand, 3, self.card_counter(self.hand, 3)) is not None or self.card_counter(self.hand, 2) is not None):
            return (total_card_combinations - self.calc_amount_of_straight_flush() - self.calc_amount_of_four_kind()) / total_card_combinations
        
        elif self.is_flush(self.hand):
            return (total_card_combinations - self.calc_amount_of_straight_flush() - self.calc_amount_of_four_kind() - self.calc_amount_of_full_house()) / total_card_combinations


        elif self.straight_high_card(self.hand) is not None:
            return (total_card_combinations - self.calc_amount_of_straight_flush() - self.calc_amount_of_four_kind() - self.calc_amount_of_full_house() - self.calc_amount_of_flush()) / total_card_combinations


        elif self.card_counter(self.hand, 3) is not None:
            return (total_card_combinations - self.calc_amount_of_straight_flush() - self.calc_amount_of_four_kind() - self.calc_amount_of_full_house() - self.calc_amount_of_flush() - self.calc_amount_of_straight()) / total_card_combinations


        elif self.card_counter(self.hand, 2) is not None and self.card_counter(self.hand,2, self.card_counter(self.hand, 2)) is not None:
            return (total_card_combinations - self.calc_amount_of_straight_flush() - self.calc_amount_of_four_kind() - self.calc_amount_of_full_house() - self.calc_amount_of_flush() - self.calc_amount_of_straight() - self.calc_amount_of_three_kind()) / total_card_combinations


        elif self.card_counter(self.hand, 2) is not None:
            return (total_card_combinations - self.calc_amount_of_straight_flush() - self.calc_amount_of_four_kind() - self.calc_amount_of_full_house() - self.calc_amount_of_flush() - self.calc_amount_of_straight() - self.calc_amount_of_three_kind() - self.calc_amount_of_two_pair()) / total_card_combinations


        else:
            return self.calc_amount_of_high_card() / total_card_combinations


        
    def calc_amount_of_straight_flush(self):
        return self.calc_number_combinations(4,1) * self.calc_number_combinations(47, (self.card_count - 5)) + self.calc_number_combinations(9,1) * self.calc_number_combinations(4,1) * self.calc_number_combinations(46, (self.card_count-5))
        
    def calc_amount_of_four_kind(self):
        return self.calc_number_combinations(13,1) * self.calc_number_combinations(48, (self.card_count - 4))
    
    def calc_amount_of_full_house(self):
        if self.card_count == 5:
            return self.calc_number_combinations(13,1) * self.calc_number_combinations(4,3) * self.calc_number_combinations(12,1) * self.calc_number_combinations(4,2)
        
        elif self.card_count == 6:
            # case 1 is that the hand contains 2 three of a kinds
            case1 = self.calc_number_combinations(13,2) * (self.calc_number_combinations(4,3) ** 2)


            # case 2 is that the hand contains 1 three of a kind, 1 pair and one other unrelated card
            case2 = self.calc_number_combinations(13,1) * self.calc_number_combinations(4,3) * self.calc_number_combinations(12,1) * self.calc_number_combinations(4,2) * self.calc_number_combinations(44,1)


            return case1 + case2
        
        else:
            # case 1 in that the hand contains two three of a kinds and one other unrelated card
            case1 = self.calc_number_combinations(13,2) * (self.calc_number_combinations(4,3) ** 2) * self.calc_number_combinations(44,1)


            # case 2 is a three of a kind and two pairs
            case2 = self.calc_number_combinations(13,1) * self.calc_number_combinations(4,3) * self.calc_number_combinations(12,2) * (self.calc_number_combinations(4,2) ** 2)


            #case 3 is a three of a kind, a pair and 2 other unrelated cards
            case3 = self.calc_number_combinations(13,1) * self.calc_number_combinations(4,3) * self.calc_number_combinations(12,1) * self.calc_number_combinations(4,2) * self.calc_number_combinations(11,2) * (self.calc_number_combinations(4,1) ** 2)


            return case1 + case2 + case3
        
    def calc_amount_of_flush(self):
        if self.card_count == 5:
            return self.calc_number_combinations(13,5) * self.calc_number_combinations(4,1) - self.calc_amount_of_straight_flush()
        
        elif self.card_count == 6:
            # case 1 is a hand that contains 6 cards of the same suit
            case1 = self.calc_number_combinations(13,6) * self.calc_number_combinations(4,1)


            # case 2 is a hand that contains 5 of the same suit, one card of another suit
            case2 = self.calc_number_combinations(13,5) * self.calc_number_combinations(4,1) * self.calc_number_combinations(39,1)


            return case1 + case2 - self.calc_amount_of_straight_flush()
        
        else:
            # case 1 is a hand that contains 7 cards of the same suit
            case1 = self.calc_number_combinations(13,7) * self.calc_number_combinations(4,1)


            # case 2 is a hand that contains 6 of the same suit and one other
            case2 = self.calc_number_combinations(13,6) * self.calc_number_combinations(4,1) * self.calc_number_combinations(39,1)


            # case 3 is 5 of the same suit and two others
            case3 = self.calc_number_combinations(13,5) * self.calc_number_combinations(4,1) * self.calc_number_combinations(39,2)


            return case1 + case2 + case3 - self.calc_amount_of_straight_flush()
        
    def calc_amount_of_straight(self):
        if self.card_count == 5:
            return self.calc_number_combinations(10,1) * (self.calc_number_combinations(4,1) ** 5) - self.calc_amount_of_straight_flush()
        
        elif self.card_count == 6:
            # case 1 is a hands that contains 6 adjacent value cards
            distinct_hands = 71


            flushes = self.calc_number_combinations(4,1) * self.calc_number_combinations(6,6) + self.calc_number_combinations(6,5) * self.calc_number_combinations(3,1)


            case1 = distinct_hands * (self.calc_number_combinations(4,1) ** 6 - flushes)


            #case 2 is a hand with 5 adjacent value cards and one card that is unrelated
            case2 = self.calc_number_combinations(10,1) * 5 * 6 * (self.calc_number_combinations(4,1) **4 -2)


            return case1 + case2
        
        else:
            #case 1 is a hand with 7 adjacent value cards
            distinct_hands = 217
            distinct_non_flush = 844


            case1 = distinct_hands * (self.calc_number_combinations(4,1) ** 7 - distinct_non_flush)


            # case 2 is 6 adjacent and 1 unrelated card
            distinct_hands = 71
            distinct_non_flush = 34


            case2 = distinct_hands * (self.calc_number_combinations(6,1) ** 2) * (self.calc_number_combinations(4,1) ** 5 - distinct_non_flush)


            # case 3 is 5 adjacent cards and 2 other cards forming a three of a kind
            case3 = self.calc_number_combinations(10,1) * self.calc_number_combinations(5,1) * self.calc_number_combinations(4,3) * (self.calc_number_combinations(4,1) ** 4 - 3)


            # case 4 is 5 adjacent and two others forming two pairs or random
            distinct_hands = 2268
            case4 = (self.calc_number_combinations(5,2) ** 2) * distinct_hands


            return case1 + case2 + case3 + case4
        
    def calc_amount_of_three_kind(self):
        if self.card_count in [5,6]:
            return self.calc_number_combinations(13,1) * self.calc_number_combinations(4,3) * self.calc_number_combinations(12, self.card_count -3) * (self.calc_number_combinations(4,1) ** (self.card_count -3))
        
        else:
            distinct_hands = self.calc_number_combinations(13,5)
            distinct_non_straight = distinct_hands - 10
            other_card_combinations = self.calc_number_combinations(4,1) ** 4 -3


            return distinct_non_straight * self.calc_number_combinations(5,1) * self.calc_number_combinations(4,3) * other_card_combinations
        
    def calc_amount_of_two_pair(self):
        if self.card_count == 5:
            return self.calc_number_combinations(13,2) * (self.calc_number_combinations(4,2) ** 2) * self.calc_number_combinations(44,1) 
        
        elif self.card_count == 6:
            #case 1 is a hand with 3 pairs
            case1 = self.calc_number_combinations(13,3) * (self.calc_number_combinations(4,2) ** 3)


            #case 2 is a hand with 2 pairs and 2 other cards
            case2 = self.calc_number_combinations(13,2) * (self.calc_number_combinations(4,2) ** 2) * self.calc_number_combinations(11,2) * (self.calc_number_combinations(4,1) ** 2)


            return case1 + case2
        
        else:
            #case 1 is 3 pairs and one other
            case1 = self.calc_number_combinations(13,3) * (self.calc_number_combinations(4,2) ** 3) * self.calc_number_combinations(10,1) * self.calc_number_combinations(4,1)


            #case2 is 2 pairs and 3 others
            case2 = (self.calc_number_combinations(13,5) -10) * self.calc_number_combinations(5,2) * 2268


            return case1 + case2
        
    def calc_amount_of_pair(self):
        if self.card_count == 5:
            return self.calc_number_combinations(13,1) * self.calc_number_combinations(4,2) * self.calc_number_combinations(12,3) * (self.calc_number_combinations(4,1) ** 3)


        elif self.card_count == 6:
            distinct_hands = self.calc_number_combinations(13,5)
            distinct_non_straight = distinct_hands - 10
            other_card_combinations = self.calc_number_combinations(4,1) ** 4 -2


            return distinct_non_straight * other_card_combinations * self.calc_number_combinations(5,1) * self.calc_number_combinations(4,2)
        
        else:
            distinct_hands = self.calc_number_combinations(13,6)
            distinct_non_straight = distinct_hands - 71
            other_card_combinations = self.calc_number_combinations(4,1) ** 5 - 34


            return distinct_non_straight * other_card_combinations * self.calc_number_combinations(6,1) * self.calc_number_combinations(4,2)
        
    def calc_amount_of_high_card(self):
        remaining_cards = self.calc_number_combinations(52, self.card_count) - self.calc_amount_of_pair() - self.calc_amount_of_two_pair() - self.calc_amount_of_three_kind() - self.calc_amount_of_straight() - self.calc_amount_of_flush() - self.calc_amount_of_full_house() - self.calc_amount_of_four_kind() - self.calc_amount_of_straight_flush()
        return remaining_cards
