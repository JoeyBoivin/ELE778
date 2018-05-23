#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# ce fichier permet de changer l'adresse de chaque information d'un rerpertoire
# a un autre.

import fileinput

# Ouverture d'un fichier en *lecture*:
fichier = "ELE778_MLP\info_vc.txt"

#pour chaque ligne qui contient la premiere adresse est rempacer par la seconde
for line in fileinput.input(fichier,inplace= True):
    line = line.replace("/home/pub/ele-778/labo/labo2/BaseDonnees/tidigits","/ELE778_MLP")
    print line
fileinput.input(fichier).close()

print "All modifications are done"
