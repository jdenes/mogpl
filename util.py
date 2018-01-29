# -*- coding: utf-8 -*-

################################
###       PROJET MOGPL       ###
###  JULIEN DENES - 3772480  ###
################################

from matplotlib import colors, pyplot


""" INPUT:    un numéro d'instance (int)                                                                                """
""" OUTPUT:   un tuple (contraintes sur les lignes (liste de listes), contraintes sur les colonnes (liste de listes))   """

def createInstance (instance):  
    path = 'instances/' + str(instance) + '.txt'
    with open(path, 'r') as content_file:
        content = content_file.read().splitlines()
    sequencesLines = []
    sequencesRows = []
    diese = False
    
    for line in content:
        if (line == '#'): diese = True
        else: 
            block = []
            for x in line.split(): block.append(int(x))
            if (not diese): sequencesLines.append(block)
            if (diese): sequencesRows.append(block)  
    return (sequencesLines, sequencesRows)

    
""" INPUT:    un tableau bidimensionnel (liste de listes) rempli de -1, 0 ou 1                                          """
"""           un tuple (contraintes sur les lignes (liste de listes), contraintes sur les colonnes (liste de listes))   """
"""           optionnel : un booléen exprimant si l'on souhaite l'affichage des contraintes de l'instance               """
""" OUTPUT:   void, affiche le tableau en gris (-1), blanc (0), noir (1)                                                """

def display (A, constraints, axis = False):
    cmap = colors.ListedColormap(['grey','white','black'])
    bounds = [-1.5, -0.5, 0.5, 1.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    img = pyplot.imshow(A, cmap = cmap, norm = norm, interpolation = 'none')
    if (axis):
        pyplot.xticks(range(len(A[0])), [str(x)[1:-1].replace(',', '\n') for x in constraints[1]], fontsize = 8)
        pyplot.yticks(range(len(A)), [str(x)[1:-1].replace(',', ' ') for x in constraints[0]], fontsize = 8)
    pyplot.show(img)
    