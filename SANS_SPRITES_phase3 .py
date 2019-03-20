#!/usr/bin/env python
# -*- coding: utf-8 -*-

from upemtk import *
import os
from random import choice


def creation_map(fichier):
    """Crée la matrice de jeu , ainsi que les autres données , a partir du fichier map passé en paramètre"""

    # On crée les différentes données
    matrice = []
    lst_k = []
    lst_b = []
    joueur = None
    titre = ""

    
    with open(fichier) as f:
        
        for y, ligne in enumerate(f):
            
            # La ligne 0 correspond au titre , on ne recupère que celui-ci sans ce qu'il y a autour
            if y == 0:
                titre = ligne.split('"')[1]
                continue
            
            lst = []
            
            # On crée la matrice, et, pour un soucis de simplicité, on met les boites et les clés dans des listes a part
            
            for x, elt in enumerate(ligne):
                
                if elt != "\n":

                    if elt == "S":
                        lst.append(".")
                        joueur = (x, y-1)
                        continue

                    if elt == "K":
                        lst_k.append((x, y - 1))
                        lst.append(".")
                        continue

                    if elt == "B":
                        lst_b.append((x, y - 1))
                        lst.append(".")
                        continue

                    lst.append(elt)
                
            matrice.append(lst)
            
    return matrice, joueur, titre, lst_k, lst_b


def afficher_jeu(joueur, nb_k, titre):
    """Fonction qui prend en paramètre les éléments susceptibles de changer, ainsi que le titre,
    et affiche tous les elements du jeu a l'écran"""
    
    # On réinitialise l'affichage pour éviter que les éléments se chevauchent
    efface_tout()
    
    for y,lst in enumerate(matrice):
        for x,elt in enumerate(lst):

            # Affichage Clé
            if (x, y) in lst_k:
                cercle(x * 50 + 25, (y * 50) + 125, 15, remplissage="Green")

            # Affichage Boite
            if (x, y) in lst_b:
                rectangle(x * 50, (y * 50) + 100, x * 50 + 50, (y * 50) + 100 + 50, remplissage="Blue")

            # Affichage Case vide
            if elt == ".":
                rectangle(x * 50, (y * 50) + 100, x * 50 + 50, (y * 50) + 100 + 50)

            # Affichage Mur
            elif elt == "W":
                rectangle(x * 50, (y * 50) + 100, x * 50 + 50, (y * 50) + 100 + 50, remplissage="Red")

            # Affichage Porte
            elif elt == "D":
                rectangle(x * 50, (y * 50) + 100, x * 50 + 50, (y * 50) + 100 + 50, remplissage="Green")
                cercle(x * 50 + 25, (y * 50) + 125, 15, remplissage="White")

            # Affichage Cible
            elif elt == "T":
                rectangle(x * 50, (y * 50) + 100, x * 50 + 50, (y * 50) + 100 + 50, couleur="Blue", epaisseur=3)

        # On affiche le joueur a la fin
        x, y = joueur
        cercle(x * 50 + 25, (y * 50) + 125, 20, remplissage="Yellow", couleur="Yellow")
    
    # On affiche les informations supplémentaires au dessus
    texte(50, 5, titre, couleur='red')
    aff_k = "Clé(s) : " + str(nb_k)
    texte(50, 50, aff_k, couleur='red')

    
    mise_a_jour()


def evenement(joueur, debug, lst_k, lst_b, matrice, Map,titre):
    """Fonction qui gère les évènements et effectue l'action appropriée selon la touche pressée"""
    
    ev = donne_evenement()
    
    # Si rien ne se passe, on renvoie les données telles qu'elles
    if ev == ("RAS",""):
        return joueur,debug,lst_k,lst_b,matrice
    
    if type_evenement(ev) == "Touche":
        
        # Si c'est une touche directionelle, on met a jour avec la fonction déplacement la position du joueur
        if touche(ev) == "Up":
            joueur = deplacement(joueur,"Up", nb_k)
            
        elif touche(ev) == "Down":
            joueur = deplacement(joueur,"Down", nb_k)
            
        elif touche(ev) == "Right":
            joueur = deplacement(joueur,"Right", nb_k)
            
        elif touche(ev) == "Left":
            joueur = deplacement(joueur,"Left", nb_k)
        
        # Si on appuie sur la touche 'r', on reset tout le jeu a partir du fichier de la map
        elif touche(ev) == "r":
            matrice, joueur, lst_k , lst_b = reset(Map)
        
        # Si on appuie sur 'd', on active le mode debug, s'activant alors dès le prochain tour de boucle
        elif touche(ev) == "d":
            debug = True
        
        # Si on appuie sur 's' (save), on sauvegarde la map dans son etat actual
        elif touche(ev) == "s":
            save_map(titre, joueur, Map)
        
        # Si on appuie sur 'l' (load), on charge la dernière sauvegarde associée a la map en question
        elif touche(ev) == "l":
            joueur, debug, lst_k, lst_b, matrice,titre = load_save(Map)

    if type_evenement(ev) == "Quitte":
        exit()
            
    return joueur,debug,lst_k,lst_b,matrice


def reset(Map):
    """Réinitialise la carte en remettant toutes les valeurs a celles de bases, prend en argument le chemin du niveau"""

    # On utilise une variable globale pour simplifier le programme
    global nb_k
    
    # On efface l'affichage précédent
    efface_tout()

    # On remet a 0 le nombre de clés
    nb_k = 0
    
    # On reprend les données de début et on les affiche a l'écran
    matrice, joueur, titre, lst_k, lst_b = creation_map(Map)
    afficher_jeu(joueur, nb_k,titre)

    return matrice, joueur,lst_k,lst_b


def collision(joueur, direction, nb_k):
    """Fonction qui vérifie si le joueur peut se déplacer dans une direction et renvoie False si le
    déplacement est possible"""
    
    x, y = joueur
    
    # On vérifie que le joueur ne sort pas du jeu
    if x in range(len(matrice[0])) and y in range(len(matrice)):
        
        # On vérifie si le joueur tente de se déplacer vers une boite
        if (x, y) in lst_b:
            
            # Si Oui, on verifie si on peut déplacer la boite
            if deplacement_box(matrice, joueur, direction) is True:
                return False
            else:
                return
        
        # Si le joueur tente de se déplacer dans une cible vide, ou une case vide, on autorise le déplacement
        if matrice[y][x] in ["T", "."]:
            return False
        
        # Si le joueur tente d'aller dans une porte, on vérifie qu'il puisse l'ouvrir
        if matrice[y][x] == "D":
            if ouverture_porte(joueur, nb_k) is True:
                return False


def deplacement_box(matrice, joueur, direction):
    """Fonction gérant le déplacement des boites, prend en paramètre la direction afin de savoir dans quel sens il faut
    déplacer la boite.
    On regarde si le déplacement de la boîte est possible, si oui, on met a jour les données"""
    x, y = joueur
    
    # On vérifie pour la direction indiquée si la boite peut se déplacer
    # (qu'elle ne rentre pas en collision avec une autre boite ou tout bloc "dur" et qu'elle ne sort pas de la matrice)
    if x in range(len(matrice[0])) and y - 1 in range(len(matrice)):
        if direction == "Up" and matrice[y-1][x] in [".", "T"] and (x, y-1) not in lst_b:
            
            # Si le déplacement est possible , on met a jour les coordonnées de la boite :
            # On récupère l'indice de la boite qui va être déplacée
            rang_box = lst_b.index((x, y))
            # Puis on le modifie
            lst_b[rang_box] = (x, y-1)
            return True
    
    # On repète les mêmes actions pour chaque direction :

    if x in range(len(matrice[0])) and y + 1 in range(len(matrice)):
        if direction == "Down" and matrice[y+1][x] in [".", "T"] and (x, y+1) not in lst_b:

            rang_box = lst_b.index((x, y))
            lst_b[rang_box] = (x, y + 1)
            return True

    if x - 1 in range(len(matrice[0])) and y in range(len(matrice)):
        if direction == "Left" and matrice[y][x-1] in [".", "T"] and (x-1, y) not in lst_b:

            rang_box = lst_b.index((x, y))
            lst_b[rang_box] = (x - 1, y)
            return True

    if x + 1 in range(len(matrice[0])) and y in range(len(matrice)):
        if direction == "Right" and matrice[y][x+1] in [".", "T"] and (x+1, y) not in lst_b:

            rang_box = lst_b.index((x, y))
            lst_b[rang_box] = (x + 1, y)
            return True


def stock_cle(joueur, action):
    """Fonction gérant le stock de clé du joueur, elle est appelée lorsque le joueur récupère ou utilise des clés
    c'est-a-dire lorsqu'il en gagne ou qu'il en perd. C'est a cela que sert le paramètre action (qui prend soit la
    valeur 'add' ou 'remove')"""
    
    global nb_k
    
    # Si on souhaite ajouter une clé
    if action == "add":
        # On recherche la clé ou se trouve le joueur, on la retire de la liste et on ajoute 1 au nombre de clés
        for elt in lst_k:

            if elt == joueur:
                lst_k.remove(elt)
                nb_k += 1
    
    # Si on souhaite utiliser une clé, alors on met a jour la variable en enlevant 1
    elif action == "remove":
        nb_k -= 1


def ouverture_porte(joueur, nb_k):
    """Fonction pour l'ouverture des portes, renvoie True si l'ouverture est possible"""
    
    x, y = joueur
    
    # Si le joueur a au moins une clé, on enlève la porte de la matrice et supprime la clé au joueur,
    # enfin on renvoie True pour signifier que l'on peut ouvrir la porte
    if nb_k > 0:
        matrice[y][x] = "."
        stock_cle(joueur, "remove")
        return True


def deplacement(joueur, direction, nb_k):
    """Prend les coordonnées du joueur et la direction dans laquelle il se rend et met a jour les données si le
    déplacement est possible"""
    
    # On regarde pour la direction indiquée si le déplacement est possible, si oui,
    # on renvoie les coordonnées du joueur mises a jour
    if direction == "Up" and collision((joueur[0],joueur[1]-1), direction, nb_k) is False:
        return joueur[0], joueur[1]-1
    
    elif direction == "Down" and collision((joueur[0],joueur[1]+1), direction, nb_k) is False:
        return joueur[0], joueur[1]+1
    
    elif direction == "Left" and collision((joueur[0]-1,joueur[1]), direction, nb_k) is False:
        return joueur[0]-1, joueur[1]
    
    elif direction == "Right" and collision((joueur[0]+1,joueur[1]), direction, nb_k) is False:
        return joueur[0]+1, joueur[1]
    
    # On retourne la position du joueur telle qu'elle si il n'y a pas eu de déplacement
    return joueur


def fonction_debug(joueur, debug):
    """Fonction permettant au joueur de faire des déplacements aléatoires de manière rapide sans a avoir a attendre une
    action de l'utilisateur"""

    ev = donne_evenement()
    
    # On regarde si le joueur désactive le mode débug
    if type_evenement(ev) == "Touche":
        if touche(ev) == "d":
            debug = False
    directions = ["Up", "Left", "Down", "Right"]
    # On renvoie le joueur après un déplacement aléatoire ainsi que l'état du débug
    return deplacement(joueur, choice(directions), nb_k), debug


def win(matrice, lst_b):
    """Fonction vérifiant si le joueur a gagné pour mettre fin au jeu"""
    
    # On vérifie, pour chaque boite de la liste, si elle est dans une cible
    for elt in lst_b:
        
        if matrice[elt[1]][elt[0]] == "T":
            
            continue
        
        else:

            # Si oui, on retourne True, sinon on retourne False
            return False

    return True


def save_map(Titre, Joueur, Map):
    """Ecrit dans un fichier (sous la forme "map.save") l'état actuel de la partie pour le récupérer plus tard"""
    
    if ".save" in Map:
        chemin_map = Map
    
    else:
        chemin_map = Map + ".save"
    
    if "\n" in Titre:
        Titre = Titre.replace("\n","")
    
    with open(chemin_map,"w") as save:
        
        # On sauvegarde (dans l'ordre) : Le titre, la position du joueur, les possitions des boites, les positions des
        # clés, le nombre de clés qu'a le joueur et enfin la matrice
        
        save.write(Titre+"\n")
        save.write(str(Joueur)+"\n")
        
        for elt in lst_b:
            
            save.write(str(elt)+";")
        
        save.write("\n")
        
        for elt in lst_k:
            
            save.write(str(elt)+";")
        
        save.write("\n")
        
        save.write(str(nb_k)+"\n")
        
        for lst in matrice:
            
            save.writelines(lst)
            save.write("\n")


def load_save(Map):
    """Fonction lisant le fichier ("map.save") sauvegardé au préalable"""
    global nb_k
    
    if ".save" not in Map:
        chemin_map = Map + ".save"
    
    else:
        chemin_map = Map
    
    debug = False
    
    with open(chemin_map) as save:
        
        matrice = []
        
        ligne = save.readlines()
        # On récupère le titre
        Titre = ligne[0]
        
        # On récupère les coordonnées de joueur (en enlevant les caractères superflus) et on les remet sous forme de tuple
        joueur = ligne[1].replace("(","").replace(")","").replace("\n","").replace(" ","").split(",")
        joueur = (int(joueur[0]),int(joueur[1]))
        
        # On lit la liste des coordonnées des boites, et comme pour 'joueur', on les remet sous forme de tuples
        lst_b = [tuple(elt.replace("(","").replace(")","").replace(" ","").split(",")) for elt in ligne[2].split(";") if elt != "\n"]
        lst_b = list(map(lambda x: (int(x[0]), int(x[1])) , lst_b))
        
        # On effectue la même opération que sur la listes des coordonnées des boites
        lst_k = [tuple(elt.replace("(","").replace(")","").replace(" ","").split(",")) for elt in ligne[3].split(";") if elt != "\n"]
        lst_k = list(map(lambda x: (int(x[0]), int(x[1])) , lst_k))
        
        # On recupère le nombre de clé en le transtypant en entier et en enlevant les caractères superflus
        nb_k = int(ligne[4].replace("\n",""))
        
        # On lit la matrice a la fin du fichier pour mettre a jour l'actuelle matrice affichée
        for ligne_matrice in ligne[5:]:
            
            lst = list()
            
            for elt in ligne_matrice:
                
                if elt != "\n":
                    
                    lst.append(elt)
            
            matrice.append(lst)
        
        # On renvoie les données mises a jour
        return joueur, debug, lst_k, lst_b, matrice,Titre


def editeur():
    """Editeur de niveau"""

    cree_fenetre(800, 500)
    selecteur = "."
    
    # On recupère les valeurs nécéssaires : hauteur/largeur et nom de fichier
    hauteur_map = entree_utilisateur("Entrez la Hauteur de la Map", int)
    largeur_map = entree_utilisateur("Entrez la Largeur de la Map", int)
    Nom_map = entree_utilisateur("Entrez le nom de fichier de la map a creer ou a modifier", str, lettres=True)

    # On cree une fenêtre adapté a la taille de la map en cours de creation
    # On impose une largeur minimale 450
    
    if largeur_map * 50 < 450:
        largeur_fenetre = 450
    else:
        largeur_fenetre = largeur_map*50
    # On ouvre la fenêtre au proportion calculées
    ferme_fenetre()
    
    # On affiche les instruction
    cree_fenetre(450,450)
    image(0,0,"sprites/instructions_editeur.png", ancrage="nw")
    attente_touche()
    ferme_fenetre()
    
    cree_fenetre(largeur_fenetre, hauteur_map*50+100)
    
    # On crée la matrice de la nouvelle carte
    carte = [["." for i in range(largeur_map)] for j in range(hauteur_map)]
    
    Continuer = True
    while Continuer:
        # On récupère les évènements et on met a jour la matrice
        affiche_editeur(carte,largeur_fenetre)
        selecteur, Continuer = gestion_ev_editeur(carte, largeur_fenetre, selecteur)
    
    ferme_fenetre()
    cree_fenetre(800, 500)
    nomfichier = entree_utilisateur("Entrez le nom de fichier", str, lettres=True)
    
    enregistrer_editeur(carte,Nom_map,nomfichier)
    
    # On ferme la fenetre pour ensuite retourner au menu
    ferme_fenetre()


def entree_utilisateur(Texte, typeval, lettres=False):
    """On affiche un message passé en paramètres dans la fenêtre , et on lui applique la fonctiona a la fin"""
    val = ""
    
    while True:
        efface_tout()
        texte(50,5,Texte,taille=15)
        texte(50,200,val)
        mise_a_jour()
        ev = donne_evenement()
            
        if type_evenement(ev) == "Touche":
                
            if touche(ev) == "Escape":
                exit()
                
            elif touche(ev) in "1234567890":
                val += touche(ev)
            
            # On autorise les lettres seulement si lettres a été passé en paramètres comme True
            elif lettres is True and touche(ev) in "azertyuiopqsdfghjklmwxcvnbAZERTYUIOPQSDFGHJKLMWXCVBN":
                val += touche(ev)
            
            elif touche(ev) == "Return":
                return typeval(val)
            
            elif touche(ev) == "BackSpace":
                val = val[:-1]
        
        if type_evenement(ev) == "Quitte":
            exit()


def affiche_editeur(carte, largeur_fenetre):
    """Similaire a afficher jeu , mais pour la map editée"""
    # On réinitialise l'affichage pour éviter que les éléments se chevauchent
    efface_tout()
    decalage = 0
    
    # On calcule le decalage si la fenêtre a la largeur minimale (450)
    if largeur_fenetre == 450:
        decalage = (largeur_fenetre-len(carte[0])*50) /2
    
    # Affichage Selecteurs
    rectangle(0,0,largeur_fenetre,99,couleur="grey",remplissage="grey")

    ###Case Vide
    rectangle(largeur_fenetre / 2 - 25, 30, largeur_fenetre / 2 + 25, 80)
    ###Boite
    rectangle(largeur_fenetre / 2 - 75, 30, largeur_fenetre / 2 - 25, 80, remplissage="Blue")
    ###Clé
    cercle(largeur_fenetre / 2 - 100, 55, 15, remplissage="Green")
    ###Porte
    rectangle(largeur_fenetre / 2 - 175, 30, largeur_fenetre / 2 - 125, 80, remplissage="Green")
    cercle(largeur_fenetre / 2 - 150, 55, 15, remplissage="White")
    ###Mur
    rectangle(largeur_fenetre / 2 + 25, 30, largeur_fenetre / 2 + 75, 80, remplissage="Red")
    ###Cible
    rectangle(largeur_fenetre / 2 + 75, 30, largeur_fenetre / 2 + 125, 80, couleur="Blue", epaisseur=3)
    ###Spawn
    cercle(largeur_fenetre / 2 + 150, 55, 20, remplissage="yellow")

    for y, lst in enumerate(carte):
        for x, elt in enumerate(lst):

            # Affichage Clé
            if elt == "K":
                cercle(x * 50 + 25 + decalage, (y * 50) + 125, 15, remplissage="Green")
                rectangle(x * 50 + decalage, (y * 50) + 100, x * 50 + 50 + decalage, (y * 50) + 100 + 50)

            # Affichage Boite
            if elt == "B":
                rectangle(x * 50 + decalage, (y * 50) + 100, x * 50 + 50 + decalage, (y * 50) + 100 + 50,
                          remplissage="Blue")

            # Affichage Case vide
            if elt == ".":
                rectangle(x * 50 + decalage, (y * 50) + 100, x * 50 + 50 + decalage, (y * 50) + 100 + 50)

            # Affichage Mur
            elif elt == "W":
                rectangle(x * 50 + decalage, (y * 50) + 100, x * 50 + 50 + decalage, (y * 50) + 100 + 50,
                          remplissage="Red")

            # Affichage Porte
            elif elt == "D":
                rectangle(x * 50 + decalage, (y * 50) + 100, x * 50 + 50 + decalage, (y * 50) + 100 + 50,
                          remplissage="Green")
                cercle(x * 50 + 25 + decalage, (y * 50) + 125, 15, remplissage="White")

            # Affichage Cible
            elif elt == "T":
                rectangle(x * 50 + decalage, (y * 50) + 100, x * 50 + 50 + decalage, (y * 50) + 100 + 50,
                          couleur="Blue", epaisseur=3)

            elif elt == "S":
                cercle(x * 50 + 25 + decalage, (y * 50) + 125, 20, remplissage="Yellow", couleur="Yellow")
                rectangle(x * 50 + decalage, (y * 50) + 100, x * 50 + 50 + decalage, (y * 50) + 100 + 50)

    mise_a_jour()


def gestion_ev_editeur(carte, largeur_fenetre, selecteur):
    decalage = 0
    Continuer = True

    if largeur_fenetre == 450:
        decalage = (largeur_fenetre - len(carte[0]) * 50) // 2

    ev = donne_evenement()

    if type_evenement(ev) == "ClicGauche":

        coordonees = (int(clic_x(ev)), int(clic_y(ev)))
        # Permet de recuperer la valeur x et y
        x, y = int((coordonees[0] - decalage) / 50), int((coordonees[1] - 100) / 50)
        if y in range(len(carte)) and x in range(len(carte[0])) and coordonees[0] in range(decalage, len(
                carte[0]) * 50 + decalage) and coordonees[1] in range(100, len(carte) * 50 + 100):
            carte[y][x] = selecteur

        ###Vérification clic sur selecteurs

        elif coordonees[0] in range(largeur_fenetre // 2 - 25, largeur_fenetre // 2 + 25) and coordonees[1] in range(30,
                                                                                                                     80):
            selecteur = "."

        elif coordonees[0] in range(largeur_fenetre // 2 - 75, largeur_fenetre // 2 - 25) and coordonees[1] in range(30,
                                                                                                                     80):
            selecteur = "B"

        elif coordonees[0] in range(largeur_fenetre // 2 - 125, largeur_fenetre // 2 - 75) and coordonees[1] in range(
                30, 80):
            selecteur = "K"

        elif coordonees[0] in range(largeur_fenetre // 2 - 175, largeur_fenetre // 2 - 125) and coordonees[1] in range(
                30, 80):
            selecteur = "D"

        elif coordonees[0] in range(largeur_fenetre // 2 + 25, largeur_fenetre // 2 + 75) and coordonees[1] in range(30,
                                                                                                                     80):
            selecteur = "W"

        elif coordonees[0] in range(largeur_fenetre // 2 + 75, largeur_fenetre // 2 + 125) and coordonees[1] in range(
                30, 80):
            selecteur = "T"

        elif coordonees[0] in range(largeur_fenetre // 2 + 125, largeur_fenetre // 2 + 175) and coordonees[1] in range(
                30, 80):
            selecteur = "S"
            
    
    if type_evenement(ev) == "Touche":
        
        #Si on appuit sur entrée , on vérifie que la map est valide avant d'autoriser son enregistrement
        if touche(ev) == "Return":
            if valide(carte):
                return selecteur, False
        """
        elif touche(ev) == "Escape":
            ferme_fenetre()
            menu()
        """
    
    if type_evenement(ev) == "Quitte":
        exit()

    return selecteur, Continuer


def valide(carte):
    
    dico_elt = dict()
    
    # On met chaque élément dans un dico par le nombre de fois ou ils apparaissent
    for ligne in carte:
        for elt in ligne:
            
            if elt not in dico_elt.keys():
                dico_elt[elt]=1
            else:
                dico_elt[elt]+=1
    
    dico_keys = dico_elt.keys()
    # On vérifie quelques erreurs et on les affiche dans la console
    
    if "T" not in dico_keys or "B" not in dico_keys or "S" not in dico_keys:
        print("Map non valide , il manque une élément obligatoire(Target , Spawn du joueur ou Box)")
        return False
    
    if dico_elt["B"] != dico_elt["T"]:
        print ("Pas le même nombre de Box et de Target")
        return False
    
    if dico_elt["S"] > 1:
        print("Il y a trop de Spawn")
        return False
    
    return True


def enregistrer_editeur(carte, Nom_map, nomfichier):
    
    # On écrit le titre de la map puis la matrice qui la compose
    with open("map/"+nomfichier,"w") as f:
        f.write("Titre : \""+Nom_map+"\"\n")
        
        for ligne in carte:
            for elt in ligne:
                f.write(elt)
            f.write("\n")


def affiche_menu(taille_fenetre):
    """Fonction affichant dans une fenetre préalablement créée tous les éléments immobiles du menu principal"""

    # On affiche le rectangle servant de couleur d'arriere-plan
    rectangle(0, 0, taille_fenetre - 1, taille_fenetre - 1, remplissage='dark blue')

    # On crée les variables correspondant au marge et a la taille des rectangles contenant le texte,
    # afin de les modifier facilement si nécessaire
    big_margin = 60
    small_margin = 40
    hauteur_rectangle = 100

    # On crée les rectangles
    for y in range(big_margin - 1, taille_fenetre - big_margin, small_margin + hauteur_rectangle):

        rectangle(big_margin, y, taille_fenetre - big_margin, y + hauteur_rectangle, remplissage='light yellow')

    # On écrit le texte a l'intérieur de chacun d'entre eux
    texte(taille_fenetre//2, 110, 'Jouer', couleur='blue', ancrage='center', taille=24)
    texte(taille_fenetre//2, 250, 'Editeur de niveau', couleur='blue', ancrage='center', taille=24)
    texte(taille_fenetre//2, 390, 'Quitter', couleur='blue', ancrage='center', taille=24)


def deplacement_selection(lst, selection, direction):
    """Prend en parametre la liste des options du menu principal, la précedente option selectionnée et la touche pressée
     par l'utilisateur (soit 'Up', soit 'Down'). Renvoie le nouvel élément de la liste sélectionné"""

    # On garde dans une variable l'indice de la précedente sélection
    i = lst.index(selection)

    # La liste des options est faite ainsi : l'element d'indice 0 est affiché en haut, le plus grand indice est en bas

    if direction == 'Up':
        # Donc si l'utilisateur a appuyé sur 'Up' (fleche du haut), on renvoie l'élément précedent dans la liste
        return lst[i - 1]

    # Si le dernier élément sélectionné est le dernier élément de la liste, on renvoie le premier
    elif selection == lst[-1]:
        return lst[0]

    # Sinon, l'utilisateur a forcément appuyé sur 'Down' (c'est la seule autre option)
    else:
        # On renvoie donc l'élément suivant
        return lst[i + 1]


def selection_menu(taille_fenetre):
    """Boucle principale du menu principal"""

    # On crée la liste des options disponibles dans le menu principal
    lst_options = ['jeu', 'editeur', 'quitter']
    # Le menu s'ouvre avec l'option tout en haut de l'ecran comme premiere selection
    selection = lst_options[0]

    while True:
        # On attend un évenement de la part de l'utilisateur
        ev = donne_evenement()
        type_ev = type_evenement(ev)

        # Si il a appuyé sur une touche
        if type_ev == 'Touche':

            # Si la touche est la fleche 'Bas' ou 'Haut' :
            if touche(ev) in ['Down', 'Up']:
                # On efface tout ce qui a été affiché
                efface_tout()
                # On réaffiche le menu
                affiche_menu(taille_fenetre)
                # La sélection change en fonction de la direction pressée
                selection = deplacement_selection(lst_options, selection, touche(ev))

            # Si la touche est 'Entrée' :
            elif touche(ev) == 'Return':
                # L'utilisateur a sélectionné son option, donc on la renvoie
                return selection

        # Si l'utilisateur a cliqué sur l'icone 'croix' pour fermer la fenetre, on quitte le programme
        if type_evenement(ev) == "Quitte":
            exit()

        # On affiche la sélection (un rectangle aux bords jaunes autour de l'option sélectionnée) et on met a jour
        # l'affichage
        affiche_selection(lst_options, selection)
        mise_a_jour()


def menu():
    """Fonction principale gérant le menu, renvoyant la sélection choisie par l'utilisateur dans le menu principal"""

    # On définit la taille de la fenetre du menu, puis on la crée
    taille_fenetre = 500
    cree_fenetre(taille_fenetre, taille_fenetre)

    # On affiche le menu une premiere fois sur la nouvelle fenetre
    affiche_menu(taille_fenetre)
    # On rentre dans la boucle principale du menu, des que l'utilisateur a appuyé sur 'Entrée', la sélection est faite
    # et renvoyée a cette fonction
    selection = selection_menu(taille_fenetre)

    # Une fois la sélection faite, on ferme la fenetre du menu pour laisser place a celle de la sélection
    ferme_fenetre()

    return selection


def affiche_selection(lst, selection):
    """Affiche le rectangle aux bords jaunes autour de la sélection dans le menu principal"""

    # Pour chaque indice d'élément dans la liste des options du menu
    for i in range(len(lst)):

        # Si l'élément d'indice i est la sélection :
        if lst[i] == selection:
            # On affiche un rectangle avec des bordures jaunes d'une épaisseur de 10px
            rectangle(50, 50 + 140*i, 450, 170 + 140*i, couleur='yellow', epaisseur=10)


def selection_niv(taille_fenetre, lst_map):
    """Boucle principale du menu de sélection de niveau"""

    # Le menu s'ouvre avec l'option tout en haut de l'écran comme premiere sélection
    selection = lst_map[0]

    # On crée des pages (des sous-listes de lst_map contenant autant de niveaux
    # qu'une page peut afficher) et on fait afficher la premiere au debut
    pages = creation_page(lst_map)
    lst_map = pages[0]

    # On initialise le nombre de pages a 0
    nb_page = 0
    while True:

        # On attend un évenement de la part de l'utilisateur
        ev = donne_evenement()
        type_ev = type_evenement(ev)

        # Si il a appuyé sur une touche
        if type_ev == 'Touche':

            # Si la touche est 'Entrée' :
            if touche(ev) == 'Return':
                # L'utilisateur a sélectionné son option, donc on la renvoie
                return selection

            # Si la touche est la fleche 'Gauche' ou 'Droite' :
            if touche(ev) in ['Left', 'Right']:
                # La page va changer, l'indice de la nouvelle page est renvoyé par la fonction selection_page
                nb_page = selection_page(nb_page, len(pages), touche(ev))
                # La liste des cartes a afficher change pour devenir la liste des cartes de la nouvelle page
                lst_map = pages[nb_page]
                # La nouvelle page s'ouvre avec l'option tout en haut sélectionnée
                selection = lst_map[0]

                # On efface la précedente page et on réaffiche le menu de sélection avec la bonne page
                efface_tout()
                affiche_menu_niv(taille_fenetre, lst_map)

            # Si la touche est la fleche 'Gauche' ou 'Droite' :
            if touche(ev) in ['Down', 'Up']:

                # La sélection va changer donc :
                # On efface tous les éléments affichés précedemment et on réaffiche le menu
                efface_tout()
                affiche_menu_niv(taille_fenetre, lst_map)
                # La nouvelle sélection est renvoyée par la fonction deplacement_selection
                selection = deplacement_selection(lst_map, selection, touche(ev))

        # Si l'utilisateur a cliqué sur l'icone 'croix' pour fermer la fenetre, on quitte le programme
        if type_ev == "Quitte":
            exit()

        # On affiche la sélection (un rectangle aux bords jaunes autour de l'option sélectionnée) et on met a jour
        # l'affichage
        affiche_selection_niv(lst_map, selection)
        mise_a_jour()


def liste_map():
    """Renvoie la liste triée de tous les niveaux et sauvegardes jouables"""

    # On crée une liste vide
    lst_map = []

    # Pour chaque élément dans la liste des fichiers dans le dossier 'map'
    for fic in os.listdir('map'):
        # Si l'élément est un fichier, on l'ajoute a la liste
        if os.path.isfile(os.path.join('map', fic)):
            lst_map.append(fic)

    # On renvoie la liste triée par la fonction sorted
    return sorted(lst_map)


def affiche_instructions():
    """Fonction affichant les instructions du menu de sélection de niveau"""

    # On crée une fenetre
    cree_fenetre(450, 450)

    # On affiche l'image contenant les instructions
    image(0, 0, 'sprites/instructions_selec_niv.png', ancrage='nw')

    # On attend que l'utilisateur appuie sur n'importe quelle touche pour continuer
    attente_touche()
    ferme_fenetre()


def affiche_menu_niv(taille_fenetre, lst_map):
    """Fonction affichant dans une fenetre préalablement créée tous les éléments immobiles du menu de sélection de
    niveau"""

    # On affiche le rectangle servant de couleur d'arriere-plan
    rectangle(0, 0, taille_fenetre - 1, taille_fenetre - 1, remplissage='dark blue')

    # On crée les variables correspondant au marge et a la taille des rectangles contenant le texte,
    # afin de les modifier facilement si nécessaire
    big_margin = 40
    small_margin = 40
    hauteur_rectangle = 50

    # On crée les rectangles
    for y in range(big_margin - 1, taille_fenetre - big_margin, small_margin + hauteur_rectangle):
        rectangle(big_margin, y, taille_fenetre - big_margin, y + hauteur_rectangle, remplissage='light yellow')

    decalage_texte = big_margin + (hauteur_rectangle//2)
    # On crée un compteur afin de s'arreter quand toutes les cartes sont affichées
    i = 0
    for y in range(decalage_texte, decalage_texte + 5*(small_margin+hauteur_rectangle), small_margin+hauteur_rectangle):
        texte(taille_fenetre // 2, y, lst_map[i], couleur='blue', ancrage='center', taille=24)
        i += 1

        # Si le compteur a dépassé l'indice maximum (len(lst) - 1), on sort de la boucle
        if i == len(lst_map):
            break


def affiche_selection_niv(lst, selection):
    """Affiche le rectangle aux bords jaunes autour de la sélection dans le menu de sélection de niveau"""

    # Pour chaque indice d'élément dans la liste des options du menu
    for i in range(len(lst)):

        # Si l'élément d'indice i est la sélection :
        if lst[i] == selection:
            # On affiche un rectangle avec des bordures jaunes d'une épaisseur de 10px
            rectangle(30, 30 + 90*i, 470, 100 + 90*i, couleur='yellow', epaisseur=10)


def menu_niv():
    """Fonction principale gérant le menu, renvoyant la sélection choisie par l'utilisateur dans le menu de sélection
    de niveau"""

    # On fait appel a la fonction ouvrant une fenetre contenant les instructions pour ce menu
    affiche_instructions()

    # On définit la taille de la fenetre du menu, puis on la crée
    taille_fenetre = 500
    cree_fenetre(taille_fenetre, taille_fenetre)

    # On crée la liste de tous les niveaux et sauvegardes jouables dans le dossier 'map'
    lst_map = liste_map()

    # On affiche le menu de sélection de niveau une premiere fois sur la nouvelle fenetre
    affiche_menu_niv(taille_fenetre, lst_map)
    # On rentre dans la boucle principale du menu, ou l'utilisateur peut faire sa sélection
    selection = selection_niv(taille_fenetre, lst_map)

    # Une fois la sélection faite, on ferme la fenetre du menu pour laisser place a celle de la sélection
    ferme_fenetre()
    # Puis on renvoie la sélection
    return selection


def creation_page(lst_map):
    """Fonction créant les pages, chacune contenant au maximum 5 cartes.
    Prend en parametre la liste de tous les niveaux et sauvegardes jouables dans le dossier 'map'.
    Renvoie une liste de listes, chaque sous-liste correspondant a une page, chaque page est donc une liste contenant au
    maximum 5 cartes"""

    nb_map = len(lst_map)

    pages = []

    i = 0
    page = []
    while i < nb_map:

        # On ajoute la carte d'indice i dans la page en train d'etre créée
        page.append(lst_map[i])
        i += 1

        # Si la page contient 5 cartes, la liste finale ajoute la liste page, puis on réinitialise la page a une liste vide
        if len(page) == 5:
            pages.append(page)
            page = []

    # Les deux lignes suivantes servent a ajouter la derniere page si celle-ci n'est pas pleine (donc que le nombre
    # total de cartes n'est pas un multiple de 5

    # Si la page n'est pas vide et qu'elle n'est pas deja dans la liste finale (donc qu'elle ne contient pas 5 cartes):
    if page != [] and page not in pages:
        # On ajoute cette page a la liste finale
        pages.append(page)

    # On renvoie la liste des pages
    return pages


def selection_page(i, nb_pages, direction):
    """Fonction prenant en parametre l'indice de la precedente page, le nombre total de pages, et la touche pressée
    par le joueur. Elle renvoie l'indice de la nouvelle page a afficher."""

    # La liste des options est faite ainsi : la page d'indice 0 sera affichée le plus "vers la gauche" possible,
    # la page avec le plus grand indice sera affichée le plus "vers la droite" possible.

    if direction == 'Left':
        # La direction est la gauche, a moins que la page soit la premiere (auquel cas on renvoie le meme indice
        # puisqu'on ne veut pas changer de page)
        if i == 0:
            return i

        # On renvoie l'indice précedent
        return i - 1

    else:
        # La direction est la droite, a moins que la page soit la derniere (auquel cas on renvoie le meme indice
        # puisqu'on ne veut pas changer de page)

        if i == nb_pages - 1:
            return i

        # On renvoie l'indice suivant
        return i + 1


if __name__ == '__main__':

    while True:
        # On ouvre le menu principal
        selection = menu()

        # Si la sélection est de quitter le menu principal
        if selection == 'quitter':
            # On quitte le programme
            exit()

        # Si la sélection est l'editeur graphique
        if selection == 'editeur':
            # On lance l'editeur
            editeur()

        # Si la sélection est de jouer
        if selection == 'jeu':
            # On ouvre le menu de sélection de niveau
            Map = 'map/' + menu_niv()

            # On crée les données nécessaires :

            # Si la carte contient la chaine '.save', alors on sait que c'est une sauvegarde et on la charge
            if ".save" in Map:
                joueur, debug, lst_k, lst_b, matrice, titre = load_save(Map)

            # Sinon c'est une carte, on crée les données
            else:
                matrice, joueur, titre, lst_k, lst_b = creation_map(Map)
                debug = False
                Win = False
                nb_k = 0

            # On crée la fenêtre, ayec une taille relative a la taille de la matrice
            taille_fenetre = (len(matrice[0]) * 50, len(matrice) * 50 + 100)
            cree_fenetre(taille_fenetre[0], taille_fenetre[1])

            # Boucle principale, tourne tant le booléen win est False, c'est-a-dire tant que le joueur n'a pas gagné
            while True:

                # On actualise l'affichage
                afficher_jeu(joueur, nb_k, titre)

                # On vérifie si le joueur n'a pas gagné
                Win = win(matrice, lst_b)

                # Si le joueur a gagné , on affiche un Bravo , et on on attend qu'il n'appuie sur n'importe quelle
                # touche pour sortir de la boucle principale et retourner au menu
                if Win is True:
                    efface_tout()
                    ferme_fenetre()
                    cree_fenetre(600,150)
                    texte(50,50, "Bravo ! Vous avez gagné")
                    attente_clic()
                    ferme_fenetre()
                    break

                # Si le debug est activé, on appelle la fonction debug, la fonction evenement sinon
                if debug is False:
                    joueur, debug, lst_k, lst_b, matrice = evenement(joueur, debug, lst_k, lst_b, matrice, Map,titre)
                else:
                    joueur, debug = fonction_debug(joueur, debug)

                # On vérifie si le joueur n'est pas sur une clé
                stock_cle(joueur, "add")

