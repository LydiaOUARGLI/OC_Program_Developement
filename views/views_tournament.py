from views.View import View
from controleurs.controller_database import load_db


class CreateTournament(View):
    # Menu for creation a new turnament
    def display_menu(self):

        start_date = self.get_user_entry(
            msg_display="Date de début du tournoi:\n> ",
            msg_error="Veuillez entrer une date au format valide: DD-MM-YYYY et supérieur à la date d'aujourd'hui",
            value_type="start_date",

        )
        end_date = self.get_user_entry(
            msg_display="Date de fin du tournoi:\n> ",
            msg_error="Veuillez entrer une date au format valide: DD-MM-YYYY",
            value_type="date"
        )

        print(start_date + " : Nouveau tournoi")

        name = input("""Nom du tournoi:\n> """)

        place = self.get_user_entry(
            msg_display="Lieu:\n> ",
            msg_error="Veuillez entrer un lieu valide",
            value_type="string"
        )

        user_selection_time_control = self.get_user_entry(
            msg_display="Contrôle de temps:\n0 - Bullet\n1 - Blitz\n2 - Coup Rapide\n> ",
            msg_error="Veuillez entrer 0, 1 ou 2.",
            value_type="selection",
            assertions=["0", "1", "2"]
        )
        if user_selection_time_control == "0":
            time_control = "Bullet"
        elif user_selection_time_control == "1":
            time_control = "Blitz"
        else:
            time_control = "Coup Rapide"

        nb_players = self.get_user_entry(
            msg_display="Nombre de joueurs (8 minimum):\n> ",
            msg_error="Veuillez entrer un nombre entier supérieur ou égal à 2.",
            value_type="num_superior",
            default_value=4
        )

        nb_rounds = self.get_user_entry(
            msg_display="Nombre de tours (4 par défaut):\n> ",
            msg_error="Veuillez entrer 4 ou plus.",
            value_type="num_superior",
            default_value=4
        )
        description = input("Description du tournoi:\n> ")
        print(f"Tournoi {name} qui aura lieu au {place} le {start_date} est créé.")
        return {
            "name": name,
            "place": place,
            "starting_date": start_date,
            "end_date": end_date,
            "time_control": time_control,
            "nb_players": nb_players,
            "rounds_nb": nb_rounds,
            "description": description
        }


class LoadTournament(View):
    # Load a registred turnament
    def display_menu(self):

        all_tournaments = load_db("tournaments")
        if all_tournaments:
            builded_selection = self.build_selection(iterable=all_tournaments,
                                                     display_msg="Choisir un tournoi:\n",
                                                     assertions=[])
            user_input = int(self.get_user_entry(
                msg_display=builded_selection['msg'] + "\n> ",
                msg_error="Veuillez entrer un nombre entier.",
                value_type="selection",
                assertions=builded_selection['assertions']
            ))
            serialized_loaded_tournament = all_tournaments[user_input-1]
            return serialized_loaded_tournament
        else:
            return False
