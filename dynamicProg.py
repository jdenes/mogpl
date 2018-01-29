# -*- coding: utf-8 -*-

################################
###       PROJET MOGPL       ###
###  JULIEN DENES - 3772480  ###
################################


""" INPUT:    une séquence (liste) de blocs à placer                            """
"""           une ligne (liste) dont les valeurs n'ont pas d'importance         """
""" OUTPUT:   un booléen indiquant si la line est colorable avec la séquence    """

def simpleFit (sequence, line):
    
    sequence = [0] + sequence # pour traiter le cas de la sous-séquence vide
    k = len(sequence)
    m = len(line)
    T = [[None for l in range(k)] for j in range(m)]
    
    for l in range(k):
        for j in range(m):
            # Si l = 0
            if (l == 0): T[j][l] = True
            # Si l > 0 :
            # Cas j < sl - 1
            elif (j < sequence[l] - 1): T[j][l] = False
            # Cas j = sl - 1
            elif (j == sequence[l] - 1):
                if (l == 1): T[j][l] = True
                else: T[j][l] = False
            # Cas j > sl - 1   
            elif (j > sequence[l] - 1):
                if (l == 1): T[j][l] = True
                elif (j < sequence[l]+1): T[j][l] = False # pour éviter une récursion avec j négatif
                else: T[j][l] = T[j-sequence[l]-1][l-1]
                
    return T[m-1][k-1]


""" INPUT:    une séquence (liste) de blocs à placer                                                             """
"""           une ligne (liste) où line[i] = 1 si la case est noire, 0 si elle est blanche, -1 si indeterminée   """
""" OUTPUT:   un booléen indiquant si la ligne est colorable avec la séquence                                    """

def coloredFit (sequence, line):
    
    sequence = [0] + sequence
    k = len(sequence)
    m = len(line)
    T = [[None for l in range(k)] for j in range(m)]
    
    for l in range(k):
        for j in range(m):
            
            # Si l = 0
            if (l == 0):
                if (1 in line[0:j+1]): T[j][l] = False
                else: T[j][l] = True               
            # Si l > 0 :
            # Cas j < sl - 1
            elif (j < sequence[l] - 1): T[j][l] = False
            # Cas j = sl - 1
            elif (j == sequence[l] - 1):
                if ((l == 1) and (not 0 in line[0:j+1])): T[j][l] = True
                else: T[j][l] = False
            # Cas j > sl - 1  
            elif (j > sequence[l] - 1):
                # Cas l = 1
                if (l == 1):
                    # Dernière case blanche
                    if (line[j] == 0):
                        T[j][l] = T[j-1][l]
                    # Dernière case noire
                    elif (line[j] == 1):
                        T[j][l] = (not 0 in line[j-sequence[l]+1:j+1]) and T[j-sequence[l]][l-1]
                    # Dernière case indéterminée
                    elif (line[j] == -1):
                        T[j][l] = (not 0 in line[j-sequence[l]+1:j+1]) and T[j-sequence[l]][l-1] or T[j-1][l]
                # Cas l > 1
                elif (j < sequence[l]+1): T[j][l] = False # pour éviter une récursion avec j négatif
                else:
                    # Dernière case blanche
                    if (line[j] == 0):
                        T[j][l] = T[j-1][l]
                    # Dernière case noire
                    elif (line[j] == 1):
                         T[j][l] = (not 0 in line[j-sequence[l]+1:j+1]) and (not line[j-sequence[l]] == 1) and T[j-sequence[l]-1][l-1]
                    # Dernière case indéterminée
                    elif (line[j] == -1):
                        T[j][l] = (not 0 in line[j-sequence[l]+1:j+1]) and (not line[j-sequence[l]] == 1) and T[j-sequence[l]-1][l-1] or T[j-1][l]

    return T[m-1][k-1]


""" INPUT:    un tuple (contraintes sur les lignes (liste de listes), contraintes sur les colonnes (liste de listes))   """
""" OUTPUT:   un tuple (tableau bidimensionnel coloré au maximum sans violation des contraintes (liste de listes),      """
"""                     booléen exprimant l'arrêt sur erreur)                                                           """

def colorationDP (constraints):

    # Initialisation   
    sequencesLines, sequencesRows = constraints
    n = len(sequencesLines) # nb de lines
    m = len(sequencesRows) # nb de colonnes
    A = [[-1 for i in range(m)] for j in range(n)]
    linesToSee = list(range(n))
    rowsToSee = list(range(m))
    
    # Début de l'itération
    while (len(linesToSee) != 0 or len(rowsToSee) != 0):
    
        # On étudie toutes les lignes à voir
        for i in linesToSee:
            for j in [j for j in range(m) if A[i][j] == -1]:
                # On regarde si chaque case est colorable en noir, puis en blanc
                tempLine = A[i][:]
                tempLine[j] = 1
                blackColorable = coloredFit (sequencesLines[i], tempLine)
                tempLine[j] = 0
                whiteColorable = coloredFit (sequencesLines[i], tempLine)
                # On teste si on peut en déduire la coloration de la case
                if (not blackColorable and not whiteColorable): return (A, False)
                elif (blackColorable and whiteColorable): pass
                elif (blackColorable):
                    A[i][j] = 1
                    if (j not in rowsToSee): rowsToSee.append(j)
                elif (whiteColorable):
                    A[i][j] = 0
                    if (j not in rowsToSee): rowsToSee.append(j)
        linesToSee[:] = []

        # On étudie toutes les colonnes à voir        
        for j in rowsToSee:
            for i in [i for i in range(n) if A[i][j] == -1]:
                # On regarde si chaque case est colorable en noir, puis en blanc
                tempRow = [A[k][j] for k in range(n)]
                tempRow[i] = 1
                blackColorable = coloredFit (sequencesRows[j], tempRow)
                tempRow[i] = 0
                whiteColorable = coloredFit (sequencesRows[j], tempRow)
                # On teste si on peut en déduire la coloration de la case
                if (not blackColorable and not whiteColorable): return (A, False)
                elif (blackColorable and whiteColorable): pass
                elif (blackColorable):
                    A[i][j] = 1
                    if (i not in linesToSee): linesToSee.append(i)
                elif (whiteColorable):
                    A[i][j] = 0
                    if (i not in linesToSee): linesToSee.append(i)  
        rowsToSee[:] = []
            
    return (A, True)
