import random

# Global variables
suits = {"Hearts", "Diamonds", "Clubs", "Spades"}
ranks = {"Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"}
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips():
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            print()  # blank line
            print("Just a reminder, Jack, Queen, King = 10")
            print("And Ace = 11 (or 1 if the total exceeds 21.  Good luck to you!!!")
            print()  # blank line
            chips.bet = int(input("How many chips would you like to bet?"))
        except ValueError:
            print("Sorry, please provide an integer")
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed", chips.total)
            else:
                break

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing

    while True:
        choice = input("Do you want to Hit or Stand? (Enter 'h' or 's')")

        if choice.lower() == 'h':
            hit(deck, hand)
        elif choice.lower() == 's':
            print("Player stands, dealer's turn")
            playing = False
        else:
            print("Sorry, please enter 'h' or 's' only.")
            continue

        break

def show_some(player, dealer):
    print("\nPlayer's Hand:")
    for card in player.cards:
        print(card)
    print("\nDealer's Hand:")
    print("<hidden card>")
    for card in dealer.cards[1:]:
        print(card)

def show_all(player, dealer):
    print("\nPlayer's Hand:")
    for card in player.cards:
        print(card)
    print("\nDealer's Hand:")
    for card in dealer.cards:
        print(card)

def player_busts(player, dealer, chips):
    print()
    print("Player busts!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print()
    print("Player wins! Woot woot!!!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print()
    print("Dealer busts! Yay you win, congrats!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print()
    print("Dealer wins!  Sorry, better luck next time!")
    chips.lose_bet()

def push(player, dealer):
    print()
    print("It's a tie! Push it through...")


def play_blackjack():
    while True:
        print("Welcome to Blackjack! Ready to play???")

        # Set up the player's chips
        player_chips = Chips()

        while True:
            # Create and shuffle the deck, deal two cards to each player
            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            player_hand.add_card(deck.deal())
            player_hand.add_card(deck.deal())

            dealer_hand = Hand()
            dealer_hand.add_card(deck.deal())
            dealer_hand.add_card(deck.deal())

            # Prompt the player for their bet
            take_bet(player_chips)

            # Show the initial cards
            show_some(player_hand, dealer_hand)

            playing = True

            while playing:
                # Prompt for player to Hit or Stand
                hit_or_stand(deck, player_hand)

                # Show card, but keep one dealer card hidden
                show_some(player_hand, dealer_hand)

                # If player's hand exceeds 21, player busts and breaks out of loop
                if player_hand.value > 21:
                    player_busts(player_hand, dealer_hand, player_chips)
                    break

                # If player hasn't busted, play dealer's hand until dealer reaches 17
                if player_hand.value <= 21:
                    while dealer_hand.value < 17:
                        hit(deck, dealer_hand)

                    # Show all cards
                    show_all(player_hand, dealer_hand)

                    if dealer_hand.value > 21:
                        dealer_busts(player_hand, dealer_hand, player_chips)
                    elif dealer_hand.value > player_hand.value:
                        dealer_wins(player_hand, dealer_hand, player_chips)
                    elif dealer_hand.value < player_hand.value:
                        player_wins(player_hand, dealer_hand, player_chips)
                    else:
                        push(player_hand, dealer_hand)

                    # Inform the player of their chip total
                    print("\nPlayer's total chips: ", player_chips.total)

                    # Check if player is out of chips
                    if player_chips.total <= 0:
                        print("You're out of chips. Thanks for playing!")
                        return

                    # Ask if they want to play again
                    if not play_again():
                        print("Thanks for playing! Good luck and see you around the casino!")
                        return
                    else:
                        # Clear hands from the previous round
                        player_hand.cards.clear()
                        dealer_hand.cards.clear()

                        print("Awesome, let's play another round!")

                        # Break out of the inner loop to start a new round
                        break

def play_again():
    while True:
        play_again_input = input("Do you want to play again? Enter 'y' or 'n': ")
        if play_again_input.lower() == 'y':
            return True
        elif play_again_input.lower() == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

# Call the play_blackjack function to start the game
play_blackjack()
