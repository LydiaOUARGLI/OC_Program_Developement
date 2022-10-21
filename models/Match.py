import random
from views.View import View


class Match:
    def __init__(self, name, players_pair):
        self.player1 = players_pair[0]
        self.score_player1 = 0
        self.color_player1 = ""
        self.player2 = players_pair[1]
        self.score_player2 = 0
        self.color_player2 = ""
        self.winner = ""
        self.name = name

    def __repr__(self):
        return ([self.player1, self.score_player1],
                [self.player2, self.score_player2])

    def assign_colors(self):
        # Attribute a random color to players (black or white)
        if random.choice([True, False]):
            self.color_player1 = "Blanc"
            self.color_player2 = "Noir"
        else:
            self.color_player1 = "Noir"
            self.color_player2 = "Blanc"

    def play_match(self):

        # Assign colors
        self.assign_colors()

        # Input scores for the played match
        print()
        winner = View().get_user_entry(
            msg_display=f"{self.player1.first_name} ({self.color_player1}) VS " +
                        f"{self.player2.first_name} ({self.color_player2})\n"
                        f"Gagnant ?\n"
                        f"0 - {self.player1.first_name} ({self.color_player1})\n"
                        f"1 - {self.player2.first_name} ({self.color_player2})\n"
                        f"2 - Égalité\n> ",
            msg_error="Veuillez entrer 0, 1 ou 2.",
            value_type="selection",
            assertions=["0", "1", "2"]
        )

        if winner == "0":
            self.winner = self.player1.first_name
            self.score_player1 += 1
        elif winner == "1":
            self.winner = self.player2.first_name
            self.score_player2 += 1
        elif winner == "2":
            self.winner = "Égalité"
            self.score_player1 += 0.5
            self.score_player2 += 0.5

        self.player1.tournament_score += self.score_player1
        self.player2.tournament_score += self.score_player2

    def serialized_match(self):
        return {
            "player1": self.player1.serialized_player(tournament_score=True),
            "score_player1": self.score_player1,
            "color_player1": self.color_player1,
            "player2": self.player2.serialized_player(tournament_score=True),
            "score_player2": self.score_player2,
            "color_player2": self.color_player2,
            "winner": self.winner,
            "name": self.name
        }
