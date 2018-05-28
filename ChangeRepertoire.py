#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# ce fichier permet de changer l'adresse de chaque information d'un rerpertoire
# a un autre.

testFile = 'info_test.txt'
trainFile = 'info_train.txt'
validationFile = 'info_vc.txt'

#Changement de l'adresse des informations de test
with open(testFile) as f:
    newText=f.read().replace('/home/pub/ele-778/labo/labo2/BaseDonnees/tidigits/', '')

with open(testFile, "w") as f:
    f.write(newText)


#Changement de l'adresse des informations d'essai
with open(trainFile) as f:
    newText=f.read().replace('/home/pub/ele-778/labo/labo2/BaseDonnees/tidigits/', '')

with open(trainFile, "w") as f:
    f.write(newText)


#Changement de l'adresse des informations de validation
with open(validationFile) as f:
    newText=f.read().replace('/home/pub/ele-778/labo/labo2/BaseDonnees/tidigits/', '')

with open(validationFile, "w") as f:
    f.write(newText)
