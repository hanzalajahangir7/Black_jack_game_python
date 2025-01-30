import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank["rank"]} of {self.suit}'
    

class Deck:
    def __init__(self):
        self.cards = []
        suits = ["spades", "clubs", "hearts", "diamonds"]
        ranks = [
            {"rank": "a", "value": 11},
            {"rank": "k", "value": 10},
            {"rank": "q", "value": 10},
            {"rank": "j", "value": 10},
            {"rank": "10", "value": 10},
            {"rank": "9", "value": 9},
            {"rank": "8", "value": 8},
            {"rank": "7", "value": 7},
            {"rank": "6", "value": 6},
            {"rank": "5", "value": 5},
            {"rank": "4", "value": 4},
            {"rank": "3", "value": 3},
            {"rank": "2", "value": 2}
        ]
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, number):
        cards_dealt = []
        for q in range(number):
            if len(self.cards) > 0:
                card = self.cards.pop()
                cards_dealt.append(card)
        return cards_dealt
    

class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)
    
    def calculate_value(self):
        self.value = 0
        has_ace = False

        for card in self.cards:
            card_value = int(card.rank["value"])
            self.value += card_value
            if card.rank["rank"] == "a":
                has_ace = True
        
        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value
    
    def is_blackjack(self):
        return self.get_value() == 21
    
    def display(self, show_all_dealer_card=False):
        print(f'{"dealer\'s" if self.dealer else "your"} hand:')
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_all_dealer_card:
                print("hidden")
            else:
                print(card)
        if not self.dealer:
            print("value:", self.get_value())
        print()


class Game:
    def play(self):
        game_number = 0 
        games_to_play = 0
         
        try:
            games_to_play = int(input("Enter how many games you wanna play? "))
        except:
            print("You must enter a number.")

        while game_number < games_to_play:
            game_number += 1

            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            # Deal two cards each to the player and dealer
            player_hand.add_card(deck.deal(2))
            dealer_hand.add_card(deck.deal(2))

            print()
            print("*" * 30)
            print(f'Game {game_number} of {games_to_play}')
            print("*" * 30)
            player_hand.display()
            dealer_hand.display()

            if self.check_winner(player_hand, dealer_hand):
                continue

            choice = ""
            while player_hand.get_value() < 21 and choice not in ['s', "stand"]:
                choice = input("Please choose 'hit' or 'stand': ").lower()
                print()
                while choice not in ['h', 's', "hit", "stand"]:
                    choice = input("Please choose 'hit' or 'stand' or (h/s): ").lower()
                    print()
                if choice in ["hit", "h"]:
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()

            if self.check_winner(player_hand, dealer_hand):
                continue

            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()

            dealer_hand.display(show_all_dealer_card=True)

            if self.check_winner(player_hand, dealer_hand):
                continue

            print("Final result")
            print("Your hand value:", player_hand_value)
            print("Dealer hand value:", dealer_hand_value)

            self.check_winner(player_hand, dealer_hand, True)

        print("\nThanks for playing")

    def check_winner(self, player_hand, dealer_hand, game_over=False):
        if not game_over:
            if player_hand.get_value() > 21:
                print("You busted")
                return True
            elif dealer_hand.get_value() > 21:
                print("Dealer busted")
                return True
            elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
                print("Both have blackjack")
                return True
            elif player_hand.is_blackjack():
                print("Player has blackjack, you win!")
                return True
            elif dealer_hand.is_blackjack():
                print("Dealer has blackjack, you lose!")
                return True
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print("You win!")
            elif player_hand.get_value() == dealer_hand.get_value():
                print("Tie!")
            else:
                print("Dealer wins!")
        return False


# To play the game
game_instance = Game()
game_instance.play()
