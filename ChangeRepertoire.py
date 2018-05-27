#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# ce fichier permet de changer l'adresse de chaque information d'un rerpertoire
# a un autre.

testFile = 'info_test.txt'
trainFile = 'info_train.txt'
validationFile = 'info_vc.txt'

with open(validationFile) as f:
    newText=f.read().replace('/home/pub/ele-778/labo/labo2/BaseDonnees', '')

with open(validationFile, "w") as f:
    f.write(newText)