"""
    Ce fichier regroupe les fonctions associées à l'application
    des règles du jeu
"""

# Modules internes
import carte
import dalle
import grenouille
import interaction
import joueur
import plateau

#########################
# Fonctions utilitaires #
#########################
def renvoie_joueur_suivant(plateau_croa, joueur_actif):
    """
       Renvoie le joueur qui succèdant à un joueur donné.
       Entrées:
         * plateau_croa: liste
           Le plateau de jeu
         * joueur_actif: liste
           Le joueur cédant son tour
       Sortie:
         * joueur_suivant: liste
           Le joueur actif du prochain tour

       Note:
         S'il y a moins de deux joueurs dans la liste de joueurs du
         plateau la fonction renvoie le joueur donné en entrée. Il peut arriver
         que la liste de joueurs soit vide si le joueur actif élimine la dernière
         reine adverse sur sa case de départ carte retournée, cette carte étant
         un brochet!
    """
    liste_joueurs = plateau.renvoie_liste_joueurs(plateau_croa)
    nombre_joueurs_en_jeu = len(liste_joueurs)
    if nombre_joueurs_en_jeu < 2:
        return(joueur_actif)
    # Trouve l'indice du joueur actif dans la liste de joueurs
    for j in range(nombre_joueurs_en_jeu):
        if liste_joueurs[j] == joueur_actif:
            # Le prochain joueur dans la liste est le joueur suivant
            # La liste est circulaire: le joueur à la position 0 est le suivant
            # du joueur à la position nombre_joueurs_en_jeu-1
            joueur_suivant = liste_joueurs[(j + 1) % nombre_joueurs_en_jeu]
            break
    return(joueur_suivant)

############################################
# Fonctions implémentant les règles du jeu #
############################################
def applique_nenuphar(plateau_croa, joueur_actif, numero_dalle_depart, numero_dalle_arrivee, choix_reine):
    """
       Applique la règle associée à la carte nénuphar: la grenouille doit changer
       de dalle sans revenir sur ses pas sauf si c'est la seule possibilité
       Entrées:
         * plateau_croa: liste
           Le plateau de jeu
         * joueur_actif: liste
           Le joueur dont c'est le tour de jouer
         * numero_dalle_depart: entier
           Le numéro de la dalle de départ
         * numero_dalle_arrivee: entier
           Le numéro de la dalle d'arrivée
         * choix_reine: booléen
           Drapeau indiquant si le joueur joue sa reine (True) ou une
           servante (False)
       Sorties:
         * joueur_suivant: liste
           Le joueur suivant
         
       Notes:
         Le joueur suivant est obigatoirement identique au joueur actif car il est
         interdit de rester sur une dalle nénuphar.
         Cette fonction marque la dalle de départ pour que le joueur actif ne
         puisse pas la choisir comme destination au prochain tour sauf s'il y est
         contraint.
         Le plateau de jeu est modifié à la sortie de la fonction.
    """
    # La dalle de départ est marquée par l'identifiant du joueur actif pour
    # qu'il ne puisse pas la choisir au prochain tour sauf si obligation
    dalle_depart = plateau.renvoie_dalle(plateau_croa, numero_dalle_depart)
    identifiant_joueur_actif = joueur.renvoie_identifiant(joueur_actif)
    dalle.modifie_dernier_occupant(dalle_depart, identifiant_joueur_actif)
    plateau.modifie_dalle(plateau_croa, numero_dalle_depart, dalle_depart)
    # La dalle d'arrivée est enrichie d'une grenouille du joueur actif
    dalle_arrivee = plateau.renvoie_dalle(plateau_croa, numero_dalle_arrivee)
    # La grenouille passe en priorité 2 pour être forcément jouée au tours suivant
    nouvelle_grenouille = grenouille.cree(identifiant_joueur_actif, choix_reine, 2)
    plateau.depose_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle_arrivee, nouvelle_grenouille)
    # Pas de modification du joueur actif puisqu'il est obligé de rejouer
    return(joueur_actif)

def applique_roseaux(plateau_croa, joueur_actif, numero_dalle_arrivee, choix_reine):
    """
       Applique la règle associée à la carte roseaux: le joueur passe la main
       Entrées:
         * plateau_croa: liste
           Le plateau de jeu
         * joueur_actif: liste
           Le joueur dont c'est le tour de jouer
         * numero_dalle_arrivee: entier
           Le numéro de la dalle d'arrivée
         * choix_reine: booléen
           Drapeau indiquant si le joueur joue sa reine (True) ou une
           servante (False)
       Sorties:
         * joueur_suivant: liste
           Le joueur suivant
         
       Notes:
         Le plateau de jeu est modifié à la sortie de la fonction.
    """
    identifiant_joueur_actif = joueur.renvoie_identifiant(joueur_actif)
    # Ajoute la grenouille à la dalle
    nouvelle_grenouille = grenouille.cree(identifiant_joueur_actif, choix_reine, 1)
    plateau.depose_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle_arrivee, nouvelle_grenouille)
    # Passe au joueur suivant
    return(renvoie_joueur_suivant(plateau_croa, joueur_actif))

def applique_moustique(plateau_croa, joueur_actif, numero_dalle_depart, numero_dalle_arrivee, choix_reine):
    """
       Applique la règle associée à la carte moustique: le joueur peut rester en
       jeu s'il choisit de bouger une autre grenouille, sinon il rend la main
       Entrées:
         * plateau_croa: liste
           Le plateau de jeu
         * joueur_actif: liste
           Le joueur dont c'est le tour de jouer
         * numero_dalle_depart: entier
           Le numéro de la dalle de départ
         * numero_dalle_arrivee: entier
           Le numéro de la dalle d'arrivée
         * choix_reine: booléen
           Drapeau indiquant si le joueur joue sa reine (True) ou une
           servante (False)
       Sorties:
         * joueur_suivant: liste
           Le joueur suivant
         
       Notes:
         Si le joueur choisit de rester dans le jeu il ne peut pas bouger une
         nouvelle fois la même grenouille, qui se voit donc attribuer une
         priorité 0.
         Le plateau de jeu est modifié à la sortie de la fonction.
    """
    identifiant_joueur_actif = joueur.renvoie_identifiant(joueur_actif)
    # On commence par mettre à jour le plateau pour qu'il soit affiché dans le bon
    # état au moment du choix
    nouvelle_grenouille = grenouille.cree(identifiant_joueur_actif, choix_reine, 1)
    plateau.depose_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle_arrivee, nouvelle_grenouille)
    # Regarde s'il y a une autre grenouille du joueur actif qui peut être jouée
    autre_grenouilles_disponibles = False
    dalles = plateau.renvoie_liste_dalles(plateau_croa)
    for numero_dalle in range(len(dalles)):
        if numero_dalle != numero_dalle_arrivee:
            grenouilles = dalle.renvoie_liste_grenouilles(dalles[numero_dalle])
            for g in grenouilles:
                identifiant = grenouille.renvoie_identifiant(g)
                priorite = grenouille.renvoie_priorite(g)
                autre_grenouilles_disponibles = (identifiant == identifiant_joueur_actif) and priorite != 0
                # On sort de la boucle sur les grenouilles de la dalle
                if autre_grenouilles_disponibles:
                    break
        # On sort de la boucle sur les dalles
        if autre_grenouilles_disponibles:
            break
    # Choisis de jouer une autre grenouille s'il y en a une de disponible sur une
    # ature dalle
    if autre_grenouilles_disponibles:
        choix = interaction.choisis(plateau_croa, joueur_actif, "Voulez-vous jouer une autre grenouille?", interaction.OUI, interaction.NON, True)
        # Si on joue une nouvelle grenouille il faut desactiver la grenouille de la dalle courante
        # Ajoute la grenouille à la dalle
        if choix:
            grenouille.modifie_priorite(nouvelle_grenouille, 0)
            plateau.depose_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle_arrivee, nouvelle_grenouille)
            return(joueur_actif)
    # Passe au joueur suivant
    return(renvoie_joueur_suivant(plateau_croa, joueur_actif))

def applique_male(plateau_croa, joueur_actif, couleur_male, numero_dalle_depart, numero_dalle_arrivee, choix_reine):
    """
       Applique la règle associée à la carte mâle: le joueur gagne une servante
       sur la dalle d'arrivée si c'est sa reine qui est arrivée sur la dalle et
       qu'il reste le jeton mâle de la bonne couleur au joueur
       Entrées:
         * plateau_croa: liste
           Le plateau de jeu
         * joueur_actif: liste
           Le joueur dont c'est le tour de jouer
         * couleur_male: entier
           La couleur du mâle présent sur la dalle, entre carte.MALE_BLEU et
           carte.MALE_VIOLET
         * numero_dalle_depart: entier
           Le numéro de la dalle de départ
         * numero_dalle_arrivee: entier
           Le numéro de la dalle d'arrivée
         * choix_reine: booléen
           Drapeau indiquant si le joueur joue sa reine (True) ou une
           servante (False)
       Sorties:
         * joueur_suivant: liste
           Le joueur suivant
         
       Notes:
         Si la reine a pu se reproduire, elle passe en priorité 2 ainsi que sa
         nouvelle servante. Le pion mâle est retiré uniquement si la reine a pu
         se reproduire. Comme il n'y a aucun moyen de renouveler le stock de
         grenouillles en réserve, de toute façon le jeton est devenu inutile.
         Le plateau de jeu est modifié à la sortie de la fonction.
    """
    identifiant_joueur_actif = joueur.renvoie_identifiant(joueur_actif)
    # C'est la reine qui arrive sur la dalle
    if choix_reine:
        # Elle peut se reproduire avec le mâle
        nombre_grenouilles_reserve = joueur.renvoie_nombre_grenouilles_reserve(joueur_actif)
        if nombre_grenouilles_reserve > 0 and \
           joueur.possede_jeton(joueur_actif, couleur_male):
            # Crée la reine sur la dalle en priorité 2
            reine = grenouille.cree(identifiant_joueur_actif, True, 2)
            plateau.depose_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle_arrivee, reine)
            # Crée la servante sur la dalle en priorité 2
            servante = grenouille.cree(identifiant_joueur_actif, False, 2)
            plateau.ajoute_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle_arrivee, servante)
            # Supprime le jeton de la liste du joueur actif
            jetons = joueur.renvoie_liste_jetons(joueur_actif)
            nouveaux_jetons = []
            for j in jetons:
                if j != couleur_male:
                    nouveaux_jetons.append(j)
            joueur.modifie_liste_jetons(joueur_actif, nouveaux_jetons)
            # Supprime une servante de la réserve
            joueur.modifie_nombre_grenouilles_reserve(joueur_actif, nombre_grenouilles_reserve - 1)
            # Passe au joueur suivant
            joueur_suivant = renvoie_joueur_suivant(plateau_croa, joueur_actif)
        # Elle ne peut pas se reproduire avec le mâle
        else:
            # Crée la reine sur la dalle en priorité 1
            reine = grenouille.cree(identifiant_joueur_actif, True, 1)
            plateau.depose_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle_arrivee, reine)
    # C'est une servante qui est arrivée sur la dalle
    else:
        servante = grenouille.cree(identifiant_joueur_actif, False, 1)
        plateau.depose_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle_arrivee, servante)
    return(renvoie_joueur_suivant(plateau_croa, joueur_actif))

def applique_vase(plateau_croa, joueur_actif, numero_dalle_depart, numero_dalle_arrivee, choix_reine):
    """
       Applique la règle associée à la carte vase: le joueur passe la main et
       sa grenouille reste inactive pour un tour
       Entrées:
         * plateau_croa: liste
           Le plateau de jeu
         * joueur_actif: liste
           Le joueur dont c'est le tour de jouer
         * numero_dalle_depart: entier
           Le numéro de la dalle de départ
         * numero_dalle_arrivee: entier
           Le numéro de la dalle d'arrivée
         * choix_reine: booléen
           Drapeau indiquant si le joueur joue sa reine (True) ou une
           servante (False)
       Sorties:
         * joueur_suivant: liste
           Le joueur suivant
         
       Notes:
         La grenouille passe en priorité 0 pour interdire sa sélection au tour
         suivant.
         Le plateau de jeu est modifié à la sortie de la fonction.
    """
    identifiant_joueur_actif = joueur.renvoie_identifiant(joueur_actif)
    # On désactive la grenouille de la dalle courante
    nouvelle_grenouille = grenouille.cree(identifiant_joueur_actif, choix_reine, 0)
    plateau.depose_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle_arrivee, nouvelle_grenouille)
    return(renvoie_joueur_suivant(plateau_croa, joueur_actif))

def applique_brochet(plateau_croa, joueur_actif, numero_dalle_depart, numero_dalle_arrivee, choix_reine):
    """
       Applique la règle associée à la carte brochet: la grenouille sort du jeu.
       Si c'est une reine, le joueur perd et toutes ses grenouilles sont retirées
       Entrées:
         * plateau_croa: liste
           Le plateau de jeu
         * joueur_actif: liste
           Le joueur dont c'est le tour de jouer
         * numero_dalle_depart: entier
           Le numéro de la dalle de départ
         * numero_dalle_arrivee: entier
           Le numéro de la dalle d'arrivée
         * choix_reine: booléen
           Drapeau indiquant si le joueur joue sa reine (True) ou une
           servante (False)
       Sorties:
         * joueur_suivant: liste
           Le joueur suivant
         
       Notes:
         Si le joueur actif sort du jeu, il est salué par un message d'au revoir.
         Il doit voir qu'il est arrivé sur une carte brochet pour comprendre
         pourquoi il sort du jeu.
         Le plateau de jeu est modifié à la sortie de la fonction.
    """    
    if choix_reine:
        identifiant_joueur_actif = joueur.renvoie_identifiant(joueur_actif)
        # Ajoute la grenouille à la dalle (juste pour l'affichage)
        nouvelle_grenouille = grenouille.cree(identifiant_joueur_actif, choix_reine, 1)
        plateau.depose_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle_arrivee, nouvelle_grenouille)
        # On choisi le joueur suivant avant de retirer le joueur actif pour avancer dans la liste des joueurs en jeu de manière naturelle
        joueur_suivant = renvoie_joueur_suivant(plateau_croa, joueur_actif)
        # Au revoir au joueur actif!
        interaction.affiche_message(plateau_croa, joueur_actif, "Au revoir " + joueur.renvoie_nom(joueur_actif))
        plateau.retire_joueur(plateau_croa, joueur_actif)
    else:
        joueur_suivant = renvoie_joueur_suivant(plateau_croa, joueur_actif)
    return(joueur_suivant)

def applique_rondin(plateau_croa, joueur_actif, numero_dalle_depart, numero_dalle_arrivee, choix_reine):
    """
       Applique la règle associée à la carte rondin: si la grenouille est une
       reine elle fait sortir du jeu les éventuelles grenouilles présentes sur le
       rondin, qui appartiennent obligatoirement à d'autres joueurs sinon la dalle
       n'aurait pas pu être sélectionnée. Si la grenouille est une servante elle
       rejoint les grenouilles présentent sur le rondin en éliminant
       éventuellement une des deux grenouilles si le rondin est déjà occupé par
       deux servantes.
       Entrées:
         * plateau_croa: liste
           Le plateau de jeu
         * joueur_actif: liste
           Le joueur dont c'est le tour de jouer
         * numero_dalle_depart: entier
           Le numéro de la dalle de départ
         * numero_dalle_arrivee: entier
           Le numéro de la dalle d'arrivée
         * choix_reine: booléen
           Drapeau indiquant si le joueur joue sa reine (True) ou une
           servante (False)
       Sorties:
         * joueur_suivant: liste
           Le joueur suivant
         
       Notes:
         On adopte le principe qu'une servante ne peut pas éliminer une autre
         servante du même joueur.
         Le plateau de jeu est modifié à la sortie de la fonction.
    """
    identifiant_joueur_actif = joueur.renvoie_identifiant(joueur_actif)
    if choix_reine:
        nouvelle_grenouille = grenouille.cree(identifiant_joueur_actif, choix_reine, 1)
        plateau.depose_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle_arrivee, nouvelle_grenouille)
    else:
        dalle_arrivee = plateau.renvoie_dalle(plateau_croa, numero_dalle_arrivee)
        grenouilles = dalle.renvoie_liste_grenouilles(dalle_arrivee)
        # Si la dalle contient déjà deux grenouilles il faut choisir celle qui
        # doit être supprimée si les deux grenouilles déjà présentes appartiennent
        # à des joueurs différents entre eux et différents du joueur actif
        if len(grenouilles) == 2:
            grenouille_gauche = grenouilles[0]
            identifiant_gauche = grenouille.renvoie_identifiant(grenouille_gauche)
            grenouille_droite = grenouilles[1]
            identifiant_droite = grenouille.renvoie_identifiant(grenouille_droite)
            # Les deux grenouilles présentes appartiennent au même joueur
            # On ne garde que la grenouille de gauche (0)
            if identifiant_gauche == identifiant_droite:
                grenouilles = [grenouille_gauche]
            # Seule la grenouille de gauche appartient au joueur actif
            # On la garde
            elif identifiant_gauche == identifiant_joueur_actif:
                grenouilles = [grenouille_gauche]
            # Seule la grenouille de droite appartient au joueur actif
            # On la garde
            elif identifiant_droite == identifiant_joueur_actif:
                grenouilles = [grenouille_droite]
            # Les grenouilles appartiennent à des joueurs différents
            # et aucune n'appartient au joueur actif
            else:
                carte_rondin = dalle.renvoie_carte(dalle_arrivee)
                dalle_gauche = dalle.cree(carte_rondin, [grenouille_gauche], -1)
                dalle_droite = dalle.cree(carte_rondin, [grenouille_droite], -1)
                choix = interaction.choisis(plateau_croa, joueur_actif, "Quelle grenouille supprimer?", dalle_gauche, dalle_droite, False)
                if choix:
                    grenouilles = [grenouilles[1]]
                else:
                    grenouilles = [grenouilles[0]]
        # On ajoute la nouvelle grenouille
        nouvelle_grenouille = grenouille.cree(identifiant_joueur_actif, choix_reine, 1)
        grenouilles.append(nouvelle_grenouille)
        dalle.modifie_liste_grenouilles(dalle_arrivee, grenouilles)
        plateau.modifie_dalle(plateau_croa, numero_dalle_arrivee, dalle_arrivee)
    # On passe au joueur suivant
    return(renvoie_joueur_suivant(plateau_croa, joueur_actif))

def applique(plateau_croa, joueur_actif, numero_dalle_depart, numero_dalle_arrivee, choix_reine):
    """
       Applique les règles du jeu: d'abord les règles prioritaires puis les règles
       de la carte présente sur la dalle d'arrivée
       Entrées:
         * plateau_croa: liste
           Le plateau de jeu
         * joueur_actif: liste
           Le joueur dont c'est le tour de jouer
         * numero_dalle_depart: entier
           Le numéro de la dalle de départ
         * numero_dalle_arrivee: entier
           Le numéro de la dalle d'arrivée
         * choix_reine: booléen
           Drapeau indiquant si le joueur joue sa reine (True) ou une
           servante (False)
       Sorties:
         * joueur_suivant: liste
           Le joueur suivant
         
       Notes:
         Les règles appliquées sont celles disponible sur le site suivant:
         https://www.origames.fr/croa/
         Il y a plusieurs points obscurs ou contradictoires dans les règles:
           * Est-ce qu'une servante créée à l'occasion de la capture d'une reine
             adverse par une servant peut rejoindre sa reine si elle est sur une
             dalle de carte rondin face visible?
             -> on décide que non
           * Est-ce qu'une servante peut éliminer une servante de son camp en
             arrivant sur un rondin?
             -> on décide que non, en particulier une servante ne peut pas aller
             sur un rondin déjà occupé par deux servantes de son camp
           * Que se passe-t'il lorsqu'une reine élimine la dernière reine adverse
             qui n'a pas bougé de sa dalle de départ et dont la carte est un
             brochet face cachée?
             -> on décide que l'élimination de la reine adverse prime sur la perte
             de sa propre reine à cause du brochet
         Concernant le devenir des servantes capturées, après lecture de
         https://www.trictrac.net/forum/sujet/croa-quelques-questions
         on prend le parti de les remettre dans la réserve de leurs joueurs
         respectifs
         Le plateau de jeu est modifié à la sortie de la fonction.
    """
    # Réinitialisation du dernier occupant de toutes les dalles
    plateau.reinitialise_dernier_occupant(plateau_croa)
    # Récupère la dalle d'arrivée
    dalle_arrivee = plateau.renvoie_dalle(plateau_croa, numero_dalle_arrivee)
    # Si la dalle d'arrivée contient une reine, élimination!
    identifiant_joueur_actif = joueur.renvoie_identifiant(joueur_actif)
    identifiant_reine = dalle.renvoie_identifiant_autre_reine(dalle_arrivee, identifiant_joueur_actif)
    # Un joueur est éliminé
    if identifiant_reine != identifiant_joueur_actif:
        joueur_elimine = plateau.renvoie_joueur(plateau_croa, identifiant_reine)
        # Ajoute la grenouille à la dalle
        # Si le joueur actif a encore une servante en réserve
        # Alors il y aura sa reine et une servante sur la case: elles auront
        # donc une priorité 2
        # Sinon la grenouille arrivant sur la case sera en priorité 1
        nombre_grenouilles_reserve = joueur.renvoie_nombre_grenouilles_reserve(joueur_actif)
        priorite_2 = choix_reine and nombre_grenouilles_reserve > 0
        # Si le joueur actif a joué sa reine et possède encore une grenouille en
        # réserve alors la servante est crée sur la dalle en priorité 2
        # La servante est créée après le message d'au revoir, comme conséquence
        # du coup joué
        if priorite_2:
            nouvelle_grenouille = grenouille.cree(identifiant_joueur_actif, choix_reine, 2)
        # Si c'est une servante qui vient d'éliminer une reine adverse
        else:
            nouvelle_grenouille = grenouille.cree(identifiant_joueur_actif, choix_reine, 2)
        plateau.depose_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle_arrivee, nouvelle_grenouille)
        # On dit au revoir au joueur éliminé
        interaction.affiche_message(plateau_croa, joueur_elimine, "Au revoir " + joueur.renvoie_nom(joueur_elimine))
        # On supprime les grenouilles du joueur éliminé
        plateau.retire_joueur(plateau_croa, joueur_elimine)
        # On ajoute une servante sur la case de la reine
        # Cas facile: le joueur actif a joué sa reine et possède une grenouille
        # en réserve, on crée la servante qui accompagne la reine
        if priorite_2:
            nouvelle_grenouille = grenouille.cree(identifiant_joueur_actif, False, 2)
            plateau.ajoute_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle_arrivee, nouvelle_grenouille)
            joueur.modifie_nombre_grenouilles_reserve(joueur_actif, nombre_grenouilles_reserve - 1)
        # La reine se trouve sur une autre case et il reste des grenouilles
        elif nombre_grenouilles_reserve > 0:
            numero_dalle = plateau.trouve_reine(plateau_croa, joueur_actif)
            nouvelle_grenouille = grenouille.cree(identifiant_joueur_actif, False, 2)
            plateau.ajoute_une_grenouille_sur_une_dalle(plateau_croa, numero_dalle, nouvelle_grenouille)
            joueur.modifie_nombre_grenouilles_reserve(joueur_actif, nombre_grenouilles_reserve - 1)
        # On passe au joueur suivant (éventuellement le joueur actif)
        return(renvoie_joueur_suivant(plateau_croa, joueur_actif))
    # Ainsi que sa carte
    carte_arrivee = dalle.renvoie_carte(dalle_arrivee)
    # Afin de lire sa face
    face_carte = carte.renvoie_face(carte_arrivee)
    # Mets la carte de la dalle face visible
    carte.modifie_face_visible(carte_arrivee, True)
    # Supprime les grenouilles présentes sur une dalle dont la carte n'est pas un rondin
    # Chaque grenouille retourne dans la réserve du joueur auquel elle appartient
    if face_carte != carte.RONDIN:
        grenouilles = dalle.renvoie_liste_grenouilles(dalle_arrivee)
        for g in grenouilles:
            identifiant_grenouille = grenouille.renvoie_identifiant(g)
            joueur_grenouille = plateau.renvoie_joueur(plateau_croa, identifiant_grenouille)
            nombre_grenouilles = joueur.renvoie_nombre_grenouilles_reserve(joueur_grenouille)
            # On ajoute une grenouille à la réserve du joueur dont la grenouille a été sortie du jeu
            joueur.modifie_nombre_grenouilles_reserve(joueur_grenouille, nombre_grenouilles + 1)
        dalle.modifie_liste_grenouilles(dalle_arrivee, [])
        plateau.modifie_dalle(plateau_croa, numero_dalle_arrivee, dalle_arrivee)
    # Modifie l'état du jeu selon la carte
    if face_carte == carte.NENUPHAR:
        joueur_suivant = applique_nenuphar(plateau_croa, joueur_actif, numero_dalle_depart, numero_dalle_arrivee, choix_reine)
    if face_carte == carte.ROSEAUX:
        joueur_suivant = applique_roseaux(plateau_croa, joueur_actif, numero_dalle_arrivee, choix_reine)
    if face_carte == carte.MOUSTIQUE:
        joueur_suivant = applique_moustique(plateau_croa, joueur_actif, numero_dalle_depart, numero_dalle_arrivee, choix_reine)
    if face_carte >= carte.MALE_BLEU and face_carte <= carte.MALE_VIOLET:
        joueur_suivant = applique_male(plateau_croa, joueur_actif, face_carte, numero_dalle_depart, numero_dalle_arrivee, choix_reine)
    if face_carte == carte.VASE:
        joueur_suivant = applique_vase(plateau_croa, joueur_actif, numero_dalle_depart, numero_dalle_arrivee, choix_reine)
    if face_carte == carte.BROCHET:
        joueur_suivant = applique_brochet(plateau_croa, joueur_actif, numero_dalle_depart, numero_dalle_arrivee, choix_reine)
    if face_carte == carte.RONDIN:
        joueur_suivant = applique_rondin(plateau_croa, joueur_actif, numero_dalle_depart, numero_dalle_arrivee, choix_reine)
    # Mets à jour les priorités maximales des différents joueurs encore en jeu
    plateau.actualise_priorites_maximales(plateau_croa)
    return(joueur_suivant)
