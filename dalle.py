"""
    Ce fichier regroupe les structures et les services associés
    à la création et à l'évolution d'une dalle
"""
# Modules internes
import carte
import graphique
import grenouille
import joueur

# Epaisseur des bords de cadres
EPAISSEUR = 6

def cree(carte, liste_grenouilles, dernier_occupant):
    """
       Crée la structure de données associée à une dalle dans son
       état initial.
       Entrées:
         * carte: liste
           La carte portée par la dalle
         * liste_grenouilles: liste
           La liste des grenouilles présentes sur la dalle
         * dernier_occupant: entier
           L'identifiant du joueur présent sur la dalle au tour précédent. La
           valeur -1 signifie qu'aucun joueur n'occupait la dalle au tour
           précédent.
       Sorties:
         * dalle: liste
           Une liste [carte, liste_grenouilles, dernier_occupant]
    """
    return([carte, liste_grenouilles, dernier_occupant])

def renvoie_carte(dalle):
    """
       Renvoie la carte de la dalle
       Entrées:
         * dalle: liste
           La dalle à consulter
       Sorties:
         * carte: liste
           La carte portée par la dalle
    """
    return(dalle[0])

def modifie_carte(dalle, carte):
    """
       Modifie la carte de la dalle
       Entrées:
         * dalle: liste
           La dalle à modifier
         * carte: liste
           La nouvelle carte de la dalle

       Notes:
         La dalle est modifié à la sortie de la fonction.
    """
    dalle[0] = carte

def renvoie_liste_grenouilles(dalle):
    """
       Renvoie la liste des grenouilles de la dalle
       Entrées:
         * dalle: liste
           La dalle à consulter
       Sorties:
         * liste_grenouilles: liste
           La liste de grenouilles de la dalle
    """
    return(dalle[1])

def modifie_liste_grenouilles(dalle, liste_grenouilles):
    """
       Modifie la liste des grenouilles de la dalle
       Entrées:
         * dalle: liste
           La dalle à modifier
         * liste_grenouilles: liste
           La liste de grenouilles de la dalle

       Notes:
         La dalle est modifié à la sortie de la fonction.
    """
    dalle[1] = liste_grenouilles

def renvoie_identifiant_autre_reine(dalle, identifiant_joueur_actif):
    """
       Renvoie l'identifiant de l'éventuelle reine de la dalle appartenant
       à un autre joueur que le joueur d'identifiant donné.
       Entrées:
         * dalle: liste
           La dalle à consulter
         * identifiant_joueur_actif: entier
           L'identifiant du joueur actif. Il permet de déterminer si une
           reine présente sur la dalle est une *autre* reine.
       Sorties:
         * identifiant: entier
           L'identifiant du joueur auquel appartient l'éventuelle reine
           présente sur la dalle. S'il n'y a pas d'autre reine, la fonction
           renvoie l'identifiant du joueur actif.
    """
    for g in dalle[1]:
        identifiant_grenouille = grenouille.renvoie_identifiant(g)
        if identifiant_grenouille != identifiant_joueur_actif and \
            grenouille.est_reine(g):
            return(identifiant_grenouille)
    return(identifiant_joueur_actif)

def renvoie_dernier_occupant(dalle):
    """
       Renvoie l'identifiant du dernier occupant de la dalle
       Entrées:
         * dalle: liste
           La dalle à consulter
       Sorties:
         * dernier_occupant: entier
           L'identifiant du joueur occupant la dalle au tour précédent. Vaut -1
           si la dalle était inoccupée au tour précédent.
    """
    return(dalle[2])

def modifie_dernier_occupant(dalle, dernier_occupant):
    """
       Modifie l'identifiant du dernier occupant de la dalle
       Entrées:
         * dalle: liste
           La dalle à modifier
         * dernier_occupant: entier
           L'identifiant du joueur occupant la dalle au tour précédent. La
           valeur -1 signifie qu'aucun joueur n'occupait la dalle au tour
           précédent.

       Notes:
         La dalle est modifié à la sortie de la fonction.
    """
    dalle[2] = dernier_occupant

def est_valide_depart(dalle, joueur_actif):
    """
       Indique si la dalle est une dalle de départ valide pour le joueur actif.
       Entrées:
         * dalle: liste
           La dalle à consulter
         * joueur_actif: liste
           Le joueur actif.
       Sorties:
         * statut: booléen
           Egal à True si la dalle est valide comme dalle de départ, à False sinon.

       Notes:
         Une dalle est valide comme départ pour le joueur actif si et seulement si
         elle contient une grenouille du joueur de priorité maximale.
         On peut exclure rapidement les dalles dont la liste de grenouilles est
         vide.
    """
    # Test rapide: s'il n'y a pas de grenouille la dalle est invalide
    if len(dalle[1]) == 0:
        return(False)
    identifiant_joueur_actif = joueur.renvoie_identifiant(joueur_actif)
    priorite_maximale_joueur = joueur.renvoie_priorite_maximale(joueur_actif)
    for g in dalle[1]:
        # La dalle est valide si elle contient une grenouille de priorité
        # égale à la priorité maximale du joueur
        if grenouille.renvoie_identifiant(g) == identifiant_joueur_actif and \
           grenouille.renvoie_priorite(g) == priorite_maximale_joueur:
            return(True)
    # La dalle est invalide: elle ne contient que des grenouilles d'autres joueurs
    # ou des grenouilles de priorité trop faible
    return(False)

def est_valide_arrivee(dalle, joueur_actif, choix_reine):
    """
       Indique si la dalle est une dalle d'arrivée valide pour le joueur actif.
       Entrées:
         * dalle: liste
           La dalle à consulter
         * joueur_actif: liste
           Le joueur actif.
       Sorties:
         * statut: booléen
           Egal à True si la dalle est valide comme dalle d'arrivée, à False sinon.

       Notes:
         Si la dalle n'est pas un rondin face visible, la dalle est valide si et
         seulement si elle ne contient pas de grenouille du joueur actif. Le
         statut du dernier occupant ne doit être pris en compte qu'en regard des
         autres dalles d'arrivées possibles: il n'est donc pas pris en compte à ce
         niveau.
         Si la dalle est un rondin face visible, alors la dalle est valide même si
         elle est déjà occupé par une grenouille du joueur actif sous les
         conditions suivantes:
           * la grenouille jouée est une servante
           * il y a au plus une grenouille du joueur actif sur le rondin
           * la grenouille du joueur actif déjà sur le rondin est une servante
         Il faut tester le fait que la carte rondin soit face visible pour éviter
         de choisir la case d'une servante qui est encore en position de départ
         sur une carte rondin dos visible.
         On peut accepter rapidement les dalles dont la liste de grenouilles est
         vide.
         On peut également accepter rapidement les dalles dont la carte n'est pas
         un rondin face visible si la première grenouille n'appartient pas au
         joueur actif (l'éventuelle seconde grenouille étant obligatoirement du
         même joueur)
    """
    # Test rapide: s'il n'y a pas de grenouille la dalle est valide
    if len(dalle[1]) == 0:
        return(True)
    # A partir d'ici il y a déjà une grenouille sur la dalle
    identifiant_joueur = joueur.renvoie_identifiant(joueur_actif)
    est_rondin = carte.renvoie_face(dalle[0]) == carte.RONDIN
    est_visible = carte.renvoie_face_visible(dalle[0])
    # Si la carte n'est pas un rondin visible la dalle n'est valide que si elle
    # n'est pas occupée par une grenouille du joueur actif
    # Il suffit de tester la première grenouille puisqu'il ne peut y avoir
    # plusieurs grenouilles de joueurs différents que sur un rondin
    if not (est_rondin and est_visible):
        return(grenouille.renvoie_identifiant(dalle[1][0]) != identifiant_joueur)
    # La carte est un rondin face visible:
    # Si le joueur est en train de jouer sa reine, la dalle est valide uniquement
    # si elle ne contient pas de servante du joueur actif
    # Si le joueur joue une servante, il faut tester si le rondin ne contient pas
    # la reine du joueur actif ou deux servantes du joueur actif
    # S'il n'y a qu'une grenouille
    if len(dalle[1]) == 1:
        g = dalle[1][0]
        grenouille_autre_joueur = grenouille.renvoie_identifiant(g) != \
                                  identifiant_joueur
        # Si le joueur joue sa reine
        if choix_reine:
            return(grenouille_autre_joueur)
        # Si le joueur joue une servante
        # La dalle est valide si elle contient la grenouille d'un autre joueur
        # ou si c'est une servante du joueur actif
        return(grenouille_autre_joueur or \
               grenouille.est_servante(g))
    # Il y a deux grenouilles sur la dalle, ce sont obligatoirement des servantes.
    identifiant_grenouille_0 = grenouille.renvoie_identifiant(dalle[1][0])
    identifiant_grenouille_1 = grenouille.renvoie_identifiant(dalle[1][1])
    # Si le joueur joue sa reine, il suffit de tester qu'aucune des deux servantes
    # n'appartient au joueur actif
    if choix_reine:
        return(identifiant_grenouille_0 != identifiant_joueur and \
               identifiant_grenouille_1 != identifiant_joueur)
    # Si le joueur joue une servante, il suffit de tester que les grenouilles
    # n'appartiennent pas toutes les deux au joueur actif
    return(identifiant_grenouille_0 != identifiant_joueur or \
           identifiant_grenouille_1 != identifiant_joueur)

def dessine(dalle, transparent, i_base, j_base, image_plateau):
    """
       Modifie l'image du plateau pour y dessiner la dalle à la position donnée.
       Entrées:
         * dalle: liste
           La dalle à dessiner
         * transparent: booléen
           Un drapeau indiquant si la carte de la dalle doit être dessinée de
           manière transparente ou opaque. Cf la documentation de carte.dessine()
         * i_base: entier
           Le numéro de ligne du coin supérieur gauche de l'image de la carte
           de la dalle dans le tableau numpy représentant le plateau de jeu
         * j_base: entier
           Le numéro de colonne du coin supérieur gauche de l'image de la carte
           de la dalle dans le tableau numpy représentant le plateau de jeu
         * image_plateau: ndarray
           Le tableau numpy dans lequel ajouter l'image représentant la dalle

       Notes:
         Selon le nombre de grenouilles, la priorité des grenouilles, la
         nature de la carte et son statut, la position de la grenouille sur
         la dalle change:
           * S'il n'y a qu'une grenouille elle est au centre, en position normale
             sauf si c'est une dalle contenant une carte vase retournée et que la
             grenouille est en priorité 0
           * S'il y a deux grenouilles, la première est positionnée au 1/4 de la
             la largeur et la deuxième aux 3/4
         Comme il n'y a que la dalle qui peut accéder à la carte, le fait que
         ce soit une carte vase visible est passé en argument de la fonction
         dessine() du module grenouille
         Le paramètre image_plateau est modifié à la sortie de la fonction.
    """
    # Dessine la carte
    carte.dessine(dalle[0], transparent, i_base, j_base, image_plateau)
    est_vase_visible = carte.renvoie_face(dalle[0]) == carte.VASE and \
                       carte.renvoie_face_visible(dalle[0])
    # Puis les grenouilles
    nombre_grenouilles = len(dalle[1])
    if nombre_grenouilles == 1:
        grenouille.dessine(dalle[1][0], 2, est_vase_visible, i_base, j_base, image_plateau)
    if nombre_grenouilles == 2:
        grenouille.dessine(dalle[1][0], 1, est_vase_visible, i_base, j_base, image_plateau)
        grenouille.dessine(dalle[1][1], 3, est_vase_visible, i_base, j_base, image_plateau)

def encadre(dalle, joueur_actif, i_base, j_base, image_plateau):
    """
       Modifie l'image du plateau pour y dessiner un cadre autour de la dalle
       donnée de couleur correspondant au joueur actif.
       Entrées:
         * dalle: liste
           La dalle à encadrer
         * joueur_actif: liste
           Le joueur actif, permettant de choisir la couleur du cadre.
         * i_base: entier
           Le numéro de ligne du coin supérieur gauche de l'image de la carte
           de la dalle dans le tableau numpy représentant le plateau de jeu
         * j_base: entier
           Le numéro de colonne du coin supérieur gauche de l'image de la carte
           de la dalle dans le tableau numpy représentant le plateau de jeu
         * image_plateau: ndarray
           Le tableau numpy dans lequel ajouter l'image représentant la dalle

       Notes:
         La longueur du côté d'une dalle est carte.COTE+2.
         Le paramètre image_plateau est modifié à la sortie de la fonction.        
    """
    couleur = joueur.COULEURS_JOUEURS[joueur.renvoie_identifiant(joueur_actif)]
    largeur = graphique.IMAGES_FACES[0].shape[0] + 2
    hauteur = graphique.IMAGES_FACES[0].shape[1] + 2
    for k in range(EPAISSEUR):
        image_plateau[i_base-k:i_base+largeur+k, j_base-k        ] = couleur
        image_plateau[i_base-k:i_base+largeur+k, j_base+hauteur+k] = couleur
        image_plateau[i_base-k        , j_base-k:j_base+hauteur+k] = couleur
        image_plateau[i_base+largeur+k, j_base-k:j_base+hauteur+k] = couleur
