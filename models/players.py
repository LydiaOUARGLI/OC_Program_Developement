

class Player:
    def __init__(self, name, first_name, dob, sex, total_score, rank=0):
        self.name = name
        self.first_name = first_name
        self.dob = dob
        self.sex = sex
        self.tournament_score = 0
        self.rank = rank
        self.total_score = total_score
        self.already_played_with = []

    def __str__(self):
        return f"Player: {self.name} - {self.tournament_score} "

    def serialized_player(self, tournament_score=False):
        serialized_player = {
            'name': self.name,
            'first_name': self.first_name,
            'dob': self.dob,
            'sex': self.sex,
            'total_score': self.total_score,
            'rank': self.rank,
            'tournament_score': self.tournament_score,
        }
        if tournament_score:
            serialized_player["tournament_score"] = tournament_score

        return serialized_player
