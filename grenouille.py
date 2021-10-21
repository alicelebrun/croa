"""
    Ce fichier regroupe les structures et les services associés
    à la création et aux manipulations d'une grenouille
"""
# Modules internes
import carte
import graphique

def cree(identifiant, statut, priorite):
    """
       Crée la structure de données associée à une grenouille dans son
       état initial.
       Entrées:
         * identifiant: entier
           L'identifiant du joueur auquel appartient la grenouille
         * statut: booléen
           Indique si la grenouille est une reine (statut=True) ou une servante
           (statut=False)
         * priorite: entier
           La priorité permet de savoir si la grenouille *doit* être jouée au
           prochain tour (priorité 2), *peut* être jouée au prochain tour
           (priorité 1) ou *ne peut pas* être jouée au prochain tour (priotité 0)
       Sorties:
         * grenouille: liste
           Une liste [identifiant, statut, priorite]
    """
    grenouille=[]
    grenouille.append(identifiant)
    grenouille.append(statut)
    grenouille.append(priorite)
    return(grenouille)

def est_reine(grenouille):
    """
       Indique si une grenouille est une reine
       Entrées:
         * grenouille: liste
           La grenouille à tester
       Sorties:
         * statut: booléen
           Egal à True si la grenouille est une reine, à False si la grenouille est
           une servante
    """
    return(grenouille[1])

def est_servante(grenouille):
    """
       Indique si une grenouille est une servante
       Entrées:
         * grenouille: liste
           La grenouille à tester
       Sorties:
         * statut: booléen
           Egal à True si la grenouille est une servante, à False si la grenouille
           est une reine
    """
    return(not grenouille[1])

def renvoie_statut(grenouille):
    """
       Renvoie le statut d'une grenouille
       Entrées:
         * grenouille: liste
           La grenouille à consulter
       Sorties:
         * statut: booléen
           Egal à True si la grenouille est une reine, False si la grenouille est
           une servante
    """
    return(grenouille[1])

def renvoie_priorite(grenouille):
    """
       Renvoie la priorité d'une grenouille
       Entrées:
         * grenouille: liste
           La grenouille à consulter
       Sorties:
         * priorité: entier
           La priorité de la grenouille

       Notes:
       La priorité peut valoir
         * 0 si la grenouille ne peut pas être sélectionnée
         * 1 si la grenouille peut être sélectionnée de manière non prioritaire
         * 2 si la grenouille doit être sélectionnée de manière prioritaire
    """
    return(grenouille[2])

def modifie_priorite(grenouille, priorite):
    """
       Modifie la priorité d'une grenouille
       Entrées:
         * grenouille: liste
           La grenouille à modifier
         * priorité: entier
           La priorité de la grenouille

      Notes:
      La priorité peut valoir
        * 0 si la grenouille ne peut pas être sélectionnée
        * 1 si la grenouille peut être sélectionnée de manière non prioritaire
        * 2 si la grenouille doit être sélectionnée de manière prioritaire
      La fonction ne renvoie rien, la grenouille passée en argument est modifiée.
    """
    grenouille[2] = priorite

def renvoie_identifiant(grenouille):
    """
       Renvoie l'identifiant d'une grenouille
       Entrées:
         * grenouille: liste
           La grenouille à consulter
       Sorties:
         * identifiant: entier
           L'identifiant de la grenouille
    """
    return(grenouille[0])

def dessine(grenouille, position, est_vase_visible, i_base, j_base, image_plateau):
    """
       Modifie l'image du plateau pour y dessiner la grenouille selon son statut
       à la position donnée.
       Entrées:
         * grenouille: liste
           La grenouille à dessiner
         * position: entier
           Cf. Notes
         * est_vase_visible: booléen
           Si True, la grenouille est dessinée la tête en bas, si False la
           grenouille est dessinée en position normale
         * i_base: entier
           Le numéro de ligne du coin supérieur gauche de l'image de la carte
           dans le tableau numpy représentant le plateau de jeu
         * j_base: entier
           Le numéro de colonne du coin supérieur gauche de l'image de la carte
           dans le tableau numpy représentant le plateau de jeu
         * image_plateau: ndarray
           Le tableau numpy dans lequel ajouter l'image représentant la carte
       Modifie une image de plateau en y dessinant une grenouille donnée
       Entrées:
         * une grenouille (cf cree())
         * une position (entier)
         * un état (booléen)
         * une coordonnée horizontale (entier)
         * une coordonnée verticale (entier)
         * une image (ndarray)

       Notes:
         La position correspond au centrage de la grenouille au sein de sa dalle.
           * 1 pour une grenouille décalée sur la gauche au 1/4 de la dalle
           * 2 pour une grenouille au centre de la dalle
           * 3 pour une grenouille décalée sur la droite aux 3/4 de la dalle
         La fonction ne renvoie rien, l'image passée en argument est modifiée
    """
    if est_reine(grenouille):
        image = graphique.IMAGES_REINES[renvoie_identifiant(grenouille)]
    else:
        image = graphique.IMAGES_SERVANTES[renvoie_identifiant(grenouille)]
    largeur = image.shape[0]
    hauteur = image.shape[1]
    largeur_carte = graphique.IMAGES_FACES[0].shape[0]
    hauteur_carte = graphique.IMAGES_FACES[0].shape[1]
    decalage_i = i_base + largeur_carte // 2 - largeur // 2
    decalage_j = j_base + (position * hauteur_carte) // 4 - hauteur // 2
    # On n'affiche que les pixels qui ne sont pas blancs, c'est-à dire
    # dont la somme des composantes rouge, vert et bleu est strictement inférieure
    # à 3
    # Si la grenouille est dans la vase il faut
    # l'afficher couchée
    if renvoie_priorite(grenouille) == 0 and est_vase_visible:
        image = image[::-1, :]
        masque = image[:,:,0] + image[:,:,1] + image[:,:,2] < 3
        image_plateau[decalage_i:decalage_i + largeur, decalage_j:decalage_j + hauteur][masque] = image[masque]
    else:
        masque = image[:,:,0] + image[:,:,1] + image[:,:,2] < 3
        image_plateau[decalage_i:decalage_i + largeur, decalage_j:decalage_j + hauteur][masque] = image[masque]
