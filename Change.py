#! /usr/bin/python
# -*- coding: latin-1 -*-
# ce fichier permet de changer du texte
import fileinput
for line in fileinput.input("info_train.txt",inplace=1):
    print(line.replace("/home/pub/ele-778/labo/labo2/BaseDonnees/tidigits","/ELE778_MLP"))
