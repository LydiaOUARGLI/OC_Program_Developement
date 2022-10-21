from controleurs.controller_database import save_db, load_tournament
from controleurs.controller_tournament import create_tournament, play_tournament
from controleurs.Controller_players import update_rankings
from views.views_player import CreatePlayer
from views.note import Report
from views.views_tournament import LoadTournament
from views.View import View


class MainMenu(View):

    def display_main_menu(self):
        while True:
            print()
            user_input = self.get_user_entry(
                msg_display="Bienvenue sur la plateforme des jeux d'échec. Que voulez vous faire ?\n"
                            "0 - Créer un nouveau tournoi\n"
                            "1 - Charger un tournoi existant\n"
                            "2 - Créer des nouveau joueurs\n"
                            "3 - Voir les rapports\n"
                            "q - Quitter\n> ",
                msg_error="Veuillez entrer une valeur valide SVP",
                value_type="selection",
                assertions=["0", "1", "2", "3", "q"]
            )

            # Create a new turnament
            if user_input == "0":
                tournament = create_tournament()
                break

            # Load a registred turnament
            elif user_input == "1":
                serialized_tournament = LoadTournament().display_menu()
                if serialized_tournament:
                    tournament = load_tournament(serialized_tournament)
                    break
                else:
                    print("Aucun tournoi sauvegardé !")
                    continue

            # Create players choice
            elif user_input == "2":
                user_input = self.get_user_entry(
                    msg_display="Nombre de joueurs à créer:\n> ",
                    msg_error="Veuillez entrer une valeur numérique valide ",
                    value_type="numeric"
                )
                for i in range(user_input):
                    serialized_player = CreatePlayer().display_menu()
                    save_db("players", serialized_player)

            # Displays reports
            elif user_input == "3":
                while True:
                    user_input = self.get_user_entry(
                        msg_display="0 - Joueurs\n1 - Tournois\nr - Retour\n> ",
                        msg_error="Veuillez faire un choix valide.",
                        value_type="selection",
                        assertions=["0", "1", "r"]
                    )

                    if user_input == "r":
                        break

                    elif user_input == "0":
                        while True:
                            user_input = self.get_user_entry(
                                msg_display="Voir le classement:\n"
                                            "0 - Par rang\n"
                                            "1 - Par ordre alphabétique\n"
                                            "r - Retour\n> ",
                                msg_error="Veuillez faire un choix valide.",
                                value_type="selection",
                                assertions=["0", "1", "r"]
                            )
                            if user_input == "r":
                                break
                            elif user_input == "0":
                                sorted_players = Report().sort_players(Report().players, by_rank=True)
                                Report().display_players_report(players=sorted_players)
                            elif user_input == "1":
                                sorted_players = Report().sort_players(Report().players, by_rank=False)
                                Report().display_players_report(players=sorted_players)

                    elif user_input == "1":
                        Report().display_tournaments_reports()
            else:
                quit()

        # Play turnament
        print()
        user_input = self.get_user_entry(
            msg_display="Que faire ?\n"
                        "0 - Jouer le tournoi\n"
                        "q - Quitter\n> ",
            msg_error="Veuillez entrer une valeur valide",
            value_type="selection",
            assertions=["0", "q"]
        )

        # results are registred in the end of the current turnament

        if user_input == "0":
            rankings = play_tournament(tournament, new_tournament_loaded=True)
        else:
            quit()

        # Display results
        print()
        print(f"Tournoi {tournament.name} terminé !\nRésultats:")
        for i, player in enumerate(rankings):
            print(f"{str(i + 1)} - {player}")

        # Update raking
        print()
        user_input = self.get_user_entry(
            msg_display="Mise à jour des classements\n"
                        "0 - Automatiquement\n"
                        "1 - Manuellement\n"
                        "q - Quitter\n> ",
            msg_error="Veuillez entrer une valeur valide",
            value_type="selection",
            assertions=["0", "1", "q"]
        )
        if user_input == "0":
            for i, player in enumerate(rankings):
                print(f'Name:{player.name} {player.first_name}')
                # update_rankings(player, i + 1)

        elif user_input == "1":
            for player in rankings:
                rank = self.get_user_entry(
                    msg_display=f"Rang de {player}:\n> ",
                    msg_error="Veuillez entrer un nombre entier.",
                    value_type="numeric"
                )
                update_rankings(player, rank)

        else:
            quit()
