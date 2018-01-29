# -*- coding: utf-8 -*-

################################
###       PROJET MOGPL       ###
###  JULIEN DENES - 3772480  ###
################################

from gurobipy import *

""" INPUT:    un tuple (contraintes sur les lignes (liste de listes), contraintes sur les colonnes (liste de listes))   """
"""           optionnel : un tableau bidimensionnel partiellement coloré (liste de listes)                              """
""" OUTPUT:   un tuple (tableau bidimenionnel coloré au maximum sans violation des contraintes (liste de listes),       """
"""                     booléen exprimant l'arrêt sur erreur)                                                           """

def colorationLP (constraints, A = None):
    
    sequencesLines, sequencesRows = constraints
    n = len(sequencesLines) # nb de lines
    m = len(sequencesRows) # nb de colonnes
    mod = Model("model")
    
    """ DECLARATION DES VARIABLES DE DECISION """
    # x_ij
    x = []
    for i in range(n):
        line = []
        for j in range(m): line.append(mod.addVar(vtype=GRB.BINARY, name="x_%d,%d" % (i, j)))
        x.append(line)
    
    # y^t_ij
    y = []
    for i in range(n):
        line = []
        for t in range(len(sequencesLines[i])):
            dim_t = []
            for j in range(m):
                dim_t.append(mod.addVar(vtype=GRB.BINARY, name="y_%d,%d,%d" % (i, j, t)))
            line.append(dim_t)
        y.append(line)     
    
    # z^t_ij
    z = []
    for j in range(m):
        col = []
        for t in range(len(sequencesRows[j])):
            dim_t = []
            for i in range(n):
                dim_t.append(mod.addVar(vtype=GRB.BINARY, name="z_%d,%d,%d" % (i, j, t)))
            col.append(dim_t)
        z.append(col)
    
    mod.update()

    """ DEFINITION DE LA FONCTION OBJECTIF """
    obj = LinExpr();
    obj = 0
    for i in range(n):
        for j in range(m): obj += x[i][j]
    
    mod.setObjective(obj, GRB.MAXIMIZE)

    """ DEFINITION DES CONTRAINTES """
    
    # Contrainte (1) : st * y^t_ij - sum(x_ik) <= 0
    for i in range(n):
        for t, st in enumerate(sequencesLines[i]):
            for j in range(m):
                mod.addConstr(st * y[i][t][j] - quicksum([x[i][k] for k in range(j, min(j+st, m))]) <= 0)

    # Contrainte (2) : st * z^t_ij - sum(x_kj) <= 0
    for j in range(m):
        for t, st in enumerate(sequencesRows[j]):
            for i in range(n):
                mod.addConstr(st * z[j][t][i] - quicksum([x[k][j] for k in range(i, min(i+st, n))]) <= 0)
    
    # Contrainte (3) : y^t_ij + sum(y^(t+1)_ik) <= 1
    for i in range(n):
        for t, st in enumerate(sequencesLines[i][:-1]):
            for j in range(m):
                mod.addConstr(y[i][t][j] + quicksum([y[i][t+1][k] for k in range(min(j+st+1, m))]) <= 1)
    
    # Contrainte (4) : z^t_ij + sum(z^(t+1)_kj) <= 1
    for j in range(m):
        for t, st in enumerate(sequencesRows[j][:-1]):
            for i in range(n):
                mod.addConstr(z[j][t][i] + quicksum([z[j][t+1][k] for k in range(min(i+st+1, n))]) <= 1)
    
    # Contrainte (5) : sum(x_ik) - sum(s_t) = 0 (ligne)
    for i in range(n):
        mod.addConstr(quicksum([x[i][j] for j in range(m)]) - quicksum(sequencesLines[i]) == 0)
    
    # Contrainte (6) : sum(x_kj) - sum(s_t) = 0 (colonne)
    for j in range(m):
        mod.addConstr(quicksum([x[i][j] for i in range(n)]) - quicksum(sequencesRows[j]) == 0)
    
    # Contrainte (7) : sum(y^t_ik) = 1
    for i in range(n):
        for t in range(len(sequencesLines[i])):
            mod.addConstr(quicksum([y[i][t][j] for j in range(m)]) == 1)

    # Contrainte (8) : sum(z^t_kj) = 1
    for j in range(m):
        for t in range(len(sequencesRows[j])):
            mod.addConstr(quicksum([z[j][t][i] for i in range(n)]) == 1)

    # Contraintes (12) et (13) : intervalle de début de y^t_ij
    for i in range(n):
        k = len(sequencesLines[i])
        for t, st in enumerate(sequencesLines[i]):
            for j in range(m):
                if (j < sum([sequencesLines[i][l] for l in range(t+1)]) - st + t):
                    mod.addConstr(y[i][t][j] == 0)
                if (m - j < sum([sequencesLines[i][l] for l in range(t,k)])+ k - 1 - t):
                    mod.addConstr(y[i][t][j] == 0)
    
    # Contraintes (14) et (15) : intervalle de début de z^t_ij
    for j in range(m):
        k = len(sequencesRows[j])
        for t, st in enumerate(sequencesRows[j]):
            for i in range(n):
                if (i < sum([sequencesRows[j][l] for l in range(t+1)]) - st + t - 1):
                    mod.addConstr(z[j][t][i] == 0)
                if (n - i < sum([sequencesRows[j][l] for l in range(t,k)])+ k - 1 - t):
                    mod.addConstr(z[j][t][i] == 0)
    
    # Contrainte pour la résolution mixte : si a_ij = 0 (resp. 1), x_ij = 0 (resp. 1)
    if A != None:
        for i in range(n):
            for j in range(m):
                if A[i][j] != -1: mod.addConstr(x[i][j] == A[i][j])
                
    """ Résolution et retour """
    mod.update()
    mod.optimize()
    
    try:
        sol = [[x[i][j].x for j in range(m)] for i in range(n)]
        return (sol, True)
    except:
        sol = [[-1 for j in range(m)] for i in range(n)]
        return (sol, False)
        