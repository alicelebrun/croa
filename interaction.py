"""
    Ce fichier regroupe les fonctions implémentant les interactions des joueurs
    avec le jeu
"""
# Modules externes
import numpy as np

# Modules du jeu
import carte
import dalle
import graphique
import grenouille
import joueur
import plateau

# Définition des dalles permettant l'interaction avec les joueurs
# Dalles OUI/NON pour les choix entre servante/reine, quitter/continuer...
OUI = dalle.cree(carte.cree(carte.NENUPHAR, carte.OUI), [], -1)
NON = dalle.cree(carte.cree(carte.NENUPHAR, carte.NON), [], -1)
# Dalles 2, 3, 4 pour le choix du nombre de joueurs
DEUX   = dalle.cree(carte.cree(carte.NENUPHAR, carte.DEUX), [], -1)
TROIS  = dalle.cree(carte.cree(carte.NENUPHAR, carte.TROIS), [], -1)
QUATRE = dalle.cree(carte.cree(carte.NENUPHAR, carte.QUATRE), [], -1)

def cree_message(joueur_actif, texte):
    """
       Crée un objet pyplot de type message affichant un texte donné dans la
       couleur associée au joueur donné.
       Entrées:
         * joueur_actif: liste
           Le joueur destinataire du message
         * texte: string
           Le contenu du message
       Sorties:
         * message: pyplot.text
           L'objet pyplot associé au message

       Notes:
         L'objet pyplot créé *doit* être détruit après usage à l'aide de sa
         méthode remove() via message.remove()
    """
    couleur= joueur.COULEURS_JOUEURS[joueur.renvoie_identifiant(joueur_actif)]
    return(graphique.cree_texte(texte, couleur))

def affiche_message(plateau_croa, joueur_actif, texte):
    """
       Affiche un message sur le plateau de jeu
       Entrées:
         * plateau_croa: liste
           Le plateau sur lequel afficher un message
         * joueur_actif: liste
           Le joueur destinataire du message
         * texte: string
           Le contenu du message

       Notes:
         La fonction met à jour la variable graphique.IMAGE_PLATEAU ainsi que le
         contenu de la fenêtre graphique. Pour une interaction dynamique agréable,
         le plateau est affiché avec le message, puis on attend une confirmation
         de lecture via un clic souris de la part du joueur. Le message est alors
         supprimé et l'affichage du plateau mis à jour. L'utilisation de la
         variable globale graphique.IMAGE_PLATEAU permet d'éviter plusieurs appels
         à la fonction coûteuse plateau.dessine()
    """
    graphique.IMAGE_PLATEAU = plateau.dessine(plateau_croa)
    message = cree_message(joueur_actif, texte)
    graphique.rafraichit(graphique.IMAGE_PLATEAU)
    graphique.attend_clic()
    message.remove()
    graphique.rafraichit(graphique.IMAGE_PLATEAU)

def selectionne_dalle(numeros_dalles_valides, liste_dalles, joueur_actif):
    """
       Permet la sélection graphique d'une dalle dans un ensemble de dalles donné.
       Entrées:
         * numeros_dalles_valides: liste
           L'ensemble des numéros de dalles parmi lesquels faire le choix
         * liste_dalles: liste
           L'ensemble des dalles du plateau
         * joueur_actif: liste
           Le joueur destinataire du message
       Sorties:
         * numero_dalle: entier
           Le numéro de la dalle sélectionnée

       Notes:
         La liste des dalles pouvant être sélectionnées est mis en valeur
         graphiquement par l'ajout d'un cadre de la couleur du joueur autour de
         chacune de ces dalles.
         Après chaque clic souris, il faut vérifier que le curseur était bien sur
         une dalle.
    """
    image_plateau_choix = np.copy(graphique.IMAGE_PLATEAU)
    for numero in numeros_dalles_valides:
      i_base, j_base = plateau.convertis_numero_dalle_vers_coordonnees(numero)
      dalle.encadre(liste_dalles[numero], joueur_actif, i_base, j_base, image_plateau_choix)
    graphique.rafraichit(image_plateau_choix)
    selection_invalide = True
    while selection_invalide:
      coordonnees = graphique.attend_clic()
      numero = plateau.convertis_coordonnees_vers_numero_dalle(coordonnees)
      if numero != -1:
        #c'est à dire si on a bien cliqué sur une dalle
        for i in numeros_dalles_valides:
          if numero == i:
            selection_invalide = False
            break
    return(numero)



def selectionne_dalle_depart(plateau_croa, joueur_actif):
    """
       Permet la sélection graphique de la dalle de départ du tour de jeu
       Entrées:
         * plateau_croa: liste
           Le plateau de jeu
         * joueur_actif: liste
           Le joueur devant sélectionner une dalle de départ
       Sorties:
         * numero_dalle: entier
           Le numéro de la dalle sélectionnée

       Notes:
         Cette fonction construit la liste des dalles de départ valides en
         s'appuyant sur dalle.est_valide_depart() puis s'appuie sur la fonction
         selectionne_dalle() pour la sélection proprement dite.
    """
    numeros_dalles_valides= []
    liste_dalles = plateau.renvoie_liste_dalles(plateau_croa)
    for i in range(len(liste_dalles)):
      if dalle.est_valide_depart(liste_dalles[i], joueur_actif):
        numeros_dalles_valides.append(i)
    return(selectionne_dalle(numeros_dalles_valides, liste_dalles, joueur_actif))

def choisis(plateau_croa, joueur_actif, texte, dalle_gauche, dalle_droite, transparent):
    """
       Permet d'effectuer un choix binaire graphiquement.
       Entrées:
         * plateau_croa: liste
           Le plateau du jeu vis-à vis duquel le choix doit se faire
         * joueur_actif: liste
           Le joueur destinataire du message
         * texte: string
           Le contenu du message décrivant le choix à faire
         * dalle_gauche: liste
           La dalle décrivant le premier terme de l'alternative
         * dalle_droite: liste
           La dalle décrivant l'autre terme de l'alternative
         * transparent: booléen
           Drapeau indiquant si les dalles décrivant l'alternative doivent
           être dessinées avec (True) ou sans (False) transparence.
       Sorties:
         * choix: booléen
           Drapeau indiquant quel terme de l'alternative a été choisi. Il vaut
           True si le choix correspond à la dalle de gauche, False s'il correspond
           à la dalle de droite

       Notes:
         L'utilisation de la transparence est nécessaire lorsque le choix doit se
         faire en rapport avec le contenu d'une dalle du jeu qui serait masquée
         par une des dalles du choix. Par exemple, si une grenouille arrive sur
         une dalle dont la carte est carte.MOUSTIQUE, il faut choisir si le joueur
         rejoue ou pas. L'une des dalles OUI ou NON pourrait masquer la dalle où
         le joueur est arrivé, rendant la raison du choix peu compréhensible.
    """
    # On rafraichit l'affichage du plateau
    graphique.IMAGE_PLATEAU = plateau.dessine(plateau_croa)
    image_plateau_copie = np.copy(graphique.IMAGE_PLATEAU)
    liste_dalles = plateau.renvoie_liste_dalles(plateau_croa)
    numeros_dalles_valides=[35, 36]
    message = cree_message(joueur_actif, texte)
    i, j = plateau.convertis_numero_dalle_vers_coordonnees(numeros_dalles_valides[0])
    dalle.dessine(dalle_gauche, transparent, i, j, graphique.IMAGE_PLATEAU)
    i, j = plateau.convertis_numero_dalle_vers_coordonnees(numeros_dalles_valides[1])
    dalle.dessine(dalle_droite,transparent, i, j, graphique.IMAGE_PLATEAU)
    graphique.rafraichit(image_plateau_copie)
    choix = selectionne_dalle(numeros_dalles_valides, liste_dalles,joueur_actif )== numeros_dalles_valides[0]
    message.remove()
    graphique.IMAGE_PLATEAU = image_plateau_copie
    graphique.rafraichit(graphique.IMAGE_PLATEAU)
    return(choix)



def choisis_grenouille(plateau_croa, joueur_actif):
    """
       Renvoie le numéro de la dalle de départ et le statut de la grenouille
       choisie.
       Entrées:
         * plateau_croa: liste
           Le plateau de jeu
         * joueur_actif: liste
           Le joueur devant choisir la grenouille à jouer
       Sorties:
         * numero_dalle_choisie: entier
           Le numéro (0..63) de la dalle de départ
         * choix_reine: booléen
           Vaut True si la grenouille choisie est une reine, False sinon

       Notes:
         On commence par sélectionner une dalle de départ valide à l'aide de la
         fonction selectionne_dalle_depart puis on sélectionne éventuellement
         laquelle des grenouilles de la dalle doit être jouée.
         Il est plus efficace d'énumérer tous les cas concernant le nombre
         et la nature des grenouilles présentes sur la dalle choisie comme
         dalle de départ:
           * 1 grenouille (servante ou reine)
           * 1 servante joueur actif 1 servante autre joueur (rondin)
           * 1 servante autre joueur 1 servante joueur actif (rondin)
           * 2 servantes joueur actif (rondin)
           * 1 servante 1 reine (mâle ou quelconqe après capture d'une reine
             adverse)
           * 1 reine 1 servante (idem cas précédent)
         S'il n'y a qu'une grenouille sur la dalle c'est la bonne, pas de choix
         à faire!
    """
    numero_dalle_choisie= selectionne_dalle_depart(plateau_croa, joueur_actif)
    dalle_depart = plateau.renvoie_dalle(plateau_croa, numero_dalle_choisie)
    grenouilles= dalle.renvoie_liste_grenouilles(dalle_depart)
    #Si il n'y a qu'une grenouille sur la dalle:
    if len(grenouilles) == 1:
      choix_reine = grenouille.est_reine(grenouilles[0])
      dalle.modifie_liste_grenouilles(dalle_depart, [])
      return(numero_dalle_choisie, choix_reine)
    #Sinon il y en a deux, laquelle prendre?
    identifiant_joueur_actif = joueur.renvoie_identifiant(joueur_actif)
    grenouille_0_active = grenouille.renvoie_identifiant(grenouilles[0]) == identifiant_joueur_actif
    grenouille_1_active = grenouille.renvoie_identifiant(grenouilles[1]) == identifiant_joueur_actif
    #Est-ce que les deux grenouilles m'appartiennent?
    #Cas avec 2 grenouilles de team différentes
    #Quand deux grenouilles de camps différents sont sur la mm case, ce sont obligatoirement deux servantes.
    if not grenouille_1_active:
      choix_reine = False
      dalle.modifie_liste_grenouilles(dalle_depart, [grenouilles[1]])
      return(numero_dalle_choisie, choix_reine)
    if not grenouille_0_active:
      choix_reine = False
      dalle.modifie_liste_grenouilles(dalle_depart, [grenouilles[0]])
      return(numero_dalle_choisie, choix_reine)
    #Cas de deux grenouilles de même famille:
    grenouille.modifie_priorite(grenouilles[0], 1)
    grenouille.modifie_priorite(grenouilles[1], 1)
    #Si les deux grenouilles sont des servantes, on laisse la première sur la dalle et on prend la deuxième.
    grenouille_0_servante = grenouille.est_servante(grenouilles[0])
    grenouille_1_servante = grenouille.est_servante(grenouilles[1])
    if grenouille_0_servante and grenouille_1_servante:
      choix_reine = False
      dalle.modifie_liste_grenouilles(dalle_depart, [grenouilles[0]])
      return(numero_dalle_choisie, choix_reine)
    #Si une des deux grenouilles est la reine, il faut faire le choix: on sélectionne la reine ou la servante?
    choix_reine = choisis(plateau_croa, joueur_actif, "Voulez-vous prendre la reine?", OUI, NON, True)
    #Si la grenouille 1 est reine et la grenouille 0 servante:
    if choix_reine and grenouille_0_servante:
      dalle.modifie_liste_grenouilles(dalle_depart, [grenouilles[0]])
    #Si la grenouille 0 est reine et la grenouille 1 servante:
    if choix_reine and grenouille_1_servante:
      dalle.modifie_liste_grenouilles(dalle_depart, [grenouilles[1]])
    #Si on n'a pas choisi la reine et que grenouille 0 est une servante, c'est quon a pris grenouille 0:
    if not choix_reine and grenouille_0_servante:
      dalle.modifie_liste_grenouilles(dalle_depart, [grenouilles[1]])
    #Dernier cas possible:
    if not choix_reine and grenouille_1_servante:
      dalle.modifie_liste_grenouilles(dalle_depart, [grenouilles[0]])
    return(numero_dalle_choisie, choix_reine)


def selectionne_dalle_arrivee(plateau_croa, joueur_actif, numero_dalle_depart, choix_reine):
    """
       Permet la sélection graphique de la dalle d'arrivée du tour de jeu
       Entrées:
         * plateau_croa: liste
           Le plateau de jeu
         * joueur_actif: liste
           Le joueur devant sélectionner une dalle de départ
         * numero_dalle_depart: entier
           Le numéro de la dalle de départ du tour de jeu
         * choix_reine: booléen
           Vaut True si le joueur est en train de jouer sa reine, False s'il joue
           une servante
       Sorties:
         * numero_dalle: entier
           Le numéro de la dalle sélectionnée

       Notes:
         Cette fonction construit la liste des dalles d'arrivée valides et
         s'appuie sur la fonction selectionne_dalle() pour la sélection proprement
         dite.
         La construction de cette liste est nettement plus complexe que pour le
         choix de la dalle de départ, car elle dépend de la position de la dalle
         de départ sur le plateau (dans un coin, sur un bord, dans le plateau),
         puis du contenu de la dalle (cf dalle.est_valide_arrivee()) et enfin du
         dernier occupant si aucune autre dalle n'est disponible (cas du roseau,
         traité comme une succession de mouvements élémentaires)
    """
    #On fabrique la liste des dalles candidates:
    numero_dalles_candidates = []
    ligne_depart, colonne_depart = plateau.convertis_numero_dalle_vers_indices(numero_dalle_depart)
    if ligne_depart > 0:
      if colonne_depart>0:
        numero_dalles_candidates.append(numero_dalle_depart -9)
      numero_dalles_candidates.append(numero_dalle_depart -8) # on ajoute les dalles de la ligne au-dessus
      if colonne_depart <7:
        numero_dalles_candidates.append(numero_dalle_depart -7)
    if colonne_depart>0:
      numero_dalles_candidates.append(numero_dalle_depart -1)
    if colonne_depart <7:
      numero_dalles_candidates.append(numero_dalle_depart +1)
    if ligne_depart <7:
      if colonne_depart>0:
        numero_dalles_candidates.append(numero_dalle_depart +7)
      numero_dalles_candidates.append(numero_dalle_depart +8) # on ajoute les dalles de la ligne au-dessous
      if colonne_depart <7:
        numero_dalles_candidates.append(numero_dalle_depart +9)
    liste_dalles = plateau.renvoie_liste_dalles(plateau_croa)
    liste_numeros_dalles_valides = []
    identifiant_joueur_actif = joueur.renvoie_identifiant(joueur_actif)
    for numero in numero_dalles_candidates:
      if dalle.est_valide_arrivee(liste_dalles[numero], joueur_actif, choix_reine):
        if dalle.renvoie_dernier_occupant(liste_dalles[numero]) == identifiant_joueur_actif:
          numero_dalle_reserve = numero
        else:
          liste_numeros_dalles_valides.append(numero)
    if len(liste_numeros_dalles_valides)== 0:
      liste_numeros_dalles_valides.append(numero_dalle_reserve)
    return(selectionne_dalle(liste_numeros_dalles_valides, liste_dalles, joueur_actif))


def definis_joueurs():
    """
       Cette fonction sert à choisir le nombre de joueurs d'une partie
       Sorties:
         * joueurs: liste
           La liste initiale des joueurs de la partie courante

       Notes:
         Le nombre de joueurs est déterminé par la sélection à la souris d'une
         des dalles DEUX, TROIS ou QUATRE positionnées de manière irrégulière
         sous un texte afin de briser la dissymétrie liée à l'affichage de trois
         dalles sur une rangée de huit dalles
    """
    plateau_croa = plateau.cree([])
    graphique.IMAGE_PLATEAU = plateau.dessine(plateau_croa)
    joueur_actif = joueur.cree("0", 0, "")
    message= cree_message(joueur_actif,"À combien voulez-vous jouer?")
    transparent = False
    numero_dalles_valides = [34, 45, 51]
    i, j = plateau.convertis_numero_dalle_vers_coordonnees(numero_dalles_valides[0])
    dalle.dessine(DEUX, transparent, i, j, graphique.IMAGE_PLATEAU)
    i, j = plateau.convertis_numero_dalle_vers_coordonnees(numero_dalles_valides[1])
    dalle.dessine(TROIS, transparent, i, j, graphique.IMAGE_PLATEAU)
    i, j = plateau.convertis_numero_dalle_vers_coordonnees(numero_dalles_valides[2])
    dalle.dessine(QUATRE, transparent, i, j, graphique.IMAGE_PLATEAU)
    liste_dalles= plateau.renvoie_liste_dalles(plateau_croa)
    choix= selectionne_dalle(numero_dalles_valides, liste_dalles, joueur_actif)
    message.remove()
    if choix == numero_dalles_valides[0]:
      joueurs= [joueur.cree("Joueur 1", 0, "NO"), joueur.cree("Joueur 2", 1, "SE")]
    if choix == numero_dalles_valides[1]:
      joueurs= [joueur.cree("Joueur 1", 0, "SO"), joueur.cree("Joueur 2", 1, "E"), joueur.cree("Joueur 3", 2, "NO")]
    if choix == numero_dalles_valides[2]:
      joueurs= [joueur.cree("Joueur 1", 0, "NE"), joueur.cree("Joueur 2", 1, "SE"), joueur.cree("Joueur 3", 2, "SO"), joueur.cree("Joueur 4", 3, "NO")]
    return(joueurs)


