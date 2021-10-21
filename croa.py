"""
   Ce fichier est l'entrée principale du jeu Croâ
   développé par la Team Alice, Cécile, Maud
"""
# Modules internes
import graphique
import interaction
import joueur
import plateau
import regles

# Booléen indiquant si l'on continue le jeu
continuer_jeu = True
# Initialise la fenêtre graphique
graphique.IMAGE_PLATEAU = plateau.dessine(plateau.cree([]))
graphique.initialise(graphique.IMAGE_PLATEAU)
while continuer_jeu:
    # On initialise les joueurs
    joueurs = interaction.definis_joueurs()
    # Création du plateau pour la partie en cours
    plateau_croa = plateau.cree(joueurs)
    # Sélection du premier joueur
    joueur_actif = joueurs[0]
    # Boucle sur la partie, gérant les évolutions du jeu
    partie_terminee = False
    # Boucle sur la partie
    while not partie_terminee:
        # Mise à jour de l'image de référence du plateau
        graphique.IMAGE_PLATEAU = plateau.dessine(plateau_croa)
        graphique.rafraichit(graphique.IMAGE_PLATEAU)
        # Si le joueur actif ne peut pas jouer, passage au joueur suivant
        if joueur.renvoie_priorite_maximale(joueur_actif) == 0:
            # Le joueur n'a que des grenouilles en priorité 0, on réveille ses
            # grenouilles et on passe au joueur suivant
            plateau.reveille_grenouilles(plateau_croa, joueur_actif)
            joueur_actif = regles.renvoie_joueur_suivant(plateau_croa, joueur_actif)
        # Le joueur actif peut jouer
        else:
            # Choix de la dalle de départ
            numero_dalle_depart, choix_reine = interaction.choisis_grenouille(plateau_croa, joueur_actif)
            plateau.reveille_grenouilles(plateau_croa, joueur_actif)
            # Choix de la dalle d'arrivee
            numero_dalle_arrivee = interaction.selectionne_dalle_arrivee(plateau_croa, joueur_actif, numero_dalle_depart, choix_reine)
            # Application des règles correspondant à la dalle d'arrivée
            joueur_actif = regles.applique(plateau_croa, joueur_actif, numero_dalle_depart, numero_dalle_arrivee, choix_reine)
            # La partie est terminée s'il ne reste plus qu'un joueur
            partie_terminee = len(plateau.renvoie_liste_joueurs(plateau_croa)) < 2
    interaction.affiche_message(plateau_croa, joueur_actif, "Bravo " + joueur.renvoie_nom(joueur_actif) + "!")
    continuer_jeu = interaction.choisis(plateau_croa, joueur_actif, "Voulez-vous continuer à jouer?", interaction.OUI, interaction.NON, True)
