#!/usr/bin/env python3
# -*- coding: latin-1 -*-

############################################
#	Permet d'adapter un fichier pour   #
#	  le nombre d'entrée désiré        #
############################################

#############
# Variables #
#############

testFile = 'info_test.txt'
trainFile = 'info_train.txt'
validationFile = 'info_vc.txt'

nbrEntree = int(input("Entrée le nombre d'entrée désiré: "))

with open(validationFile) as f:
	line = f.readline()
	while line:
		words = line.split()
		print words[0]
		if int(words[0]) > nbrEntree:
			print 'plus grand'
			with open(words[1]) as f2:
				line2 = f2.readline()
				while line2:
					numbers = line2.split()
					max = float(numbers[11])
					if numbers
					print min
					line2 = f2.readline()
		line = f.readline()


