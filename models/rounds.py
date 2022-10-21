from controleurs.time_stamp import get_timestamp
from models.Match import Match


class Round:
    def __init__(self, name, players_pairs, load_match: bool = False):
        self.name = name
        self.players_pairs = players_pairs
        # The user can load matches in the empty list assigned to the variable match or create a new one
        if load_match:
            self.matchs = []
        else:

            self.matchs = self.create_matchs()
        self.start_date = get_timestamp()
        self.end_date = ""

    def __str__(self):
        return self.name

    def create_matchs(self):
        matchs = []
        for i, pair in enumerate(self.players_pairs):
            matchs.append(Match(name=f"Match {i}", players_pair=pair))
        return matchs

    def mark_as_complete(self):
        # When the match is finished the user input the results
        self.end_date = get_timestamp()

        print(f"{self.end_date} : {self.name} terminé.")
        print("Veuillez saisir les résultats des matchs joués:")
        for match in self.matchs:
            match.play_match()

    def serialized_round(self):
        ser_players_pairs = []
        for pair in self.players_pairs:
            ser_players_pairs.append(
                (
                    pair[0].serialized_player(tournament_score=True),
                    pair[1].serialized_player(tournament_score=True)
                 )
            )

        return {
            "name": self.name,
            "players_pairs": ser_players_pairs,
            "matchs": [match.serialized_match() for match in self.matchs],
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
