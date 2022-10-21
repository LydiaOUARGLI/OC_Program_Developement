from views.views_player import CreatePlayer
from models.players import Player
from controleurs.controller_database import update_player_rank, save_db


def create_player():

    # Load player information
    user_entries = CreatePlayer().display_menu()

    # Players arguments
    player = Player(
        user_entries['name'],
        user_entries['first_name'],
        user_entries['dob'],
        user_entries['sex'],
        user_entries['total_score'],
        user_entries['rank'])

    # serialization:
    serialized_player = player.serialized_player(tournament_score=False)

    # Save player in database
    save_db("players", serialized_player)
    return player


def update_rankings(player, rank, score=True):
    if score:
        player.total_score += player.tournament_score
    player.rank = rank
    serialized_player = player.serialized_player(tournament_score=True)
    print(serialized_player['name'])
    update_player_rank("players", serialized_player)
    print(f"Update du rang de {player}:\nScore total: {player.total_score}\nRang: {player.rank}")
