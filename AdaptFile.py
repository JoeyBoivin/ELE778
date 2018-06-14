#!/usr/bin/python
# -*- coding: latin-1 -*-

####################################################################################################
# Auteurs : Joey Boivin et Julien Burson							   #
# Date : 13 juin 2018										   #
# Cours : ELE 778 a l'Ecole de Technologie Superieure						   #
# Nom du fichier : AdaptFile                                                                       #
#                                                                                                  #
# **Les accents n'ont pas ete utilise intentionnellement pour des raisons de compatibilitees**     #
#												   #
# Fonction du fichier : Ce code permet d'adapter le nombre d'entree desire de chaque .txt  	   #
# fournie afin de pouvoir les traiter par la suite sur la meme base.				   #
# Si le fichier fournie contient plus de données que d�siree alors le code supprime des lignes    #
# avec pour critere le 13e terme de chaque ligne, qui est l'energie statique.		   	   #
# Si le fichier fournie contient moins de donnees que desiree, alors le code ajoute des lignes en  #
# appliquant une moyenne de deux lignes et inserant la nouvelle entre les deux.			   #
####################################################################################################

# La fonction randrange permet d'obtenir une valeur aleatoirement selon la longueur d'une variable
from random import randrange

##############################################
###### Declaration variables globales ########
##############################################

test = 'info_test.txt'          # fichier des donnees de test de generalisation
train = 'info_train.txt'        # fichier des donnees d'entrainement
validation = 'info_vc.txt'      # fichier des donnees de validation croisee
config = 'Configuration.txt'    # fichier des configurations du reseau de neuronne
nubArray = []                   # tableau de reels(statique&dynamique) de chaque trame d'un fichiers audio
lineArray = []                  # tableau de chaque trame d'un fichier audio

####################################################################################################

# Acquisition du nombre d'entree desiree dans le fichier de configuration
with open(config) as entree:
    nbrEntree = int(entree.readlines()[1])


# Fonction qui execute la tache principale demandee
def adapt(fichier):

    # Ouvre le fichier choisit et lit chaque ligne pour en retirer son nombre de trame, ainsi que son chemin d'acces
    with open(fichier) as f:
        line = f.readline()

        while line:
            words = line.split()  # Separe le nombre de trame et le chemin
            ecart = 0

            # Si le nombre de donnee dans le fichier est superieur au nombre d'entree demande
            if int(words[0]) > nbrEntree:
                ecart = int(words[0]) - nbrEntree

                # ouvre le chemin d'acces et lit chaque lignes
                with open(words[1]) as f2:
                    line2 = f2.readline()
                    x = 0

                    '''
                    Pour chaque ligne de donnees deux tableaux sont cree, le premier est lineArray qui
                    contient(string) de chaque trame de donneeset le second est un tableau de numbArray
                    qui contient(real) chaque 13e terme (l'energie statique) de chaque ligne 
                    '''
                    while line2:
                        lineArray.insert(x, line2)
                        numbers = line2.split()
                        nubArray.insert(x, float(numbers[12]))
                        line2 = f2.readline()
                        x = x + 1

                    '''
                    Tant que l'ecart entre le nombre de donnee dans le fichier et le nombre de donnees desiree
                    est plus grand que zero alors on cherche le plus petit terme d'energie statique et enregistre
                    sa position dans le tableau nubArray, puis suprimme le terme et la ligne dans les deux tableaux
                    dont la position correpond au minimum trouve.
                    '''
                    while ecart > 0:
                        minpos = nubArray.index(min(nubArray))
                        del lineArray[minpos]
                        del nubArray[minpos]
                        ecart = ecart - 1

                    '''
                    Ouvre le fichier "temp" avec le meme chemin d'acces de depart afin de mettre la nouvelle base de donnees
                    avec le nombre de trame adapte.
                    '''
                    f3 = open('temp/' + words[1], 'w')
                    for i, elem in enumerate(lineArray):
                        f3.write(lineArray[i])
                    f3.close()
                    del nubArray[:]
                    del lineArray[:]

            # Si le nombre de donnee dans le fichier est inférieur au nombre d'entree demande
            elif int(words[0]) < nbrEntree:

                # Tableau qui permettront la 
                a = []
                b = []
                average = []
                ecart = nbrEntree - int(words[0])

                # ouvre le chemin d'acces et lit chaque lignes
                with open(words[1]) as f2:
                    line2 = f2.readline()
                    x = 0

                    '''
                    Les deux tableaux,lineArray et nubArray se remplisse en lisant les lignes
                    Le tableau lineArray(string) contient tous les lignes d'un fichier audio
                    Le tableau nubArray(real) est un tableau qui contient tous les termes de chaque trame du fichier audio
                    '''
                    while line2:
                        lineArray.insert(x, line2)
                        nubArray.insert(x, line2.split())
                        line2 = f2.readline()
                        x = x + 1

                    '''
                    La fonction ranrange permet de cree un nombre aleatoir entre 0 et le nombre de ligne dans le fichier -1
                    Puis l'enregiste dans la variable index_a.
                    Donc le tableau a contient toutes les valeurs(real) de la ligne a l'index_a et le tableau b contient toutes
                    les valeurs(real) de la ligne a l'index_b
                    '''
                    while ecart > 0:
                        index_a = randrange(len(lineArray) - 1)
                        index_b = index_a + 1
                        a = list(nubArray[index_a])
                        b = list(nubArray[index_b])
                        y = 0

                        '''
                        tant que Y est inferieur a 26(nombre de valeur pour chaque trame), le tableau average
                        se remplit des valeurs moyennes de chaque termes en ayant pour reference les tableau a et b.
                        '''
                        while y < 26:
                            average.insert(y, str((float(a[y]) + float(b[y])) / 2))
                            y = y + 1
                        average.append('\r\n')    #Ajoute un changement de ligne pour conserver la mise en page des donnees
                        ecart = ecart - 1

                        '''
                        le tableau average qui est un tableau de string est insere a la place de la ligne B dans les tableaux
                        lineArray(string) et nubArray(real)
                        '''
                        lineArray.insert(index_b, ' '.join(list(average)))   #Cree un espace entre chaque valeur
                        nubArray.insert(index_b, list(average))

                        # Vide les tableaux a, b et average
                        del average[:]
                        del a[:]
                        del b[:]

                    '''
                    Ouvre le fichier "temp" avec la meme chemin d'acces de depart afin de mettre la nouvelle base de donne
                    avec le nombre de trame adapte.
                    Puis, ferme le ficher et suprimme le donnees dans le tableaux lineArray
                    '''
                    f3 = open('temp/' + words[1], 'w')
                    for i, elem in enumerate(lineArray):
                        f3.write(lineArray[i])
                    f3.close()
                    del lineArray[:]

                '''
                Si le nombre de donnees dans le fichier est egale au nombre de donnees souhaite
                alors le code copie l'entierete des trames du fichier audio dans celui du dossier 'temp' 
                '''
            else:
                with open(words[1]) as f2:
                    with open('temp/' + words[1], 'w') as f3:
                        for line in f2:
                            f3.write(line)

            line = f.readline()

#Effectue l'adaptation pour les trois bases de donnees.
adapt(test)
adapt(train)
adapt(validation)
