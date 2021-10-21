"""
    Ce fichier regroupe les fonctions implémentant l'affichage graphique du jeu
"""

# Modules externes
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

IMAGES_FACES = [img.imread("Images/" + name + ".png") for name in \
                ["nenuphar", "roseaux", "moustique", "male_bleu", \
                 "male_jaune", "male_orange", "male_rose", "male_vert", \
                 "male_violet", "vase", "brochet", "rondin"]]
IMAGES_DOS = [img.imread("Images/" + name + ".png") for name in \
              ["eau_peu_profonde", "eau_profonde_1", "eau_profonde_2", \
               "oui", "non", "deux", "trois", "quatre"]]

IMAGES_REINES = [img.imread("Images/reine_" + name + ".png") for name in \
                 ["bleue", "rose", "rouge", "verte"]]
IMAGES_SERVANTES = [img.imread("Images/servante_" + name + ".png") for \
                    name in ["bleue", "rose", "rouge", "verte"]]

IMAGE_FOND = img.imread("Images/fond.png")

# Fenêtre graphique pour le visuel du jeu
# FIG est l'identifiant de la figure pyplot contenant l'image du plateau
# AX est le système d'axes de la figure
FIG, AX = plt.subplots(figsize=(9, 9), dpi=100, frameon=False)
# Pas d'affichage des axes
AX.axis('off')
# Pas de marges dans la fenêtre
FIG.tight_layout(pad=0,rect=[0,0,1,1])
# Image du plateau
IMAGE_PLATEAU = None

def initialise(image):
    """
       Cette fonction sert à initialiser la fenêtre graphique du jeu.
       Entrées:
         * image: ndarray
           L'image à afficher dans la fenêtre pyplot.

       Notes:
         Une image est un tableau numpy de dimensions (largeur, hauteur, 3) car
         la couleur est représentée par un triplet de réels dans [0,1]:
         (0,0,0) -> noir
         (1,1,1) -> blanc
         (0.5, 0.5, 0.5) -> gris moyen
         (1,0,0) -> rouge
         (0,1,0) -> vert
         (0,0,1) -> bleu
         Cette fonction ne renvoie rien: elle initialise le composant graphique
         global IMG qui est l'objet pyplot correspondant à une image donnée sous
         la forme d'un tableau. Elle crée également la fenêtre graphique pyplot.
    """
    global IMG
    FIG.show()
    IMG = AX.imshow(image)

def rafraichit(image):
    """
       Cette fonction est utilisée pour modifier le contenu de la fenêtre
       graphique du jeu.
       Entrées:
         * image: ndarray
           L'image à afficher dans la fenêtre pyplot.

       Notes:
         Une image est un tableau numpy de dimensions (largeur, hauteur, 3) car
         la couleur est représentée par un triplet de réels dans [0,1]:
         (0,0,0) -> noir
         (1,1,1) -> blanc
         (0.5, 0.5, 0.5) -> gris moyen
         (1,0,0) -> rouge
         (0,1,0) -> vert
         (0,0,1) -> bleu
         Cette fonction modifie le contenu du composant graphique global IMG qui
         est l'objet pyplot correspondant à une image donnée sous la forme d'un
         tableau.
    """
    global IMG
    IMG.set_data(image)
    IMG.axes.figure.canvas.draw()

def attend_clic():
    """
       Cette fonction est utilisée pour lire les coordonnées du curseur de la
       souris dans la fenêtre graphique et renvoyer les coordonnées associées
       dans le tableau numpy correspondant à l'image affichée.
       Sorties:
         * coordonnees: liste
           Coordonnées (ligne, colonne) du tableau numpy correspondant aux
           coordonnées du pointeur de la souris sur l'image affichée dans
           la fenêtre pyplot

       Notes:
         Une image stockée au format numpy (ndarray) est affichée avec le
         numéro de colonne du tableau comme abscisse et le numéro de ligne
         comme ordonnée. On passe donc des coordonnées graphiques aux
         coordonnées ndarray en permutant les composantes.
    """
    l_point = plt.ginput(1, timeout=0, show_clicks=False)
    while len(l_point)==0:
        l_point = plt.ginput(1, timeout=0, show_clicks=False)
    point = l_point[0]
    # Les coordonnées de la souris correspondent aux numéros de colonne et de
    # ligne du tableau ndarray de l'image affichée.
    # Par ailleurs, les coordonnées du pointeur sont des nombres réels qu'il
    # faut convertir en entiers pour localiser le pixel dans le tableau
    return([int(point[1]), int(point[0])])

def cree_texte(texte, couleur):
    """
       Cette fonction est utilisée pour modifier le contenu de la fenêtre
       graphique du jeu.
       Entrées:
         * image: ndarray
           L'image à afficher dans la fenêtre pyplot.

       Notes:
         Une image est un tableau numpy de dimensions (largeur, hauteur, 3) car
         la couleur est représentée par un triplet de réels dans [0,1]:
         (0,0,0) -> noir
         (1,1,1) -> blanc
         (0.5, 0.5, 0.5) -> gris moyen
         (1,0,0) -> rouge
         (0,1,0) -> vert
         (0,0,1) -> bleu
         Cette fonction modifie le contenu du composant graphique global IMG qui
         est l'objet pyplot correspondant à une image donnée sous la forme d'un
         tableau.
    """
    # On définit les couleurs dérivées
    couleur_foncee = [0.5 * i for i in couleur]
    couleur_claire = [0.5 + 0.5 * i for i in couleur_foncee]
    # On positionne le texte
    return(FIG.text(0.5, 0.6, texte, horizontalalignment='center', \
                    verticalalignment='center', color=couleur_foncee, size=24, transform=AX.transAxes, bbox=dict(boxstyle="round", ec=couleur, fc=couleur_claire)))
