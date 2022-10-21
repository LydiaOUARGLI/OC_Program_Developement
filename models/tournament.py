from models.rounds import Round


class Tournament:
    """Tournament attributes"""
    def __init__(self, name, place, starting_date, end_date, time_control, player, rounds_nb=4,  description=''):
        self.name = name
        self.place = place
        self.starting_date = starting_date
        self.end_date = end_date
        self.time_control = time_control
        self.players = player
        self.rounds_nb = rounds_nb
        self.rounds = []
        self.description = description

    def __str__(self):
        return f"Tournament: {self.name}"

    """Create new rounds"""

    def create_round(self, round_number):
        players_pairs = self.players_pairs_generation(instant_round=round_number)
        round = Round("Round " + str(round_number + 1), players_pairs)
        self.rounds.append(round)

    """Create players pair """
    def sorted_players(self, instant_round):

        # For the first round players are sorted by rank
        if instant_round == 0:
            sorted_players = sorted(self.players, key=lambda x: x.rank, reverse=True)

        # For other rounds players are sorted by total_score
        else:
            sorted_players = []
            temporary_sorted_list = sorted(self.players, key=lambda x: x.total_score, reverse=True)
            # we associate the temporary list to sorted list except for players who got the same total_score

            for index, player in enumerate(temporary_sorted_list):
                try:
                    sorted_players.append(player)
                except player.total_score == player[index-1].total_score:
                    if player.rank > player[index+1].rank:
                        sorted_players.append(player[index])
                        sorted_players.append(player[index+1])
                    else:
                        sorted_players.append(player[index+1])
                        sorted_players.append(player[index])
                except IndexError:
                    sorted_players.append(player)
        return sorted_players

    def players_pairs_generation(self, instant_round):
        sorted_players = self.sorted_players(instant_round)
        # Repart the sorted list into two different lists
        half = len(self.players)//2
        upper_players_part = sorted_players[:half]
        lower_players_part = sorted_players[half:]
        # Select the best player from each list and make players into pairs for the first round
        players_pairs = []
        if instant_round == 0:
            for i, player in enumerate(upper_players_part):
                j = 0
                while j < len(lower_players_part)-1:
                    player2 = lower_players_part[i+j]
                    if player2 not in player.already_played_with and player != player2:
                        players_pairs.append((player, player2))
                        player.already_played_with.append(player2)
                        player2.already_played_with.append(player)
                        break
                    else:
                        j = j + 1
                        continue
        else:
            sorted_index = []
            for i, player in enumerate(sorted_players):
                j = 0
                if player not in sorted_index:
                    while j < len(sorted_players)-1:
                        try:
                            player2 = sorted_players[j+i]
                            if player2 not in player.already_played_with and player != player2 \
                                    and player2 not in sorted_index:
                                players_pairs.append((player, player2))
                                player.already_played_with.append(player2)
                                player2.already_played_with.append(sorted_players[i])
                                sorted_index.append(player2)
                                break
                            else:
                                j = j + 1
                                continue
                        except IndexError:
                            break
        return players_pairs

    def get_rankings(self, by_score=True):
        # In default we return turnament ranking by the total score of every player or it can be by players rank points
        if by_score:
            sorted_players = sorted(self.players, key=lambda x: x.tournament_score, reverse=True)
        else:
            sorted_players = sorted(self.players, key=lambda x: x.rank, reverse=True)

        return sorted_players

    def serialized_tournament(self, save_rounds=False):
        serialized_tournament = {
            "name": self.name,
            "place": self.place,
            "starting_date": self.starting_date,
            "end_date": self.end_date,
            "time_control": self.time_control,
            "players": [player.serialized_player(tournament_score=True) for player in self.players],
            "rounds_nb": self.rounds_nb,
            "rounds": [round.serialized_round() for round in self.rounds],
            "description": self.description
        }

        if save_rounds:
            serialized_tournament["rounds"] = [round.serialized_round() for round in self.rounds]

        return serialized_tournament
