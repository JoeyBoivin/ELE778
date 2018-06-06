#!/usr/bin/env python3
# -*- coding: latin-1 -*-

####################################################################################################
# Auteurs : Joey Boivin et Burson Julien
# Date : 4 juin 2018
# Cours : ELE 778 à l'Ecole de Technologie Superieure
# Nom du fichier : AdaptFile
#
# Fonction du fichier : Ce code permet d'adapter le nombre d'entrée désiré de chaque .txt
# fournie afin de pouvoir les traiter par la suite sur la même base.
# Si le fichier fournie contient plus de données que désirée alors le code suprimme des lignes
# avec pour critère le 12 ème terme de chaque ligne, qui est l'énergie statique.
# Si le fichier founie contient moins de données que désirée alors le code ajoute des lignes en
# appliquant une moyenne de deux lignes et insérant la nouvelle entre les deux.
####################################################################################################

# importation de la fonction randrange qui permet de faire un numéro aléatoire
from random import randrange

####################################################################################################
######################################### Variables ################################################
####################################################################################################
testFile = 'info_test.txt'
trainFile = 'info_train.txt'
validationFile = 'info_vc.txt'
config = 'Configuration.txt'
nubArray = []
lineArray = []
####################################################################################################

# Demande à l'utilisateur le nombre d'entrée désirée
with open(config) as entree:
    nbrEntree = int(entree.readlines()[1])
    print nbrEntree

#nbrEntree = int(input("Entrée le nombre d'entrée désiré: "))

# Ouvre le fichier validation file et lit les adresses des fichiers de données
with open(trainFile) as f:
    line = f.readline()
    # Sépare chaque termes de l'adresse de données
    while line:
        words = line.split()
        ecart = 0
        # Si le nombre de donnée dans le fichier est supérieur au nombre d'entrée demandé
        if int(words[0]) > nbrEntree:
            ecart = int(words[0])-nbrEntree
            print 'plus grand'
            # ouvre le chemins des données et lit cahque lignes
            with open(words[1]) as f2:
                line2 = f2.readline()
                x = 0
                # pour chaque ligne de données deux tableaux sont crée, le premier est lineArray qui
                # contient chaque lignes de données et le second est un tableau de numbArray qui
                # contient chaque 12 eme terme (l'énergie statique) de chaque ligne
                while line2:
                    lineArray.insert(x,line2)
                    numbers = line2.split()
                    nubArray.insert(x,float(numbers[12]))
                    line2 = f2.readline()
                    x = x+1
                # Tant que l'écart entre le nombre de donnée dans le fichier et le nombre de données désirée
                # est plus grand que zéro alos On cherche le plus petit terme d'énergie statique et enregiste
                # sa position dans le tableau nubArray, puis suprimme le terme et la ligne dans les deux tableux
                # dont la position correpond au minimum trouvé.
                while ecart > 0:
                    minpos = nubArray.index(min(nubArray))
                    del lineArray[minpos]
                    del nubArray[minpos]
                    ecart = ecart-1
                # Ouvre le fichier "temp" avec la même adresse de départ afins de mettre la nouvelle base de donné
                # dont le nombre de données souhaité est enregistré.
                # Puis, ferme le ficher et suprimme les données dans les tableaux nubArray et lineArray
                f3 = open('temp/'+ words[1],'w')
                for i, elem in enumerate(lineArray):
                    f3.write(lineArray[i])
                f3.close()
                del nubArray[:]
                del lineArray[:]
        # Si le nombre de donnée dans le fichier est inférieur au nombre d'entrée demandé
        elif int(words[0]) < nbrEntree:
            print 'plus petit'
            # crée trois tableaux vide
            a = []
            b = []
            average = []
            # écart est la valeur du nombre d'entrée demandé moins le nombre d'entrée dans le fichier
            ecart = nbrEntree - int(words[0])
            # Permet de lire toutes les lignes de données contenue dans words[1]
            with open(words[1]) as f2:
                line2 = f2.readline()
                x = 0
                # Les deux tableaux,lineArray et nubArray se remplisse en lisant les lignes
                # Le tableau lineArray est un tablau de ligne
                # Le tableau nubArray est un tableau qui contient tout les termes indépendanment des lignes
                while line2:
                    lineArray.insert(x, line2)
                    nubArray.insert(x, line2.split())
                    line2 = f2.readline()
                    x = x + 1
                # La fonction random permet de crée un nombre aléatoir entre 0 et 1 - le nombre de ligne dans le fichier
                # Puis l'enregiste dans la variable index_a.
                # Donc le tableau a contient toutes les valeurs de la ligne à l'index_a et le tableau b contient toutes
                # les valeurs de la ligne à l'index_b
                while ecart > 0:
                    index_a = randrange(len(lineArray)-1)
                    index_b = index_a + 1
                    a = list(nubArray[index_a])
                    b = list(nubArray[index_b])
                    y = 0
                    # tant que Y est inférieur à 26, le tableau average ce remplit des valeurs moyenne de chaque termes
                    # en ayant pour référence les tableau a et b.
                    while y < 26:
                        average.insert(y, str((float(a[y])+float(b[y]))/2))
                        y = y+1
                    average.append('\r\n')
                    ecart = ecart-1
                    # le tableau average qui est une ligne est insert a la place de la ligne B dans les tableau
                    # lineArray et nubArray
                    lineArray.insert(index_b,' '.join(list(average)))
                    nubArray.insert(index_b, list(average))
                    # Vide les tableaux a, b et avergage
                    del average[:]
                    del a[:]
                    del b[:]
                # Ouvre le fichier "temp" avec la même adresse de départ afins de mettre la nouvelle base de donné
                # dont le nombre de données souhaité est enregistré.
                # Puis, ferme le ficher et suprimme le données dans le tableaux lineArray
                f3 = open('temp/' + words[1], 'w')
                for i, elem in enumerate(lineArray):
                    f3.write(lineArray[i])
                f3.close()
                del lineArray[:]
        # Si le nombre de données dans le fichier est égale au nombre de données souhaité
        # alors le code ouvre le fichier "temp" avec la même adresse de départ afins de mettre la base de donnés
        else:
            print 'egal'
            with open(words[1]) as f2:
                with open('temp/' + words[1], 'w') as f3:
                    for line in f2:
                        f3.write(line)

        line = f.readline()
