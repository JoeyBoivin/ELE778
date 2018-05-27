#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# ce fichier permet de changer l'adresse de chaque information d'un rerpertoire
# a un autre.

with open('info_test.txt') as f:
    newText=f.read().replace('/home/pub/ele-778/labo/labo2/BaseDonnees', '')

with open('info_test.txt', "w") as f:
    f.write(newText)
