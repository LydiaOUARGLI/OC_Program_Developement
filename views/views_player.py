from views.View import View
from controleurs.controller_database import load_db


class CreatePlayer(View):
    # Create new players
    def display_menu(self):
        name = input("""Nom du joueur:\n> """)
        first_name = input("""Prénom de joueur:\n> """)
        dob = self.get_user_entry(
            msg_display="Date de naissance:\n> ",
            msg_error="Veuillez entrer une date au format valide: DD-MM-YYYY",
            value_type="date",
        )
        sex = self.get_user_entry(
            msg_display="Sexe (H ou F):\n> ",
            msg_error="Veuillez entrer H ou F",
            value_type="selection",
            assertions=["H", "h", "F", "f"]
        ).upper()
        rank = self.get_user_entry(
            msg_display="Rang:\n> ",
            msg_error="Veuillez entrer une valeur numérique valide.",
            value_type="numeric"
        )
        print(f"Joueur {first_name} {name} créé.")
        return {
            "name": name,
            "first_name": first_name,
            "dob": dob,
            "sex": sex,
            "total_score": 0,
            "rank": rank,
        }


class LoadPlayer(View):
    # Load registred players in the database
    def display_menu(self, nb_players_to_load):

        all_players = load_db("players")
        serialized_loaded_players = []
        for i in range(nb_players_to_load):
            print(f"Plus que {str(nb_players_to_load - i)} joueurs à charger.")
            display_msg = "Choisir un joueur:\n"
            assertions = []
            for j, player in enumerate(all_players):
                display_msg = display_msg + f"{str(j+1)} - {player['first_name']} " \
                                            f"{player['name']} / rank {player['rank']}\n"
                assertions.append(str(j+1))
            user_input = int(self.get_user_entry(
                msg_display=display_msg,
                msg_error="Veuillez entrer un nombre entier.",
                value_type="selection",
                assertions=assertions
            ))
            if all_players[user_input-1] not in serialized_loaded_players:
                serialized_loaded_players.append(all_players[user_input-1])
            else:
                print("Joueur déjà chargé. Merci de choisir un autre joueur.")
                nb_players_to_load += 1
        return serialized_loaded_players
