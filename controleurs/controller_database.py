from pathlib import Path
from tinydb import TinyDB
from tinydb import where
from models.players import Player
from models.tournament import Tournament


def save_db(db_name, serialized_data):
    Path("data/").mkdir(exist_ok=True)
    try:
        db = TinyDB(f"data/{db_name}.json")
    except FileNotFoundError:
        with open(f"data/{db_name}.json", "w"):
            pass
        db = TinyDB("data/" + db_name + ".json")

    db.insert(serialized_data)
    print(f"{serialized_data['name']} sauvegardé avec succès.")


def update_db(db_name, serialized_data):
    db = TinyDB(f"data/{db_name}.json")
    db.update(
        serialized_data,
        where('name') == serialized_data['name']
    )
    print(f"{serialized_data['name']} updaté avec succès.")


def update_player_rank(db_name, serialized_data):
    db = TinyDB(f"data/{db_name}.json")
    db.update(
            {'rank': serialized_data['rank'], 'total_score': serialized_data['total_score']},
            where('name') == serialized_data['name']
    )
    print(f"{serialized_data['name']} mise à jour avec succès.")


def load_db(db_name):
    db = TinyDB(f"data/{db_name}.json")
    return db.all()


def load_player(serialized_player, load_tournament_score=False):
    player = Player(
        serialized_player["name"],
        serialized_player["first_name"],
        serialized_player["dob"],
        serialized_player["sex"],
        serialized_player["total_score"],
        serialized_player["rank"]
    )
    if load_tournament_score:
        player.tournament_score = serialized_player["tournament_score"]
    return player


def load_tournament(serialized_tournament):
    loaded_tournament = Tournament(
        serialized_tournament["name"],
        serialized_tournament["place"],
        serialized_tournament["starting_date"],
        serialized_tournament["end_date"],
        serialized_tournament["time_control"],
        [load_player(player, load_tournament_score=True) for player in serialized_tournament["players"]],
        serialized_tournament["rounds_nb"],
        serialized_tournament["description"]
    )
    return loaded_tournament
