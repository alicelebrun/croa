"""
   Ce fichier regroupe les structures et les services associés
   à la création et à l'évolution d'une carte
"""
# Modules internes
import graphique

# Identifiants des faces de cartes
NENUPHAR    = 0
ROSEAUX     = 1
MOUSTIQUE   = 2
MALE_BLEU   = 3
MALE_JAUNE  = 4
MALE_ORANGE = 5
MALE_ROSE   = 6
MALE_VERT   = 7
MALE_VIOLET = 8
VASE        = 9
BROCHET     = 10
RONDIN      = 11

# Identifiants des dos de cartes
EAU_PEU_PROFONDE = 0
EAU_PROFONDE_1   = 1
EAU_PROFONDE_2   = 2
OUI              = 3
NON              = 4
DEUX             = 5
TROIS            = 6
QUATRE           = 7

def cree(face, dos):
    """
       Crée la structure de données associée à une carte dans son
       état initial.
       Entrées:
         * face: entier
           un identifiant de la face de la carte
         * dos: entier
           un identifiant du dos de la carte
       Sorties:
         * carte: liste
           une liste [face_visible, face, dos]

       Note:
         Les identifiants de face et de dos doivent être renseignés en
         utilisant les noms globaux du module.
         L'identifiant de face visible signifie:
           * True, la face est visible
           * False, la face est invisible
         Il vaut False par défaut.
    """
    carte = [False,face,dos]
    return(carte)

def renvoie_face_visible(carte):
    """
       Renvoie True si la carte est visible côté face
       Entrées:
         * carte: liste
           La carte à consulter
       Sorties:
         * face_visible: booléen
           True si la face est visible, False si le dos est visible
    """
    return(carte[0])

def modifie_face_visible(carte, drapeau):
    """
       Modifie le drapeau indiquant si la face de la carte est visible
       Entrées:
         * carte: liste
           La carte à modifier
         * drapeau: booléen
           True si la face est visible, False si le dos est visible

       Notes:
         La carte est modifié à la sortie de la fonction.
    """
    carte[0] = drapeau

def renvoie_face(carte):
    """
       Renvoie l'identifiant de la face de la carte (NENUPHAR etc)
       Entrées:
         * carte: liste
           La carte à consulter
       Sorties:
         * un entier
    """
    return(carte[1])

def renvoie_dos(carte):
    """
       Renvoie l'identifiant du dos de la carte (EAU_PEU_PROFONDE etc)
       Entrées:
         * carte: liste
           La carte à consulter
       Sorties:
         * dos: entier
           L'identifiant du dos de la carte
    """
    return(carte[2])

#carte=[face_visible, face, dos]
#importer : import matplotlib.pyplot as plt
def dessine(carte, transparent, i_base, j_base, image_plateau):
    """
       Modifie l'image du plateau pour y dessiner le dos ou la face de la carte
       selon son état à la position donnée
       Entrées:
         * carte: liste
           La carte à dessiner
         * transparent: booléen
           Un drapeau indiquant si l'image doit être transparente ou opaque. Si
           le drapeau vaut True, les pixels de l'image sont mélangés à ceux du
           plateau en proportions égales. Si le drapeau vaut False, les pixels de
           l'image remplacent ceux du plateau.
         * i_base: entier
           Le numéro de ligne du coin supérieur gauche de l'image de la carte
           dans le tableau numpy représentant le plateau de jeu
         * j_base: entier
           Le numéro de colonne du coin supérieur gauche de l'image de la carte
           dans le tableau numpy représentant le plateau de jeu
         * image_plateau: ndarray
           Le tableau numpy dans lequel ajouter l'image représentant la carte

       Notes:
         Le paramètre image_plateau est modifié à la sortie de la fonction.
    """
    image_face=graphique.IMAGES_FACES[carte[1]]
    image_dos=graphique.IMAGES_DOS[carte[2]]
    largeur_carte_face = image_face.shape[0]
    hauteur_carte_face = image_face.shape[1]
    largeur_carte_dos = image_dos.shape[0]
    hauteur_carte_dos = image_dos.shape[1]
    if transparent:
        if carte[0]:
            image_plateau[i_base: i_base + largeur_carte_face , j_base : j_base + hauteur_carte_face] = 0.5 * (image_plateau[i_base: i_base + largeur_carte_face , j_base : j_base + hauteur_carte_face] + image_face)
        else:
            image_plateau[i_base: i_base + largeur_carte_dos , j_base : j_base + hauteur_carte_dos] = 0.5 * (image_plateau[i_base: i_base + largeur_carte_dos , j_base : j_base + hauteur_carte_dos] + image_dos)
    else:
        if carte[0]:
            image_plateau[i_base: i_base + largeur_carte_face , j_base : j_base + hauteur_carte_face]=image_face
        else:
            image_plateau[i_base: i_base + largeur_carte_dos , j_base : j_base + hauteur_carte_dos]=image_dos
