# -*- coding: utf-8 -*-

################################
###       PROJET MOGPL       ###
###  JULIEN DENES - 3772480  ###
################################

from time import time
from util import createInstance, display
from dynamicProg import colorationDP
from linearProg import colorationLP
from sys import version_info


""" INPUT:    un tuple (contraintes sur les lignes (liste de listes), contraintes sur les colonnes (liste de listes))   """
""" OUTPUT:   un tuple (tableau bidimensionnel coloré au maximum sans violation des contraintes (liste de listes),      """
"""                     booléen exprimant l'arrêt sur erreur)                                                           """

def colorationMixed (constraints):
    
    # On colorie la grille à l'aide de la programmation dynamique
    A, finished = colorationDP(constraints)
    # S'il n'y a pas d'erreur et que le coloriage est incomplet, on continue avec la PLNE
    if not finished: return (A, False)
    if not [-1 in ligne for ligne in A]: return (A, True)
    # Si le coloriage est complet, on retourne directement le résultat
    else: return colorationLP(constraints, A) 

    
""" Début du main : affiche une interface facile d'utilisation pour choisir l'instance à résoudre et la méthode """

print("\n_______________________________________________________________________________________________________\n")
print("                                   A DISCRETE TOMOGRAPHY PUZZLE SOLVER                                  ")
print("_______________________________________________________________________________________________________\n")

# Entrée des paramètres de l'utilisateur
checkM = False
checkI = False
while (not checkM):
    if (version_info[0] == 2): method = raw_input("CHOSE SOLVING METHOD (1: Dynamic Programming, 2: Linear Programming, 3: Mixed method):\n>> ")
    else: method = input("CHOSE SOLVING METHOD (1: Dynamic Programming, 2: Linear Programming, 3: Mixed method):\n>> ")
    if (method in ['1','2','3']): checkM = True
    else: print("Please chose 1, 2 or 3!\n")
while (not checkI):
    if (version_info[0] == 2): instance = raw_input("CHOSE INSTANCE TO SOLVE (an integer between 0 and 16):\n>> ")
    else: instance = input("CHOSE INSTANCE TO SOLVE (an integer between 0 and 16):\n>> ")
    if (instance in [str(x) for x in range(17)]): checkI = True
    else: print("Please chose an integer between 0 and 16!\n")

# Lancement de la résolution
print("\nSTARTING TO SOLVE INSTANCE %s USING %s..." %(instance, ["DYNAMIC PROGRAMMING", "LINEAR PROGRAMMING", "MIXED METHOD"][int(method) - 1]))
print("-------------------------------------------------------------------------------------------------------\n")

start = time()
constraints = createInstance(int(instance))
if (int(method) == 1): sol, finished = colorationDP(constraints)
if (int(method) == 2): sol, finished = colorationLP(constraints)
if (int(method) == 3): sol, finished = colorationMixed(constraints)
if (int(method) == 2 or int(method) == 3):
    print ("\n-------------------------------------------------------------------------------------------------------\n")

# Affichage des résultats
print("Execution time: %s sec " % (time() - start))
if (finished): print ("Grid coloration finished without error! Displaying solution...")
else: print ("Impossible to color the grid. Displaying coloration before error...")
display(sol, constraints, axis = False)

print("_______________________________________________________________________________________________________\n")
