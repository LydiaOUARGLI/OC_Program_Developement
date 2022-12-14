from controleurs.controller_database import load_db
from views.View import View
from operator import itemgetter


class Report(View):

    def __init__(self):
        self.players = load_db("players")
        self.tournaments = load_db("tournaments")

    def display_players_report(self, players=None):
        # if the user want to display a special turnament players we pass True to the turnament_player and put a list
        # of players in the function argument, if the user does not precise anything
        # all registred players will be loaded
        if players is None:
            players = []
        players = players

        builded_selection = self.build_selection(iterable=players,
                                                 display_msg="Voir les détails d'un joueur:\n",
                                                 assertions=["r"])

        while True:
            print("Classement: ")
            # Ranking display
            # Select a player in the ranking list to display the player details
            user_input = self.get_user_entry(
                msg_display=builded_selection['msg'] + "r - Retour\n> ",
                msg_error="Veuillez faire un choix valide.",
                value_type="selection",
                assertions=builded_selection['assertions']
            )

            if user_input == "r":
                break

            else:
                selected_player = players[int(user_input)-1]
                # Display players details
                while True:
                    print(f"Détails du joueur {selected_player['name']}:")
                    print(f"Rang: {selected_player['rank']}\n"
                          f"Score total: {selected_player['total_score']}\n"
                          f"Nom: {selected_player['name']}\n"
                          f"Prénom: {selected_player['first_name']}\n"
                          f"Date de naissance: {selected_player['dob']}\n"
                          f"Sexe: {selected_player['sex']}\n"
                          )

                    user_input = self.get_user_entry(
                        msg_display="Que faire ?\n r - Retour\n> ",
                        msg_error="Veuillez faire un choix valide.",
                        value_type="selection",
                        assertions=["r"]
                    )
                    if user_input == "r":
                        break

    def display_tournaments_reports(self):

        builded_selection = self.build_selection(
            iterable=self.tournaments,
            display_msg="Voir les détails d'un tournoi:\n",
            assertions=['r']
        )

        while True:
            print("Tournois:")
            # Display all registred turnaments
            # Select a turnament from the registred list to show its details

            user_input = self.get_user_entry(
                msg_display=builded_selection['msg'] + "r - Retour\n> ",
                msg_error="Veuillez faire un choix valide.",
                value_type="selection",
                assertions=builded_selection['assertions']
            )

            if user_input == "r":
                break

            else:
                selected_tournament = self.tournaments[int(user_input) - 1]
                # Display the selected turnament details
                while True:
                    print(f"Détails du tournoi {selected_tournament['name']}\n"
                          f"Nom: {selected_tournament['name']}\n"
                          f"Lieu: {selected_tournament['place']}\n"
                          f"Date: {selected_tournament['starting_date']}\n"
                          f"Contrôle du temps: {selected_tournament['time_control']}\n"
                          f"Nombre de rounds: {selected_tournament['rounds_nb']}\n"
                          f"Description: {selected_tournament['description']}\n"
                          )

                    user_input = self.get_user_entry(
                        msg_display="Que faire ?\n"
                                    "0 - Voir les participants\n"
                                    "1 - Voir les tours\n"
                                    "r - Retour\n"
                                    "> ",
                        msg_error="Veuillez entrer une sélection valide",
                        value_type="selection",
                        assertions=["0", "1", "2", "r"]
                    )

                    if user_input == "r":
                        break

                    elif user_input == "0":
                        while True:
                            user_input = self.get_user_entry(
                                msg_display="Type de classement:\n"
                                            "0 - Par rang\n"
                                            "1 - Par ordre alphabétique\n"
                                            "r - Retour\n"
                                            "> ",
                                msg_error="Veuillez entrer une sélection valide",
                                value_type="selection",
                                assertions=["0", "1", "r"]
                            )
                            if user_input == "r":
                                break
                            elif user_input == "0":
                                sorted_players = self.sort_players(selected_tournament["players"],
                                                                   by_rank=True)
                                self.display_players_report(players=sorted_players)
                            elif user_input == "1":
                                sorted_players = self.sort_players(selected_tournament["players"],
                                                                   by_rank=False)
                                self.display_players_report(players=sorted_players)
                    elif user_input == "1":
                        self.display_rounds(selected_tournament["rounds"])

    def display_rounds(self, rounds: list):
        builded_selection = self.build_selection(
            iterable=rounds,
            display_msg="Voir les détails d'un round:\n",
            assertions=['r']
        )
        while True:
            print("Rounds:")

            user_input = self.get_user_entry(
                msg_display=builded_selection['msg'] + "r - Retour\n> ",
                msg_error="Veuillez faire un choix valide.",
                value_type="selection",
                assertions=builded_selection['assertions']
            )

            if user_input == "r":
                break

            else:
                selected_round = rounds[int(user_input) - 1]
                while True:
                    print(f"Détails du round {selected_round['name']}\n"
                          f"Nom: {selected_round['name']}\n"
                          f"Nombre de matchs: {len(selected_round['matchs'])}\n"
                          f"Date de début: {selected_round['start_date']}\n"
                          f"Date de fin: {selected_round['end_date']}\n"
                          )
                    user_input = self.get_user_entry(
                        msg_display="Que faire ?\n0 - Voir les matchs\nr - Retour\n> ",
                        msg_error="Veuillez faire un choix valide",
                        value_type="selection",
                        assertions=["0", "r"]
                    )
                    if user_input == "r":
                        break
                    else:
                        builded_selection = self.build_selection(
                            iterable=selected_round['matchs'],
                            display_msg="Voir les détails d'un match\n",
                            assertions=['r']
                        )
                        print("Matchs:")
                        user_input = self.get_user_entry(
                            msg_display=builded_selection['msg'] + "r - Retour\n> ",
                            msg_error="Veuillez faire un choix valide.",
                            value_type="selection",
                            assertions=builded_selection['assertions']
                        )

                        if user_input == "r":
                            break
                        else:
                            selected_match = selected_round['matchs'][int(user_input) - 1]
                            while True:
                                print(f"Détails du {selected_match['name']}\n"
                                      f"Joueur 1 ({selected_match['color_player1']}): " +
                                      f"{selected_match['player1']['name']} ({selected_match['score_player1']} pts)\n"
                                      f"Joueur 2 ({selected_match['color_player2']}): " +
                                      f"{selected_match['player2']['name']} ({selected_match['score_player2']} pts)\n"
                                      f"Gagnant: {selected_match['winner']}\n"
                                      )
                                user_input = self.get_user_entry(
                                    msg_display="Que faire ?\nr - Retour\n> ",
                                    msg_error="Veuillez faire un choix valide",
                                    value_type="selection",
                                    assertions=["r"]
                                )
                                if user_input == "r":
                                    break

    @staticmethod
    def sort_players(players: list, by_rank: bool) -> list:
        # Sort players by rank or by name order
        if by_rank:
            sorted_players = sorted(players, key=itemgetter('rank'))
        else:
            sorted_players = sorted(players, key=itemgetter('name'))

        return sorted_players
