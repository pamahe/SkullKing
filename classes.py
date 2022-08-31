import random
import os


class Card(object):

    def __init__(self, color, number):
        self.color = color
        self.number = number

    def __repr__(self):
        if self.number:
            print(f"{self.number} - {self.color}")
        else:
            print(f"{self.color}")


class Deck(object):

    def __init__(self):
        self.cards = []

    def create(self):
        for color in ['rouge', 'blueu', 'jaune', 'noir']:
            for number in range(1, 14):
                self.cards.append(Card(color, number))
        for i in range(5):
            self.cards.append(Card('pirate', None))
            self.cards.append(Card('escape', None))
        self.cards.extend([
            Card('mermaid', None), Card('mermaid', None), Card('skullking', None)
        ])

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop(0)


class Joueur(object):

    def __init__(self, name):
        self.name = name
        self.bets = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.plis = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.primes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.score = 0
        self.hand = []

    def get_score(self):
        for i in range(len(self.bets)):
            if self.bets[i] != self.plis[i]:
                self.score -= 10 * abs(self.plis[i] - self.bets[i])
                self.score += self.primes[i]
            else:
                self.score += 20 * self.plis[i]
                self.score += self.primes[i]

    def print_hand(self):
        print(f"Main de {self.name} : ", end='')
        for card in self.hand:
            print(card, end='')
        print("")


class Game(object):

    def __int__(self):
        self.joueurs = []
        self.first_player_index = 0

    def play(self):
        deck = Deck()

        print("Combien de joueurs ?")
        nb_players = input(">")

        for i in nb_players:
            name = input(f"Nom du joueur {i} ? ")
            self.joueurs.append(Joueur(name))

        for manche in range(1, 11):
            deck.create()
            deck.shuffle()

            for card_to_draw in range(1, manche):
                for joueur in self.joueurs:
                    joueur.hand.append(deck.draw())

            self.get_bets(manche)

            for pli in range(1, manche):
                cards_played = self.play_pli()
                winner_index = self.get_pli_winner(cards_played)
                self.update_scores(winner_index, manche)
                self.first_player_index += 1
                print(f"Player {self.joueurs[winner_index].name} gagne le pli !")

    def display_score(self):
        for joueur in self.joueurs:
            joueur.get_score()
            print(f"{joueur.name}:{joueur.score}", end=' ')

    def get_bets(self, manche):
        for joueur in self.joueurs:
            os.system('clear')
            self.display_score()
            joueur.print_hand()
            joueur.bets[manche] = input("Combien pensez-vous gagner de plis ? ")

    def play_pli(self):
        called_color = None
        cards_played = []
        ordre_des_joueurs = self.joueurs[self.first_player_index:] + self.joueurs[:self.first_player_index]
        for joueur in ordre_des_joueurs:
            os.system('clear')
            print("Cards played : ", end='')
            for card in cards_played:
                print(f"{card}", end=' ')
            print("")
            joueur.print_hand()
            invalid_play = True
            while invalid_play:

                card = None
                while card is None:
                    card = input("Choisissez une carte à jouer : ")
                    if card in joueur.hand:
                        card = joueur.hand.pop(joueur.hand.index(card))
                    else:
                        card = None

                if called_color is not None:
                    if card.color not in ['rouge', 'bleu', 'jaune', 'noir']:
                        invalid_play = False
                    elif card.color == called_color:
                        invalid_play = False
                    else:
                        if any([hand_card.color == called_color for hand_card in joueur.hand]):
                            invalid_play = True
                            print("Vous devez jouer la couleur demandée !")
                else:
                    if card.color in ['rouge', 'bleu', 'jaune', 'noir']:
                        called_color = card.color
                        invalid_play = False

            cards_played.append(card)

        return cards_played

    def get_pli_winner(self, cards_played, called_color):
        winner_index = None

        colors = [card.color for card in cards_played]
        if 'skullking' in colors:
            if 'mermaid' in colors:
                winning_index = colors.index('mermaid')
                prime = 50
            else:
                winning_index = colors.index('skullking')
                prime = 0
                for color in colors:
                    if color == 'pirate':
                        prime += 30
        else:
            values = []
            for card in cards_played:
                if card.color != 'black' and card.color != called_color:
                    values.append(0)
                elif card.color == called_color:
                    value = card.number
                else:  # card is black
                    value = card.number + 13
            winner_index = values.index(max(values))

        return winner_index

    def update_scores(self, winner_index, manche):
        pass