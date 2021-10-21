"""
    Ce fichier regroupe les structures et les services associés
    à la création et à l'évolution du plateau
"""
# Modules externes
import numpy as np

# Modules internes
import carte
import dalle
import graphique
import grenouille
import joueur


# Les dalles du plateau ne commencent pas au bord mais sont
# décalées de la même valeur en x et y
DECALAGE = 195
# Les coins supérieur gauche des dalles sont distants de leurs
# voisins horizontaux de (pas, 0) et verticaux de (0, pas)
PAS = 179

def cree(liste_joueurs):
    """
       Crée la structure de données associée à un plateau dans son
       état initial.
       Entrées:
         * liste_joueurs: liste
           La liste des joueurs initialement dans le jeu.
       Sorties:
         * plateau: liste
           Une liste [liste_joueurs, liste_dalles]

       Notes:
         La liste des dalles est construite partiellement à partir de la liste
         des joueurs puisque le nombre de joueurs détermine leur position initiale.
    """
    # Création des cartes
    liste_cartes = []
    for i in range(6):
        liste_cartes.append(carte.cree(carte.NENUPHAR   , carte.EAU_PEU_PROFONDE))
    for i in range(4):
        liste_cartes.append(carte.cree(carte.NENUPHAR   , carte.EAU_PROFONDE_1  ))
    for i in range(4):
        liste_cartes.append(carte.cree(carte.NENUPHAR   , carte.EAU_PROFONDE_2  ))
    for i in range(10):
        liste_cartes.append(carte.cree(carte.ROSEAUX    , carte.EAU_PEU_PROFONDE))
    for i in range(3):
        liste_cartes.append(carte.cree(carte.ROSEAUX    , carte.EAU_PROFONDE_1  ))
    for i in range(3):
        liste_cartes.append(carte.cree(carte.ROSEAUX    , carte.EAU_PROFONDE_2  ))
    for i in range(4):
        liste_cartes.append(carte.cree(carte.MOUSTIQUE  , carte.EAU_PEU_PROFONDE))
    for i in range(2):
        liste_cartes.append(carte.cree(carte.MOUSTIQUE  , carte.EAU_PROFONDE_1  ))
    for i in range(2):
        liste_cartes.append(carte.cree(carte.MOUSTIQUE  , carte.EAU_PROFONDE_2  ))
    liste_cartes.append(carte.cree(carte.MALE_BLEU  , carte.EAU_PEU_PROFONDE))
    liste_cartes.append(carte.cree(carte.MALE_BLEU  , carte.EAU_PROFONDE_1  ))
    liste_cartes.append(carte.cree(carte.MALE_JAUNE , carte.EAU_PEU_PROFONDE))
    liste_cartes.append(carte.cree(carte.MALE_JAUNE , carte.EAU_PROFONDE_1  ))
    liste_cartes.append(carte.cree(carte.MALE_ORANGE, carte.EAU_PEU_PROFONDE))
    liste_cartes.append(carte.cree(carte.MALE_ORANGE, carte.EAU_PROFONDE_1  ))
    liste_cartes.append(carte.cree(carte.MALE_ROSE  , carte.EAU_PEU_PROFONDE))
    liste_cartes.append(carte.cree(carte.MALE_ROSE  , carte.EAU_PROFONDE_2  ))
    liste_cartes.append(carte.cree(carte.MALE_VERT  , carte.EAU_PEU_PROFONDE))
    liste_cartes.append(carte.cree(carte.MALE_VERT  , carte.EAU_PROFONDE_2  ))
    liste_cartes.append(carte.cree(carte.MALE_VIOLET, carte.EAU_PEU_PROFONDE))
    liste_cartes.append(carte.cree(carte.MALE_VIOLET, carte.EAU_PROFONDE_2  ))
    for i in range(4):
        liste_cartes.append(carte.cree(carte.VASE       , carte.EAU_PEU_PROFONDE))
    for i in range(2):
        liste_cartes.append(carte.cree(carte.BROCHET    , carte.EAU_PROFONDE_1  ))
    for i in range(2):
        liste_cartes.append(carte.cree(carte.BROCHET    , carte.EAU_PROFONDE_2  ))
    for i in range(2):
        liste_cartes.append(carte.cree(carte.RONDIN     , carte.EAU_PEU_PROFONDE))
    for i in range(2):
        liste_cartes.append(carte.cree(carte.RONDIN     , carte.EAU_PROFONDE_1  ))
    for i in range(2):
        liste_cartes.append(carte.cree(carte.RONDIN     , carte.EAU_PROFONDE_2  ))
    # Création des dalles
    liste_dalles = [dalle.cree(c, [], -1) for c in liste_cartes]
    # Mélange des dalles
    np.random.seed()
    np.random.shuffle(liste_dalles)
    # Position initiale des grenouilles en fonction du nombre de joueurs
    nombre_joueurs = len(liste_joueurs)
    if nombre_joueurs == 2:
        liste_dalles[0][1]  = [grenouille.cree(0, True,  1)]
        liste_dalles[1][1]  = [grenouille.cree(0, False, 1)]
        liste_dalles[8][1]  = [grenouille.cree(0, False, 1)]
        liste_dalles[63][1] = [grenouille.cree(1, True,  1)]
        liste_dalles[62][1] = [grenouille.cree(1, False, 1)]
        liste_dalles[55][1] = [grenouille.cree(1, False, 1)]
    elif nombre_joueurs == 3:
        liste_dalles[48][1] = [grenouille.cree(0, False, 1)]
        liste_dalles[56][1] = [grenouille.cree(0, True,  1)]
        liste_dalles[57][1] = [grenouille.cree(0, False, 1)]
        liste_dalles[30][1] = [grenouille.cree(1, False, 1)]
        liste_dalles[39][1] = [grenouille.cree(1, True,  1)]
        liste_dalles[46][1] = [grenouille.cree(1, False, 1)]
        liste_dalles[0][1]  = [grenouille.cree(2, True,  1)]
        liste_dalles[1][1]  = [grenouille.cree(2, False, 1)]
        liste_dalles[8][1]  = [grenouille.cree(2, False, 1)]
    elif nombre_joueurs == 4:
        liste_dalles[6][1]  = [grenouille.cree(0, False, 1)]
        liste_dalles[7][1]  = [grenouille.cree(0, True,  1)]
        liste_dalles[15][1] = [grenouille.cree(0, False, 1)]
        liste_dalles[55][1] = [grenouille.cree(1, False, 1)]
        liste_dalles[62][1] = [grenouille.cree(1, False, 1)]
        liste_dalles[63][1] = [grenouille.cree(1, True,  1)]
        liste_dalles[48][1] = [grenouille.cree(2, False, 1)]
        liste_dalles[56][1] = [grenouille.cree(2, True,  1)]
        liste_dalles[57][1] = [grenouille.cree(2, False, 1)]
        liste_dalles[0][1]  = [grenouille.cree(3, True,  1)]
        liste_dalles[1][1]  = [grenouille.cree(3, False, 1)]
        liste_dalles[8][1]  = [grenouille.cree(3, False, 1)]
    return([liste_joueurs, liste_dalles])

def renvoie_liste_joueurs(plateau):
    """
       Renvoie la liste des joueurs du plateau
       Entrées:
         * plateau: liste
           Le plateau à consulter
       Sorties:
         * liste_joueurs: liste
           La liste des joueurs encore en jeu du plateau.
    """
    return(plateau[0])

def modifie_liste_joueurs(plateau, liste_joueurs):
    """
       Modifie la liste des joueurs du plateau
       Entrées:
         * plateau: liste
           Le plateau à modifier
         * liste_joueurs: liste
           La nouvelle liste de joueurs du plateau

       Notes:
         Le plateau est modifié à la sortie de la fonction.
    """
    plateau[0] = liste_joueurs

def renvoie_joueur(plateau, identifiant):
    """
       Renvoie le joueur du plateau correspondant à l'identifiant donné.
       Entrées:
         * plateau: liste
           Le plateau à consulter
         * identifiant: entier
           L'identifiant du joueur cherché
       Sorties:
         * joueur: liste
           Le joueur correspondant à l'identifiant donné

       Notes:
         La fonction fait l'hypothèse que l'identifiant donné correspond bien à
         un joueur de la liste de joueurs du plateau donné.
         Un message d'erreur est affiché dans le cas contraire, et la fonction
         renvoie une liste vide.
    """
    for j in plateau[0]:
        if joueur.renvoie_identifiant(j) == identifiant:
            return(j)
    # Ne devrait jamais arriver là
    print("Erreur dans plateau.renvoie_joueur, identifiant=", identifiant, "inconnu")
    return([])

def retire_joueur(plateau, joueur_a_retirer):
    """
       Retire le joueur donné de la liste des joueurs du plateau donné
       ainsi que toutes ses grenouilles des dalles du plateau.
       Entrées:
         * plateau: liste
           Le plateau à modifier
         * joueur_a_retirer: liste
           Le joueur à retirer du plateau donné.

       Notes:
         Le retrait d'un joueur consiste à retirer le joueur donné de la liste
         des joueurs du plateau donné, mais également ses grenouilles des listes
         de grenouilles des dalles du plateau.
         Le plateau est modifié à la sortie de la fonction.
    """
    identifiant_joueur_a_retirer = joueur.renvoie_identifiant(joueur_a_retirer)
    # On retire d'abord les grenouilles du joueur de toutes les dalles
    for i in range(len(plateau[1])):
        grenouilles = dalle.renvoie_liste_grenouilles(plateau[1][i])
        nouvelles_grenouilles = []
        for g in grenouilles:
            # Si la grenouille n'appartient pas au joueur à retirer on la conserve
            if grenouille.renvoie_identifiant(g) != identifiant_joueur_a_retirer:
                nouvelles_grenouilles.append(g)
        dalle.modifie_liste_grenouilles(plateau[1][i], nouvelles_grenouilles)
    # On retire ensuite le joueur de la liste des joueurs du plateau
    nouveaux_joueurs = []
    for i in range(len(plateau[0])):
        if joueur.renvoie_identifiant(plateau[0][i]) != identifiant_joueur_a_retirer:
            nouveaux_joueurs.append(plateau[0][i])
    plateau[0] = nouveaux_joueurs

def actualise_priorites_maximales(plateau):
    """
       Mets à jour les priorités maximales des joueurs en jeu du plateau donné.
       Entrées:
         * plateau: liste
           Le plateau à modifier

       Notes:
         La mise à jour des priorités maximales consiste à modifier les joueurs
         encore en jeu dans le plateau donné en déterminant pour chacun des
         joueurs du plateau la plus grande priorité de ses grenouilles en jeu.
         Le calcul se fait en parcourant les dalles du plateau, et pour chaque
         dalle la liste de ses grenouilles. Chaque grenouille permet de mettre
         à jour la priorité maximale du joueur correspondant.
         Le plateau est modifié à la sortie de la fonction.       
    """
    nombre_joueurs = len(plateau[0])
    identifiants_joueurs = []
    priorites_maximales = []
    # Initialise la liste des identifiants des joueurs en jeu
    # et les nouvelles priorites maximales
    for i in range(nombre_joueurs):
        identifiants_joueurs.append(joueur.renvoie_identifiant(plateau[0][i]))
        priorites_maximales.append(0)
    # Parcours toutes les dalles
    for d in plateau[1]:
        grenouilles = dalle.renvoie_liste_grenouilles(d)
        # Pour chaque grenouille de la dalle
        for g in grenouilles:
            identifiant_grenouille = grenouille.renvoie_identifiant(g)
            priorite_grenouille = grenouille.renvoie_priorite(g)
            # Trouve à quel joueur appartient la grenouille
            for i in range(nombre_joueurs):
                if identifiants_joueurs[i] == identifiant_grenouille:
                    # Mets à jour la priorité maximale
                    priorites_maximales[i] = max(priorites_maximales[i], priorite_grenouille)
    # Mets à jour les priorités maximales
    for i in range(nombre_joueurs):
        joueur.modifie_priorite_maximale(plateau[0][i], priorites_maximales[i])

def renvoie_liste_dalles(plateau):
    """
       Renvoie la liste des dalles du plateau
       Entrées:
         * plateau: liste
           Le plateau à consulter
       Sorties:
         * liste_dalles: liste
           La liste des dalles du plateau.
    """
    return(plateau[1])

def modifie_liste_dalles(plateau, liste_dalles):
    """
       Modifie la liste des dalles du plateau
       Entrées:
         * plateau: liste
           Le plateau à modifier
         * liste_dalles: liste
           La nouvelle liste des dalles du plateau.

       Notes:
         Le plateau est modifié à la sortie de la fonction.
    """
    plateau[1] = liste_dalles

def renvoie_dalle(plateau, numero_dalle):
    """
       Renvoie la dalle du plateau en position numero_dalle
       Entrées:
         * plateau: liste
           Le plateau à consulter
         * numero_dalle: entier
           Le numéro de la dalle à renvoyer
       Sorties:
         * dalle: liste
           La dalle à la position numero_dalle dans la liste de dalles du plateau.
    """
    return(plateau[1][numero_dalle])

def modifie_dalle(plateau, numero_dalle, dalle):
    """
       Remplace la dalle du plateau en position numero_dalle par la dalle donnée
       Entrées:
         * plateau: liste
           Le plateau à modifier
         * numero_dalle: entier
           Le numéro de la dalle à modifier
         * dalle: liste
           La dalle devant remplacer la dalle du plateau à la position
           numero_dalle.

       Notes:
         Le plateau est modifié à la sortie de la fonction.
    """
    plateau[1][numero_dalle] = dalle

def reveille_grenouilles(plateau, joueur_actif):
    """
       Modifie la priorité des grenouilles du plateau appartenant au joueur actif.
       Entrées:
         * plateau: liste
           Le plateau à modifier
         * joueur_actif: liste
           Le joueur dont il faut modifier la priorité des grenouilles

       Notes:
         Mets toutes les grenouilles du joueur actif qui étaient en priorité 0 à
         la priorité 1 ou 2 selon le nombre de grenouilles du joueur sur la dalle.
         Il peut y avoir à la fois la reine et une servante sur la carte vase:
         + la reine dans l'état 0 car elle est tombée sur la carte vase il y a
           deux tours
         + la servante dans l'état 2 car elle vient d'être créée par l'élimination
           d'un autre joueur par le joueur actif au tour précédent
         Le plateau est modifié à la sortie de la fonction.
    """
    # Identifiant du joueur actif
    identifiant_joueur_actif = joueur.renvoie_identifiant(joueur_actif)
    for d in plateau[1]:
        liste_grenouilles = dalle.renvoie_liste_grenouilles(d)
        for g in liste_grenouilles:
            if grenouille.renvoie_identifiant(g) == identifiant_joueur_actif and \
                   grenouille.renvoie_priorite(g) == 0:
                grenouille.modifie_priorite(g, len(liste_grenouilles))

def depose_une_grenouille_sur_une_dalle(plateau, numero_dalle, nouvelle_grenouille):
    """
       Dépose une grenouille sur la dalle de numéro donné du plateau.
       Entrées:
         * plateau: liste
           Le plateau à modifier
         * numero_dalle: entier
           Le numéro de la dalle devant accueillir la grenouille
         * nouvelle_grenouille: liste
           La grenouille constituant la nouvelle liste de grenouille de la dalle
           de numéro donnée du plateau.

       Notes:
         La dalle modifiée a une liste de grenouilles réduite à la nouvelle
         grenouille.
         Le plateau est modifié à la sortie de la fonction.
    """
    dalle_arrivee = renvoie_dalle(plateau, numero_dalle)
    dalle.modifie_liste_grenouilles(dalle_arrivee, [nouvelle_grenouille])
    modifie_dalle(plateau, numero_dalle, dalle_arrivee)

def ajoute_une_grenouille_sur_une_dalle(plateau, numero_dalle, nouvelle_grenouille):
    """
       Ajoute une grenouille sur la dalle de numéro donné du plateau.
       Entrées:
         * plateau: liste
           Le plateau à modifier
         * numero_dalle: entier
           Le numéro de la dalle devant accueillir la grenouille
         * nouvelle_grenouille: liste
           La grenouille à ajouter à la liste de grenouilles de la dalle
           de numéro donnée du plateau.

       Notes:
         Le plateau est modifié à la sortie de la fonction.
    """
    dalle_arrivee = renvoie_dalle(plateau, numero_dalle)
    grenouilles = dalle.renvoie_liste_grenouilles(dalle_arrivee)
    grenouilles.append(nouvelle_grenouille)
    dalle.modifie_liste_grenouilles(dalle_arrivee, grenouilles)
    modifie_dalle(plateau, numero_dalle, dalle_arrivee)

def trouve_reine(plateau, joueur_actif):
    """
       Renvoie le numéro de la dalle contenant la reine du joueur actif
       Entrées:
         * plateau: liste
           Le plateau à consulter
         * joueur_actif: liste
           Le joueur dont on cherche la reine
    """
    identifiant_joueur_actif = joueur.renvoie_identifiant(joueur_actif)
    numero_dalle = 0
    for d in plateau[1]:
        grenouilles = dalle.renvoie_liste_grenouilles(d)
        # Si la liste grenouilles est vide le corps de la boucle n'est pas
        # exécuté
        for g in grenouilles:
            if grenouille.renvoie_identifiant(g) == identifiant_joueur_actif and \
               grenouille.est_reine(g):
                return(numero_dalle)
        numero_dalle += 1
    return(numero_dalle)
    
def reinitialise_dernier_occupant(plateau):
    """
       Remet à -1 l'identifiant du dernier occupant des dalles du plateau
       Entrées:
         * plateau: liste
           Le plateau à modifier

       Notes:
         Le plateau est modifié à la sortie de la fonction.
    """
    for d in plateau[1]:
        dalle.modifie_dernier_occupant(d, -1)

########
# Fonctions de changement de repérage des dalles:
# + Repérage linéaire (par numéro): en ligne en partant
#   du coin supérieur gauche (dalle 0) au coin inférieur
#   droit (dalle 63)
# + Repérage matriciel (par indice): (i, j) où i est
#   l'indice de la ligne (0 pour la ligne supérieure) et
#   j l'indice de la colonne (0 pour la colonne de gauche)
# + Repérage par les coordonnées du coin supérieur gauche
#   i_base = DECALAGE, j_base = DECALAGE pour la dalle
#   supérieur gauche dans une image stockée comme ndarray
#   Cela revient à tourner l'image d'un quart de tour dans
#   le sens trigonométrique
########
def convertis_numero_dalle_vers_indices(numero):
    """
       Convertis un numéro de dalle (entre 0 et 63) en indices
       de ligne et de colonne (entre 0 et 7)
       Entrées:
         * numero: entier
           Le numéro de dalle à convertir en indices
       Sorties:
         * indices: liste
           La paire [indice de ligne, indice de colonne] associée au numéro
           de dalle donné.

       Notes:
         Les dalles sont identifiées de deux manières dans le plateau:
           + Repérage linéaire (par numéro): en ligne en partant
             du coin supérieur gauche (dalle 0) au coin inférieur
             droit (dalle 63)
           + Repérage matriciel (par indice): (i, j) où i est
             l'indice de la ligne (0 pour la ligne supérieure) et
             j l'indice de la colonne (0 pour la colonne de gauche)         
    """
    return([numero // 8, numero % 8])

def convertis_indices_dalle_vers_numero(indices):
    """
       Convertis des indices de dalle (entre 0 et 7) en numéros de dalle
       (entre 0 et 63)
       Entrées:
         * indices: liste
           La paire [indice de ligne, indice de colonne] d'indices d'une dalle.
       Sorties:
         * numero: entier
           Le numéro de dalle correspondant aux indices donnés.

       Notes:
         Les dalles sont identifiées de deux manières dans le plateau:
           + Repérage linéaire (par numéro): en ligne en partant
             du coin supérieur gauche (dalle 0) au coin inférieur
             droit (dalle 63)
           + Repérage matriciel (par indice): (i, j) où i est
             l'indice de la ligne (0 pour la ligne supérieure) et
             j l'indice de la colonne (0 pour la colonne de gauche)         
    """
    return(8 * indices[0] + indices[1])

def convertis_numero_dalle_vers_coordonnees(numero):
    """
       Convertis un numéro de dalle (entre 0 et 63) en
       coordonnees du coin supérieur gauche de l'image de la carte
       de cette dalle dans une image de plateau.
       Entrées:
         * numero: entier
           Le numéro de dalle à convertir en indices
       Sorties:
         * indices: liste
           La paire [indice de ligne, indice de colonne] associée au numéro
           de dalle donné.
        
       Notes:
         Le repérage de l'image de la carte d'une dalle à partir de son numéro
         revient à convertir les repérages suivants:
           + Repérage linéaire (par numéro): en ligne en partant
             du coin supérieur gauche (dalle 0) au coin inférieur
             droit (dalle 63)
           + Repérage par les coordonnées du coin supérieur gauche
             i_base = DECALAGE, j_base = DECALAGE pour la dalle
             supérieur gauche dans une image stockée comme ndarray
    """
    indices = convertis_numero_dalle_vers_indices(numero)
    return(convertis_indices_dalle_vers_coordonnees(indices))

def convertis_coordonnees_vers_numero_dalle(coordonnees):
    """
       Convertis les indices d'une entrée d'une ndarray d'image de plateau
       en numéro de dalle (entre 0 et 63) dont l'image de la carte contient
       l'entrée donnée.
       Entrées:
         * coordonnées: liste
           Liste de taille deux d'entiers
       Sorties:
         * numero: entier
           Numéro de la dalle dont l'image de la carte dans l'image d'un plateau
           contient les cooronnées données
        
       Notes:
         Le repérage de l'image de la carte d'une dalle à partir de son numéro
         revient à convertir les repérages suivants:
           + Repérage linéaire (par numéro): en ligne en partant
             du coin supérieur gauche (dalle 0) au coin inférieur
             droit (dalle 63)
           + Repérage par les coordonnées du coin supérieur gauche
             i_base = DECALAGE, j_base = DECALAGE pour la dalle
             supérieur gauche dans une image stockée comme ndarray
         Si les coordonnées ne correspondent pas à un point d'une dalle, le
         numéro renvoyé est égal à -1
    """
    numero_ligne = (coordonnees[0] - DECALAGE) // PAS
    if numero_ligne < 0 or numero_ligne > 7:
        return(-1)
    numero_colonne = (coordonnees[1] - DECALAGE) // PAS
    if numero_colonne < 0 or numero_colonne > 7:
        return(-1)
    return(convertis_indices_dalle_vers_numero([numero_ligne, numero_colonne]))

def convertis_indices_dalle_vers_coordonnees(indices):
    """
       Convertis les indices de la dalle (entre 0 et 7) en coordonnées
       du coin supérieur gauche de l'image de la carte de cette dalle dans une
       image de plateau.
       Entrées:
         * indices: liste
           Les indices de ligne et de colonne d'une dalle à convertir en
           coordonnees
       Sorties:
         * coordonnees: liste
           Les coordonnées dans un ndarray représentant l'image d'un plateau du
           coin supérieur gauche de l'image d'une dalle d'indices donnés.
        
       Notes:
         Le repérage de l'image de la carte d'une dalle à partir de son numéro
         revient à convertir les repérages suivants:
           + Repérage matriciel (par indice): (i, j) où i est
             l'indice de la ligne (0 pour la ligne supérieure) et
             j l'indice de la colonne (0 pour la colonne de gauche)
           + Repérage par les coordonnées du coin supérieur gauche
             i_base = DECALAGE, j_base = DECALAGE pour la dalle
             supérieur gauche dans une image stockée comme ndarray
    """
    return([DECALAGE + indices[0] * PAS, DECALAGE + indices[1] * PAS])

def dessine(plateau):
    """
       Crée une image représentant un plateau dans son état courant
       Entrées:
         * plateau: liste
           Le plateau à dessiner
       Sorties:
         * image: ndarray
           Un tableau numpy (HxLx3) où chaque point de l'image est représenté
           par un triplet (rouge, vert, bleu) de réels dans [0, 1]
    """
    image_plateau = np.copy(graphique.IMAGE_FOND)
    # Numéro de la dalle en cours
    numero_dalle = 0
    # Parcours des 8x8 dalles
    for i in range(8):
        for j in range(8):
            i_base, j_base = convertis_indices_dalle_vers_coordonnees([i, j])
            dalleIJ = plateau[1][numero_dalle]
            dalle.dessine(dalleIJ, False, i_base, j_base, image_plateau)
            numero_dalle += 1
    # Parcours des joueurs encore en jeu
    for j in plateau[0]:
        joueur.dessine(j, image_plateau)
    return(image_plateau)
