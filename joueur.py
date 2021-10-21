"""
   Ce fichier regroupe les structures et les services associés
   à la création et à l'évolution d'un joueur
"""

# Modules internes
import carte
import graphique

# Couleurs associées aux joueurs
COULEURS_JOUEURS = [(81/255, 222/255, 255/255), (224/255, 181/255, 208/255), \
                    (219/255, 145/255, 132/255), (197/255, 224/255, 147/255)]
JETONS_MALES = [carte.MALE_BLEU, carte.MALE_JAUNE, carte.MALE_ORANGE, \
                carte.MALE_ROSE, carte.MALE_VERT, carte.MALE_VIOLET]

# Marge permettant d'espacer les grenouilles en réserve et les jetons mâles
MARGE = 10

# Demi-largeur de l'inscription Croâ! sur le plateau
DEMI_CROA = 200

def cree(nom, identifiant, position_camp):
    """
       Crée la structure de données associée à un joueur dans son
       état initial.
       Entrées:
         * nom: string
           Le nom du joueur
         * identifiant: entier
           L'identifiant du joueur, permettant de marquer ses grenouilles
         * position_camp: string
           La position du camp du joueur autour du plateau
       Sorties:
         * joueur: liste
           Une liste [nom, nombre_grenouille_reserve, liste_jetons_males,
           priorite_maximale, identifiant, position_camp]

       Notes:
         La position du camp du joueur peut prendre les valeurs suivantes:
           * 'NO' pour le joueur au nord-ouest du plateau (en haut à gauche)
           * 'NE' pour le joueur au nord-est du plateau (en haut à droite)
           * 'E' pour le joueur à l'est du plateau (à droite)
           * 'SE' pour le joueur au sud-est du plateau (en bas à droite)
           * 'SO' pour le joueur au sud-ouest du plateau (en bas à gauche)
    """
    nombre_grenouille_reserve = 4
    liste_jetons_males = JETONS_MALES
    priorite_maximale = 1
    return([nom, nombre_grenouille_reserve, liste_jetons_males, priorite_maximale, identifiant, position_camp])

def possede_jeton(joueur, couleur_male):
    """
       Test si le joueur donné possède le jeton mâle de la couleur donnée
       Entrées:
         * joueur: liste
           Le joueur à tester
         * couleur_male: entier
           La couleur de mâle à tester. Elle correspond à un identifiant de
           carte mâle entre carte.MALE_BLEU et carte.MALE_VIOLET.
       Sorties:
         * statut: booléen
         Egal à True si le joueur possède le jeton de la couleur donnée, False
         sinon.
    """
    for couleur in joueur[2]:
      if couleur==couleur_male:
        return(True)
    return(False)

def renvoie_nom(joueur):
    """
       Renvoie le nom du joueur
       Entrées:
         * joueur: liste
           Le joueur à consulter
       Sorties:
         * nom: string
           Le nom du joueur
    """
    return(joueur[0])

def renvoie_nombre_grenouilles_reserve(joueur):
    """
       Renvoie le nombre de grenouilles en réserve
       Entrées:
         * joueur: liste
           Le joueur à consulter
       Sorties:
         * nombre_grenouille_reserve: entier
           Le nombre de grenouilles en réserve du joueur
    """
    return(joueur[1])

def modifie_nombre_grenouilles_reserve(joueur, nombre_grenouilles_reserve):
    """
       Modifie le nombre de grenouilles en réserve
       Entrées:
         * joueur: liste
           Le joueur à modifier
         * nombre_grenouille_reserve: entier
           Le nouveau nombre de grenouilles en réserve du joueur

       Notes:
         Le joueur est modifié à la sortie de la fonction.
    """
    joueur[1]= nombre_grenouilles_reserve

def renvoie_liste_jetons(joueur):
    """
       Renvoie la liste des jetons mâles d'un joueur
       Entrées:
         * joueur: liste
           Le joueur à consulter
       Sorties:
         * liste_jetons: liste
           La liste des jetons mâles encore disponibles du joueur
    """
    return(joueur[2])

def modifie_liste_jetons(joueur, jetons_male):
    """
       Modifie la liste des jetons mâles d'un joueur
       Entrées:
         * joueur: liste
           Le joueur à consulter
         * liste_jetons: liste
           La liste des jetons mâles encore disponibles du joueur

       Notes:
         Le joueur est modifié à la sortie de la fonction.
    """
    joueur[2]= jetons_male

def renvoie_priorite_maximale(joueur):
    """
       Renvoie la priorité maximale des grenouilles du joueur
       Entrées:
         * joueur: liste
           Le joueur à consulter
       Sorties:
         * priorite_maximale: entier
           La priorité maximale des grenouilles du joueur
    """
    return(joueur[3])

def modifie_priorite_maximale(joueur, priorite_maximale):
    """
       Modifie la priorité maximale des grenouilles du joueur
       Entrées:
         * joueur: liste
           Le joueur à consulter
         * priorite_maximale: entier
           La priorité maximale des grenouilles du joueur

       Notes:
         Le joueur est modifié à la sortie de la fonction.
    """
    joueur[3]= priorite_maximale


def renvoie_identifiant(joueur):
    """
       Renvoie l'identifiant du joueur
       Entrées:
         * joueur: liste
           Le joueur à consulter
       Sorties:
         * priorite_maximale: entier
           La priorité maximale des grenouilles du joueur
    """
    return(joueur[4])

def renvoie_position_camp(joueur):
    """
       Renvoie la position du camp du joueur
       Entrées:
         * joueur: liste
           Le joueur à consulter
       Sorties:
         * position_camp: string
           La position du camp du joueur autour du plateau

       Notes:
         La position du camp du joueur peut prendre les valeurs suivantes:
           * 'NO' pour le joueur au nord-ouest du plateau (en haut à gauche)
           * 'NE' pour le joueur au nord-est du plateau (en haut à droite)
           * 'E' pour le joueur à l'est du plateau (à droite)
           * 'SE' pour le joueur au sud-est du plateau (en bas à droite)
           * 'SO' pour le joueur au sud-ouest du plateau (en bas à gauche)
    """
    return(joueur[5])

def dessine(joueur, image_plateau):
    """
       Modifie l'image du plateau pour y dessiner les jetons et les grenouilles
       en réserve du joueur selon la position de son camp
       Entrées:
         * joueur: liste
           Le joueur à dessiner
         * image_plateau: ndarray
           Le tableau numpy dans lequel ajouter l'image représentant le joueur

       Notes:
         Le paramètre image_plateau est modifié à la sortie de la fonction.
    """
    largeur_fond= graphique.IMAGE_FOND.shape[0]
    hauteur_fond= graphique.IMAGE_FOND.shape[1]

    #affichage des servantes:
    if joueur[1]>0:
      image_servante = graphique.IMAGES_SERVANTES[joueur[4]]
      masque = image_servante[:, :, 0] + image_servante[:, :, 1] + image_servante[:, :, 2] < 3.0
      largeur_servante = image_servante.shape[0]
      hauteur_servante = image_servante.shape[1]
      largeur_carte = graphique.IMAGES_FACES[0].shape[0]
      hauteur_carte = graphique.IMAGES_FACES[0].shape[1]

      if joueur[5]== "NO":
        i_base = MARGE
        j_base = (largeur_carte - largeur_servante)// 2
        for i in range(joueur[1]):
          image_plateau[i_base: i_base + largeur_servante , j_base : j_base + hauteur_servante][masque] = image_servante[masque]
          i_base += hauteur_servante + MARGE
      if joueur[5]== "NE":
        i_base = MARGE
        j_base = largeur_fond - (largeur_carte - largeur_servante)// 2
        for i in range(joueur[1]):
          image_plateau[i_base: i_base + largeur_servante , j_base : j_base + hauteur_servante][masque] = image_servante[masque]
          i_base += hauteur_servante + MARGE
      if joueur[5]== "SO":
        i_base = hauteur_fond - (MARGE + hauteur_servante)
        j_base = (largeur_carte - largeur_servante)// 2
        for i in range(joueur[1]):
          image_plateau[i_base: i_base + largeur_servante , j_base : j_base + hauteur_servante][masque] = image_servante[masque]
          i_base -= hauteur_servante + MARGE
      if joueur[5]== "SE":
        i_base = hauteur_fond - (MARGE + hauteur_servante)
        j_base = largeur_fond - (largeur_carte - largeur_servante)// 2
        for i in range(joueur[1]):
          image_plateau[i_base: i_base + largeur_servante , j_base : j_base + hauteur_servante][masque] = image_servante[masque]
          i_base -= hauteur_servante + MARGE
      if joueur[5]== "E":
        i_base = hauteur_fond//2 - (DEMI_CROA + MARGE + hauteur_servante)
        j_base = largeur_fond - (largeur_carte - largeur_servante)// 2
        for i in range(joueur[1]):
          image_plateau[i_base: i_base + largeur_servante , j_base : j_base + hauteur_servante][masque] = image_servante[masque]
          i_base -= hauteur_servante + MARGE

    #affichage des jetons:
    if len(joueur[2])>0:
      largeur_male = graphique.IMAGES_FACES[0].shape[0]
      hauteur_male = graphique.IMAGES_FACES[0].shape[1]
      couleur = COULEURS_JOUEURS[joueur[4]]
      if joueur[5] == "NO":
        i_base = hauteur_male//4
        j_base = largeur_male
        for i in range(len(joueur[2])):
          image_male= graphique.IMAGES_FACES[joueur[2][i]]
          vignette = image_male[::2, ::2]
          image_plateau[i_base: i_base + largeur_male//2 , j_base : j_base + hauteur_male//2] = vignette
          masque = vignette[:, :, 0] + vignette[:, :, 1] + vignette[:, :, 2] == 3
          image_plateau[i_base: i_base + largeur_male//2 , j_base : j_base + hauteur_male//2][masque] = couleur
          j_base += largeur_male//2 + MARGE

      if joueur[5] == "NE":
        i_base = hauteur_male//4
        j_base = largeur_fond - (3*largeur_male //2)
        for i in range(len(joueur[2])):
          image_male= graphique.IMAGES_FACES[joueur[2][i]]
          vignette = image_male[::2, ::2]
          image_plateau[i_base: i_base + largeur_male//2 , j_base : j_base + hauteur_male//2] = vignette
          masque = vignette[:, :, 0] + vignette[:, :, 1] + vignette[:, :, 2] == 3
          image_plateau[i_base: i_base + largeur_male//2 , j_base : j_base + hauteur_male//2][masque] = couleur
          j_base -= largeur_male//2 + MARGE

      if joueur[5] == "SO":
        i_base = hauteur_fond - (3*hauteur_male//4)
        j_base = largeur_male
        for i in range(len(joueur[2])):
          image_male= graphique.IMAGES_FACES[joueur[2][i]]
          vignette = image_male[::2, ::2]
          image_plateau[i_base: i_base + largeur_male//2 , j_base : j_base + hauteur_male//2] = vignette
          masque = vignette[:, :, 0] + vignette[:, :, 1] + vignette[:, :, 2] == 3
          image_plateau[i_base: i_base + largeur_male//2 , j_base : j_base + hauteur_male//2][masque] = couleur
          j_base += largeur_male//2 + MARGE

      if joueur[5] == "SE":
        i_base = hauteur_fond - (3*hauteur_male//4)
        j_base = largeur_fond - (3*largeur_male //2)
        for i in range(len(joueur[2])):
          image_male= graphique.IMAGES_FACES[joueur[2][i]]
          vignette = image_male[::2, ::2]
          image_plateau[i_base: i_base + largeur_male//2 , j_base : j_base + hauteur_male//2] = vignette
          masque = vignette[:, :, 0] + vignette[:, :, 1] + vignette[:, :, 2] == 3
          image_plateau[i_base: i_base + largeur_male//2 , j_base : j_base + hauteur_male//2][masque] = couleur
          j_base -= largeur_male//2 + MARGE

      if joueur[5] == "E":
        i_base = hauteur_fond//2 + DEMI_CROA + MARGE
        j_base = largeur_fond - (3*largeur_male //4)
        for i in range(len(joueur[2])):
          image_male= graphique.IMAGES_FACES[joueur[2][i]]
          vignette = image_male[::2, ::2]
          image_plateau[i_base: i_base + largeur_male//2 , j_base : j_base + hauteur_male//2] = vignette
          masque = vignette[:, :, 0] + vignette[:, :, 1] + vignette[:, :, 2] == 3
          image_plateau[i_base: i_base + largeur_male//2 , j_base : j_base + hauteur_male//2][masque] = couleur
          i_base += hauteur_male//2 + MARGE







